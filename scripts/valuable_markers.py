'''
Created July 23, 2019

@author: Matt Healy

Purpose: 
	Generate .csv of all markers that have appeared in less than 0.001% of
	incidents. Perhaps this script should be named `find_useless_markers.py`.
'''
import pandas as pd
from util.config import set_configs

set_configs(__file__)

important_columns = ["Marker", "Device_type", "Version", "All_issues_percentage"]

def run():
	# RDK-B
	csv_dataframe = pd.DataFrame(columns=important_columns)
	for device_type in ["Both", "XB3", "XB6", "Others"]:

		df = pd.read_csv(f"static/ErrorMarkers_Percentages/RDKB/{device_type}.csv")[
			important_columns]
		df["All_issues_percentage"] = df["All_issues_percentage"].apply(
			lambda x: float(x.replace('%', '')))
		df = df.groupby(by=["Device_type", "Marker", "Version"], as_index=False).sum()
		df = df.sort_values(by=["Device_type", "Marker", "All_issues_percentage"],
			ascending=False).drop_duplicates(subset=["Device_type", "Marker"], 
			keep='first')
		df_useless = df[df["All_issues_percentage"] < 0.001].reset_index(drop=True)
		df_useless.dropna(subset=["Marker"], inplace=True)
		df_useless["Category"] = device_type
		csv_dataframe = csv_dataframe.append(df_useless, sort=False)
		df_useless.drop(columns=["Category"], inplace=True)

	csv_dataframe.to_csv('output_folder/useless_markers/RDKB.csv', index=False)

	# RDK-V
	csv_dataframe = pd.DataFrame(columns=important_columns)
	for device_type in ["Both", "XG", "XI5", "Others"]:

		df = pd.read_csv(f"static/ErrorMarkers_Percentages/RDKV/{device_type}.csv")[
		important_columns]
		df["All_issues_percentage"] = df["All_issues_percentage"].apply(
			lambda x: float(x.replace('%', '')))
		df = df.sort_values(by=["Device_type", "Marker", "All_issues_percentage"],
			ascending=False).drop_duplicates(subset=["Device_type", "Marker"],
			keep='first')
		df_useless = df[df["All_issues_percentage"] < 0.001].reset_index(drop=True)
		df_useless.dropna(subset=["Marker"], inplace=True)
		df_useless["Category"] = device_type
		csv_dataframe = csv_dataframe.append(df_useless, sort=False)
		df_useless.drop(columns=["Category"], inplace=True)

	csv_dataframe.to_csv('output_folder/useless_markers/RDKV.csv', index=False)

if __name__ == "__main__":
	run()