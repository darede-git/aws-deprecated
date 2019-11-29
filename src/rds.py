import boto3
import os
import re
from src.region import Region


class RDS(object):

    def __init__(self, session):
        self._session = session

    def get_rds(self):
        ret = []
        for regiao in Region(self._session).get_regions():
            client = self._session.client('rds', region_name=regiao)
            response = client.describe_db_instances()
            if len(response.get('DBInstances')) > 0:
                for func in response.get('DBInstances'):
                    ret.append(self.create_rds(func, regiao))
        return ret

    def create_rds(self, lin, region):
        return {'Name': lin.get('DBInstanceIdentifier'), 
                'Engine':  lin.get('Engine'), 'Endpoint': lin.get('Endpoint'),
                'CA': lin.get('CACertificateIdentifier'),
                'Arn': lin.get('DBInstanceArn'), 'Region': region}

    def check_version(self, rds):
        version = rds.get('CA')
        return True if '2015' in version else False

    def check_rds(self):
        ret = []
        rds_list = self.get_rds()
        if len(rds_list) > 0:
            for rds in rds_list:
                if self.check_version(rds):
                    ret.append(rds)
        return ret

    def main(self):
        warns = self.check_rds()
        for rds in warns:
            print('RDS "{}" running on region "{}" is using "{}".'.format(
                    rds.get('Name'), rds.get('Region'), rds.get('CA')
                ) + ' Please, consider update CA configuration!')
