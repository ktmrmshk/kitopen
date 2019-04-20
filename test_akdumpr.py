import unittest
import logging
from akdumpr import papireq

#logging.basicConfig(level=logging.DEBUG)


class Test_papireq(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_get(self):
        pr = papireq()
        ret = pr.get('/identity-management/v1/open-identities/l2p6n6flvfhdaqn5/account-switch-keys', [('search', 'media mg')])
        
        logging.warning(ret.status_code)
        logging.warning(pr.getjson(ret))

        self.assertTrue( ret.status_code == 200)

    def test_post(self):
        '''
        $ http --auth-type edgegrid -a default: ‘:/papi/v1/search/find-by-value?accountSwitchKey=1-BGIGR:1-8BYUX’  hostname=space.ktmrmshk.com
        '''

        pr = papireq()
        body={'hostname': 'space.ktmrmshk.com'}
        ret = pr.post('/papi/v1/search/find-by-value?accountSwitchKey=1-BGIGR:1-8BYUX', body)

        logging.warning(ret.status_code)
        logging.warning(ret.json())
        self.assertTrue( ret.status_code == 200)

if __name__ == '__main__':
    unittest.main()
