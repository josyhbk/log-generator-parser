import jsonlines
import time

from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time

app = Flask(__name__)

_INF = float("inf")

graphs = {}
graphs['tx'] = Histogram('tx_value', 'Histogram for the tx values.', buckets=(500, 1000, 5000, 9000, _INF))
graphs['rx'] = Histogram('rx_value', 'Histogram for the rx values.', buckets=(500, 1000, 5000, 9000, _INF))

@app.route("/")
def hello():
    return """
<xmp>
HI, welcome to a simple landing page,
Go to the path /parse to start generating metrics,
You can then visit the path /metrics in case you would like to see plain text metrics
or open this url to view Grafana Dashboards:
http://localhost:3000/d/pvXvovKWz/parser-log-metrics?orgId=1
</xmp>"""

@app.route("/parse")
def parse():
    start_time = time.time()
    # this line assumes you ran log.py first, if you only want to test this script
    # change the file to extract.log
    with jsonlines.open('/opt/samples.log') as reader:
        for obj in reader:
            graphs['tx'].observe(obj["Tx"])
            graphs['rx'].observe(obj["Rx"])
    message = "--- Parse completed in" + "--- " +'{:f}'.format((time.time() - start_time)) + " seconds ---"
    return str(message)

@app.route("/metrics")
def metrics():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
        print (str(res))
    return Response(res, mimetype="text/plain")
