from akdumpr import papireq
import sys

def usage():
  print('usage: python3 akpost credential_file open_url bodyjson')
  print('''ex: python3 akcmdr .edgerc "/papi/v1/contracts" '{"name":"abc123"}' ''')

if len(sys.argv) != 4:
  usage()
  exit()

pp = papireq(sys.argv[1])
print('credential file: {}'.format(sys.argv[1]))

r=pp.post(sys.argv[2], sys.argv[3])
pp.dump(r)

