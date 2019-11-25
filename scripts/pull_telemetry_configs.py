#!/usr/bin/python3
import os, logging
import static.credentials as creds
from util.EmailSender import send_simple_message
from util.classes import Device
from static.static import device_types, device_dict
from util.web_pa import WebpaUtils as web_pa
from util.config import set_configs

logging.info("Started")

# set_configs(__file__)

dir_path = os.getcwd()

def run():
	products = device_dict.keys()

	for product in products:
		logging.info(f"Product: {product}")
		outstanding_markers = False
		output_path = f"{dir_path}/output_folder/telemetry_differences/{product}.txt"
		open(output_path, 'w').close()

		for device_type in device_dict[product]["devices"].keys():
			logging.info(f"Device Type: {device_type}")

			device = Device(device_type)
			device.write_macs_to_local_file()

			if device_type == "XI5":
				mac = device.find_online_device()
				file_path = web_pa.get_live_logs_by_mac(estb_mac=mac, device_type=device_type)

			elif device_type in ["XB3", "XB6", "XF3", "XG"]:
				ip = device.find_online_device()
				file_path = web_pa.get_live_logs_by_ip(
					ip_addr=ip, device_type=device_type)

			need_to_be_updated = device.get_configs_difference()
			if len(need_to_be_updated) > 0: outstanding_markers = True 

			need_to_be_updated = "<br>".join(need_to_be_updated)
			string_to_write = f"""<h1>{device_type}</h1><p>{need_to_be_updated}
				</p>\n\n"""

			with open(output_path, "a") as file:
				file.write(string_to_write)

		file = open(output_path, "r")
		BODY = file.read()
		file.close()

		if outstanding_markers:
			logging.info(f'Sending email to: {device.get_recipient_list()}')

			send_simple_message(
				sender=device.get_email_sender(),
				recipient=device.get_recipient_list(),
				subject=device.get_email_subject(),
				message=BODY)
		else:
			logging.info(f"No updates detected. NOT sending email")

			send_simple_message(
				sender=device.get_email_sender(),
				recipient=["matthew_healy@comcast.com", "vasavi_mahadev@comcast.com"],
				subject=device.get_email_subject(),
				message=BODY)


if __name__ == "__main__":
	print("Pull Telemetry configs working")
	logging.info("-------------- Job Initiated -------------")
	run()
	logging.info("--------------- Job Finished --------------")
