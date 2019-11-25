from util.splunk import query_splunk
from util.web_pa import WebpaUtils as web_pa

def write_to_file():
	result = query_splunk('''earliest=-120m index=rdk-json TG3482PC2_3.12p8s1_PROD_sey
		SYS_ERROR_KernelPanic_reboot | stats count as cnt by searchResult{}.mac''',
		kwargs_oneshot={'count' : 10000})

	macs = [elem['searchResult{}.mac'] for elem in result]
	estb_macs = [web_pa.ecm_to_estb(mac) for mac in macs]
	ips = sorted([ip for ip in estb_macs if ip is not False])

	with open('output_folder/kernal_panic/estb_macs.txt', 'w') as file: file.write('\n'.join(ips))
	with open('output_folder/kernal_panic/estb_macs.txt', 'r') as file: print(file.read())

write_to_file()