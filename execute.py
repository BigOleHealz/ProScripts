#!/usr/bin/env python3
'''
Created August 8, 2019

@author: Matt Healy
'''
import argparse, os
from util.classes import Device

path = 'scripts'

if __name__ == "__main__":
	choices = [os.path.splitext(file)[0] for file in os.listdir(path) if file.endswith('.py')]
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--script', dest='script', type=str, choices=choices,
		help='Type in the script you want executed', default='daily_percentages')
	args = parser.parse_args()
	imported = getattr(__import__(path, fromlist=[args.script]), args.script)

	imported.run()
