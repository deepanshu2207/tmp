from extractthinker import Extractor
from docling import Document
from sagemaker_llm import SageMakerLLM

# Initialize your LLM connector
llm = SageMakerLLM(endpoint_name='your-sagemaker-endpoint')

# Define your extraction schema
schema = {
    "effective_date": "The date the contract becomes effective.",
    "signatories": "The names and titles of the people who signed the contract.",
    "confidential_info": "Any clauses or sections about confidentiality."
}

# Load your contract document
doc = Document.from_file('path/to/contract.pdf')

# Initialize ExtractThinker with your LLM
extractor = Extractor(llm=llm, schema=schema)

# Run extraction
results = extractor.extract(doc)
print(results)
