from akdumpr import papireq, papiapp
import sys, re

def usage():
  'listfile: cid, gid, pid, pname, ver'
  print('usage: akhost credential_file listfile')
  print('ex: akhost credfile listfile.txt')

if len(sys.argv) != 3:
  usage()
  exit()

#pp = papireq(sys.argv[1])
#print('credential file: {}'.format(sys.argv[1]))

#r=pp.get(sys.argv[2])
#pp.dump(r)

def test():
  pp=papiapp('1H3N4NC.cred')
  print(pp.get_cnamehost('ctr_3-1H3N4NC', 'grp_65684', 'prp_340792', 1))

if __name__ == '__main__':
  #test()
  pp=papiapp(sys.argv[1])
  with open(sys.argv[2]) as f:
    for line in f:
      params = line.strip()
      if params == '':
        continue
      params2 = re.findall('[^\s]+', params)
      #params2 = [ p.strip() for p in params]
      #print(params2)
      #print(pp.get_cnamehost(params2[0], params2[1], params2[2], params2[4]))
      r = pp.get_cnamehost(params2[0], params2[1], params2[2], params2[4])
      ret=[]
      for h in r:
        ret.append('{} -> {}'.format(h[0], h[1]))
      print(' / '.join(ret))





