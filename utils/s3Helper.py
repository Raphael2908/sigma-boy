import boto3
from dotenv import load_dotenv
import os
from botocore.client import Config  

load_dotenv(override=True)

class s3Helper: 
    
    BUCKET_NAME: str = "sigma-boy-bucket"  # static

    s3: object = boto3.client('s3', 
        region_name="ap-southeast-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        config=Config(signature_version='v4')
    ) # s3 client

    def upload(self, image_path: str, key: str, prompt: str = None) -> str:
        """ Upload image of user to s3 bucket so that ai model and pull, return string url""" 
        if(image_path == None): 
            return Exception('error, no image path')
        with open(image_path, "rb") as f:
            self.s3.put_object(
                Bucket=self.BUCKET_NAME,
                Key=key,
                Body=f,
                ContentType="image/png",   
                Metadata={"prompt": prompt or ""}
            )
        url = self.s3.generate_presigned_url(
            'get_object', 
            Params={'Bucket':self.BUCKET_NAME, 'Key':key},
            ExpiresIn=3600
        )
        print(url)
        
        return url 