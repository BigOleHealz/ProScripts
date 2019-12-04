
device_types = {
	"XF3": "RDKB",
	"XB3": "RDKB",
	"XB6": "RDKB",
	"XI5": "RDKV",
	"XG": "RDKV"
}

device_dict = {
	"RDKB" : {
		"email_subject": "Missing Mandatory Markers on RDK-B",
		"recipient_list": ["matthew_healy@comcast.com",
			"arun_sunny@comcast.com",
			"vasavi_mahadev@comcast.com",
			],
		"devices" : {
			"XF3" : {
				"splunk_query_macs": "search earliest=-1m index=rdk-json PX5001_3* prod comcast | stats count by mac | fields - count| head 35",
				"splunk_query_daily_percentages": 'search earliest=-15m index=rdk-json sourcetype=rdk-json (TG3482PC2 OR CGM4140COM) PROD_sey RDKB "WIFI_INFO_*" comcast |rex "(?<stage_time>WIFI_INFO_\\w+\\":\\"\\d+\\")" max_match=300|mvexpand stage_time |rename searchResult{}.Version as Verison|rex field=stage_time WIFI_INFO_(?P<stage>\\w+)\\":\\"(?<value>\\d+)\\" |eval MODEL=mvindex(split(Verison,"_"),0) | eval type = IF(MODEL LIKE "TG1682%","XB3",  IF(MODEL LIKE "DPC3941%","XB3",  IF(MODEL LIKE "DPC3939%","XB3",  IF(MODEL LIKE "TG3482PC2%","XB6", IF(MODEL LIKE "CGM4140COM%","XB6",IF(MODEL LIKE "CGA4131COM%","XB6",XF3)))))) | strcat "WIFI_INFO" "_" stage marker| stats dc(mac) as devices by marker type',
				"command" : "Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6",
				"logpath" : "/tmp/DCMresponse.txt",
				"model" : "PX5001_3",
				"confluence_page_id" : 588864951,
				"confluence_vs_portal_email_list" : ["Matthew_HEALY@comcast.com", 
													# "vasavi_mahadev@comcast.com", 
													# "Prasob_Kizhedath2@cable.comcast.com"
													],

			},
			"XB3" : {
				"splunk_query_macs": "search earliest=-1m index=rdk-json TG1682_3* prod comcast | stats count by mac | fields - count| head 35",
				"splunk_query_daily_percentages": 'search earliest=-15m index=rdk-json sourcetype=rdk-json (TG3482PC2 OR CGM4140COM) PROD_sey RDKB "WIFI_INFO_*" comcast |rex "(?<stage_time>WIFI_INFO_\\w+\\":\\"\\d+\\")" max_match=300|mvexpand stage_time |rename searchResult{}.Version as Verison|rex field=stage_time WIFI_INFO_(?P<stage>\\w+)\\":\\"(?<value>\\d+)\\" |eval MODEL=mvindex(split(Verison,"_"),0) | eval type = IF(MODEL LIKE "TG1682%","XB3",  IF(MODEL LIKE "DPC3941%","XB3",  IF(MODEL LIKE "DPC3939%","XB3",  IF(MODEL LIKE "TG3482PC2%","XB6", IF(MODEL LIKE "CGM4140COM%","XB6",IF(MODEL LIKE "CGA4131COM%","XB6",XF3)))))) | strcat "WIFI_INFO" "_" stage marker| stats dc(mac) as devices by marker type',
				"command" : "Device.X_CISCO_COM_CableModem.IPv6Address",
				"logpath" : "/tmp/DCMresponse.txt",
				"model" : "TG1682_3",
				"confluence_page_id" : 111991581,
				"confluence_vs_portal_email_list" : ["Matthew_HEALY@comcast.com", 
													"vasavi_mahadev@comcast.com", 
													"arun_sunny@comcast.com"],
			},
			"XB6" : {
				"splunk_query_macs": "search earliest=-1m index=rdk-json TG3482PC2_3* prod comcast | stats count by mac | fields - count| head 35",
				"splunk_query_daily_percentages": 'search earliest=-15m index=rdk-json sourcetype=rdk-json (TG3482PC2 OR CGM4140COM) PROD_sey RDKB "WIFI_INFO_*" comcast |rex "(?<stage_time>WIFI_INFO_\\w+\\":\\"\\d+\\")" max_match=300|mvexpand stage_time |rename searchResult{}.Version as Verison|rex field=stage_time WIFI_INFO_(?P<stage>\\w+)\\":\\"(?<value>\\d+)\\" |eval MODEL=mvindex(split(Verison,"_"),0) | eval type = IF(MODEL LIKE "TG1682%","XB3",  IF(MODEL LIKE "DPC3941%","XB3",  IF(MODEL LIKE "DPC3939%","XB3",  IF(MODEL LIKE "TG3482PC2%","XB6", IF(MODEL LIKE "CGM4140COM%","XB6",IF(MODEL LIKE "CGA4131COM%","XB6",XF3)))))) | strcat "WIFI_INFO" "_" stage marker| stats dc(mac) as devices by marker type',
				"command" : "Device.X_CISCO_COM_CableModem.IPv6Address",
				"logpath" : "/tmp/DCMSettings.conf",
				"model" : "TG3482PC2_3",
				"confluence_page_id" : 152733303,
				"confluence_vs_portal_email_list" : ["Matthew_HEALY@comcast.com",
													# "vasavi_mahadev@comcast.com", 
													# "sridharguptha_guntha@comcast.com"
													],
			}
		},
	},
	"RDKV" : {
		"email_subject": "Missing Mandatory Markers on RDK-V",
		"recipient_list": ["matthew_healy@comcast.com",
				"Dileep_Ravindranathan@cable.comcast.com",
				"Nirmal_Unnikrishnan@cable.comcast.com",
				"vasavi_mahadev@comcast.com",
				],
		"devices" : {
			"XI5" : {
				"splunk_query_macs": "search earliest=-1m index=rdk-json PX051AEI_3* prod comcast | stats count by mac | fields - count| head 35",
				"splunk_query_daily_percentages": 'search earliest=-15m index=rdk-json sourcetype=rdk-json PXD01ANI|fieldsummary|dedup field|table field',
				"command" : "Device.DeviceInfo.X_COMCAST-COM_STB_IP",
				"logpath" : "/tmp/DCMSettings.conf",
				"model" : "PX051AEI_3",
				"confluence_page_id" : 536722578,
				"confluence_vs_portal_email_list" : ["Matthew_HEALY@comcast.com",
													# "vasavi_mahadev@comcast.com", 
													# "dileep_ravindranathan@cable.comcast.com"
													],
			},
			"XG" : {
				"splunk_query_macs": "search earliest=-1m index=rdk-json MX011AN_3* prod comcast | stats count by mac | fields - count| head 35",
				"splunk_query_daily_percentages": 'search earliest=-15m index=rdk-json sourcetype=rdk-json PXD01ANI|fieldsummary|dedup field|table field',
				"command" : "Device.DeviceInfo.X_COMCAST-COM_STB_IP",
				"logpath" : "/tmp/DCMSettings.conf",
				"model" : "MX011AN_3",
				"confluence_page_id" : 110497816,
				"confluence_vs_portal_email_list" : ["Matthew_HEALY@comcast.com",
													# "vasavi_mahadev@comcast.com",
													# "dileep_ravindranathan@cable.comcast.com"
													],
			},
		}
	}
}