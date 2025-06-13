import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from extract_thinker import Extractor
from extract_thinker.models.transformers import TransformersModel
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

class PersonInfo(BaseModel):
    """Example schema for extraction"""
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

class LocalLlamaExtractor:
    def __init__(self, model_path: str, device: str = "auto"):
        """
        Initialize the local Llama model extractor
        
        Args:
            model_path: Path to your local Llama model directory
            device: Device to run the model on ("cuda", "cpu", or "auto")
        """
        self.model_path = model_path
        self.device = self._get_device(device)
        
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
            return {}
    
    def batch_extract(self, texts: List[str], schema: BaseModel,
                     temperature: float = 0.1,
                     max_tokens: int = 512) -> List[Dict[str, Any]]:
        """
        Extract data from multiple texts
        
        Args:
            texts: List of input texts
            schema: Pydantic model defining the extraction schema
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            List of extracted data dictionaries
        """
        results = []
        for i, text in enumerate(texts):
            print(f"Processing text {i+1}/{len(texts)}...")
            result = self.extract_data(text, schema, temperature, max_tokens)
            results.append(result)
        return results

def main():
    """Example usage of the LocalLlamaExtractor"""
    
    # Initialize extractor with your local model path
    MODEL_PATH = "/path/to/your/llama/model"  # Update this path
    
    try:
        extractor = LocalLlamaExtractor(MODEL_PATH)
        
        # Example 1: Extract person information
        person_text = """
        John Smith is a 35-year-old software engineer working at Google. 
        He lives in San Francisco and has been developing AI applications 
        for the past 8 years.
        """
        
        print("Extracting person information...")
        person_result = extractor.extract_data(person_text, PersonInfo)
        print("Person extraction result:")
        print(json.dumps(person_result, indent=2))
        
        # Example 2: Extract company information
        company_text = """
        TechCorp is a innovative technology company founded in 2015. 
        They specialize in artificial intelligence and machine learning solutions.
        The company has grown to over 500 employees and is headquartered in Austin, Texas.
        """
        
        print("\nExtracting company information...")
        company_result = extractor.extract_data(company_text, CompanyInfo)
        print("Company extraction result:")
        print(json.dumps(company_result, indent=2))
        
        # Example 3: Batch processing
        batch_texts = [
            "Sarah Johnson, 28, works as a data scientist in Boston.",
            "Microsoft was founded in 1975 and operates in the technology sector with over 180,000 employees.",
            "Dr. Robert Brown is a 45-year-old cardiologist practicing in New York."
        ]
        
        print("\nBatch processing mixed data...")
        # For mixed data, you might want to create a more generic schema
        class MixedInfo(BaseModel):
            entity_type: str  # "person" or "company"
            name: str
            details: Dict[str, Any] = {}
        
        batch_results = extractor.batch_extract(batch_texts, MixedInfo)
        print("Batch extraction results:")
        for i, result in enumerate(batch_results):
            print(f"Text {i+1}: {json.dumps(result, indent=2)}")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Update MODEL_PATH to point to your local Llama model")
        print("2. Install required packages: pip install extract-thinker transformers torch")
        print("3. Ensure your model files are properly downloaded")

# Alternative implementation using direct model inference
class DirectLlamaExtractor:
    """
    Alternative approach using direct model inference without ExtractThinker
    Useful if you want more control over the extraction process
    """
    
    def __init__(self, model_path: str, device: str = "auto"):
        self.model_path = model_path
        self.device = self._get_device(device)
        
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
    
    def create_extraction_prompt(self, text: str, schema: BaseModel) -> str:
        """Create a prompt for extraction based on schema"""
        schema_fields = []
        for field_name, field_info in schema.model_fields.items():
            field_type = field_info.annotation
            schema_fields.append(f"- {field_name}: {field_type}")
        
        prompt = f"""Extract the following information from the text and return it as JSON:

Schema:
{chr(10).join(schema_fields)}

Text: {text}

JSON Output:"""
        return prompt
    
    def extract_with_prompt(self, text: str, schema: BaseModel) -> Dict[str, Any]:
        """Extract data using custom prompt"""
        prompt = self.create_extraction_prompt(text, schema)
        
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True)
        if self.device == "cuda":
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract JSON from response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return {"raw_response": response}

if __name__ == "__main__":
    main()