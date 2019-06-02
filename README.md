# Overview

This test connects to all devices defined in the testbed, and parses are mac address tabel
if a vlan have les then x mac-addresse test case fails. 

# Running

```
easypy mac_job.py -html_logs -testbed_file ../testbed.yaml
```

# Run from Dockerfile
```
docker run -it $(docker build . -q)
```



## Links
https://developer.cisco.com/docs/pyats/
https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/index.html
