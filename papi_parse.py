import json

class Papils(object):
  def __init__(self):
    pass

  def parseRuleTree(self, ruletree):
    for k,v in ruletree['rules'].items():
      print(k)
    else:
      print()

    self.parseRule(ruletree['rules'], [ruletree['rules']['name']])

  def parseRule(self, rule, rulename):
    self.parseBehavior(rule['behaviors'], rulename)
    for crule in rule['children']:
      self.parseRule(crule, rulename+[crule['name']])

  def parseBehavior(self, behaviors, rulename):
    
    print('-------')
    print( '.'.join(rulename) )
    for b in behaviors:
      if b['name']=='origin':
        opt = b['options']
        print( '.'.join(rulename) )
        print( opt['originType'] )
        print( opt['hostname'] )
      
      print('>>{}'.format(b['name']))

      #if children
      #print(b['name'])
    else:
      print()

   


if __name__ == '__main__':
  p=Papils()
  with open('ruletree.json') as f:
    ruletree=json.load(f)
    p.parseRuleTree(ruletree)



