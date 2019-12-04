'''
Created on Mar 30, 2019

@author: vmoodg987
'''
import os, re, json, requests
import pandas as pd
import static.credentials as creds
from static.static import device_types, device_dict

class EditConfluence:
	BASE_URL = r'https://stbit02.ccp.xcal.tv/'
	headers = {'Content-Type': 'application/json'}
	users = (creds.mhealy_ntid, creds.mhealy_password)
	USERNAME = creds.USERNAME
	PASSWORD = creds.PASSWORD
	REST_URL = 'stbLogs/getLogs?format=json'
	
	def __init__( self):
		self.jsn_data = {}
		 
	def __del__(self):
		class_name = self.__class__.__name__
		print(class_name, "destroyed")
	
	# Get page id
	def get_page_id(self, device_type):
		return device_dict[device_types[device_type]]["devices"][device_type][
			'confluence_page_id']

	# Get page version
	def get_page_version(self, page_id):
		url = 'https://etwiki.sys.comcast.net/rest/api/content/' + str(page_id)
		try:
			page_info = json.loads(requests.get(url, headers=self.headers, 
				auth=self.users).text)
			page_version = page_info['version']['number']
			return page_version
		except Exception as e:
			print("Exception in getting page version :", e)
			return None

	# Get page version
	def get_page_title(self, page_id):
		url = 'https://etwiki.sys.comcast.net/rest/api/content/' + str(page_id)
		try:
			page_info = json.loads(requests.get(url, headers=self.headers, 
				auth=self.users).text)
			page_title = page_info['title']
			return page_title
		except Exception as e:
			print ("Exception in getting page version :",e )
			return None

	# Get page contents
	def get_page_contents(self, page_id):
		url = '''https://etwiki.sys.comcast.net/rest/api/content/{id}?expand=body.storage'''.format(id=page_id)
		try:
			page_contents = json.loads(requests.get(url, headers=self.headers,
				auth=self.users).text)
			contents = str(page_contents['body']['storage']['value'])
			return pd.read_html(contents, header=0)[0]
		except Exception as e:
			print("Exception in getting page contents : ", e)
			return None
	
	def get_data(self, jsn_data):
		new_data = '''
			<table class=\"wrapped\">
				 <colgroup>
					<col />
					<col />
					<col />
				 </colgroup>                     
				 <tbody>                      
					<tr>
					   <td><strong>Splunk search Parameter</strong></td>
					   <td><strong>String</strong></td>                            
					   <td><strong>File</strong></td>
					</tr>'''

		for data in jsn_data:
			#list of characters to be replace to avoid xhtml parsing errors
			char_list = ['<', '>', '/', '&']
			if data.keys():
				new_data = new_data + '''
				<tr> 
					<td>''' + re.sub("|".join(char_list), "",data["header"]) + '''</td>
					<td>''' + re.sub("|".join(char_list), "",data["content"])  +'''</td>
					<td>''' + re.sub("|".join(char_list), "",data["type"])  +  '''</td>
				</tr>'''
				
		new_data = new_data + "</tbody></table>"
		return new_data.replace('\n','').replace('     ', '')

	# Update the page
	def update_page(self, page_id, page_version, title, data):
		url = 'https://etwiki.sys.comcast.net/rest/api/content/{id}'.format(id=page_id) 
		update_data = {
			"id": page_id,
			"type": "page",
			"title": title,
			"space": {
				"key": "CPE"
			},
			"body": {
				"storage": {
					"value": str(data),
					"representation": "storage"
				}
			},
			"version": {
				"number": page_version + 1
			}
		}
		update_page_status = requests.put(url, headers=self.headers, auth=self.users,
			data=json.dumps(update_data))
		return update_page_status.status_code
	
	def edit_confluence_page(self,page_title):
		page_id = self.get_page_id(page_title)

		if page_id != None:
			page_version = self.get_page_version(page_id)
			if page_version != None:
				jsn_data = self.get_data(data)
				return self.update_page(page_id, page_version, page_title, jsn_data)

