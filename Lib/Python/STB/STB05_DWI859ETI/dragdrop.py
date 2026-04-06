import boto3
import sys
import urllib.request


# file_key = 'EvQUAL/ICONS/RDK_Remote.png'  # The key of the file in the S3 bucket
# local_file_path = 'D:/SourceCodes/hi.png' # Local file path where you want to save the downloaded file

file_key = sys.argv[1]  # The key of the file in the S3 bucket
local_file_path = sys.argv[2]  # Local file path where you want to save the downloaded file

# Initialize a session using Amazon S3
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
s3 = session.client('s3')


# Download the file from S3 to a local location

def copy_paste(path1, path2):
    with open(path1, 'r') as source_file:
        source_contents = source_file.read()
    with open(path2, 'a') as destination_file:
        destination_file.write(source_contents)


try:
    print(bucket_name)
    print(file_key)
    print(local_file_path)
    # s3.download_file(bucket_name, file_key, local_file_path)
    url = "https://elasticbeanstalk-ap-south-1-509040541908.s3.ap-south-1.amazonaws.com/"+file_key
    urllib.request.urlretrieve(url, local_file_path)
    print(f"Local path:{local_file_path}")
    print(f"File downloaded to {local_file_path}")
    example_path = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/TestSuite/STB"
    if example_path in local_file_path:
        dest_path = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/TestSuite/STB/STB05_DWI859ETI/STB05_DWI859ETI.robot"
        copy_paste(local_file_path, dest_path)
except Exception as e:
    print(f"An error occurred: {str(e)}")
