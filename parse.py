import json
import re

def extract_json_from_response(response):
    # Remove markdown code blocks if present
    response = re.sub(r'^```(?:json)?\s*', '', response, flags=re.MULTILINE)
    response = re.sub(r'\s*```$', '', response, flags=re.MULTILINE)
    
    # Remove triple quotes
    response = response.strip('"""').strip("'''")
    
    # Parse JSON
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None

# Usage
response = '''```json
{"name": "John", "age": 30, "city": "New York"}
```'''

data = extract_json_from_response(response)
print(data)
