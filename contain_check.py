import sys

def usage():
  print('usage:')
  print('python3 contain_check.py bigfile listfile')

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('arg error')
    usage()
    exit()

  bigfile = sys.argv[1]
  listfile = sys.argv[2]

  with open(bigfile) as fbig:
    bigstr=fbig.read()
    with open(listfile) as flist:
      cnt=0
      for h in flist:
        host = h.strip()
        if host == '':
          continue
        cnt+=1
        print(host)
        if bigstr.find(host) == -1:
          print('  {} is not contained in {}'.format(host, bigfile))
        else:
          print(' => OK')
      else:
        print('Done!')
        print('{} hosts was checked.'.format(cnt))


