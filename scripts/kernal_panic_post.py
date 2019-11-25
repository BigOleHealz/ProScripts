import os, time, re, json
from datetime import datetime as dt

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

def find_pid_row(contents: list):
	pattern = r'Process'
	for i, row in enumerate(contents):
		if re.search(pattern, row): return i
	return False

@timeit
def run():
	output_folder = f'{os.getcwd()}/output_folder/kernal_panic/logs'
	output_file = f'{os.getcwd()}/output_folder/kernal_panic/traces.txt'
	open(output_file, 'w').close()

	for filename in os.listdir(output_folder):
		
		with open(f'{output_folder}/{filename}', 'r') as f:
			content_lines = f.readlines()

		idx_pid = find_pid_row(content_lines)
		if idx_pid:
			with open(output_file, 'a') as file:
				ipv6 = filename.split('_')[0]
				trace = content_lines[idx_pid].strip('\n')
				file.write(f'{trace}-{ipv6}\n')

	with open(output_file, 'r') as file: lines = file.readlines()
	content = ''.join(sorted(lines))
	with open(output_file, 'w') as file: file.write(content)
	with open(output_file, 'r') as file: content = [line.strip('\n') for line \
		in file.readlines()]

	data = {}
	for trace in content:
		process = trace.split()[1]
		macs = data.get(process, None)
		mac = trace.split('-')[-1].split('.')[0]

		if macs: data[process].append(mac)
		else: data[process] = [mac]

	with open(f'{os.getcwd()}/output_folder/kernal_panic/counts.txt', 'w') as file:
		file.write(json.dumps(data, indent=4, sort_keys=True))

if __name__ == "__main__":
	run()