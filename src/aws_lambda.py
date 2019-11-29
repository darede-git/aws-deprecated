import boto3
import os
import re
from src.region import Region


class Lambda():

    def __init__(self, session):
        self._session = session

    def get_lambdas(self):
        ret = []
        for regiao in Region(self._session).get_regions():
            client = self._session.client('lambda', region_name=regiao)
            response = client.list_functions()
            if len(response.get('Functions')) > 0:
                for func in response.get('Functions'):
                    ret.append(self.create_lambda(func, regiao))
        return ret

    def create_lambda(self, lin, region):
        return {'Name': lin.get('FunctionName'), 'Runtime':  lin.get('Runtime'), 
                'Arn': lin.get('FunctionArn'), 'Region':region}

    def get_version(self, text):
        ret = re.findall(r'\d', text)
        return ret

    def check_version(self, func):
        ver = self.get_version(func.get('Runtime'))
        if 'python' in func.get('Runtime'):
            return False if int(ver[0]) < 3 else True
        elif 'node' in func.get('Runtime'):
            return False if int(ver[0]) < 10 else True
        else:
            return True

    def get_warnings(self):
        ret = []
        lambdas = self.get_lambdas()
        if len(lambdas) > 0:
            for func in lambdas:
                if not self.check_version(func):
                    ret.append(func)
        return ret

    def main(self):
        warns = self.get_warnings()
        for func in warns:
            print('Function "{}" running on region "{}" is using "{}".'.format(
                    func.get('Name'), func.get('Region'), func.get('Runtime')
                ) + ' Please, consider update it to a newer runtime!')


#if __name__ == '__main__':
#    start_time = datetime.now()
#    main()
#    end_time = datetime.now()
#    print('Duration: {}'.format(end_time - start_time))