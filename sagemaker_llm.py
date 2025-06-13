import boto3
import json
import time

class SageMakerLLM:
    def __init__(self, endpoint_name, region_name='eu-west-2'):
        self.endpoint_name = endpoint_name
        self.client = boto3.client('sagemaker-runtime', region_name=region_name)


    def generate_async(self, prompt, s3_input_location, **kwargs):
        # Prepare the payload as your Llama 3.2 endpoint expects
        payload = {
            "inputs": prompt,
            "parameters": kwargs,
            "s3_input_location": s3_input_location
        }
        response = self.client.invoke_endpoint_async(
            EndpointName=self.endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        result = json.loads(response['Body'].read())
        # Adjust this depending on your endpoint's response format
        return result['generated_text']
