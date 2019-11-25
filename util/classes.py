#!/usr/bin/python3.6
import splunklib.results as results, splunklib.client as client
from static.static import device_types, device_dict
import os, json, pandas as pd, numpy as np, logging, random
from static.credentials import splunk_creds as creds
from util.web_pa import WebpaUtils as web_pa
from util.splunk import query_splunk

class Product(object):

	def __init__(self, product_type: str):
		self.__product_type = product_type
		self.__email_sender = "MarkerAlert@comcast.com"
		self.__email_subject = f"Missing Mandatory Markers on {product_type}"
		self.__recipient_list = device_dict[product_type]

	def get_email_sender(self) -> str:
		return self.__email_sender

	def get_product_type(self) -> str:
		return self.__product_type

	def get_email_subject(self) -> str:
		return self.__email_subject

	def get_recipient_list(self) -> list:
		return self.__recipient_list


class Device(Product):

	__local_macs_path = "/home/mhealy066/scripts/TelemetryProject/static/device_addresses/{}.txt"

	def __init__(self, device_type: str):
		self.__device_type = device_type
		super().__init__(device_types[self.__device_type])
		self.__splunk_query_macs = device_dict[self.get_product_type()]["devices"][device_type]["splunk_query_macs"]
		self.__splunk_query_daily_percents = device_dict[self.get_product_type()]["devices"][device_type]["splunk_query_daily_percentages"]
		self.__logpath = device_dict[self.get_product_type()]["devices"][device_type]["logpath"]
		self.__command = device_dict[self.get_product_type()]["devices"][device_type]["command"]

	def get_device_type(self) -> str:
		return self.__device_type

	def get_splunk_macs_query(self) -> str:
		return self.__splunk_query_macs

	def get_splunk_daily_percents_query(self):
		return self.__splunk_query_daily_percent

	def get_logpath(self) -> str:
		return self.__logpath

	def get_command(self) -> str:
		return self.__command

	def find_online_device(self) -> str:
		"""
		Loop through some known MAC addresses (that we have stored locally) of the 
		given device type checking if that router is online. Once we have found one 
		that is online, return that MAC address if the device is of type XI5, 
		else return the IP address
		"""
		found_one = False
		with open(self.__local_macs_path.format(self.get_device_type()), "r") as file:
			macs = file.read().splitlines()
		random.shuffle(macs)

		while found_one == False:

			mac = macs.pop()
			found_one = web_pa.router_is_online(mac)

			logging.info(f'{mac} is {found_one}')
			if found_one:
				if self.get_device_type() == "XI5":
					logging.info(f"MAC for {self.get_device_type()} : {mac}")
					return mac
				elif self.get_device_type() in ["XB3", "XB6", "XF3", "XG"]:
					ip = web_pa.ip_from_mac(mac=mac, device_type=self.get_device_type())
					logging.info(f"IP for {self.get_device_type()} : {ip}")
					return ip

	def get_static_error_df(self) -> pd.DataFrame:
		'''Pulls the most up-to-date telemetry errors for the given device type'''
		return pd.read_csv(f"/home/mhealy066/scripts/TelemetryProject/static/static_markers/RDK_PEM_MARKERS_{self.get_device_type()}.csv", sep=",")

	def get_conf_error_df(self) -> pd.DataFrame:
		return pd.read_csv(f"/home/mhealy066/scripts/TelemetryProject/static/confluence_markers/{self.get_device_type()}.csv")

	def get_configs_difference(self) -> np.ndarray:
		"""
		Finds the error markers in the most recent configs that are not present
		in the field devices configs

		Parameters:
			path (str): Path to the local folder containing the device's configs
		"""
		file_path = f"/home/mhealy066/scripts/TelemetryProject/CpeLogs/DOWNLOADED/LIVE/{self.get_device_type()}/{self.get_logpath()}"
		
		def parse_configs(path) -> list:
			"""Removes the heading from the json return by the """
			def __remove_double_quotes(data: str) -> str:
				#some peculiar logic to root cause the issue
				str_data = data.replace("{\"" ,"vikr").replace("\",\"" , "sandep")
				str_data = str_data.replace("\" : \"","arun").replace("\":\"","bindhu")\
					.replace("\"}", "gauth")
				str_data = str_data.replace("\"","")
				return str_data.replace("vikr","{\"" ).replace("sandep","\",\"" )\
					.replace("arun","\"  :  \"").replace("bindhu","\":\"")\
					.replace("gauth","\"}" ).replace("\\","#")

			with open(path, "r",encoding="utf8") as fin:
				content = fin.readlines()

				for i in range(len(content)):
					if "urn:settings:TelemetryProfile" in content[i]:
						data_string = content[i].split('telemetryProfile":' )
						data_string = data_string[1].split(",\"schedule\":\"")
						parse_data = ''

						if self.get_device_type() in ['XB3', 'XB6', 'XF3']:
							parse_data = data_string[0].replace("\"cid\":\"0\"","cid:0")
						elif self.get_device_type() == 'XG' or self.get_device_type() == 'XI5':
							parse_data = __remove_double_quotes(data_string[0])      
						try:
							jsn_data= json.loads(parse_data)
							return jsn_data
						except Exception as e:
							logging.info(e)

		data = parse_configs(file_path)
		errors_configs = list(pd.DataFrame(data)["header"])

		df_conf_errors = self.get_static_error_df()
		errors_conf = list(df_conf_errors["Marker"])

		need_to_be_updated = np.setdiff1d(errors_conf, errors_configs)

		return need_to_be_updated

	def write_macs_to_local_file(self):
		macs_list = [web_pa.ecm_to_estb(mac) for mac in self.get_macs()]

		macs_string = "\n".join(macs_minus2)
		with open(self.__local_macs_path.format(self.get_device_type()), "w") as file:
			file.write(macs_string)

	def get_macs(self) -> list:
		service = client.connect(
		    host=creds["host"],
		    port=creds["port"],
		    scheme=creds["scheme"],
		    username=creds["username"],
		    password=creds["password"])

		kwargs_oneshot = {'count': 10000}
		oneshotsearch_results = service.jobs.oneshot(self.get_splunk_macs_query(), **kwargs_oneshot)

		# Get the results and display them using the ResultsReader
		reader = results.ResultsReader(oneshotsearch_results)
		splunk_events = [dict(item) for index, item in enumerate(reader)]
		
		df = pd.DataFrame(splunk_events)
		macs = df["mac"].to_list()
		return macs

	def get_daily_errors(self) -> list:
		service = client.connect(
		    host=creds["host"],
		    port=creds["port"],
		    scheme=creds["scheme"],
		    username=creds["username"],
		    password=creds["password"])

		kwargs_oneshot = {'count': 10000}
		oneshotsearch_results = service.jobs.oneshot(self.get_splunk_daily_percents_query(), **kwargs_oneshot)

		reader = results.ResultsReader(oneshotsearch_results)
		splunk_events = [dict(item) for index, item in enumerate(reader)]
		if len(splunk_events) > 0:
			df = pd.DataFrame(splunk_events)
			return df["marker"].to_list()
		else:
			return []
			