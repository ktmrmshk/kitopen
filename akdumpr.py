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
    for k,v in response.headers.items():
      print(": ".join([k,v]))

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
    
    if r.status_code!=200:
      print('>>> Err: {}, ver{}, status={}, pid={}'.format(propname, ver, r.status_code, pid))
      return

    if filename is None:
      if propname is None:
        propname=pid
      filename='{}.v{}.json'.format(propname, ver)

    os.makedirs(os.path.join('dump', cid, gid), exist_ok=True)
    with open( os.path.join('dump', cid, gid, filename), 'w') as f:
      f.write(r.content.decode('utf-8'))
  
  def dump_rules_in_group(self, cid, gid):
    r = self.get_properties(cid, gid)
    if r.status_code!=200:
      print('>>> Err: get_properties(): cid={}, gid={}, status={}'.format(cid, gid, r.status_code))
      return

    plist = json.loads(r.content.decode('utf-8'))
    #print(plist)
    for p in plist['properties']['items']:
      ver=int()
      if p['productionVersion'] != None:
        ver=p['productionVersion']
      elif p['stagingVersion'] != None:
        ver=p['stagingVersion']
      else:
        ver=p['latestVersion']
      print(p['propertyName'])
      self.dump_rules(cid, gid, p['propertyId'], ver, p['propertyName'])

  def dump_rules_in_contract(self, cid):
    gids={}
    r=self.get_group()
    j=json.loads(r.content.decode('utf-8'))
    for g in j['groups']['items']:
      if 'contractIds' in g and cid in g['contractIds']:
        gids[ g['groupId'] ] = g['groupName']
    #print(gids)
    
    for gid in gids.keys():
      self.dump_rules_in_group(cid, gid)


def usage():
  print('usage: python3 akacurl contractid credential_file')

if __name__ == '__main__':
  #pp = papirec()
  #r=pp.get('/diagnostic-tools/v1/locations')
  #pp.dump(r)
  
  if len(sys.argv) != 3:
    print('error')
    usage()
    exit()

  #ppap = papiapp('1H3N4NC.cred')
  ppap = papiapp(sys.argv[2])
  
  #r=ppap.get_contract()
  #ppap.dump(r)
  #r=ppap.get_group()
  #ppap.dump(r)

  ### ctr_1-GNLXD, grp_104613
  #r=ppap.get_properties('ctr_3-1H3N4NC', 'grp_65684')
  #ppap.dump(r)

  ### prp_385479 (sdjptools.akamaized.net)
  #ppap.dump_rules('ctr_1-GNLXD', 'grp_20628', 'prp_385479', 5)

  #ppap.dump_rules_in_group('ctr_1-GNLXD', 'grp_104613')
  ppap.dump_rules_in_contract(sys.argv[1])
  #ppap.dump_rules_in_contract('ctr_3-1H3N4NC')


