'''
MIT License

Copyright (c) 2017 Masa Kitamura

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
'''


import json
import datetime
import os
import sys

class Papils(object):
  def __init__(self):
    '''
    data scheme
    * dict
      - cid, gid, pid, pname, ver, [(dp,edgehost)], is_secure, [(rule, origin type, origin host, FOSSLtype, CNmatch value, [pincert CN, pincert expiration])]   
    '''
    self.record={}

  def parseRuleTree(self, ruletree):
    self.record['ver']=ruletree['propertyVersion']
    self.record['cid']=ruletree['contractId']
    self.record['pname']=ruletree['propertyName']
    self.record['gid']=ruletree['groupId']
    self.record['pid']=ruletree['propertyId']
    self.record['origin']=[]

    self.is_secure=''
    if 'is_secure' not in ruletree['rules']['options']:
      self.record['is_secure']=False
    else:
      self.record['is_secure']=ruletree['rules']['options']['is_secure']

    self.parseRule(ruletree['rules'], [ruletree['rules']['name']], self.record['is_secure'])


  def parseRule(self, rule, rulename, is_secure):
    self.parseBehavior(rule['behaviors'], rulename, is_secure)
    for crule in rule['children']:
      self.parseRule(crule, rulename+[crule['name']], is_secure)

  def parseBehavior(self, behaviors, rulename, is_secure):
    originb=[]
    for b in behaviors:
      if b['name'] == 'origin':
        originb.append(b)
    
    if originb:
      for b in originb:
        self.parseOrigin(b, is_secure, rulename)

  def parseOrigin(self, b, is_secure, rulename):
    'b: behavior dict'
    if b['name'] != 'origin':
      return
    opt=b['options']
    

    rec={}
    rec['pincert']=[]
    rec['rulename']=' > '.join(rulename).replace('default > ', '')

    rec['origintype']=opt['originType']
    if opt['originType'] == 'NET_STORAGE':
      try:
        rec['originhost']='{}/{}/'.format(opt['netStorage']['downloadDomainName'], opt['netStorage']['cpCode'])
      except Exception:
        #rec['originhost']=''
        pass

    elif opt['originType'] == 'CUSTOMER':
      rec['originhost']=opt['hostname']
      if is_secure:
        if opt['verificationMode'] == 'CUSTOM':
          rec['fossltype']=opt['originCertsToHonor']
          rec['fosslcn']=opt['customValidCnValues']
          if opt['originCertsToHonor'] == 'CUSTOM_CERTIFICATES':
            self.pin_certs=opt['customCertificates']
            for pinc in opt['customCertificates']:
              d=datetime.datetime.fromtimestamp(pinc['notAfter']/1e3)
              pin_expire='{}/{}/{}'.format(d.year, d.month, d.day)
              rec['pincert'].append( (pinc['subjectCN'], pin_expire) )
        elif opt['verificationMode'] == 'PLATFORM_SETTINGS':
          rec['fossltype'] = 'PLATFORM_SETTINGS'
    else:
      raise
    self.record['origin'].append(rec)
    return

  def __str__(self):
    cid = self.record['cid']
    gid = self.record['gid']
    pid = self.record['pid']
    pname = self.record['pname']
    ver = self.record['ver']
    is_secure = self.record['is_secure']
    origin = self.record['origin']
    export_origin=[]
    for org in origin:
      tmp_org={}
      tmp_org['rulename'] = org['rulename']
      tmp_org['origintype'] = org.get('origintype', '-')
      tmp_org['originhost'] = org.get('originhost', '-')
      tmp_org['fossltype'] = org.get('fossltype', '-')
      tmp_org['fosslcn'] = org.get('fosslcn', '-')
      tmp_org['pincert'] = org['pincert']
      export_origin.append(tmp_org)

    return '{}, {}, {}, {}, {}, {}, {}'.format(cid, gid, pid, pname, ver, is_secure, export_origin)


  def printline(self):
    def str_fosslcn(fosslcn):
      return ' or '.join(fosslcn)
       
    cid = self.record['cid']
    gid = self.record['gid']
    pid = self.record['pid']
    pname = self.record['pname']
    ver = self.record['ver']
    is_secure = self.record['is_secure']
    origin = self.record['origin']
    export_origin=[]
    for org in origin:
      tmp_org={}
      tmp_org['rulename'] = org['rulename']
      tmp_org['origintype'] = org.get('origintype', '-')
      tmp_org['originhost'] = org.get('originhost', '-')
      tmp_org['fossltype'] = org.get('fossltype', '-')
      tmp_org['fosslcn'] = org.get('fosslcn', '-')
      if org['pincert'] == []:
        print( '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(cid, gid, pid, pname, ver, is_secure, tmp_org['rulename'].decode('utf-8'), tmp_org['origintype'], tmp_org['originhost'], tmp_org['fossltype'], str_fosslcn( tmp_org['fosslcn']), '-', '-') )
      else:
        for p in org['pincert']:
          print( '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(cid, gid, pid, pname, ver, is_secure, tmp_org['rulename'].decode('utf-8'), tmp_org['origintype'], tmp_org['originhost'], tmp_org['fossltype'], str_fosslcn(tmp_org['fosslcn']), p[0], p[1]) )

def walk(rootdir):
  for root, subdir, files in os.walk(rootdir):
    for f in files:
      filepath=os.path.join(root, f)
      ruletree=''
      if not filepath.endswith('.json'):
        continue
      with open(filepath) as fin:
        ruletree=json.load(fin)
      try:
        p=Papils()
        p.parseRuleTree(ruletree)
        p.printline()
      except Exception as err:
        print('ERR: {} at {}'.format(err, filepath))

def usage():
  print('usage: python3 papi_parse.py dirname')

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('error:')
    usage()
    exit()

  walk(sys.argv[1])



