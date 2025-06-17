import json
import boto3
from litellm.llms.custom import CustomLLM
from typing import Optional

class SageMakerLLM(CustomLLM):
    def _init_(self, endpoint_name: str, region: str, **kwargs):
        self.endpoint_name = endpoint_name
        self.region = region
        self.client = boto3.client("sagemaker-runtime", region_name=region)

    def completion(self, model: str, messages: list, **kwargs) -> dict:
        prompt = messages[-1]["content"]

        payload = {
            "inputs": prompt,
            "parameters": {"temperature": kwargs.get("temperature", 0.7)}
        }

        response = self.client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            ContentType="application/json",
            Body=json.dumps(payload)
        )

        result = json.loads(response["Body"].read())
        return {"choices": [{"message": {"content": result[0]["generated_text"]}}]}

from litellm import completion, register_llm_provider

register_llm_provider(name="sagemaker", llm_provider_class=SageMakerLLM)

Now use it
response = completion(
    model="sagemaker",
    messages=[{"role": "user", "content": "Summarize this contract"}],
    endpoint_name="your-sagemaker-endpoint-name",
    region="us-east-1"
)

print(response["choices"][0]["message"]["content"])