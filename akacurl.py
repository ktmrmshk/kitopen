#!/usr/local/bin/python3
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json
import sys

class papireq(object):
  def __init__(self, edgerc_file='.edgerc'):
    self.edgerc_file=edgerc_file
    self.edgerc=EdgeRc(self.edgerc_file)
    self.baseurl='{}{}'.format('https://', self.edgerc.get('default', 'host'))

    self.s = requests.Session()
    self.s.auth = EdgeGridAuth.from_edgerc(self.edgerc, 'default')
    
  def get(self, req_path):
    req='{}{}'.format(self.baseurl, req_path)
    response=self.s.get(req)
    return response
  
  def dump(self, response):
    print(response.url)
    print(response.status_code)

    #print(r.content.decode('utf-8'))
    j=json.loads(response.content.decode('utf-8'))
    print(json.dumps(j, indent=2))

class papiapp(object):
  def __init__(self, edgerc_file='.edgerc'):
    self.pp=papireq(edgerc_file)
  def dump_rules(self, filename=None):
    pass
  def dump_group(self):
    r = self.pp.get('/papi/v1/groups')
    self.pp.dump(r)
  def dump_contract(self):
    r = self.pp.get('/papi/v1/contracts')
    self.pp.dump(r)
  def dump_properties(self, cid, gid):
    '''
    default filenmae: prop_cid_gid.json
    '''
    r = self.pp.get('/papi/v1/properties?contractId={}&groupId={}'.format(cid, gid))
    self.pp.dump(r)
  def dump_rules(self, cid, gid, pid, ver, propname=None, filename=None):
    r = self.pp.get('/papi/v1/properties/{}/versions/{}/rules?contractId={}&groupId={}&validateRules=false'.format(pid, ver, cid, gid))
    self.pp.dump(r)
    
    if filename is None:
      if propname is None:
        propname=pid
      filename='{}.v{}.json'.format(propname, ver)

    with open(filename, 'w') as f:
      f.write(r.content.decode('utf-8'))


if __name__ == '__main__':
  #pp = papirec()
  #r=pp.get('/diagnostic-tools/v1/locations')
  #pp.dump(r)
  
  ppap = papiapp()
  #ppap.dump_group()
  #ppap.dump_contract()

  ### ctr_1-GNLXD, grp_20628
  #ppap.dump_properties('ctr_1-GNLXD', 'grp_20628')

  ### prp_385479 (sdjptools.akamaized.net)
  ppap.dump_rules('ctr_1-GNLXD', 'grp_20628', 'prp_385479', 5)


