import os, re, json
from util.utility_functions import timer

def find_pid_indexes(contents: str):
	pattern = r'CPU: [0-9] PID: ([0-9])* ([\S])*: ([\S])*'
	return [(m.start(0), m.end(0)) for m in re.finditer(pattern, contents)]

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
			if macs: trace_dict[trace].append(mac)
			else:  trace_dict[trace] = [mac]

	with open(f'{os.getcwd()}/output_folder/kernal_panic/counts.txt', 'w') as file:
		file.write(json.dumps(trace_dict, indent=4, sort_keys=True))
	

if __name__ == "__main__":
	run()