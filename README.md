This is a checkmk (https://checkmk.com/) plugin for the status of Hosted CEs.

The script queries the condor queue status of the Hosted CE, and counts jobs in running, idle and held status respectedly, and queries the factory for the attributes "GlideinConfigPerEntryMaxHeld" and "GlideinMonitorTotalRequestedIdle" of the Hosted CE.

Status of a Hosted CE is critical if:
1. There are no running jobs, but there are jobs idling for more than 10 minutes.

2. If there are jobs in "requested_idle" jobs:

  * If there are no running jobs, but there are jobs in "held" status (jobs are held by the CE)
  
  * If there are no running jobs, and no held and idle jobs, too (obs are not entering the CE)
  
  * If there are running jobs, but the held jobs exceeds 90% of the "GlideinConfigPerEntryMaxHeld" configured for the Hosted CE
  
  * Regardless of running jobs, if held jobs exceeds the "GlideinConfigPerEntryMaxHeld" configured for the Hosted CE
