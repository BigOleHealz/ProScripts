#!/usr/bin/python3
import pandas as pd, numpy as np, logging, re
from static.static import device_types, device_dict
from classes import Device
from util.config import set_configs

output_folder = "output_folder/duplicates/"
markers_output_file = "markers.txt"
duplicates_output_file = "duplicates.txt"


def replaceMultiple(mainString, toBeReplaces, newString):
	'''
	Replace a set of multiple sub strings with a new string in main string.
	'''
	for elem in toBeReplaces:
		if elem in mainString:
			mainString = mainString.replace(elem, newString)
	return mainString

def normalize_column(column):
	return_column = column.str.lower()
	return_column = return_column.apply(lambda x: re.sub(r'[^\w\s]', '', x))
	return_column = return_column.apply(
		lambda x: replaceMultiple(x, [' ', '_'], ''))
	return return_column

def find_duplicates_markers():
	important_column = "Splunk search Parameter"
	output_file = f"{output_folder}/{markers_output_file}"
	with open(output_file, 'w')as file:
		file.write("<h1>Markers</h1>")

	device_xb3 = Device("XB3")
	xb3 = device_xb3.get_conf_error_df()
	xb3["Table"] = device_xb3.get_device_type()
	xb3["lowercase"] = xb3[important_column].str.lower()
	dups_xb3 = xb3[xb3["lowercase"].duplicated(keep=False)].sort_values(
		by=["lowercase"], axis=0).drop(columns=["lowercase", "File"])
	dups_xb3_string = dups_xb3[[
		important_column, "String"]].to_html(index=False)
	string_to_write = f"<h2>{device_xb3.get_device_type()}</h2>{dups_xb3_string}<br>"
	with open(output_file, "a") as file:
		file.write(string_to_write)
		logging.info(f"Wrote {device_xb3.get_device_type()} duplicates - Markers")

	device_xb6 = Device("XB6")
	xb6 = device_xb6.get_conf_error_df()
	xb6["Table"] = device_xb6.get_device_type()
	xb6["lowercase"] = xb6[important_column].str.lower()
	dups_xb6 = xb6[xb6["lowercase"].duplicated(keep=False)].sort_values(
		by=["lowercase"], axis=0).drop(columns=["lowercase", "File"])
	dups_xb6_string = dups_xb6[[
		important_column, "String"]].to_html(index=False)
	string_to_write = f"<h2>{device_xb6.get_device_type()}</h2>{dups_xb6_string}<br>"
	with open(output_file, "a") as file:
		file.write(string_to_write)
		logging.info(f"Wrote {device_xb6.get_device_type()} duplicates- Markers")

	# Overlap?
	xb3_unique = xb3.drop_duplicates(subset=[important_column], keep='first')
	xb6_unique = xb6.drop_duplicates(subset=[important_column], keep='first')
	df_combine = xb3_unique.append(
		xb6_unique)[[important_column, "String", "Table"]]
	df_combine["lowercase"] = df_combine[important_column].str.lower()

	dups_combine = df_combine[df_combine["lowercase"].duplicated(
		keep=False)].sort_values(by=["lowercase", "Table"])

	dups_combine.drop_duplicates(subset=["lowercase", "Table"], inplace=True)
	dups_combine.reset_index(drop=True, inplace=True)
	dups_combine.drop(columns=["lowercase"], inplace=True)

	s_xb3 = dups_combine[dups_combine["Table"] == "XB3"].reset_index(drop=True)
	s_xb6 = dups_combine[dups_combine["Table"] == "XB6"].reset_index(drop=True)

	df = pd.DataFrame(
		{"XB6": s_xb3[important_column], "XB3": s_xb6[important_column]})

	dups_combine_string = df.to_html(index=False)
	string_to_write = f"<h2>Duplicates between XB3 & XB6</h2>{dups_combine_string}<br>"

	with open(output_file, "a") as file:
		file.write(string_to_write)
		logging.info("Wrote XB3 & XB6 duplicates - Markers")

def find_duplicates_descriptions():
	important_column = "String"
	output_file = output_folder + duplicates_output_file
	with open(output_file, 'w')as file:
		file.write("<h1>Descriptions</h1>")

	# XB3
	device_xb3 = Device("XB3")
	xb3 = device_xb3.get_conf_error_df()
	xb3["normalized"] = normalize_column(xb3[important_column])
	xb3_dups = xb3[xb3["normalized"].duplicated(keep=False)]
	xb3_dups.sort_values(by=["normalized"], inplace=True)
	xb3_dups.reset_index(drop=True, inplace=True)

	xb3_dups_str = xb3_dups.to_html(index=False)
	string_to_write = f"<h2>Duplicated in {self.get_device_type()}</h2>{xb3_dups_str}<br>"

	with open(output_file, "a") as file:
		file.write(string_to_write)
		logging.info(f"Wrote {self.get_device_type()} duplicates - Description")

	# XB6
	device_xb6 = Device("XB6")
	xb6 = device_xb6.get_conf_error_df()
	xb6["normalized"] = normalize_column(xb6[important_column])
	xb6_dups = xb6[xb6["normalized"].duplicated(keep=False)]
	xb6_dups.sort_values(by=["normalized"], inplace=True)
	xb6_dups.reset_index(drop=True, inplace=True)

	xb6_dups_str = xb6_dups.to_html(index=False)
	string_to_write = f"<h2>Duplicated in {self.get_device_type()}</h2>{xb6_dups_str}<br>"

	with open(output_file, "a") as file:
		file.write(string_to_write)
		logging.info(f"Wrote {self.get_device_type()} duplicates - Description")

	xb3["Table"] = device_xb3.get_device_type()
	xb6["Table"] = device_xb6.get_device_type()
	df_combine = xb3.append(xb6)

	dups_combine = df_combine[df_combine["normalized"].duplicated(keep=False)]
	dups_combine.drop_duplicates(
		subset=["Splunk search Parameter"], keep=False, inplace=True)
	dups_combine.sort_values(by=["normalized", "Table"], inplace=True)
	dups_combine.reset_index(drop=True, inplace=True)

	dups_combine_str = dups_combine.to_html(index=False)
	string_to_write = f"<h2>Duplicates between XB3 & XB6</h2>{dups_combine_str}<br>"

	with open(output_file, "a") as file:
		file.write(string_to_write)
		logging.info("Wrote XB3 & XB6 duplicates - Description")

	important_column = "String"
	output_file = output_folder + duplicates_output_file
	with open(output_file, 'w')as file: file.write("<h1>Descriptions</h1>")

	# XB3
	xb3 = pd.read_csv("static/ErrorMarkers/xb3.csv", sep=",").drop(columns=["File"])
	xb3["normalized"] = normalize_column(xb3[important_column])
	xb3_dups = xb3[xb3["normalized"].duplicated(keep=False)]
	xb3_dups.sort_values(by=["normalized"], inplace=True)
	xb3_dups.reset_index(drop=True, inplace=True)

	xb3_dups_str = xb3_dups.to_html(index=False)
	string_to_write = f"<h2>Duplicate Descriptions in XB3</h2>{xb3_dups_str}<br>"

	with open(output_file, "a") as file: file.write(string_to_write)

	# XB6
	xb6 = pd.read_csv("static/ErrorMarkers/xb6.csv", sep=",").drop(columns=["File"])
	xb6["normalized"] = normalize_column(xb6[important_column])
	xb6_dups = xb6[xb6["normalized"].duplicated(keep=False)]
	xb6_dups.sort_values(by=["normalized"], inplace=True)
	xb6_dups.reset_index(drop=True, inplace=True)

	xb6_dups_str = xb6_dups.to_html(index=False)
	string_to_write = f"<h2>Duplicate Descriptions in XB6</h2>{xb6_dups_str}<br>"

	with open(output_file, "a") as file:
		file.write(string_to_write)

	xb3["Table"] = "XB3"
	xb6["Table"] = "XB6"
	df_combine = xb3.append(xb6)

	dups_combine = df_combine[df_combine["normalized"].duplicated(keep=False)]
	dups_combine.drop_duplicates(subset=["Splunk search Parameter"], keep=False, inplace=True)
	dups_combine.sort_values(by=["normalized", "Table"], inplace=True)
	dups_combine.reset_index(drop=True, inplace=True)

	dups_combine_str = dups_combine.to_html(index=False)
	string_to_write = f"<h2>Duplicate Descriptions between XB3 & XB6</h2>{dups_combine_str}<br>"

	with open(output_file, "a") as file:
		file.write(string_to_write)

def format_email():
	string_to_send = ""
	with open(output_folder + markers_output_file, "r") as markers_file:
		string_to_send += markers_file.read()

	with open(output_folder + duplicates_output_file, "r") as duplicates_file:
		string_to_send += duplicates_file.read()

	send_simple_message(sender="MarkerAlert@comcast.com", 
						recipient=["Matthew_HEALY@comcast.com"],
						subject="Duplicates",
						message=string_to_send)

def run():
	logging.info("---------------- Initiating ------------------")
	find_duplicates_markers()
	find_duplicates_descriptions()
	format_email()
	logging.info("----------------- Finished -------------------")

if __name__ == "__main__":
	run()
