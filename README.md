# severless-crud-porject

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

Search for S3 in the AWS console:

![Search S3](https://github.com/user-attachments/assets/95398f1d-6257-474d-b49a-77cb97a1b1b9)

Create a S3 bucket for uploading images:

![create bucket search](https://github.com/user-attachments/assets/2036b96c-cc53-4041-87c0-df699d85ec0d)

Give the bucket a name, leave all other settings default and create the bucket:

![name origin bucket](https://github.com/user-attachments/assets/9ea47637-0ce6-45ea-b183-7c65e5765a6f)

![create origin bucket](https://github.com/user-attachments/assets/70c0b4a2-37fa-4148-8571-9957457b00f8)

Create a folder in the origin bucket and name it "images":

![origin create folder](https://github.com/user-attachments/assets/07417f85-09fb-44fd-935f-4d05a5211afb)

![origin folder created](https://github.com/user-attachments/assets/2e93c6df-5242-4c42-ae15-636dff402e23)

Repeat again to create a second bucket for the scaled image destination:

![name destination bucket](https://github.com/user-attachments/assets/f223fc1f-6ccc-45d4-b7d2-e88ed4942de2)

![create origin bucket](https://github.com/user-attachments/assets/401867b2-fc4c-46d5-9b9e-83203d89c652)

Create a folder in the destination bucket and name it "resized":

![destination create folder](https://github.com/user-attachments/assets/e5b819bd-47e2-4831-9bd5-eecc85e792ad)

![destination folder created](https://github.com/user-attachments/assets/04667814-438c-4458-aada-f51cd475ba10)


Search for AWS ECR (Elastic Container Registry):

![search ecr](https://github.com/user-attachments/assets/4e9ed15e-5a49-4ad4-8d8e-6a23b6aa6a95)

Create an AWS ECR, set the repository as public and give it a name:

![ECR create](https://github.com/user-attachments/assets/bfc82b4c-7cc0-4086-aeb9-3c6380fbfb9d)

![ECR config](https://github.com/user-attachments/assets/d5ac1bd7-8d44-43be-a69a-0830df2b0b8e)

![ECR created](https://github.com/user-attachments/assets/60482c75-a8a9-437d-a079-dd36b4c1aa68)

Write the Python code the application:

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
Create the Dockerfile to build your docker image:

```bash
# Docker image from Amazon ECR Public Gallery
FROM public.ecr.aws/lambda/python
# Install Pillow exstension
RUN pip install Pillow
# Copy application code
COPY app.py ./
# Execute lambda_handler
CMD ["app.lambda_handler"]
```




