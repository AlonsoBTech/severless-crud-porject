# Severless CRUD Project

## 📋 <a name="table">Table of Contents</a>

1. 🤖 [Introduction](#introduction)
2. ⚙️ [Prerequisites](#prerequisites)
3. 🔋 [What Is Being Created](#what-is-being-created)
4. 🤸 [Quick Guide](#quick-guide)

5. ## <a name="introduction">🤖 Introduction</a>

![image](https://github.com/user-attachments/assets/5b155759-393b-4d78-8f08-a2d101e093fe)



## <a name="prerequisites">⚙️ Prerequisites</a>

Make sure you have the following:

- AWS Account
- AWS IAM User
- Python installed
- IDE of choice to write Python app
- Docker installed

## <a name="what-is-being-created">🔋 What Is Being Created</a>

What we will be creating and using:

- Amazon S3 Bucket
- Lambda Function
- Elastic Container Registry
- Python App
- Docker Image

## <a name="quick-guide">🤸 Quick Guide</a>

Search for S3 in the AWS console.

![Search S3](https://github.com/user-attachments/assets/95398f1d-6257-474d-b49a-77cb97a1b1b9)

Create a S3 bucket for uploading images.

![create bucket search](https://github.com/user-attachments/assets/2036b96c-cc53-4041-87c0-df699d85ec0d)

Give the bucket a name, leave all other settings default and create the bucket.

![name origin bucket](https://github.com/user-attachments/assets/9ea47637-0ce6-45ea-b183-7c65e5765a6f)

![create origin bucket](https://github.com/user-attachments/assets/70c0b4a2-37fa-4148-8571-9957457b00f8)

Create a folder in the origin bucket and name it **images**.

![origin create folder](https://github.com/user-attachments/assets/07417f85-09fb-44fd-935f-4d05a5211afb)

![origin folder created](https://github.com/user-attachments/assets/2e93c6df-5242-4c42-ae15-636dff402e23)

Repeat the steps again to create a second bucket for the scaled image destination.

![name destination bucket](https://github.com/user-attachments/assets/f223fc1f-6ccc-45d4-b7d2-e88ed4942de2)

![create origin bucket](https://github.com/user-attachments/assets/401867b2-fc4c-46d5-9b9e-83203d89c652)

Create a folder in the destination bucket and name it **resized**.

![destination create folder](https://github.com/user-attachments/assets/e5b819bd-47e2-4831-9bd5-eecc85e792ad)

![destination folder created](https://github.com/user-attachments/assets/04667814-438c-4458-aada-f51cd475ba10)


Search for AWS Lambda.

![lambda search](https://github.com/user-attachments/assets/2cdf007b-71e3-402b-a694-f199d6cadd21)

Select **Author from scratch**, give the function a name, select **Python 3.12** as the Runtime, select **x86_64** as the 
Architecture and create the Lambda function.

![create lambda](https://github.com/user-attachments/assets/23daad29-ecee-483e-a442-ce20e3b71a09)

Now configure the image scaler origin S3 bucket to trigger the Lambda function. Open the origin S3 bucket.

![origin bucket](https://github.com/user-attachments/assets/d8439e59-57c4-432f-a08d-49f4c61e5d78)

Select properties.

![s3 origin properties](https://github.com/user-attachments/assets/826e708e-9f13-4316-8736-959c2a2d0160)

Scroll down to **Event notifications** and click **Create event notification**.

![origin event](https://github.com/user-attachments/assets/9228958e-5b68-4483-8fbd-da506ee71073)

Give the event a name, set the prefixes for the **images** folder created in the S3 origin bucket, set the suffix so that 
any **.jpg** image will trigger the event and choose **Put** as the event type.

![origin event general conf](https://github.com/user-attachments/assets/7a949018-b366-49ac-8dee-27d4a157df9b)

Select **Lambda function** as the destination, for the specify Lambda function select **Choose from your Lambda functions**
and select the Lambda function created earlier then save the changes.

![origin event destination conf](https://github.com/user-attachments/assets/86a1f5fd-c85f-4331-9a27-9bc36e41bf5a)

Navigate to the Lambda function and check the overview to see the S3 trigger added.

![lambda overview](https://github.com/user-attachments/assets/4d797ac0-c19c-411a-ba05-f511fd2e17c6)


Write the Python code for the lambda function:

```bash
import json
import boto3
from PIL import Image

 
s3_client = boto3.client('s3')
dest_bucket_name = 'aeb-image-scaler-destination'

def lambda_handler(event, context):

    try:
        # Extract relevant information
        s3_event = event['Records'][0]['s3']
        bucket_name = s3_event['bucket']['name']
        object_key = s3_event['object']['key']

        # Downloading the image from the S3 origin bucket
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

        # Saving the scaled image in the S3 destination bucket
        s3_client.put_object(Body=object_content, Bucket=dest_bucket_name, Key=f'resized/{object_key}' )

        return {
            'statusCode': 200,
            'body': json.dumps('succesfully scaled image')
        }

    except Exception as e:
        print(f'Error {e}')
        return {
            'statusCode': 200,
            'body': json.dumps('Error scaling image')
        }
```

