#!/usr/local/bin/python3
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json
import sys

edgerc=EdgeRc('.edgerc')
baseurl='{}{}'.format('https://', edgerc.get('default', 'host'))

s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, 'default')

#req='{}{}'.format(baseurl, '/diagnostic-tools/v1/locations')
req='{}{}'.format(baseurl, sys.argv[1])
r = s.get(req)

print(req)
print(r.status_code)

#print(r.content.decode('utf-8'))
j=json.loads(r.content.decode('utf-8'))
print(json.dumps(j, indent=2))




