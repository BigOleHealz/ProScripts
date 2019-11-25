#!/usr/bin/python3
import pandas as pd, numpy as np, os
from util.config import set_configs
from classes import Device
from EmailSender import send_simple_message

set_configs(__file__)

dir_path = os.getcwd()
important_columns = ["Marker", "Device_type", "Version", "All_issues_percentage"]

recipient_list = {
	"RDKB" : {
		"XB3" : ["Matthew_HEALY@comcast.com",
			# "vasavi_mahadev@comcast.com",
	#		"Prasob_Kizhedath2@cable.comcast.com"
			],
		"XB6" : ["Matthew_HEALY@comcast.com",
			# "vasavi_mahadev@comcast.com",
			# "arun_sunny@comcast.com",
			],
		"XF3" : ["Matthew_HEALY@comcast.com",
			# "vasavi_mahadev@comcast.com",
			# "sridharguptha_guntha@comcast.com"
			],
		},
	"RDKV" : {
		"XI5" : ["Matthew_HEALY@comcast.com",
			# "vasavi_mahadev@comcast.com",
			# "dileep_ravindranathan@cable.comcast.com"
			],
		"XG" : ["Matthew_HEALY@comcast.com",
			# "vasavi_mahadev@comcast.com",
			# "dileep_ravindranathan@cable.comcast.com"
			],
	}
}

def run():
	for product in recipient_list.keys():
		for device_type in recipient_list[product].keys():

			df_conf = device.get_conf_error_df()
			df_conf = df_conf.drop_duplicates(subset=["Splunk search Parameter"])
			df_conf = df_conf[df_conf["Splunk search Parameter"].str.contains("WIFI_|SYS_|RF_")]
			df_conf = df_conf[~df_conf["Splunk search Parameter"].str.contains("_split", case=False)]
			conf_markers = df_conf["Splunk search Parameter"]

			df_perc = pd.read_csv(f"{dir_path}/static/ErrorMarkers_Percentages/{product}/{device_type}.csv")[important_columns]
			df_perc["All_issues_percentage"] = df_perc["All_issues_percentage"].apply(lambda x: float(x.replace('%', '')))
			df_perc = df_perc.groupby(by=["Device_type", "Marker", "Version"], as_index=False).sum()
			perc_markers = df_perc["Marker"]

			diff = np.setdiff1d(conf_markers, perc_markers)

			string_markers = "<br>".join(diff)
			string_to_write = f"<h1>{device_type}</h1><p>{string_markers}"

			send_simple_message(
				sender="MarkerAlert@comcast.com", 
				recipient=recipient_list[product][device_type],
				subject=f"{device_type} - Unreported Markers",
				message=string_to_write)
