import boto3
from dotenv import load_dotenv
import os
from botocore.client import Config
from botocore.exceptions import ClientError
import logging  

load_dotenv(override=True)

class s3Helper: 
    
    BUCKET_NAME: str = "sigma-boi-bucket"  # static

    s3: object = boto3.client('s3', 
        region_name="ap-southeast-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        config=Config(signature_version='v4')
    ) # s3 client

    def upload(self, image_path: str, key: str, prompt: str = None, advice: str = None) -> str:
        """ Upload image of user to s3 bucket so that ai model and pull, return string url""" 
        if(image_path == None): 
            return Exception('error, no image path')
        with open(image_path, "rb") as f:
            self.s3.put_object(
                Bucket=self.BUCKET_NAME,
                Key=key,
                Body=f,
                ContentType="image/png",   
                Metadata={"prompt": prompt or "", "advice": advice or ""}
            )
        url = self.s3.generate_presigned_url(
            'get_object', 
            Params={'Bucket':self.BUCKET_NAME, 'Key':key},
            ExpiresIn=18000
        )
        print(url)
        
        return url

    def upload_file_content(self, file_content: bytes, key: str, filename: str, prompt: str = None) -> str:
        """ Upload file content directly to s3 bucket, return presigned url"""
        if file_content is None:
            raise Exception('error, no file content')
        
        print(f"S3Helper - Uploading with key: {key}, filename: {filename}")
        
        # Determine content type from filename
        content_type = "image/png"
        if filename.lower().endswith(('.jpg', '.jpeg')):
            content_type = "image/jpeg"
        elif filename.lower().endswith('.gif'):
            content_type = "image/gif"
        elif filename.lower().endswith('.webp'):
            content_type = "image/webp"
        
        self.s3.put_object(
            Bucket=self.BUCKET_NAME,
            Key=key,
            Body=file_content,
            ContentType=content_type,   
            Metadata={"prompt": prompt or "", "filename": filename}
        )
        
        url = self.s3.generate_presigned_url(
            'get_object', 
            Params={'Bucket':self.BUCKET_NAME, 'Key':key},
            ExpiresIn=18000
        )
        print(f"File uploaded to S3: {url}")
        
        return url

    def download(self, image_key: str, path): 
        """Download the image specified by the image_key and store it in the mesh folder"""
        
        self.s3.download_file('sigma-boi-bucket', image_key, path)
        return path


    def upload_txt(self, filename: str, unique_key:str):
        try:
            # Upload the file
            s3_key=f"guidance-{unique_key}.txt"
            self.s3.upload_file(Filename=filename, Bucket=self.BUCKET_NAME, Key=s3_key)
            print(f"'{s3_key}' uploaded successfully to '{self.BUCKET_NAME}/{s3_key}'")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def generate_presigned_url(self, unique_key:str):
        try:
            response = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.BUCKET_NAME, 'Key': unique_key},
                ExpiresIn=180000,
            )
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response
        
