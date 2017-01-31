import httplib
import random
import json
import time

import xconfig
import requests

# Sample data to be sent via post.
sample = []
for i in range(xconfig.SAMPLE_DATA_MAX):
    sample.append({'userCode': i, 'timeSpent': random.random()})

for s in sample:
    # Encodes client data in json format
    cdata = json.dumps(s)

    # make request
    print 'sent: %s' % cdata

    res = requests.post(xconfig.SITE_SERVER_URL + "/site", data=cdata, headers={
        'Content-Type': 'application/json'
    })

    try:
        # Get the answer
        print 'received: %s' % res.json()
    except:
        pass
    finally:
        res.close()

    # Wait between requests
    time.sleep(0.5)
