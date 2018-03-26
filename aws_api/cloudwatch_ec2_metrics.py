"""
CloudWatch EC2 metrics getter for Nagios

Usage: cloudwatch_ec2_metrics.py $metric_name $instance_id $unit_type

Note: $unit_type parameter is not required (using raw data without any convertation)

Usage example:

cloudwatch_ec2_metrics.py CPUUtilization i-1q2w3e4r

"""
import sys
import boto3
from datetime import datetime, timedelta
from operator import itemgetter

profile_name = 'aws-profile-name'
region_name = 'region-name'


def create_boto_client(aws_profile_name, aws_region_name, resource_name):
    aws_session = boto3.Session(profile_name=aws_profile_name)
    client = aws_session.client(resource_name, region_name=aws_region_name)
    return client


def main(ec2_client):
    if len(sys.argv) < 3:
        sys.exit("Usage: %s metric_name instance_id unit_type\nAvailable unit_type (for value converting): kb, mb, gb" %
                 __file__.split('/')[-1:][0])

    metric_name = sys.argv[1]
    instance_id = sys.argv[2]
    k = 1 if len(sys.argv) < 4 else sys.argv[3]

    unit_map = {
        'kb': 1024,
        'mb': 1048576,
        'gb': 1073741824,
        1: 1
    }
    r = ec2_client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            }
        ],
        StartTime=datetime.now() - timedelta(hours=8),
        EndTime=datetime.now(),
        Statistics=[
            'SampleCount', 'Average'
        ],
        Period=300
    )

    data_raw = r.get('Datapoints')
    if data_raw:
        data = sorted(data_raw, key=itemgetter('Timestamp'))
        print("%(metric)s=%(value)s|%(metric)s=%(value)s" % {
            'metric': metric_name,
            'value': round(data[-1:][0]['Average'] / unit_map[k], 3)
        })
    else:
        sys.exit(2)


if __name__ == '__main__':
    ec2_client = create_boto_client(profile_name, region_name, 'cloudwatch')
    main(ec2_client)
