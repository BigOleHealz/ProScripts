# Overview
This repository has 4 folders with the followinging purposes:
* output_folder - Hold output data generated from scripts
* scripts - Runnable scripts to be executed
* static - Stores input data used by scripts as well as a static.py which stores commonly recurring values in a JSON and a credentials.py that stores valid credentials for Splunk, Mailgun, and WebPA credentials. May need to be updated each time before running script depending on which script (will specify below)
* util - Stores helpful utility functions and classes that came up multiple times during the implementation of this repo

# Usage
In the command line, type the following:
`ssh mhealy066@96.118.150.198`
`source env/bin/activate`
`cd scripts/TelemetryProject`
Make sure that the _ntid_ and _password_ variables in the static/credentials.py file are set equal to valid credentials with T-Rex server access.
Then, to run a particular script enter:
`python execute.py -s [confluence_vs_portal | daily_percentages | find_duplicates | kernal_panic_pre | kernal_panic_post | populate_gnr | pull_telemetry_configs | valuable_markers]`
