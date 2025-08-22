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

    def download(self, image_key: str, path): 
        """Download the image specified by the image_key and store it in the mesh folder"""
        
        self.s3.download_file('sigma-boy-bucket', image_key, path)
        return path
# s3Helper = s3Helper()

# s3Helper.upload("SleepyJoe.png", "test-llm", "Help me")