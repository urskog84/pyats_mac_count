FROM ciscotestautomation/pyats:latest

COPY mac_job.py mac_test.py testbed.yaml requirements.txt ./

RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt
CMD easypy mac_job.py -html_logs -testbed_file testbed.yaml