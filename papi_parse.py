import json
import datetime
import os
import sys
'''
output:
contract, group, property name, version, rule, origin, is_secure, origin type, origin host, FOSSLtype, CNmatch value, pincert CN,  pincert expiredate

d=datetime.datetime.fromtimestamp(1613886492000/1e3)
d.year
'''

class Papils(object):
  def __init__(self):
    pass

  def parseRuleTree(self, ruletree):
    for k,v in ruletree.items():
      if k != 'rules':
        print('{}: {}'.format(k,v))    
    print(ruletree['rules']['options'])
    print('=============')
    
    
    self.ver=ruletree['propertyVersion']
    self.cid=ruletree['contractId']
    self.pname=ruletree['propertyName']
    self.gid=ruletree['groupId']

    self.is_secure=''
    if 'is_secure' not in ruletree['rules']['options']:
      self.is_secure=False
    else:
      self.is_secure=ruletree['rules']['options']['is_secure']

    self.parseRule(ruletree['rules'], [ruletree['rules']['name']], self.is_secure)

    self.printline()

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
      print( ', '.join(rulename) )
      self.rulename=' > '.join(rulename).replace('default, ', '')
      for b in originb:
        self.parseOrigin(b, is_secure)
      print('-------')

  def parseOrigin(self, b, is_secure):
    'b: behavior dict'
    if b['name'] != 'origin':
      return
    opt=b['options']
    
    self.origintype=opt['originType']
    if opt['originType'] == 'NET_STORAGE':
      print('downloadDomainName', opt['netStorage']['downloadDomainName'] ) 
      print('cpCode', opt['netStorage']['cpCode'] )
      self.originhost='{}/{}/'.format(opt['netStorage']['downloadDomainName'], opt['netStorage']['cpCode'])
    
    elif opt['originType'] == 'CUSTOMER':
      print('hostname', opt['hostname'] )
      self.originhost=opt['hostname']
      if is_secure:

        print('verificationMode', opt['verificationMode'])
        if opt['verificationMode'] == 'CUSTOM':
          self.fossltype=opt['originCertsToHonor']
          self.fosslcn=opt['customValidCnValues']
          print('originCertsToHonor', opt['originCertsToHonor'])
          print('customValidCnValues', opt['customValidCnValues'])
          if opt['originCertsToHonor'] == 'CUSTOM_CERTIFICATES':
            print(opt['customCertificates'])
            self.pin_certs=opt['customCertificates']
          else:
            self.pin_certs=opt['customCertificates'] = None
        elif opt['verificationMode'] == 'PLATFORM_SETTINGS':
          self.fossltype = 'PLATFORM_SETTINGS'
          self.fosslcn = '-'
          self.pin_certs=None
      else:
        self.fossltype='-'
        self.fosslcn='-'
        self.pin_certs=None
    else:
      raise
    if self.originhost=='':
      self.originhost='-'
    return

  def printline(self):
    'contract, group, property name, version, rule, origin type, origin host, is_secure, FOSSLtype, CNmatch value, pincert CN,  pincert expiredate'
    line=['>>>']
    line.append( self.cid )
    line.append( self.gid )
    line.append( self.pname )
    line.append( str(self.ver) )
    line.append( self.rulename )
    line.append( self.origintype )
    line.append( self.originhost )
    line.append( str(self.is_secure) )

    line.append( self.fossltype )
    line.append( ' or '.join(self.fosslcn) )
    
    

    if self.pin_certs is None:
      tmpline=list(line)
      tmpline.append('-')
      tmpline.append('-')
      print(', '.join(tmpline))
    else:
      for c in self.pin_certs:
        tmpline=list(line)
        pin_cn=str( c['subjectCN'] )
        d=datetime.datetime.fromtimestamp(c['notAfter']/1e3)
        pin_expire='{}/{}/{}'.format(d.year, d.month, d.day)
        tmpline.append(pin_cn)
        tmpline.append(pin_expire)
        print(', '.join(tmpline))


  def walk(self, rootdir):
    for root, subdir, files in os.walk(rootdir):
      for f in files:
        filepath=os.path.join(root, f)
        ruletree=''
        if not filepath.endswith('.json'):
          continue
        print(filepath)
        with open(filepath) as fin:
          ruletree=json.load(fin)
        try:
          self.parseRuleTree(ruletree)
        except Exception as err:
          print('ERR: ',err)

def usage():
  print('usage: python3 papi_parse.py dirname')

if __name__ == '__main__':
  #p=Papils()
  #with open(sys.argv[1]) as f:
  #  ruletree=json.load(f)
  #  p.parseRuleTree(ruletree)

  if len(sys.argv) != 2:
    print('error:')
    usage()
    exit()

  
  p=Papils()
  p.walk(sys.argv[1])



