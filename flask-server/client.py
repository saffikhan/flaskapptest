import httplib
import random
import json
import time

import xconfig

# Sample data to be sent via post.
sample = []
for i in range(xconfig.SAMPLE_DATA_MAX):
    sample.append({'userCode': i, 'timeSpent': random.random()})


# Starts the connection to the site
conn = httplib.HTTPConnection(xconfig.SITE_SERVER_HOST,
                              xconfig.SITE_SERVER_PORT)

for s in sample:
    # Encodes client data in json format
    cdata = json.dumps(s)

    # Send to site
    conn.request('POST', '/site', cdata, {
        'Content-Type': 'application/json'
    })
    try:
        # Get the answer
        data = conn.getresponse().read()
        print json.loads(data)
    except:
        pass
    finally:
        conn.close()

    # Wait between requests
    time.sleep(0.001)
