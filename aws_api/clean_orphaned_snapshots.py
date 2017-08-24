import boto3

# set your api username
profile_name = 'aws-cli-poweruser'


def clean_snapshot(client, snap_id):
    return 1 if client.delete_snapshot(SnapshotId=snap_id)['ResponseMetadata']['HTTPStatusCode'] == 200 else 0


def main():
    '''
    Detect orphaned snapshots from an EC2 account. Requires configured aws profile on machine
    http://docs.aws.amazon.com/cli/latest/reference/configure/
    '''
    aws_session = boto3.Session(profile_name=profile_name)
    ec2 = aws_session.client('ec2')
    alive_ami = {}
    for ami in ec2.describe_images(Owners=['self'])['Images']:
        id = ami['ImageId']
        if id not in alive_ami.keys():
            alive_ami[id] = []
        alive_ami[id].extend(list([snap['Ebs']['SnapshotId'] for snap in ami['BlockDeviceMappings']]))

    # list of attached to AMI snapshots
    alive_snaps = list([item for sublist in alive_ami.values() for item in sublist])

    snap_list = list([s['SnapshotId'] for s in ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']])
    orphaned_snaps = list(set(snap_list) - set(alive_snaps))
    print('Orphaned snapshots:' % orphaned_snaps)
    if orphaned_snaps:
        [clean_snapshot(ec2, snap_id) for snap_id in orphaned_snaps]

if __name__ == '__main__':
    main()
