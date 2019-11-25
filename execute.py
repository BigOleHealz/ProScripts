from scripts.kernal_panic import write_to_file
import argparse, os

path = 'scripts'

if __name__ == "__main__":

	choices = [os.path.splitext(file)[0] for file in os.listdir('scripts/') if file.endswith('.py')]
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--script', dest='script', type=str, choices=choices,
		help='Type in the script you want executed', default='daily_percentages')
	args = parser.parse_args()

	imported = getattr(__import__(path, fromlist=[args.script]), args.script)

	if args.script == 'kernal_panic':
		imported.write_to_file()
	elif args.script in ['confluence_vs_portal', 'daily_percentages', 'find_duplicates', 'kernal_panic_post', 'pull_telemetry_configs', 'valuable_markers']:
		imported.run()
