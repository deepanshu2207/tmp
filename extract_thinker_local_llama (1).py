import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from extract_thinker import Extractor
from extract_thinker.models.transformers import TransformersModel
from pydantic import BaseModel
from typing import Optional, Dict, Any, Union
import json
from pathlib import Path

# Docling imports (optional - only if document processing is needed)
try:
    from docling.document_converter import DocumentConverter
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.models.tesseract_ocr_model import TesseractOcrOptions
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    print("Docling not available. Install with: pip install docling")

class PersonInfo(BaseModel):
    """Example schema for person extraction"""
    name: str
    age: Optional[int] = None
    occupation: Optional[str] = None
    location: Optional[str] = None

class CompanyInfo(BaseModel):
    """Example schema for company extraction"""
    company_name: str
    industry: Optional[str] = None
    founded_year: Optional[int] = None
    employees: Optional[int] = None

class DocumentInfo(BaseModel):
    """Example schema for document extraction"""
    title: Optional[str] = None
    author: Optional[str] = None
    document_type: Optional[str] = None
    key_points: Optional[str] = None
    summary: Optional[str] = None

class LocalLlamaExtractor:
    def __init__(self, model_path: str, device: str = "auto", enable_docling: bool = True):
        """
        Initialize the local Llama model extractor with optional Docling support
        
        Args:
            model_path: Path to your local Llama model directory
            device: Device to run the model on ("cuda", "cpu", or "auto")
            enable_docling: Whether to enable Docling for document processing
        """
        self.model_path = model_path
        self.device = self._get_device(device)
        self.enable_docling = enable_docling and DOCLING_AVAILABLE
        
        # Initialize Docling if available and enabled
        if self.enable_docling:
            self._init_docling()
        
        # Load tokenizer and model
        print(f"Loading tokenizer from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True
        )
        
        # Add padding token if it doesn't exist
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print(f"Loading model on {self.device}...")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )
        
        # Create text generation pipeline
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto" if self.device == "cuda" else None,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        
        # Create ExtractThinker model wrapper
        self.extract_model = TransformersModel(
            model=self.pipeline,
            model_name="local-llama"
        )
        
        # Initialize extractor
        self.extractor = Extractor(self.extract_model)
    
    def _get_device(self, device: str) -> str:
        """Determine the appropriate device"""
        if device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return device
    
    def _init_docling(self):
        """Initialize Docling document converter"""
        try:
            # Configure pipeline options for better OCR
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = True
            pipeline_options.do_table_structure = True
            pipeline_options.table_structure_options.do_cell_matching = True
            
            # Configure OCR options
            ocr_options = TesseractOcrOptions()
            ocr_options.force_full_page_ocr = True
            
            self.doc_converter = DocumentConverter(
                allowed_formats=[
                    InputFormat.PDF, 
                    InputFormat.DOCX, 
                    InputFormat.HTML,
                    InputFormat.PPTX,
                    InputFormat.TXT
                ],
                pdf_pipeline_options=pipeline_options
            )
            print("Docling initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize Docling: {e}")
            self.enable_docling = False
    
    def process_document(self, file_path: Union[str, Path]) -> str:
        """
        Process a document file and extract text using Docling
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text from the document
        """
        if not self.enable_docling:
            raise RuntimeError("Docling is not available. Install with: pip install docling")
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            print(f"Processing document: {file_path}")
            result = self.doc_converter.convert(file_path)
            
            # Extract text content
            text_content = result.document.export_to_markdown()
            print(f"Successfully extracted {len(text_content)} characters from document")
            
            return text_content
        except Exception as e:
            raise RuntimeError(f"Failed to process document {file_path}: {e}")
    
    def extract_from_document(self, file_path: Union[str, Path], schema: BaseModel,
                            temperature: float = 0.1, max_tokens: int = 512) -> Dict[str, Any]:
        """
        Extract structured data from a document file
        
        Args:
            file_path: Path to the document file
            schema: Pydantic model defining the extraction schema
            temperature: Sampling temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Extracted data as dictionary
        """
        # First, process the document to extract text
        text = self.process_document(file_path)
        
        # Then extract structured data from the text
        return self.extract_data(text, schema, temperature, max_tokens)
    
    def extract_data(self, text: str, schema: BaseModel, 
                    temperature: float = 0.1, 
                    max_tokens: int = 512) -> Dict[str, Any]:
        """
        Extract structured data from text using the specified schema
        
        Args:
            text: Input text to extract from
            schema: Pydantic model defining the extraction schema
            temperature: Sampling temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Extracted data as dictionary
        """
        try:
            # Configure generation parameters
            generation_config = {
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "do_sample": temperature > 0,
                "pad_token_id": self.tokenizer.eos_token_id
            }
            
            # Perform extraction
            result = self.extractor.extract(
                text=text,
                schema=schema,
                **generation_config
            )
            
            return result.model_dump() if hasattr(result, 'model_dump') else result
            
        except Exception as e:
            print(f"Extraction error: {e}")
            return {"error": str(e), "raw_text": text[:500] + "..." if len(text) > 500 else text}

# Alternative implementation using direct model inference
class DirectLlamaExtractor:
    """
    Alternative approach using direct model inference without ExtractThinker
    Useful if you want more control over the extraction process
    """
    
    def __init__(self, model_path: str, device: str = "auto", enable_docling: bool = True):
        self.model_path = model_path
        self.device = self._get_device(device)
        self.enable_docling = enable_docling and DOCLING_AVAILABLE
        
        if self.enable_docling:
            self._init_docling()
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )
    
    def _get_device(self, device: str) -> str:
        if device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return device
    
    def _init_docling(self):
        """Initialize Docling document converter"""
        if not DOCLING_AVAILABLE:
            self.enable_docling = False
            return
            
        try:
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = True
            pipeline_options.do_table_structure = True
            
            self.doc_converter = DocumentConverter(
                allowed_formats=[InputFormat.PDF, InputFormat.DOCX, InputFormat.HTML, InputFormat.TXT],
                pdf_pipeline_options=pipeline_options
            )
        except Exception as e:
            print(f"Warning: Could not initialize Docling: {e}")
            self.enable_docling = False
    
    def process_document(self, file_path: Union[str, Path]) -> str:
        """Process document and extract text"""
        if not self.enable_docling:
            raise RuntimeError("Docling is not available")
        
        file_path = Path(file_path)
        result = self.doc_converter.convert(file_path)
        return result.document.export_to_markdown()
    
    def create_extraction_prompt(self, text: str, schema: BaseModel) -> str:
        """Create a prompt for extraction based on schema"""
        schema_fields = []
        for field_name, field_info in schema.model_fields.items():
            field_type = field_info.annotation
            required = "required" if field_info.is_required() else "optional"
            schema_fields.append(f"- {field_name} ({required}): {field_type}")
        
        prompt = f"""Extract the following information from the text and return it as valid JSON:

Schema:
{chr(10).join(schema_fields)}

Text: {text}

Return only valid JSON without any additional text or formatting:"""
        return prompt
    
    def extract_with_prompt(self, text: str, schema: BaseModel,
                          temperature: float = 0.1, max_tokens: int = 512) -> Dict[str, Any]:
        """Extract data using custom prompt"""
        prompt = self.create_extraction_prompt(text, schema)
        
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=2048)
        if self.device == "cuda":
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode only the generated part
        generated_tokens = outputs[0][len(inputs['input_ids'][0]):]
        response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        # Extract JSON from response
        try:
            # Try to find JSON in the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Try to parse the entire response as JSON
                return json.loads(response.strip())
        except json.JSONDecodeError:
            return {"error": "Could not parse JSON", "raw_response": response}

def main():
    """Example usage of the LocalLlamaExtractor"""
    
    # Initialize extractor with your local model path
    MODEL_PATH = "/path/to/your/llama/model"  # Update this path
    
    try:
        extractor = LocalLlamaExtractor(MODEL_PATH, enable_docling=True)
        
        # Example 1: Extract from text
        person_text = """
        John Smith is a 35-year-old software engineer working at Google. 
        He lives in San Francisco and has been developing AI applications 
        for the past 8 years.
        """
        
        print("Extracting person information from text...")
        person_result = extractor.extract_data(person_text, PersonInfo)
        print("Person extraction result:")
        print(json.dumps(person_result, indent=2))
        
        # Example 2: Extract from document (if Docling is available)
        if extractor.enable_docling:
            print("\nDocument processing example:")
            # Replace with actual document path
            # document_path = "/path/to/your/document.pdf"
            # doc_result = extractor.extract_from_document(document_path, DocumentInfo)
            # print("Document extraction result:")
            # print(json.dumps(doc_result, indent=2))
            print("Docling is available for document processing")
        else:
            print("Docling not available - text extraction only")
        
        # Example 3: Company information extraction
        company_text = """
        TechCorp is an innovative technology company founded in 2015. 
        They specialize in artificial intelligence and machine learning solutions.
        The company has grown to over 500 employees and is headquartered in Austin, Texas.
        """
        
        print("\nExtracting company information...")
        company_result = extractor.extract_data(company_text, CompanyInfo)
        print("Company extraction result:")
        print(json.dumps(company_result, indent=2))
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Update MODEL_PATH to point to your local Llama model")
        print("2. Install required packages: pip install extract-thinker transformers torch")
        print("3. Optional: pip install docling (for document processing)")
        print("4. Ensure your model files are properly downloaded")

if __name__ == "__main__":
    main()