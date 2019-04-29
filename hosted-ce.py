#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import argparse
import sys
import htcondor

# Nagios exit status
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

def main():
    args = parse_args()
    states = [STATE_OK]
    messages = []

    
    coll = htcondor.Collector(args.hostname)
    schedd_ad = coll.locate(htcondor.DaemonTypes.Schedd)
    schedd = htcondor.Schedd(schedd_ad)
    submitted_jobs = False
    stats = {
        'held': 0,
        'idle_long': 0
    }

    # Check for held job
    for job in schedd.xquery(requirements = 'RoutedJob == TRUE'):
        if 'JobStatus' in job and job['JobStatus'] == 5:
            stats['held'] += 1
            continue
        
        # Has the routed job been idle for longer than 10 minutes, ie not submitted
        if job['JobStatus'] == 1 and (job['ServerTime'] - job['EnteredCurrentStatus']) > 60*10 and 'GridJobStatus' not in job:
            stats['idle_long'] += 1
            continue

        # Check for grid job id
        if 'GridJobId' in job:
            # Check for remote
            gridJobId = job['GridJobId']
            try:
                remote_id = gridJobId.split(" ")[-1:]
            except:
                pass

    if stats['held'] > 0:
        print("Held Job(s)")
        sys.exit(STATE_CRITICAL)
    if stats['idle_long'] > 0:
        print("Long idle Job")
        sys.exit(STATE_CRITICAL)

    print('OK')
    sys.exit(STATE_OK)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname')
    return parser.parse_args()

if __name__ == "__main__":
    # Run script as main
    main()
