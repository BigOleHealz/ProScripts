#!/usr/bin/python3.6
import requests
import static.credentials as creds

def send_simple_message(sender, recipient, subject, message=""):
	return requests.post(creds.mailgun_url,
		auth=("api", creds.api_key),
		data={"from": sender,
				"h:sender": sender,
				"to": recipient,
				"subject": subject,
				"html": message,
				})