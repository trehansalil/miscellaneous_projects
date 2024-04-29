import boto3
import os
import botocore
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

s3_bucket_folder_name = "s3://lungxraydataset/data/train/NORMAL"
aws_key = os.environ['AWS_KEY']
aws_secret = os.environ['AWS_SECRET']
resize_dimensions = os.environ['RESIZE_DIMENSIONS']
region = 'us-east-1'

s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    region_name=region,    
)

resize_dimensions: tuple[int, int] = tuple(
    map(int, os.environ["RESIZE_DIMENSIONS"].split("x"))
)

upload_path = "/".join(s3_bucket_folder_name.split("/")[:-1])

upload_path += "/resized/"

bucket_name = s3_bucket_folder_name.split('/')[2]
prefix = '/'.join(s3_bucket_folder_name.split('/')[3:])

print(bucket_name, prefix)

response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

def resize_image(image_path, resized_path):
    # Reads, resizes and saves the image
    with Image.open(image_path) as img:
        resized_img = img.resize(resize_dimensions)
        resized_img.save(resized_path)


print('Files in the bucket:')
for obj in response['Contents']:
    s3_client.download_file(bucket_name, obj["Key"], obj["Key"].split("/")[-1])
    
    
    resized_path = os.path.join("resized", obj["Key"].split("/")[-1])
    upload_path_s3 = upload_path+obj["Key"].split("/")[-1]
    
    resize_image(
        obj["Key"].split("/")[-1], 
        resized_path
    )
    
    s3_client.upload_file(
        Bucket=bucket_name, 
        Key=obj["Key"].split("/")[-1], 
        Filename=resized_path
    )
    
    break
