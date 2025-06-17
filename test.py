import json
from langchain_aws.llms.sagemaker_endpoint import LLMContentHandler

class MyContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
        input_payload = {
            "inputs": prompt,
            "parameters": model_kwargs
        }
        return json.dumps(input_payload).encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]

from langchain_aws.llms import SagemakerEndpoint

llm = SagemakerEndpoint(
    endpoint_name="your-endpoint-name",
    region_name="us-east-1",  # Replace with your AWS region
    credentials_profile_name="default",  # Replace with your AWS profile name
    content_handler=MyContentHandler(),
    model_kwargs={"temperature": 0.7}  # Adjust parameters as needed
)

from extract_thinker import Extractor, Field

sample_contract = """
This Agreement is made on the 5th day of June, 2023 between Alpha Corp, represented by John Doe, and Beta Inc., represented by Jane Smith. 
The agreement includes a 12-month term beginning July 1, 2023. Both parties agree to the terms outlined herein, including payment obligations and confidentiality clauses. 
Signed by: John Doe, CEO of Alpha Corp and Jane Smith, CFO of Beta Inc.
"""

schema = {
    "effective_date": Field(description="The date the contract is made or becomes effective"),
    "signatories": Field(description="Names and titles of individuals signing the contract"),
    "term_length": Field(description="Duration or length of the contract"),
    "key_terms": Field(description="Important terms or clauses mentioned in the contract"),
}

extractor = Extractor(llm=llm, schema=schema)
results = extractor.extract(sample_contract)
print(results)
