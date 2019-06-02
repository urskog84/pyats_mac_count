# Overview

This test connects to all devices defined in the testbed, and parses are mac address tabel
if a vlan have les then x mac-addresse test case fails. 

# Running

```
easypy mac_job.py -html_logs -testbed_file ../testbed.yaml
```

# Docker
```
docker run -v c:/git/pyats_mac_count:/pyats/git -it ciscotestautomation/pyats:latest easypy run job /pyats/git/examples/basic/job/basic_example_job.py
```



## Links
https://developer.cisco.com/docs/pyats/
https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/index.html
