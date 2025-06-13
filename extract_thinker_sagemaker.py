import json
import boto3
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from extract_thinker import Extractor
from extract_thinker.document_loader.document_loader_docling import DocumentLoaderDocling
from extract_thinker.llm.llm_base import LLMBase
from extract_thinker.models.classification import Classification
from extract_thinker.models.contract import Contract


class SageMakerLlama32LLM(LLMBase):
    """Custom LLM implementation for SageMaker Llama 3.2 endpoint"""
    
    def __init__(self, endpoint_name: str, region_name: str = "us-east-1"):
        self.endpoint_name = endpoint_name
        self.region_name = region_name
        self.runtime = boto3.client('sagemaker-runtime', region_name=region_name)
        
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate response from SageMaker Llama 3.2 endpoint
        """
        # Convert messages to Llama 3.2 format
        prompt = self._format_messages_for_llama(messages)
        
        # Prepare payload for SageMaker endpoint
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": kwargs.get("max_tokens", 2048),
                "temperature": kwargs.get("temperature", 0.1),
                "top_p": kwargs.get("top_p", 0.9),
                "do_sample": True,
                "stop": ["<|eot_id|>"]
            }
        }
        
        try:
            # Invoke SageMaker endpoint
            response = self.runtime.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            # Parse response
            result = json.loads(response['Body'].read().decode())
            
            # Extract generated text
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
            else:
                generated_text = result.get('generated_text', '')
            
            # Clean up the response (remove the input prompt)
            if prompt in generated_text:
                generated_text = generated_text.replace(prompt, '').strip()
                
            return generated_text
            
        except Exception as e:
            print(f"Error calling SageMaker endpoint: {e}")
            raise
    
    def _format_messages_for_llama(self, messages: List[Dict[str, str]]) -> str:
        """
        Format messages for Llama 3.2 chat template
        """
        formatted_prompt = "<|begin_of_text|>"
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                formatted_prompt += f"<|start_header_id|>system<|end_header_id|>\n\n{content}<|eot_id|>"
            elif role == "user":
                formatted_prompt += f"<|start_header_id|>user<|end_header_id|>\n\n{content}<|eot_id|>"
            elif role == "assistant":
                formatted_prompt += f"<|start_header_id|>assistant<|end_header_id|>\n\n{content}<|eot_id|>"
        
        # Add assistant header for response
        formatted_prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"
        
        return formatted_prompt


@dataclass
class InvoiceData:
    """Example data model for invoice extraction"""
    invoice_number: str
    date: str
    vendor_name: str
    total_amount: float
    line_items: List[Dict[str, Any]]
    tax_amount: Optional[float] = None
    due_date: Optional[str] = None


@dataclass
class PersonalInfo:
    """Example data model for personal information extraction"""
    name: str
    email: str
    phone: str
    address: str
    date_of_birth: Optional[str] = None


class DocumentExtractor:
    """Main class for document extraction using ExtractThinker"""
    
    def __init__(self, sagemaker_endpoint_name: str, region_name: str = "us-east-1"):
        # Initialize the custom LLM
        self.llm = SageMakerLlama32LLM(
            endpoint_name=sagemaker_endpoint_name,
            region_name=region_name
        )
        
        # Initialize document loader with docling
        self.document_loader = DocumentLoaderDocling()
        
        # Initialize extractor
        self.extractor = Extractor(
            document_loader=self.document_loader,
            llm=self.llm
        )
    
    def extract_invoice_data(self, file_path: str) -> InvoiceData:
        """
        Extract structured invoice data from document
        """
        try:
            result = self.extractor.extract(file_path, InvoiceData)
            return result
        except Exception as e:
            print(f"Error extracting invoice data: {e}")
            raise
    
    def extract_personal_info(self, file_path: str) -> PersonalInfo:
        """
        Extract personal information from document
        """
        try:
            result = self.extractor.extract(file_path, PersonalInfo)
            return result
        except Exception as e:
            print(f"Error extracting personal info: {e}")
            raise
    
    def extract_contract_data(self, file_path: str) -> Contract:
        """
        Extract contract information using built-in Contract model
        """
        try:
            result = self.extractor.extract(file_path, Contract)
            return result
        except Exception as e:
            print(f"Error extracting contract data: {e}")
            raise
    
    def classify_document(self, file_path: str, classifications: List[str]) -> Classification:
        """
        Classify document into predefined categories
        """
        try:
            result = self.extractor.classify(file_path, classifications)
            return result
        except Exception as e:
            print(f"Error classifying document: {e}")
            raise


def main():
    """
    Example usage of the DocumentExtractor
    """
    # Configuration
    SAGEMAKER_ENDPOINT_NAME = "your-llama32-endpoint-name"
    REGION_NAME = "us-east-1"
    
    # Initialize extractor
    extractor = DocumentExtractor(
        sagemaker_endpoint_name=SAGEMAKER_ENDPOINT_NAME,
        region_name=REGION_NAME
    )
    
    # Example 1: Extract invoice data
    try:
        invoice_path = "path/to/your/invoice.pdf"
        invoice_data = extractor.extract_invoice_data(invoice_path)
        print("Invoice Data Extracted:")
        print(f"Invoice Number: {invoice_data.invoice_number}")
        print(f"Vendor: {invoice_data.vendor_name}")
        print(f"Total: ${invoice_data.total_amount}")
        print(f"Date: {invoice_data.date}")
        print("---")
    except Exception as e:
        print(f"Invoice extraction failed: {e}")
    
    # Example 2: Extract personal information
    try:
        personal_doc_path = "path/to/personal_document.pdf"
        personal_info = extractor.extract_personal_info(personal_doc_path)
        print("Personal Information Extracted:")
        print(f"Name: {personal_info.name}")
        print(f"Email: {personal_info.email}")
        print(f"Phone: {personal_info.phone}")
        print("---")
    except Exception as e:
        print(f"Personal info extraction failed: {e}")
    
    # Example 3: Document classification
    try:
        doc_path = "path/to/document.pdf"
        classifications = ["invoice", "contract", "resume", "legal_document", "other"]
        classification_result = extractor.classify_document(doc_path, classifications)
        print("Document Classification:")
        print(f"Document Type: {classification_result.classification}")
        print(f"Confidence: {classification_result.confidence}")
        print("---")
    except Exception as e:
        print(f"Classification failed: {e}")
    
    # Example 4: Contract extraction
    try:
        contract_path = "path/to/contract.pdf"
        contract_data = extractor.extract_contract_data(contract_path)
        print("Contract Data Extracted:")
        print(f"Contract Type: {contract_data.contract_type}")
        print(f"Parties: {contract_data.parties}")
        print(f"Start Date: {contract_data.start_date}")
        print(f"End Date: {contract_data.end_date}")
    except Exception as e:
        print(f"Contract extraction failed: {e}")


# Advanced usage example with custom extraction
def advanced_extraction_example():
    """
    Advanced example showing custom data models and extraction
    """
    
    @dataclass
    class MedicalReport:
        patient_name: str
        patient_id: str
        diagnosis: List[str]
        medications: List[Dict[str, str]]
        doctor_name: str
        date: str
        recommendations: List[str]
    
    # Initialize extractor
    extractor = DocumentExtractor(
        sagemaker_endpoint_name="your-llama32-endpoint-name",
        region_name="us-east-1"
    )
    
    try:
        medical_report_path = "path/to/medical_report.pdf"
        medical_data = extractor.extractor.extract(medical_report_path, MedicalReport)
        
        print("Medical Report Extracted:")
        print(f"Patient: {medical_data.patient_name}")
        print(f"Diagnosis: {', '.join(medical_data.diagnosis)}")
        print(f"Doctor: {medical_data.doctor_name}")
        print(f"Date: {medical_data.date}")
        
    except Exception as e:
        print(f"Medical report extraction failed: {e}")


if __name__ == "__main__":
    # Run basic examples
    main()
    
    # Run advanced example
    print("\n" + "="*50)
    print("ADVANCED EXTRACTION EXAMPLE")
    print("="*50)
    advanced_extraction_example()
