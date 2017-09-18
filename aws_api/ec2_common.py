import time
import boto3
import sys

profile_name = 'aws-api-user'  # set this value to your api username
aws_session = boto3.Session(profile_name=profile_name)
ec2_client = aws_session.client('ec2')


def check_instance_status(ec2_client, instances_id: list):
    return ec2_client.describe_instance_status(InstanceIds=instances_id)


def start_instance(ec2_client, instances_id: list):
    print(ec2_client.start_instances(InstanceIds=instances_id))
    time.sleep(10)
    status = check_instance_status(ec2_client, instances_id)
    while any(list([instance['SystemStatus']['Status'] != 'ok' for instance in status['InstanceStatuses']])):
        status = check_instance_status(ec2_client, instances_id)
        print('Waiting for instances start', flush=True)
        time.sleep(10)
    return status


def stop_instance(ec2_client, instances_id: list):
    print(ec2_client.stop_instances(InstanceIds=instances_id))


def create_ami(ec2_client, ec2_instance_id, ami_name):
    return ec2_client.create_image(
        InstanceId=ec2_instance_id,
        Name=ami_name
    )['ImageId']


def check_ami_status(ec2_client, ami_id='', ami_name=''):
    """
    Get state of requested AMI (by id or name)
    :param ec2_client: client object
    :param ami_id: string with id
    :param ami_name: string with name
    :return: state of requested ami name/id
    """
    if ami_name:
        filter_name = 'name'
        filter_value = ami_name
    elif ami_id:
        filter_name = 'image-id'
        filter_value = ami_id
    else:
        sys.exit('AMI id or name required')
    ami_details = ec2_client.describe_images(
        Owners=['self'],
        Filters=[
            {
                'Name': filter_name,
                'Values': [filter_value]
            }
        ]
    )
    if ami_details['Images']:
        return ami_details['Images'][0]['State']
    else:
        sys.exit('Probably wrong AMI name/id provided')


def list_ami(ec2_client) -> list:
    """
    Return all EC2 AMIs
    :param client: ec2 client object
    :return: list of images info
    """
    return ec2_client.describe_images(Owners=['self'])['Images']


def delete_ami(ec2_client, ami_id_list):
    """
    Deleting requested AMI
    :param client: ec2 client object
    :param ami_id_list: list of ami ids
    :return:
    """
    for ami_id in ami_id_list:
        print("Deregistering %s" % ami_id)
        ec2_client.deregister_image(ImageId=ami_id)
