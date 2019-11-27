import os
from util.splunk import query_splunk
from util.web_pa import WebpaUtils as web_pa

def write_to_file(dict_list):
	macs = [elem['mac'] for elem in dict_list]
	estb_macs = [web_pa.ecm_to_estb(mac) for mac in macs]
	estb_macs= sorted([ip for ip in estb_macs if ip is not False])

	with open(f'{os.getcwd()}/output_folder/kernal_panic/estb_macs.txt', 'w') as file:
		file.write('\n'.join(estb_macs))

def run():
	result = query_splunk('''earliest=-120m index=rdk-json TG3482PC2_3.12p8s1_PROD_sey
		SYS_ERROR_KernelPanic_reboot | stats count by mac''',
		kwargs_oneshot={'count' : 10000})

	write_to_file(result)
