import json
import pandas as pd
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging
from pathlib import Path
from llm_inference import LLMInference

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FieldDefinition:
    """Data class for field definitions from Excel"""
    field_name: str
    field_type: str
    description: str
    required: bool = True
    validation_rules: Optional[str] = None
    example_value: Optional[str] = None

@dataclass
class ExtractedInvoiceData:
    """Dynamic data class for extracted invoice data"""
    fields: Dict[str, Any] = field(default_factory=dict)
    
    def get_field(self, field_name: str) -> Any:
        """Get a specific field value"""
        return self.fields.get(field_name)
    
    def set_field(self, field_name: str, value: Any) -> None:
        """Set a specific field value"""
        self.fields[field_name] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.fields.copy()

class FieldConfigLoader:
    """Class to load field definitions from Excel file"""
    
    def __init__(self, excel_file_path: str):
        """
        Initialize field config loader
        
        Args:
            excel_file_path: Path to Excel file containing field definitions
        """
        self.excel_file_path = Path(excel_file_path)
        self.field_definitions = []
        self.load_field_definitions()
    
    def load_field_definitions(self) -> None:
        """Load field definitions from Excel file"""
        try:
            # Read Excel file
            df = pd.read_excel(self.excel_file_path)
            
            # Expected columns in Excel file
            required_columns = ['field_name', 'field_type', 'description']
            optional_columns = ['required', 'validation_rules', 'example_value']
            
            # Validate required columns
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Required column '{col}' not found in Excel file")
            
            # Process each row
            for _, row in df.iterrows():
                # Skip empty rows
                if pd.isna(row['field_name']) or not str(row['field_name']).strip():
                    continue
                
                field_def = FieldDefinition(
                    field_name=str(row['field_name']).strip(),
                    field_type=str(row['field_type']).strip(),
                    description=str(row['description']).strip(),
                    required=bool(row.get('required', True)),
                    validation_rules=str(row['validation_rules']).strip() if pd.notna(row.get('validation_rules')) else None,
                    example_value=str(row['example_value']).strip() if pd.notna(row.get('example_value')) else None
                )
                
                self.field_definitions.append(field_def)
            
            logger.info(f"Loaded {len(self.field_definitions)} field definitions from Excel file")
            
        except Exception as e:
            logger.error(f"Error loading field definitions from Excel: {e}")
            raise
    
    def get_field_definitions(self) -> List[FieldDefinition]:
        """Get all field definitions"""
        return self.field_definitions.copy()
    
    def get_field_by_name(self, field_name: str) -> Optional[FieldDefinition]:
        """Get field definition by name"""
        for field_def in self.field_definitions:
            if field_def.field_name == field_name:
                return field_def
        return None
    
    def get_required_fields(self) -> List[FieldDefinition]:
        """Get only required fields"""
        return [f for f in self.field_definitions if f.required]
    
    def get_optional_fields(self) -> List[FieldDefinition]:
        """Get only optional fields"""
        return [f for f in self.field_definitions if not f.required]

class DynamicInvoiceExtractor:
    """Main class for extracting invoice data using dynamic field definitions"""
    
    def __init__(self, sagemaker_endpoint_name: str, field_config_path: str):
        """
        Initialize the invoice extractor
        
        Args:
            sagemaker_endpoint_name: Name of the SageMaker async endpoint
            field_config_path: Path to Excel file with field definitions
        """
        self.llm_inference = LLMInference(sagemaker_endpoint_name)
        self.field_config = FieldConfigLoader(field_config_path)
        self.field_definitions = self.field_config.get_field_definitions()
        
    def create_json_schema(self) -> Dict[str, Any]:
        """
        Create JSON schema from field definitions
        
        Returns:
            JSON schema for the expected output
        """
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for field_def in self.field_definitions:
            # Map field types to JSON schema types
            type_mapping = {
                "string": "string",
                "number": "number",
                "integer": "integer",
                "boolean": "boolean",
                "array": "array",
                "date": "string",
                "currency": "string"
            }
            
            json_type = type_mapping.get(field_def.field_type.lower(), "string")
            
            field_schema = {
                "type": json_type,
                "description": field_def.description
            }
            
            # Add example if available
            if field_def.example_value:
                field_schema["example"] = field_def.example_value
            
            # Add validation rules if available
            if field_def.validation_rules:
                field_schema["pattern"] = field_def.validation_rules
            
            schema["properties"][field_def.field_name] = field_schema
            
            # Add to required fields if necessary
            if field_def.required:
                schema["required"].append(field_def.field_name)
        
        return schema
    
    def create_field_descriptions(self) -> str:
        """
        Create detailed field descriptions for the prompt
        
        Returns:
            Formatted field descriptions
        """
        descriptions = []
        
        # Group fields by type for better organization
        field_groups = {}
        for field_def in self.field_definitions:
            field_type = field_def.field_type.lower()
            if field_type not in field_groups:
                field_groups[field_type] = []
            field_groups[field_type].append(field_def)
        
        for field_type, fields in field_groups.items():
            descriptions.append(f"\n{field_type.upper()} FIELDS:")
            for field_def in fields:
                desc = f"- {field_def.field_name}: {field_def.description}"
                if field_def.example_value:
                    desc += f" (Example: {field_def.example_value})"
                if not field_def.required:
                    desc += " [OPTIONAL]"
                descriptions.append(desc)
        
        return "\n".join(descriptions)
    
    def create_extraction_prompt(self, invoice_text: str) -> str:
        """
        Create a structured prompt for the LLM to extract invoice data
        
        Args:
            invoice_text: Raw text content of the invoice
            
        Returns:
            Formatted prompt for LLM
        """
        field_descriptions = self.create_field_descriptions()
        json_schema = self.create_json_schema()
        
        prompt = f"""You are an expert invoice data extraction system. Extract the following information from the invoice text and return it as valid JSON.

FIELD DEFINITIONS:
{field_descriptions}

INVOICE TEXT:
{invoice_text}

INSTRUCTIONS:
1. Extract ALL available fields from the invoice text
2. If a field is not found or not applicable, set it to null
3. For array fields, return as JSON arrays
4. For currency fields, include the currency symbol and amount
5. For date fields, use ISO format (YYYY-MM-DD) when possible
6. Ensure all field names match exactly as specified above
7. Return ONLY the JSON response, no additional text

EXPECTED JSON STRUCTURE:
{json.dumps(json_schema, indent=2)}

JSON Response:"""
        
        return prompt
    
    def validate_extracted_data(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate the structure and content of extracted data
        
        Args:
            data: Parsed JSON data from LLM
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        if not isinstance(data, dict):
            errors.append("Response is not a valid JSON object")
            return False, errors
        
        # Check required fields
        required_fields = [f.field_name for f in self.field_definitions if f.required]
        for field_name in required_fields:
            if field_name not in data:
                errors.append(f"Required field '{field_name}' is missing")
            elif data[field_name] is None or data[field_name] == "":
                errors.append(f"Required field '{field_name}' is empty")
        
        # Validate field types and rules
        for field_def in self.field_definitions:
            field_name = field_def.field_name
            if field_name in data and data[field_name] is not None:
                value = data[field_name]
                
                # Type validation
                if field_def.field_type.lower() == "number" and not isinstance(value, (int, float)):
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        errors.append(f"Field '{field_name}' should be a number")
                
                elif field_def.field_type.lower() == "integer" and not isinstance(value, int):
                    try:
                        int(value)
                    except (ValueError, TypeError):
                        errors.append(f"Field '{field_name}' should be an integer")
                
                elif field_def.field_type.lower() == "boolean" and not isinstance(value, bool):
                    if str(value).lower() not in ['true', 'false', '1', '0']:
                        errors.append(f"Field '{field_name}' should be a boolean")
                
                elif field_def.field_type.lower() == "array" and not isinstance(value, list):
                    errors.append(f"Field '{field_name}' should be an array")
                
                # Validation rules
                if field_def.validation_rules and isinstance(value, str):
                    if not re.match(field_def.validation_rules, value):
                        errors.append(f"Field '{field_name}' does not match validation pattern")
        
        return len(errors) == 0, errors
    
    def extract_invoice_data(self, invoice_text: str) -> Optional[ExtractedInvoiceData]:
        """
        Extract invoice data from text using LLM
        
        Args:
            invoice_text: Raw text content of the invoice
            
        Returns:
            ExtractedInvoiceData object with extracted information or None if extraction fails
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
            is_valid, errors = self.validate_extracted_data(parsed_data)
            if not is_valid:
                logger.warning(f"Data validation warnings: {errors}")
                # Continue processing even with validation warnings
            
            # Create ExtractedInvoiceData object
            invoice_data = ExtractedInvoiceData()
            invoice_data.fields = parsed_data
            
            logger.info(f"Successfully extracted {len(parsed_data)} fields from invoice")
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error during invoice extraction: {e}")
            return None
    
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
    
    def process_invoice_file(self, file_path: str) -> Optional[ExtractedInvoiceData]:
        """
        Process an invoice file and extract data
        
        Args:
            file_path: Path to the invoice file
            
        Returns:
            ExtractedInvoiceData object with extracted information
        """
        try:
            # For text files
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    invoice_text = f.read()
            else:
                # For PDF files, you would need to add PDF text extraction
                raise NotImplementedError("PDF processing not implemented. Please convert to text first.")
            
            return self.extract_invoice_data(invoice_text)
            
        except Exception as e:
            logger.error(f"Error processing invoice file {file_path}: {e}")
            return None
    
    def export_results_to_excel(self, results: List[ExtractedInvoiceData], output_path: str) -> None:
        """
        Export extraction results to Excel file
        
        Args:
            results: List of extracted invoice data
            output_path: Path for output Excel file
        """
        try:
            # Convert results to DataFrame
            rows = []
            for i, result in enumerate(results):
                row = {"invoice_index": i + 1}
                row.update(result.to_dict())
                rows.append(row)
            
            df = pd.DataFrame(rows)
            
            # Write to Excel
            df.to_excel(output_path, index=False)
            logger.info(f"Results exported to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting results to Excel: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize the extractor with field configuration
    extractor = DynamicInvoiceExtractor(
        sagemaker_endpoint_name="your-sagemaker-endpoint-name",
        field_config_path="invoice_fields.xlsx"
    )
    
    # Example invoice text
    sample_invoice = """
    INVOICE #INV-2024-001
    Date: 2024-01-15
    Vendor: ABC Corporation
    Amount: $1,500.00
    
    Bill To:
    XYZ Company
    123 Main Street
    New York, NY 10001
    
    Ship To:
    XYZ Company Warehouse
    456 Oak Avenue
    Los Angeles, CA 90001
    
    Line Items:
    1. Product A - Quantity: 10, Unit Price: $50.00, Total: $500.00
    2. Product B - Quantity: 5, Unit Price: $200.00, Total: $1,000.00
    
    Subtotal: $1,500.00
    Tax: $0.00
    Total: $1,500.00
    """
    
    # Extract data
    result = extractor.extract_invoice_data(sample_invoice)
    
    if result:
        print("Extracted Fields:")
        for field_name, value in result.to_dict().items():
            print(f"  {field_name}: {value}")
    else:
        print("Failed to extract invoice data")
