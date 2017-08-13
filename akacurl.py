#!/usr/local/bin/python3
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json
import sys, os.path, os


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
  def dump(self, response):
    self.pp.dump(response)

  def get_rules(self, filename=None):
    pass
  def get_group(self):
    r=self.pp.get('/papi/v1/groups')
    #self.pp.dump(r)
    return r

  def get_contract(self):
    r = self.pp.get('/papi/v1/contracts')
    #self.pp.dump(r)
    return r

  def get_properties(self, cid, gid):
    '''
    default filenmae: prop_cid_gid.json
    '''
    r = self.pp.get('/papi/v1/properties?contractId={}&groupId={}'.format(cid, gid))
    #self.pp.dump(r)
    return r

  def dump_rules(self, cid, gid, pid, ver, propname=None, filename=None):
    r = self.pp.get('/papi/v1/properties/{}/versions/{}/rules?contractId={}&groupId={}&validateRules=false'.format(pid, ver, cid, gid))
    #self.pp.dump(r)
    
    if filename is None:
      if propname is None:
        propname=pid
      filename='{}.v{}.json'.format(propname, ver)

    os.makedirs(os.path.join('dump', gid), exist_ok=True)
    with open( os.path.join('dump', gid, filename), 'w') as f:
      f.write(r.content.decode('utf-8'))
  
  def dump_rules_in_group(self, cid, gid):
    r = self.get_properties(cid, gid)
    plist = json.loads(r.content.decode('utf-8'))
    #print(plist)
    for p in plist['properties']['items']:
      print(p['propertyName'])
      self.dump_rules(cid, gid, p['propertyId'], p['productionVersion'], p['propertyName'])




if __name__ == '__main__':
  #pp = papirec()
  #r=pp.get('/diagnostic-tools/v1/locations')
  #pp.dump(r)
  
  ppap = papiapp()
  #r=ppap.get_group()
  #ppap.dump(r)
  #ppap.get_contract()

  ### ctr_1-GNLXD, grp_104613
  #ppap.get_properties('ctr_1-GNLXD', 'grp_104613')

  ### prp_385479 (sdjptools.akamaized.net)
  #ppap.dump_rules('ctr_1-GNLXD', 'grp_20628', 'prp_385479', 5)

  ppap.dump_rules_in_group('ctr_1-GNLXD', 'grp_104613')
