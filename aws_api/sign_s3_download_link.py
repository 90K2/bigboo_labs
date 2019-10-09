import boto3

OBJECT_URL = "https://bucket-name.s3-us-west-2.amazonaws.com/full/path/to/file.dmp"

BUCKET = OBJECT_URL.split(".s3")[0].split("//")[1]
FILE_PATH = OBJECT_URL.split(".com/")[1]

profile_name = 'aws-api-user'  # set this value to your api username
region = "us-west-2"  # your bucket's region
link_ttl = 43200  # signed download link lifetime


def sign_url(bucket_name, file_full_path):
    """
    Sign direct download link for any s3 file
    :param bucket_name:
    :param file_full_path:
    :return: download link str
    """
    boto_session = boto3.Session(profile_name=profile_name)
    s3 = boto_session.client('s3', region_name=region)
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': file_full_path},
        ExpiresIn=link_ttl
    )

