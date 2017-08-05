import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json

edgerc=EdgeRc('.edgerc')
baseurl='{}{}'.format('https://', edgerc.get('default', 'host'))

s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, 'default')

req='{}{}'.format(baseurl, '/diagnostic-tools/v1/locations')
r = s.get(req)

print(req)
print(r.status_code)

#print(r.content.decode('utf-8'))
j=json.loads(r.content.decode('utf-8'))
print(json.dumps(j, indent=2))




