import os
import boto3
from datetime import datetime
from src.rds import RDS
from src.aws_lambda import Lambda


AWS_PROFILE = os.getenv('AWS_PROFILE')
session = boto3.Session(profile_name=AWS_PROFILE)


if __name__ == '__main__':
    start_time = datetime.now()
    print('----------------RDS----------------')
    RDS(session).main()
    print('----------------LAMBDA----------------')
    Lambda(session).main()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    