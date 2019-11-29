import boto3
import os
import re


class Region():

    def __init__(self, session):
        self._session = session

    def get_regions(self):
        ec2 = self._session.client('ec2')
        regions = ec2.describe_regions()
        return [name.get('RegionName') for name in regions.get('Regions')]