#!/usr/bin/env python3
'''
Created August 8, 2019

@author: Matt Healy

Purpose: Please type the command `python execute.py [-s|--script]
	[confluence_vs_portal | daily_percentages | find_duplicates | kernal_panic_pre |
	kernal_panic_post | pull_telemetry_configs | valuable_markers]`
'''
import argparse, os

path = 'scripts'

if __name__ == "__main__":
	choices = [os.path.splitext(file)[0] for file in os.listdir(path) if file.endswith('.py')]
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--script', dest='script', type=str, choices=choices,
		help='Type in the script you want executed', default='daily_percentages')
	args = parser.parse_args()

	imported = getattr(__import__(path, fromlist=[args.script]), args.script)

	imported.run()
