'''
Created Nov 15, 2019

@author: Matt Healy

Purpose: From locally stored folder full of recently-pulled device logs, create
	a dict with types {string : set} with kernal panic trace markers as the 
	key and the [unique] set of MACs that exhibited that marker as the value. 
	After the dictionary has been created, we cast the values to lists so that 
	we can write the dict to a .txt file (sets are not compatible with JSON)
'''
import os, re, json
from util.utility_functions import timer

def find_pid_indexes(contents: str):
	'''
	Return start & end indices of all kernal panic traces in the content passed-in

	:param contents: resetinfo.txt.0 file contents
	:return indexes: list of tuples containing the indexes of the first & last
		characters of the kernal panic trace
	'''
	pattern = r'CPU: [0-9] PID: ([0-9])* ([\S])*: ([\S])*'
	indexes = [(m.start(0), m.end(0)) for m in re.finditer(pattern, contents)]
	return indexes

@timer
def run():
	output_folder = f'{os.getcwd()}/output_folder/kernal_panic/logs'
	output_file = f'{os.getcwd()}/output_folder/kernal_panic/traces.txt'
	open(output_file, 'w').close()

	trace_dict = {}
	for filename in os.listdir(output_folder):
		mac = filename.split('.')[0]
		with open(f'{output_folder}/{filename}', 'r') as f: content = f.read()

		for (start, end) in find_pid_indexes(content):
			trace = content[start:end].split()[-1]
			macs = trace_dict.get(trace, None)
			if macs: trace_dict[trace].add(mac)
			else: trace_dict[trace] = {mac}

	trace_dict = {key : list(trace_dict[key]) for key in trace_dict.keys()}
	with open(f'{os.getcwd()}/output_folder/kernal_panic/counts.txt', 'w') as file:
		file.write(json.dumps(trace_dict, indent=4, sort_keys=True))
	
if __name__ == "__main__":
	run()
