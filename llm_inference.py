import json
import time
import boto3
from typing import Optional, Dict, Any
import logging
from botocore.exceptions import ClientError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMInference:
    """Class for handling LLM inference with SageMaker async endpoints"""
    
    def __init__(self, endpoint_name: str, region_name: str = 'us-east-1'):
        """
        Initialize the LLM inference client
        
        Args:
            endpoint_name: Name of the SageMaker async endpoint
            region_name: AWS region where the endpoint is deployed
        """
        self.endpoint_name = endpoint_name
        self.region_name = region_name
        
        # Initialize AWS clients
        self.sagemaker_runtime = boto3.client('sagemaker-runtime', region_name=region_name)
        self.s3_client = boto3.client('s3', region_name=region_name)
        
        # Configuration for Llama 3.1 8B
        self.max_tokens = 2048
        self.temperature = 0.1  # Low temperature for consistent extraction
        self.top_p = 0.9
        
    def prepare_llama_payload(self, prompt: str) -> Dict[str, Any]:
        """
        Prepare the payload for Llama 3.1 8B model
        
        Args:
            prompt: Input prompt for the model
            
        Returns:
            Formatted payload for the model
        """
        # Format prompt for Llama 3.1 (chat format)
        formatted_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert at extracting structured data from invoices. Extract the requested information accurately and return it as valid JSON.<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
        
        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "do_sample": True,
                "stop": ["<|eot_id|>"],
                "return_full_text": False
            }
        }
        
        return payload
    
    def invoke_async_endpoint(self, payload: Dict[str, Any]) -> Optional[str]:
        """
        Invoke the SageMaker async endpoint
        
        Args:
            payload: Model payload
            
        Returns:
            Output location (S3 path) or None if failed
        """
        try:
            # Convert payload to JSON
            json_payload = json.dumps(payload)
            
            # Invoke async endpoint
            response = self.sagemaker_runtime.invoke_endpoint_async(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                InputLocation=json_payload,  # For async, this would typically be an S3 path
                Accept='application/json'
            )
            
            # Return the output location
            return response.get('OutputLocation')
            
        except ClientError as e:
            logger.error(f"AWS Client Error during endpoint invocation: {e}")
            return None
        except Exception as e:
            logger.error(f"Error invoking async endpoint: {e}")
            return None
    
    def invoke_sync_endpoint(self, payload: Dict[str, Any]) -> Optional[str]:
        """
        Invoke the SageMaker endpoint synchronously (fallback option)
        
        Args:
            payload: Model payload
            
        Returns:
            Model response or None if failed
        """
        try:
            # Convert payload to JSON
            json_payload = json.dumps(payload)
            
            # Invoke sync endpoint
            response = self.sagemaker_runtime.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json_payload,
                Accept='application/json'
            )
            
            # Parse response
            result = json.loads(response['Body'].read().decode())
            
            # Extract generated text
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            elif isinstance(result, dict):
                return result.get('generated_text', '')
            else:
                logger.error(f"Unexpected response format: {result}")
                return None
                
        except ClientError as e:
            logger.error(f"AWS Client Error during endpoint invocation: {e}")
            return None
        except Exception as e:
            logger.error(f"Error invoking sync endpoint: {e}")
            return None
    
    def wait_for_async_result(self, output_location: str, max_wait_time: int = 300) -> Optional[str]:
        """
        Wait for async endpoint result and retrieve from S3
        
        Args:
            output_location: S3 path where result will be stored
            max_wait_time: Maximum time to wait in seconds
            
        Returns:
            Model response or None if failed/timeout
        """
        try:
            # Parse S3 location
            if not output_location.startswith('s3://'):
                logger.error(f"Invalid S3 output location: {output_location}")
                return None
            
            # Extract bucket and key
            s3_path = output_location[5:]  # Remove 's3://'
            bucket, key = s3_path.split('/', 1)
            
            # Wait for result
            start_time = time.time()
            while time.time() - start_time < max_wait_time:
                try:
                    # Try to get the object
                    response = self.s3_client.get_object(Bucket=bucket, Key=key)
                    result = json.loads(response['Body'].read().decode())
                    
                    # Extract generated text
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get('generated_text', '')
                    elif isinstance(result, dict):
                        return result.get('generated_text', '')
                    else:
                        logger.error(f"Unexpected response format: {result}")
                        return None
                        
                except ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchKey':
                        # Result not ready yet, wait and retry
                        time.sleep(5)
                        continue
                    else:
                        logger.error(f"S3 error: {e}")
                        return None
                        
            logger.error(f"Timeout waiting for async result after {max_wait_time} seconds")
            return None
            
        except Exception as e:
            logger.error(f"Error waiting for async result: {e}")
            return None
    
    def infer(self, prompt: str, use_async: bool = True) -> Optional[str]:
        """
        Run inference on the LLM
        
        Args:
            prompt: Input prompt
            use_async: Whether to use async endpoint (default: True)
            
        Returns:
            Model response or None if failed
        """
        try:
            # Prepare payload
            payload = self.prepare_llama_payload(prompt)
            
            if use_async:
                # Use async endpoint
                logger.info("Using async endpoint for inference")
                output_location = self.invoke_async_endpoint(payload)
                
                if output_location:
                    return self.wait_for_async_result(output_location)
                else:
                    logger.warning("Async endpoint failed, falling back to sync")
                    return self.invoke_sync_endpoint(payload)
            else:
                # Use sync endpoint
                logger.info("Using sync endpoint for inference")
                return self.invoke_sync_endpoint(payload)
                
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            return None
    
    def batch_infer(self, prompts: list, use_async: bool = True) -> list:
        """
        Run batch inference on multiple prompts
        
        Args:
            prompts: List of input prompts
            use_async: Whether to use async endpoint
            
        Returns:
            List of model responses
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            logger.info(f"Processing prompt {i+1}/{len(prompts)}")
            result = self.infer(prompt, use_async=use_async)
            results.append(result)
            
            # Add small delay to avoid overwhelming the endpoint
            if i < len(prompts) - 1:
                time.sleep(1)
        
        return results

# Example usage and testing
if __name__ == "__main__":
    # Initialize the inference client
    llm = LLMInference("your-sagemaker-endpoint-name")
    
    # Test prompt
    test_prompt = """Extract the invoice number and line items from this invoice:
    
    INVOICE #12345
    Line 1: Product A, shipped from New York
    Line 2: Product B, shipped from California
    """
    
    # Run inference
    result = llm.infer(test_prompt)
    
    if result:
        print("LLM Response:")
        print(result)
    else:
        print("Failed to get response from LLM")
