import json
import boto3
from PIL import Image
import io

s3_client = boto3.client('s3')
dest_bucket_name = 'PLACE_DESTINATION_BUCKET_NAME_HERE'

def lambda_handler(event, context):
    try:
        # Retrieving information about the uploaded image
        s3_event = event['Records'][0]['s3']
        bucket_name = s3_event['bucket']['name']
        object_key = s3_event['object']['key']
        
        # Downloading the image from the S3 bucket
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        object_content = response['Body'].read()

        # Opening the image using Pillow
        image = Image.open(io.BytesIO(object_content))
        
        # Scaling the image by half
        new_size = (int(image.width / 2), int(image.height / 2))
        resized_image = image.resize(new_size)
        
        # Preparing the scaled image for saving
        buffer = io.BytesIO()
        resized_image.save(buffer, format=image.format)
        buffer.seek(0)
        
        # Saving the scaled image in the destination bucket
        s3_client.put_object(Body=buffer, Bucket=dest_bucket_name, Key=f'resized/{object_key}')

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully scaled image')
        }
        
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Error scaling image')
        }
