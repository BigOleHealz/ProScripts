#!/usr/bin/python3.6
import pandas as pd, numpy as np, os
from util.config import set_configs
from collections import Counter
from util.EmailSender import send_simple_message
from datetime import datetime, timedelta

# set_configs(__file__)

dir_path = os.path.dirname(os.path.realpath(__file__))
important_columns = ["Marker", "Device_type", "Version", "All_issues_percentage"]

recipient_list = {
	"RDKB" : {
		"XB3" : ["Matthew_HEALY@comcast.com",
			# "vasavi_mahadev@comcast.com",
			# "Prasob_Kizhedath2@cable.comcast.com"
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
		for device in recipient_list[product].keys():

			list_conf = pd.read_csv(f"{dir_path}/static/ErrorMarkers/{device}.csv")["Splunk search Parameter"]
			output_file_name = f"{dir_path}/output_folder/daily_percentages/{device}.csv"

			list_markers = []
			for date in ["2019-06-18", "2019-06-19", "2019-06-20", "2019-06-21"]:

				list_perc = pd.read_csv(f"{dir_path}/static/daily_percentages/{date}/{device}.csv", error_bad_lines=False)["Marker"]
				list_perc.dropna(inplace=True)

				list_markers.extend(np.setdiff1d(list_conf, list_perc))

			counts = pd.DataFrame(pd.Series(Counter(list_markers)).sort_values(ascending=False)).reset_index()
			counts = counts[counts["index"].str.contains("WIFI_|SYS_|RF_")]
			counts = counts[~counts["index"].str.contains("_split", case=False)].reset_index(drop=True)
			counts.to_csv(output_file_name, index=False, header=False)

			string_to_write = counts.to_html(header=False, index=False, border=0)
			
			for recipient in recipient_list[product][device]:
				send_simple_message(
					sender="MarkerAlert@comcast.com", 
					recipient=recipient,
					subject=f"{device} - Unreported Markers",
					message=string_to_write)

			