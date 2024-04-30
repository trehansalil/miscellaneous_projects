import boto3
import os
from PIL import Image
from dotenv import load_dotenv

def lambda_handler(event, context):
    """Process images in the S3 bucket."""
    try:
        # Load environment variables
        load_dotenv()
        resize_dimensions: tuple[int, int] = tuple(
            map(int, os.environ["RESIZE_DIMENSIONS"].split("x"))
        )        

        s3_client = get_s3_client()
        resize_dimensions = get_resize_dimensions()
        upload_path = get_upload_path()
        bucket_name, prefix = get_bucket_and_prefix()

        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        print('Files in the bucket:')
        for obj in response['Contents']:
            try:
                s3_client.download_file(bucket_name, obj["Key"], obj["Key"].split("/")[-1])

                resized_path = os.path.join("resized", obj["Key"].split("/")[-1])
                upload_path_s3 = upload_path + obj["Key"].split("/")[-1]

                resize_image(
                    obj["Key"].split("/")[-1],
                    resized_path,
                    resize_dimensions=resize_dimensions
                )

                s3_client.upload_file(
                    Bucket=bucket_name,
                    Key=obj["Key"].split("/")[-1],
                    Filename=resized_path
                )

                print(f"Resized and uploaded {obj['Key']}")

            except Exception as e:
                print(f"Error processing {obj['Key']}: {e}")
            break
    except Exception as e:
        print(f"Error processing images: {e}")
        raise e

def get_s3_client():
    """Create and return an S3 client."""
    aws_key = os.environ['AWS_KEY']
    aws_secret = os.environ['AWS_SECRET']
    region = 'us-east-1'

    return boto3.client(
        "s3",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=region,
    )

def get_resize_dimensions():
    """Return the resize dimensions as a tuple."""
    return tuple(map(int, os.environ["RESIZE_DIMENSIONS"].split("x")))

def get_upload_path():
    """Return the upload path."""
    s3_bucket_folder_path = "s3://lungxraydataset/data/train/NORMAL"
    return "/".join(s3_bucket_folder_path.split("/")[:-1]) + "/resized/"

def get_bucket_and_prefix():
    """Return the bucket name and prefix."""
    s3_bucket_folder_path = "s3://lungxraydataset/data/train/NORMAL"
    bucket_name = s3_bucket_folder_path.split('/')[2]
    prefix = '/'.join(s3_bucket_folder_path.split('/')[3:])
    return bucket_name, prefix

def resize_image(image_path, resized_path, resize_dimensions):
    """Resize the image at image_path and save it to resized_path."""

    with Image.open(image_path) as img:
        resized_img = img.resize(resize_dimensions)
        resized_img.save(resized_path)