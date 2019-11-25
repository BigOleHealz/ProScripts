#!/usr/bin/python3.6
import splunklib.results as results, splunklib.client as client
import time, json, pandas as pd, random
from datetime import datetime, timedelta
from static.credentials import splunk_creds as creds
from static import static


def query_splunk(query: str, kwargs_oneshot={}):
	service = client.connect(
		host=creds["host"],
		port=creds["port"],
		scheme=creds["scheme"],
		username=creds["username"],
		password=creds["password"])
	query = 'search ' + query
	oneshotsearch_results = service.jobs.oneshot(query, **kwargs_oneshot)
	reader = results.ResultsReader(oneshotsearch_results)
	
	return [dict(item) for index, item in enumerate(reader)]


def get_daily_errors(device_type: str):
	# Create a Service instance and log in
	service = client.connect(
		host=creds["host"],
		port=creds["port"],
		scheme=creds["scheme"],
		username=creds["username"],
		password=creds["password"])

	product_type = static.device_types[device_type]
	query = static.device_dict[product_type]["devices"][device_type]["splunk_query_daily_percentages"]
	kwargs_oneshot = {'count': 10000}
	oneshotsearch_results = service.jobs.oneshot(query, **kwargs_oneshot)

	reader = results.ResultsReader(oneshotsearch_results)
	splunk_events = [dict(item) for index, item in enumerate(reader)]
	if len(splunk_events) > 0:
		df = pd.DataFrame(splunk_events)
		return df["marker"].to_list()
	else:
		return []


if __name__ == "__main__":
	print(get_macs("XB6"))


