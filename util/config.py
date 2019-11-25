import logging
import pandas as pd, os

def set_configs(filename):
	pd.set_option('display.max_rows', 300)
	pd.set_option('display.max_columns', 300)
	pd.set_option('display.width', 1800)
	pd.set_option('display.max_colwidth', 300)

	file_text = filename.split('/')[-1].split('.')[0]
	log_file_name = f"/app/log/{file_text}.log"

	if not os.path.exists(log_file_name): open(log_file_name, 'w').close()

	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
		datefmt='%m-%d %H:%M:%S',
		filename=log_file_name,
		filemode='a')

if __name__ == "__main__":
	set_configs()