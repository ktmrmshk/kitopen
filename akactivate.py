from akdumpr import papireq
import sys, json

class akactivate(object):
    def __init__(self, cred):
        self.pp = papireq(cred)

    def get_ids(self, propname):
        '''
        return (contract_id, grpup_id, prop_id)
        '''
        q_dict={'propertyName': propname }
        r=self.pp.post('/papi/v1/search/find-by-value', json.dumps(q_dict) )
        #self.pp.dump(r)
        if r.status_code != 200:
            raise Exception('staetus code: {}'.format(r.status))
        j=json.loads(r.content.decode('utf-8'))
        if len( j['versions']['items'] ) == 0:
            raise Exception('not found prop {}'.format(propname))
        assert propname == j['versions']['items'][0]['propertyName']
        contract_id = j['versions']['items'][0]['contractId']
        group_id = j['versions']['items'][0]['groupId']
        prop_id = j['versions']['items'][0]['propertyId']
        return (contract_id, group_id, prop_id)

    def request_path(self, propname):
        cid, gid, pid = self.get_ids(propname)
        return '/papi/v1/properties/prp_{}/activations?contractId=ctr_{}&groupId=grp_{}'.format(pid, cid, gid)

    def request_body(self, ver, nw, email, note=''):
        body=dict()
        body['propertyVersion'] = ver
        if nw == 'prod':
            body['network'] = 'PRODUCTION'
        elif nw == 'stg':
            body['network'] = 'STAGING'
        else:
            raise Exception('nw type {} is invalid: stg or prod'.format(nw))
        body['notifyEmails'] = [email]
        body['note']=note
        return body
    
    def activate(self, propname, nw, ver, email, note='activation by PAPI'):
        path=self.request_path(propname)
        body=self.request_body(ver, nw, email, note)
        body['complianceRecord'] = {'noncomplianceReason': 'NO_PRODUCTION_TRAFFIC'}
        r = self.pp.post(path, json.dumps(body))
        self.pp.dump(r)

        if r.status_code == 400:
            j=json.loads(r.content.decode('utf-8'))
            msg_ids=[]
            for w in j['warnings']:
                msg_ids.append(w['messageId'])
            print(msg_ids)

            body['acknowledgeWarnings'] = msg_ids
            r = self.pp.post(path, json.dumps(body))
            self.pp.dump(r)
        print('activation requested')


    
def test():
    aa = akactivate('jal.cred')
    ret = aa.activate('book-i.jal.co.jp', 'stg', 12, 'mkitamur@akamai.com')    
    print(ret)
    
    
    
def main():
    def usage():
        print('usage: python3 akactivate credential_file propertyname stg/prod ver')
        print('''ex: python3 akactivate .edgerc space.ktmrmshk.com stg 34''')

    if len(sys.argv) != 5:
        usage()
        exit()
    
    aa = akactivate(sys.argv[1])
    print('credential file: {}'.format(sys.argv[1]))
    #ret = aa.activate('book-i.jal.co.jp', 'stg', 12, 'mkitamur@akamai.com')    
    ret = aa.activate(sys.argv[2], sys.argv[3], int(sys.argv[4]), 'mkitamur@akamai.com')
    print(ret)

if __name__ == '__main__':
    #test()
    main()



