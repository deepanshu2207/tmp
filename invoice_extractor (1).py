import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging
from llm_inference import LLMInference

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LineItem:
    """Data class for invoice line items"""
    id: str
    description: str
    shipper_address: str

@dataclass
class InvoiceData:
    """Data class for extracted invoice data"""
    invoice_number: str
    line_items: List[LineItem]

class InvoiceExtractor:
    """Main class for extracting invoice data using LLM"""
    
    def __init__(self, sagemaker_endpoint_name: str):
        """
        Initialize the invoice extractor
        
        Args:
            sagemaker_endpoint_name: Name of the SageMaker async endpoint
        """
        self.llm_inference = LLMInference(sagemaker_endpoint_name)
        
    def create_extraction_prompt(self, invoice_text: str) -> str:
        """
        Create a structured prompt for the LLM to extract invoice data
        
        Args:
            invoice_text: Raw text content of the invoice
            
        Returns:
            Formatted prompt for LLM
        """
        prompt = f"""Extract the following information from this invoice text and return it as valid JSON:

1. Invoice Number
2. Line Items (each with: line item ID, description, and shipper address)

Invoice Text:
{invoice_text}

Return the data in this exact JSON format:
{{
    "invoice_number": "string",
    "line_items": [
        {{
            "id": "string",
            "description": "string", 
            "shipper_address": "string"
        }}
    ]
}}

Only return the JSON response, no additional text or explanation."""
        
        return prompt
    
    def parse_llm_response(self, response: str) -> Optional[Dict]:
        """
        Parse the LLM response and extract JSON data
        
        Args:
            response: Raw response from LLM
            
        Returns:
            Parsed JSON data or None if parsing fails
        """
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                logger.error("No JSON found in LLM response")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            return None
    
    def validate_extracted_data(self, data: Dict) -> bool:
        """
        Validate the structure of extracted data
        
        Args:
            data: Parsed JSON data from LLM
            
        Returns:
            True if data is valid, False otherwise
        """
        if not isinstance(data, dict):
            return False
            
        # Check required fields
        if 'invoice_number' not in data or 'line_items' not in data:
            return False
            
        # Validate invoice number
        if not isinstance(data['invoice_number'], str) or not data['invoice_number'].strip():
            return False
            
        # Validate line items
        if not isinstance(data['line_items'], list):
            return False
            
        for item in data['line_items']:
            if not isinstance(item, dict):
                return False
            required_fields = ['id', 'description', 'shipper_address']
            for field in required_fields:
                if field not in item or not isinstance(item[field], str):
                    return False
                    
        return True
    
    def extract_invoice_data(self, invoice_text: str) -> Optional[InvoiceData]:
        """
        Extract invoice data from text using LLM
        
        Args:
            invoice_text: Raw text content of the invoice
            
        Returns:
            InvoiceData object with extracted information or None if extraction fails
        """
        try:
            # Create prompt for LLM
            prompt = self.create_extraction_prompt(invoice_text)
            
            # Get response from LLM
            logger.info("Sending request to LLM for invoice extraction")
            llm_response = self.llm_inference.infer(prompt)
            
            if not llm_response:
                logger.error("No response from LLM")
                return None
            
            # Parse LLM response
            parsed_data = self.parse_llm_response(llm_response)
            if not parsed_data:
                logger.error("Failed to parse LLM response")
                return None
            
            # Validate extracted data
            if not self.validate_extracted_data(parsed_data):
                logger.error("Extracted data validation failed")
                return None
            
            # Create InvoiceData object
            line_items = []
            for item_data in parsed_data['line_items']:
                line_item = LineItem(
                    id=item_data['id'],
                    description=item_data['description'],
                    shipper_address=item_data['shipper_address']
                )
                line_items.append(line_item)
            
            invoice_data = InvoiceData(
                invoice_number=parsed_data['invoice_number'],
                line_items=line_items
            )
            
            logger.info(f"Successfully extracted data for invoice: {invoice_data.invoice_number}")
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error during invoice extraction: {e}")
            return None
    
    def process_invoice_file(self, file_path: str) -> Optional[InvoiceData]:
        """
        Process an invoice file and extract data
        
        Args:
            file_path: Path to the invoice file (text or PDF)
            
        Returns:
            InvoiceData object with extracted information
        """
        try:
            # For text files
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    invoice_text = f.read()
            else:
                # For PDF files, you would need to add PDF text extraction
                # using libraries like PyPDF2, pdfplumber, etc.
                raise NotImplementedError("PDF processing not implemented. Please convert to text first.")
            
            return self.extract_invoice_data(invoice_text)
            
        except Exception as e:
            logger.error(f"Error processing invoice file {file_path}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize the extractor
    extractor = InvoiceExtractor("your-sagemaker-endpoint-name")
    
    # Example invoice text
    sample_invoice = """
    INVOICE #INV-2024-001
    
    Line Item 1:
    ID: LI-001
    Description: Widget A - Blue Color
    Shipper: ABC Corp, 123 Main St, New York, NY 10001
    
    Line Item 2:
    ID: LI-002
    Description: Widget B - Red Color
    Shipper: XYZ Shipping, 456 Oak Ave, Los Angeles, CA 90001
    """
    
    # Extract data
    result = extractor.extract_invoice_data(sample_invoice)
    
    if result:
        print(f"Invoice Number: {result.invoice_number}")
        print("Line Items:")
        for item in result.line_items:
            print(f"  ID: {item.id}")
            print(f"  Description: {item.description}")
            print(f"  Shipper: {item.shipper_address}")
            print()
    else:
        print("Failed to extract invoice data")
