"""
Clear old Amazon LoadBalancer access logs from S3
"""
import boto3
from datetime import datetime, timezone

DELETE_FOR_LAST = 24  # max files age in hours
AWS_PROFILE_NAME = "aws-profile-name"
ACCOUNT_ID = "account-id"
REGION_NAME = "region-name"
S3_BUCKET_NAME = "bucket-with-alb-logs"
S3_PREFIX = "AWSLogs/%(AccountId)s/elasticloadbalancing/%(RegionName)s" % {'AccountId': ACCOUNT_ID, 'RegionName': REGION_NAME}


def s3_get_files_list(s3_client, bucket, prefix=None):
    all_files_keys = []
    # Create a paginator to pull 1000 objects at a time
    paginator = s3_client.get_paginator('list_objects')
    if prefix:
        pageresponse = paginator.paginate(Bucket=bucket, Prefix=prefix)
    else:
        pageresponse = paginator.paginate(Bucket=bucket)

    # PageResponse Holds 1000 objects at a time and will continue to repeat in chunks of 1000.
    for pageobject in pageresponse:
        if pageobject.get("Contents") is not None:
            for file in pageobject["Contents"]:
                all_files_keys.append(file)
    print('Total files inside of %s: %s' % (prefix, len(all_files_keys)))
    return all_files_keys


def s3_delete_file(s3_client, bucket, files_list):
    return s3_client.delete_objects(
                Bucket=bucket,
                Delete={
                    'Objects': files_list
                }
            )


def main():
    today = datetime.now(timezone.utc)
    aws_session = boto3.Session(profile_name=AWS_PROFILE_NAME, region_name=REGION_NAME)
    s3_client = aws_session.client('s3')
    log_files_list = s3_get_files_list(s3_client, S3_BUCKET_NAME, S3_PREFIX)

    to_delete = []
    for file in log_files_list:
        diff_in_h = (today - file['LastModified']).total_seconds()/3600
        if diff_in_h > DELETE_FOR_LAST:
            to_delete.append({'Key': file['Key']})

    if to_delete:
        print('Will be deleted %s files' % len(to_delete))
        delete_result = s3_delete_file(s3_client, S3_BUCKET_NAME, to_delete)
        print(delete_result)
    else:
        print('Nothing to delete')


if __name__ == '__main__':
    main()
