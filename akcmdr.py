from akdumpr import papireq
import sys

def usage():
  print('usage: akcmdr credential_file open_url')
  print('ex: akcmdr .edgerc "/papi/v1/contracts"')

if len(sys.argv) != 3:
  usage()
  exit()

pp = papireq(sys.argv[1])
print('credential file: {}'.format(sys.argv[1]))

r=pp.get(sys.argv[2])
pp.dump(r)

