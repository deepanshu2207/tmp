import pandas as pd
from typing import List, Dict, Any

def create_invoice_fields_template() -> List[Dict[str, Any]]:
    """
    Create a comprehensive template for invoice field definitions
    
    Returns:
        List of field definitions for the Excel template
    """
    fields = [
        # Basic Invoice Information
        {
            "field_name": "invoice_number",
            "field_type": "string",
            "description": "Unique invoice identifier",
            "required": True,
            "validation_rules": r"^[A-Z0-9\-]+$",
            "example_value": "INV-2024-001"
        },
        {
            "field_name": "invoice_date",
            "field_type": "date",
            "description": "Date when invoice was issued",
            "required": True,
            "validation_rules": None,
            "example_value": "2024-01-15"
        },
        {
            "field_name": "due_date",
            "field_type": "date",
            "description": "Payment due date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-02-15"
        },
        {
            "field_name": "purchase_order_number",
            "field_type": "string",
            "description": "Purchase order reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "PO-2024-100"
        },
        
        # Vendor Information
        {
            "field_name": "vendor_name",
            "field_type": "string",
            "description": "Name of the vendor/supplier",
            "required": True,
            "validation_rules": None,
            "example_value": "ABC Corporation"
        },
        {
            "field_name": "vendor_address",
            "field_type": "string",
            "description": "Vendor's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "123 Business St, City, State 12345"
        },
        {
            "field_name": "vendor_phone",
            "field_type": "string",
            "description": "Vendor's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-123-4567"
        },
        {
            "field_name": "vendor_email",
            "field_type": "string",
            "description": "Vendor's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "billing@abc-corp.com"
        },
        {
            "field_name": "vendor_tax_id",
            "field_type": "string",
            "description": "Vendor's tax identification number",
            "required": False,
            "validation_rules": None,
            "example_value": "12-3456789"
        },
        
        # Customer/Bill To Information
        {
            "field_name": "customer_name",
            "field_type": "string",
            "description": "Name of the customer being billed",
            "required": True,
            "validation_rules": None,
            "example_value": "XYZ Company"
        },
        {
            "field_name": "customer_address",
            "field_type": "string",
            "description": "Customer's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "456 Main St, City, State 67890"
        },
        {
            "field_name": "customer_phone",
            "field_type": "string",
            "description": "Customer's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-987-6543"
        },
        {
            "field_name": "customer_email",
            "field_type": "string",
            "description": "Customer's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "accounts@xyz-company.com"
        },
        
        # Shipping Information
        {
            "field_name": "ship_to_name",
            "field_type": "string",
            "description": "Name for shipping recipient",
            "required": False,
            "validation_rules": None,
            "example_value": "XYZ Company Warehouse"
        },
        {
            "field_name": "ship_to_address",
            "field_type": "string",
            "description": "Shipping address",
            "required": False,
            "validation_rules": None,
            "example_value": "789 Warehouse Blvd, City, State 11111"
        },
        {
            "field_name": "shipping_method",
            "field_type": "string",
            "description": "Method of shipping",
            "required": False,
            "validation_rules": None,
            "example_value": "Ground"
        },
        {
            "field_name": "tracking_number",
            "field_type": "string",
            "description": "Shipment tracking number",
            "required": False,
            "validation_rules": None,
            "example_value": "1Z999AA1234567890"
        },
        
        # Financial Information
        {
            "field_name": "subtotal",
            "field_type": "currency",
            "description": "Subtotal amount before tax",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "tax_amount",
            "field_type": "currency",
            "description": "Total tax amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$120.00"
        },
        {
            "field_name": "tax_rate",
            "field_type": "number",
            "description": "Tax rate as percentage",
            "required": False,
            "validation_rules": None,
            "example_value": "8.00"
        },
        {
            "field_name": "discount_amount",
            "field_type": "currency",
            "description": "Total discount amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$50.00"
        },
        {
            "field_name": "shipping_cost",
            "field_type": "currency",
            "description": "Shipping and handling cost",
            "required": False,
            "validation_rules": None,
            "example_value": "$25.00"
        },
        {
            "field_name": "total_amount",
            "field_type": "currency",
            "description": "Final total amount due",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,595.00"
        },
        {
            "field_name": "currency",
            "field_type": "string",
            "description": "Currency code",
            "required": False,
            "validation_rules": r"^[A-Z]{3}$",
            "example_value": "USD"
        },
        
        # Line Items (Arrays)
        {
            "field_name": "line_items",
            "field_type": "array",
            "description": "Array of line items with details",
            "required": True,
            "validation_rules": None,
            "example_value": '[{"id": "1", "description": "Product A", "quantity": 10, "unit_price": 50.00, "total": 500.00}]'
        },
        {
            "field_name": "line_item_count",
            "field_type": "integer",
            "description": "Total number of line items",
            "required": False,
            "validation_rules": None,
            "example_value": "5"
        },
        
        # Payment Information
        {
            "field_name": "payment_terms",
            "field_type": "string",
            "description": "Payment terms and conditions",
            "required": False,
            "validation_rules": None,
            "example_value": "Net 30"
        },
        {
            "field_name": "payment_method",
            "field_type": "string",
            "description": "Preferred payment method",
            "required": False,
            "validation_rules": None,
            "example_value": "Bank Transfer"
        },
        {
            "field_name": "bank_account_number",
            "field_type": "string",
            "description": "Bank account number for payment",
            "required": False,
            "validation_rules": None,
            "example_value": "1234567890"
        },
        {
            "field_name": "routing_number",
            "field_type": "string",
            "description": "Bank routing number",
            "required": False,
            "validation_rules": r"^[0-9]{9}$",
            "example_value": "123456789"
        },
        
        # Additional Fields
        {
            "field_name": "reference_number",
            "field_type": "string",
            "description": "Additional reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "REF-2024-001"
        },
        {
            "field_name": "project_code",
            "field_type": "string",
            "description": "Project or job code",
            "required": False,
            "validation_rules": None,
            "example_value": "PROJ-2024-001"
        },
        {
            "field_name": "department",
            "field_type": "string",
            "description": "Department or cost center",
            "required": False,
            "validation_rules": None,
            "example_value": "IT Department"
        },
        {
            "field_name": "approval_status",
            "field_type": "string",
            "description": "Invoice approval status",
            "required": False,
            "validation_rules": None,
            "example_value": "Approved"
        },
        {
            "field_name": "notes",
            "field_type": "string",
            "description": "Additional notes or comments",
            "required": False,
            "validation_rules": None,
            "example_value": "Rush order - expedited shipping"
        },
        
        # Compliance and Legal
        {
            "field_name": "contract_number",
            "field_type": "string",
            "description": "Contract reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "CONTRACT-2024-001"
        },
        {
            "field_name": "license_required",
            "field_type": "boolean",
            "description": "Whether special license is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "regulatory_code",
            "field_type": "string",
            "description": "Regulatory or compliance code",
            "required": False,
            "validation_rules": None,
            "example_value": "FDA-2024-001"
        },
        
        # Dates and Timestamps
        {
            "field_name": "delivery_date",
            "field_type": "date",
            "description": "Expected or actual delivery date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-20"
        },
        {
            "field_name": "service_period_start",
            "field_type": "date",
            "description": "Service period start date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-01"
        },
        {
            "field_name": "service_period_end",
            "field_type": "date",
            "description": "Service period end date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-31"
        },
        
        # Quality and Inspection
        {
            "field_name": "quality_inspection_required",
            "field_type": "boolean",
            "description": "Whether quality inspection is required",
            "required": False,
            "validation_rules": None,
            "example_value": "true"
        },
        {
            "field_name": "inspection_certificate",
            "field_type": "string",
            "description": "Inspection certificate number",
            "required": False,
            "validation_rules": None,
            "example_value": "CERT-2024-001"
        },
        
        # International Trade
        {
            "field_name": "country_of_origin",
            "field_type": "string",
            "description": "Country where goods were manufactured",
            "required": False,
            "validation_rules": None,
            "example_value": "United States"
        },
        {
            "field_name": "customs_value",
            "field_type": "currency",
            "description": "Customs declared value",
            "required": False,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "harmonized_code",
            "field_type": "string",
            "description": "Harmonized tariff code",
            "required": False,
            "validation_rules": None,
            "example_value": "8471.30.01"
        },
        
        # Insurance and Warranty
        {
            "field_name": "insurance_required",
            "field_type": "boolean",
            "description": "Whether insurance is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "warranty_period",
            "field_type": "string",
            "description": "Warranty period for products",
            "required": False,
            "validation_rules": None,
            "example_value": "12 months"
        },
        
        # Environmental and Sustainability
        {
            "field_name": "eco_friendly",
            "field_type": "boolean",
            "description": "Whether products are eco-friendly",
            "required": False,
            "validation_rules": None,
            "example_value": "true"
        },
        {
            "field_name": "carbon_footprint",
            "field_type": "string",
            "description": "Carbon footprint information",
            "required": False,
            "validation_rules": None,
            "example_value": "Low carbon footprint"
        },
        {
            "field_name": "recycling_instructions",
            "field_type": "string",
            "description": "Product recycling instructions",
            "required": False,
            "validation_rules": None,
            "example_value": "Recycle at electronic waste center"
        }
    ]
    
    return fields

def create_excel_template(output_file: str = "invoice_fields.xlsx") -> None:
    """
    Create Excel template file with field definitions
    
    Args:
        output_file: Name of the output Excel file
    """
    try:
        # Get field definitions
        fields = create_invoice_fields_template()
        
        # Create DataFrame
        df = pd.DataFrame(fields)
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            # Write the data
            df.to_excel(writer, sheet_name='Invoice_Fields', index=False)
            
            # Get the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Invoice_Fields']
            
            # Add formatting
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Format the header row
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Set column widths
            column_widths = {
                'field_name': 25,
                'field_type': 15,
                'description': 40,
                'required': 12,
                'validation_rules': 30,
                'example_value': 25
            }
            
            for col_num, (col_name, width) in enumerate(column_widths.items()):
                worksheet.set_column(col_num, col_num, width)
            
            # Add data validation for field_type column
            field_types = ['string', 'number', 'integer', 'boolean', 'array', 'date', 'currency']
            worksheet.data_validation(f'B2:B{len(fields) + 1}', {
                'validate': 'list',
                'source': field_types
            })
            
            # Add data validation for required column
            worksheet.data_validation(f'D2:D{len(fields) + 1}', {
                'validate': 'list',
                'source': ['TRUE', 'FALSE']
            })
        
        print(f"Excel template created successfully: {output_file}")
        print(f"Total fields defined: {len(fields)}")
        
        # Print summary by field type
        field_type_counts = {}
        for field in fields:
            field_type = field['field_type']
            field_type_counts[field_type] = field_type_counts.get(field_type, 0) + 1
        
        print("\nField type distribution:")
        for field_type, count in sorted(field_type_counts.items()):
            print(f"  {field_type}: {count} fields")
            
    except Exception as e:
        print(f"Error creating Excel template: {e}")

def create_sample_usage_script(output_file: str = "sample_usage.py") -> None:
    """
    Create a sample usage script showing how to use the extractor
    
    Args:
        output_file: Name of the output Python file
    """
    sample_code = '''"""
Sample usage script for the Dynamic Invoice Extractor
"""

from dynamic_invoice_extractor import DynamicInvoiceExtractor
import json

def main():
    # Initialize the extractor
    extractor = DynamicInvoiceExtractor(
        sagemaker_endpoint_name="your-sagemaker-endpoint-name",
        field_config_path="invoice_fields.xlsx"
    )
    
    # Sample invoice text
    sample_invoice = """
    INVOICE #INV-2024-001
    Date: January 15, 2024
    Due Date: February 15, 2024
    PO Number: PO-2024-100
    
    From: ABC Corporation
    123 Business Street
    New York, NY 10001
    Phone: +1-555-123-4567
    Email: billing@abc-corp.com
    Tax ID: 12-3456789
    
    Bill To:
    XYZ Company
    456 Main Street
    Los Angeles, CA 90001
    Phone: +1-555-987-6543
    Email: accounts@xyz-company.com
    
    Ship To:
    XYZ Company Warehouse
    789 Warehouse Boulevard
    Los Angeles, CA 90002
    
    Line Items:
    1. Product A - Premium Widget
       Quantity: 10
       Unit Price: $50.00
       Total: $500.00
       
    2. Product B - Standard Widget
       Quantity: 5
       Unit Price: $200.00
       Total: $1,000.00
       
    3. Service Fee - Installation
       Quantity: 1
       Unit Price: $150.00
       Total: $150.00
    
    Subtotal: $1,650.00
    Tax (8%): $132.00
    Shipping: $25.00
    Total: $1,807.00
    
    Payment Terms: Net 30
    Payment Method: Bank Transfer
    Account Number: 1234567890
    Routing Number: 123456789
    
    Notes: Rush order - expedited shipping required
    Project Code: PROJ-2024-001
    Department: IT Department
    """
    
    # Extract data
    print("Extracting invoice data...")
    result = extractor.extract_invoice_data(sample_invoice)
    
    if result:
        print("\\nExtraction successful!")
        print(f"Total fields extracted: {len(result.fields)}")
        
        # Print extracted data
        print("\\nExtracted Data:")
        for field_name, value in result.to_dict().items():
            print(f"  {field_name}: {value}")
        
        # Save to JSON file
        with open("extracted_data.json", "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        print("\\nData saved to extracted_data.json")
        
    else:
        print("Failed to extract invoice data")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open(output_file, 'w') as f:
            f.write(sample_code)
        print(f"Sample usage script created: {output_file}")
    except Exception as e:
        print(f"Error creating sample script: {e}")

def create_field_customization_guide(output_file: str = "field_customization_guide.md") -> None:
    """
    Create a guide for customizing fields
    
    Args:
        output_file: Name of the output markdown file
    """
    guide_content = '''# Invoice Field Customization Guide

## Overview
This guide explains how to customize the invoice extraction fields by modifying the Excel configuration file.

## Excel File Structure

The `invoice_fields.xlsx` file contains the following columns:

### Required Columns:
- **field_name**: Unique identifier for the field (no spaces, use underscores)
- **field_type**: Data type of the field
- **description**: Human-readable description of what the field contains

### Optional Columns:
- **required**: Boolean indicating if the field is mandatory (TRUE/FALSE)
- **validation_rules**: Regular expression pattern for validation
- **example_value**: Sample value to help the LLM understand the expected format

## Supported Field Types

1. **string**: Text data (names, addresses, descriptions)
2. **number**: Numeric values with decimals (prices, percentages)
3. **integer**: Whole numbers (quantities, counts)
4. **boolean**: True/false values (yes/no questions)
5. **array**: Lists of items (line items, tags)
6. **date**: Date values (invoice date, due date)
7. **currency**: Monetary values (amounts, costs)

## Field Naming Conventions

- Use lowercase letters and underscores
- Be descriptive but concise
- Avoid special characters and spaces
- Examples: `invoice_number`, `vendor_name`, `total_amount`

## Validation Rules

Use regular expressions to validate field values:

- **Email**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}import pandas as pd
from typing import List, Dict, Any

def create_invoice_fields_template() -> List[Dict[str, Any]]:
    """
    Create a comprehensive template for invoice field definitions
    
    Returns:
        List of field definitions for the Excel template
    """
    fields = [
        # Basic Invoice Information
        {
            "field_name": "invoice_number",
            "field_type": "string",
            "description": "Unique invoice identifier",
            "required": True,
            "validation_rules": r"^[A-Z0-9\-]+$",
            "example_value": "INV-2024-001"
        },
        {
            "field_name": "invoice_date",
            "field_type": "date",
            "description": "Date when invoice was issued",
            "required": True,
            "validation_rules": None,
            "example_value": "2024-01-15"
        },
        {
            "field_name": "due_date",
            "field_type": "date",
            "description": "Payment due date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-02-15"
        },
        {
            "field_name": "purchase_order_number",
            "field_type": "string",
            "description": "Purchase order reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "PO-2024-100"
        },
        
        # Vendor Information
        {
            "field_name": "vendor_name",
            "field_type": "string",
            "description": "Name of the vendor/supplier",
            "required": True,
            "validation_rules": None,
            "example_value": "ABC Corporation"
        },
        {
            "field_name": "vendor_address",
            "field_type": "string",
            "description": "Vendor's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "123 Business St, City, State 12345"
        },
        {
            "field_name": "vendor_phone",
            "field_type": "string",
            "description": "Vendor's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-123-4567"
        },
        {
            "field_name": "vendor_email",
            "field_type": "string",
            "description": "Vendor's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "billing@abc-corp.com"
        },
        {
            "field_name": "vendor_tax_id",
            "field_type": "string",
            "description": "Vendor's tax identification number",
            "required": False,
            "validation_rules": None,
            "example_value": "12-3456789"
        },
        
        # Customer/Bill To Information
        {
            "field_name": "customer_name",
            "field_type": "string",
            "description": "Name of the customer being billed",
            "required": True,
            "validation_rules": None,
            "example_value": "XYZ Company"
        },
        {
            "field_name": "customer_address",
            "field_type": "string",
            "description": "Customer's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "456 Main St, City, State 67890"
        },
        {
            "field_name": "customer_phone",
            "field_type": "string",
            "description": "Customer's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-987-6543"
        },
        {
            "field_name": "customer_email",
            "field_type": "string",
            "description": "Customer's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "accounts@xyz-company.com"
        },
        
        # Shipping Information
        {
            "field_name": "ship_to_name",
            "field_type": "string",
            "description": "Name for shipping recipient",
            "required": False,
            "validation_rules": None,
            "example_value": "XYZ Company Warehouse"
        },
        {
            "field_name": "ship_to_address",
            "field_type": "string",
            "description": "Shipping address",
            "required": False,
            "validation_rules": None,
            "example_value": "789 Warehouse Blvd, City, State 11111"
        },
        {
            "field_name": "shipping_method",
            "field_type": "string",
            "description": "Method of shipping",
            "required": False,
            "validation_rules": None,
            "example_value": "Ground"
        },
        {
            "field_name": "tracking_number",
            "field_type": "string",
            "description": "Shipment tracking number",
            "required": False,
            "validation_rules": None,
            "example_value": "1Z999AA1234567890"
        },
        
        # Financial Information
        {
            "field_name": "subtotal",
            "field_type": "currency",
            "description": "Subtotal amount before tax",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "tax_amount",
            "field_type": "currency",
            "description": "Total tax amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$120.00"
        },
        {
            "field_name": "tax_rate",
            "field_type": "number",
            "description": "Tax rate as percentage",
            "required": False,
            "validation_rules": None,
            "example_value": "8.00"
        },
        {
            "field_name": "discount_amount",
            "field_type": "currency",
            "description": "Total discount amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$50.00"
        },
        {
            "field_name": "shipping_cost",
            "field_type": "currency",
            "description": "Shipping and handling cost",
            "required": False,
            "validation_rules": None,
            "example_value": "$25.00"
        },
        {
            "field_name": "total_amount",
            "field_type": "currency",
            "description": "Final total amount due",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,595.00"
        },
        {
            "field_name": "currency",
            "field_type": "string",
            "description": "Currency code",
            "required": False,
            "validation_rules": r"^[A-Z]{3}$",
            "example_value": "USD"
        },
        
        # Line Items (Arrays)
        {
            "field_name": "line_items",
            "field_type": "array",
            "description": "Array of line items with details",
            "required": True,
            "validation_rules": None,
            "example_value": '[{"id": "1", "description": "Product A", "quantity": 10, "unit_price": 50.00, "total": 500.00}]'
        },
        {
            "field_name": "line_item_count",
            "field_type": "integer",
            "description": "Total number of line items",
            "required": False,
            "validation_rules": None,
            "example_value": "5"
        },
        
        # Payment Information
        {
            "field_name": "payment_terms",
            "field_type": "string",
            "description": "Payment terms and conditions",
            "required": False,
            "validation_rules": None,
            "example_value": "Net 30"
        },
        {
            "field_name": "payment_method",
            "field_type": "string",
            "description": "Preferred payment method",
            "required": False,
            "validation_rules": None,
            "example_value": "Bank Transfer"
        },
        {
            "field_name": "bank_account_number",
            "field_type": "string",
            "description": "Bank account number for payment",
            "required": False,
            "validation_rules": None,
            "example_value": "1234567890"
        },
        {
            "field_name": "routing_number",
            "field_type": "string",
            "description": "Bank routing number",
            "required": False,
            "validation_rules": r"^[0-9]{9}$",
            "example_value": "123456789"
        },
        
        # Additional Fields
        {
            "field_name": "reference_number",
            "field_type": "string",
            "description": "Additional reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "REF-2024-001"
        },
        {
            "field_name": "project_code",
            "field_type": "string",
            "description": "Project or job code",
            "required": False,
            "validation_rules": None,
            "example_value": "PROJ-2024-001"
        },
        {
            "field_name": "department",
            "field_type": "string",
            "description": "Department or cost center",
            "required": False,
            "validation_rules": None,
            "example_value": "IT Department"
        },
        {
            "field_name": "approval_status",
            "field_type": "string",
            "description": "Invoice approval status",
            "required": False,
            "validation_rules": None,
            "example_value": "Approved"
        },
        {
            "field_name": "notes",
            "field_type": "string",
            "description": "Additional notes or comments",
            "required": False,
            "validation_rules": None,
            "example_value": "Rush order - expedited shipping"
        },
        
        # Compliance and Legal
        {
            "field_name": "contract_number",
            "field_type": "string",
            "description": "Contract reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "CONTRACT-2024-001"
        },
        {
            "field_name": "license_required",
            "field_type": "boolean",
            "description": "Whether special license is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "regulatory_code",
            "field_type": "string",
            "description": "Regulatory or compliance code",
            "required": False,
            "validation_rules": None,
            "example_value": "FDA-2024-001"
        },
        
        # Dates and Timestamps
        {
            "field_name": "delivery_date",
            "field_type": "date",
            "description": "Expected or actual delivery date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-20"
        },
        {
            "field_name": "service_period_start",
            "field_type": "date",
            "description": "Service period start date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-01"
        },
        {
            "field_name": "service_period_end",
            "field_type": "date",
            "description": "Service period end date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-31"
        },
        
        # Quality and Inspection
        {
            "field_name": "quality_inspection_required",
            "field_type": "boolean",
            "description": "Whether quality inspection is required",
            "required": False,
            "validation_rules": None,
            "example_value": "true"
        },
        {
            "field_name": "inspection_certificate",
            "field_type": "string",
            "description": "Inspection certificate number",
            "required": False,
            "validation_rules": None,
            "example_value": "CERT-2024-001"
        },
        
        # International Trade
        {
            "field_name": "country_of_origin",
            "field_type": "string",
            "description": "Country where goods were manufactured",
            "required": False,
            "validation_rules": None,
            "example_value": "United States"
        },
        {
            "field_name": "customs_value",
            "field_type": "currency",
            "description": "Customs declared value",
            "required": False,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "harmonized_code",
            "field_type": "string",
            "description": "Harmonized tariff code",
            "required": False,
            "validation_rules": None,
            "example_value": "8471.30.01"
        },
        
        # Insurance and Warranty
        {
            "field_name": "insurance_required",
            "field_type": "boolean",
            "description": "Whether insurance is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "warranty_period",
            "field_type": "string",
            "description": "Warranty period for products",
            "required": False,
            "validation_rules": None,
            "example_value": "12 months"
        },
        

- **Phone**: `^[\\+]?[0-9\\-\\(\\)\\s]+import pandas as pd
from typing import List, Dict, Any

def create_invoice_fields_template() -> List[Dict[str, Any]]:
    """
    Create a comprehensive template for invoice field definitions
    
    Returns:
        List of field definitions for the Excel template
    """
    fields = [
        # Basic Invoice Information
        {
            "field_name": "invoice_number",
            "field_type": "string",
            "description": "Unique invoice identifier",
            "required": True,
            "validation_rules": r"^[A-Z0-9\-]+$",
            "example_value": "INV-2024-001"
        },
        {
            "field_name": "invoice_date",
            "field_type": "date",
            "description": "Date when invoice was issued",
            "required": True,
            "validation_rules": None,
            "example_value": "2024-01-15"
        },
        {
            "field_name": "due_date",
            "field_type": "date",
            "description": "Payment due date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-02-15"
        },
        {
            "field_name": "purchase_order_number",
            "field_type": "string",
            "description": "Purchase order reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "PO-2024-100"
        },
        
        # Vendor Information
        {
            "field_name": "vendor_name",
            "field_type": "string",
            "description": "Name of the vendor/supplier",
            "required": True,
            "validation_rules": None,
            "example_value": "ABC Corporation"
        },
        {
            "field_name": "vendor_address",
            "field_type": "string",
            "description": "Vendor's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "123 Business St, City, State 12345"
        },
        {
            "field_name": "vendor_phone",
            "field_type": "string",
            "description": "Vendor's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-123-4567"
        },
        {
            "field_name": "vendor_email",
            "field_type": "string",
            "description": "Vendor's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "billing@abc-corp.com"
        },
        {
            "field_name": "vendor_tax_id",
            "field_type": "string",
            "description": "Vendor's tax identification number",
            "required": False,
            "validation_rules": None,
            "example_value": "12-3456789"
        },
        
        # Customer/Bill To Information
        {
            "field_name": "customer_name",
            "field_type": "string",
            "description": "Name of the customer being billed",
            "required": True,
            "validation_rules": None,
            "example_value": "XYZ Company"
        },
        {
            "field_name": "customer_address",
            "field_type": "string",
            "description": "Customer's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "456 Main St, City, State 67890"
        },
        {
            "field_name": "customer_phone",
            "field_type": "string",
            "description": "Customer's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-987-6543"
        },
        {
            "field_name": "customer_email",
            "field_type": "string",
            "description": "Customer's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "accounts@xyz-company.com"
        },
        
        # Shipping Information
        {
            "field_name": "ship_to_name",
            "field_type": "string",
            "description": "Name for shipping recipient",
            "required": False,
            "validation_rules": None,
            "example_value": "XYZ Company Warehouse"
        },
        {
            "field_name": "ship_to_address",
            "field_type": "string",
            "description": "Shipping address",
            "required": False,
            "validation_rules": None,
            "example_value": "789 Warehouse Blvd, City, State 11111"
        },
        {
            "field_name": "shipping_method",
            "field_type": "string",
            "description": "Method of shipping",
            "required": False,
            "validation_rules": None,
            "example_value": "Ground"
        },
        {
            "field_name": "tracking_number",
            "field_type": "string",
            "description": "Shipment tracking number",
            "required": False,
            "validation_rules": None,
            "example_value": "1Z999AA1234567890"
        },
        
        # Financial Information
        {
            "field_name": "subtotal",
            "field_type": "currency",
            "description": "Subtotal amount before tax",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "tax_amount",
            "field_type": "currency",
            "description": "Total tax amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$120.00"
        },
        {
            "field_name": "tax_rate",
            "field_type": "number",
            "description": "Tax rate as percentage",
            "required": False,
            "validation_rules": None,
            "example_value": "8.00"
        },
        {
            "field_name": "discount_amount",
            "field_type": "currency",
            "description": "Total discount amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$50.00"
        },
        {
            "field_name": "shipping_cost",
            "field_type": "currency",
            "description": "Shipping and handling cost",
            "required": False,
            "validation_rules": None,
            "example_value": "$25.00"
        },
        {
            "field_name": "total_amount",
            "field_type": "currency",
            "description": "Final total amount due",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,595.00"
        },
        {
            "field_name": "currency",
            "field_type": "string",
            "description": "Currency code",
            "required": False,
            "validation_rules": r"^[A-Z]{3}$",
            "example_value": "USD"
        },
        
        # Line Items (Arrays)
        {
            "field_name": "line_items",
            "field_type": "array",
            "description": "Array of line items with details",
            "required": True,
            "validation_rules": None,
            "example_value": '[{"id": "1", "description": "Product A", "quantity": 10, "unit_price": 50.00, "total": 500.00}]'
        },
        {
            "field_name": "line_item_count",
            "field_type": "integer",
            "description": "Total number of line items",
            "required": False,
            "validation_rules": None,
            "example_value": "5"
        },
        
        # Payment Information
        {
            "field_name": "payment_terms",
            "field_type": "string",
            "description": "Payment terms and conditions",
            "required": False,
            "validation_rules": None,
            "example_value": "Net 30"
        },
        {
            "field_name": "payment_method",
            "field_type": "string",
            "description": "Preferred payment method",
            "required": False,
            "validation_rules": None,
            "example_value": "Bank Transfer"
        },
        {
            "field_name": "bank_account_number",
            "field_type": "string",
            "description": "Bank account number for payment",
            "required": False,
            "validation_rules": None,
            "example_value": "1234567890"
        },
        {
            "field_name": "routing_number",
            "field_type": "string",
            "description": "Bank routing number",
            "required": False,
            "validation_rules": r"^[0-9]{9}$",
            "example_value": "123456789"
        },
        
        # Additional Fields
        {
            "field_name": "reference_number",
            "field_type": "string",
            "description": "Additional reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "REF-2024-001"
        },
        {
            "field_name": "project_code",
            "field_type": "string",
            "description": "Project or job code",
            "required": False,
            "validation_rules": None,
            "example_value": "PROJ-2024-001"
        },
        {
            "field_name": "department",
            "field_type": "string",
            "description": "Department or cost center",
            "required": False,
            "validation_rules": None,
            "example_value": "IT Department"
        },
        {
            "field_name": "approval_status",
            "field_type": "string",
            "description": "Invoice approval status",
            "required": False,
            "validation_rules": None,
            "example_value": "Approved"
        },
        {
            "field_name": "notes",
            "field_type": "string",
            "description": "Additional notes or comments",
            "required": False,
            "validation_rules": None,
            "example_value": "Rush order - expedited shipping"
        },
        
        # Compliance and Legal
        {
            "field_name": "contract_number",
            "field_type": "string",
            "description": "Contract reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "CONTRACT-2024-001"
        },
        {
            "field_name": "license_required",
            "field_type": "boolean",
            "description": "Whether special license is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "regulatory_code",
            "field_type": "string",
            "description": "Regulatory or compliance code",
            "required": False,
            "validation_rules": None,
            "example_value": "FDA-2024-001"
        },
        
        # Dates and Timestamps
        {
            "field_name": "delivery_date",
            "field_type": "date",
            "description": "Expected or actual delivery date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-20"
        },
        {
            "field_name": "service_period_start",
            "field_type": "date",
            "description": "Service period start date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-01"
        },
        {
            "field_name": "service_period_end",
            "field_type": "date",
            "description": "Service period end date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-31"
        },
        
        # Quality and Inspection
        {
            "field_name": "quality_inspection_required",
            "field_type": "boolean",
            "description": "Whether quality inspection is required",
            "required": False,
            "validation_rules": None,
            "example_value": "true"
        },
        {
            "field_name": "inspection_certificate",
            "field_type": "string",
            "description": "Inspection certificate number",
            "required": False,
            "validation_rules": None,
            "example_value": "CERT-2024-001"
        },
        
        # International Trade
        {
            "field_name": "country_of_origin",
            "field_type": "string",
            "description": "Country where goods were manufactured",
            "required": False,
            "validation_rules": None,
            "example_value": "United States"
        },
        {
            "field_name": "customs_value",
            "field_type": "currency",
            "description": "Customs declared value",
            "required": False,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "harmonized_code",
            "field_type": "string",
            "description": "Harmonized tariff code",
            "required": False,
            "validation_rules": None,
            "example_value": "8471.30.01"
        },
        
        # Insurance and Warranty
        {
            "field_name": "insurance_required",
            "field_type": "boolean",
            "description": "Whether insurance is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "warranty_period",
            "field_type": "string",
            "description": "Warranty period for products",
            "required": False,
            "validation_rules": None,
            "example_value": "12 months"
        },
        

- **Currency Code**: `^[A-Z]{3}import pandas as pd
from typing import List, Dict, Any

def create_invoice_fields_template() -> List[Dict[str, Any]]:
    """
    Create a comprehensive template for invoice field definitions
    
    Returns:
        List of field definitions for the Excel template
    """
    fields = [
        # Basic Invoice Information
        {
            "field_name": "invoice_number",
            "field_type": "string",
            "description": "Unique invoice identifier",
            "required": True,
            "validation_rules": r"^[A-Z0-9\-]+$",
            "example_value": "INV-2024-001"
        },
        {
            "field_name": "invoice_date",
            "field_type": "date",
            "description": "Date when invoice was issued",
            "required": True,
            "validation_rules": None,
            "example_value": "2024-01-15"
        },
        {
            "field_name": "due_date",
            "field_type": "date",
            "description": "Payment due date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-02-15"
        },
        {
            "field_name": "purchase_order_number",
            "field_type": "string",
            "description": "Purchase order reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "PO-2024-100"
        },
        
        # Vendor Information
        {
            "field_name": "vendor_name",
            "field_type": "string",
            "description": "Name of the vendor/supplier",
            "required": True,
            "validation_rules": None,
            "example_value": "ABC Corporation"
        },
        {
            "field_name": "vendor_address",
            "field_type": "string",
            "description": "Vendor's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "123 Business St, City, State 12345"
        },
        {
            "field_name": "vendor_phone",
            "field_type": "string",
            "description": "Vendor's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-123-4567"
        },
        {
            "field_name": "vendor_email",
            "field_type": "string",
            "description": "Vendor's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "billing@abc-corp.com"
        },
        {
            "field_name": "vendor_tax_id",
            "field_type": "string",
            "description": "Vendor's tax identification number",
            "required": False,
            "validation_rules": None,
            "example_value": "12-3456789"
        },
        
        # Customer/Bill To Information
        {
            "field_name": "customer_name",
            "field_type": "string",
            "description": "Name of the customer being billed",
            "required": True,
            "validation_rules": None,
            "example_value": "XYZ Company"
        },
        {
            "field_name": "customer_address",
            "field_type": "string",
            "description": "Customer's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "456 Main St, City, State 67890"
        },
        {
            "field_name": "customer_phone",
            "field_type": "string",
            "description": "Customer's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-987-6543"
        },
        {
            "field_name": "customer_email",
            "field_type": "string",
            "description": "Customer's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "accounts@xyz-company.com"
        },
        
        # Shipping Information
        {
            "field_name": "ship_to_name",
            "field_type": "string",
            "description": "Name for shipping recipient",
            "required": False,
            "validation_rules": None,
            "example_value": "XYZ Company Warehouse"
        },
        {
            "field_name": "ship_to_address",
            "field_type": "string",
            "description": "Shipping address",
            "required": False,
            "validation_rules": None,
            "example_value": "789 Warehouse Blvd, City, State 11111"
        },
        {
            "field_name": "shipping_method",
            "field_type": "string",
            "description": "Method of shipping",
            "required": False,
            "validation_rules": None,
            "example_value": "Ground"
        },
        {
            "field_name": "tracking_number",
            "field_type": "string",
            "description": "Shipment tracking number",
            "required": False,
            "validation_rules": None,
            "example_value": "1Z999AA1234567890"
        },
        
        # Financial Information
        {
            "field_name": "subtotal",
            "field_type": "currency",
            "description": "Subtotal amount before tax",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "tax_amount",
            "field_type": "currency",
            "description": "Total tax amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$120.00"
        },
        {
            "field_name": "tax_rate",
            "field_type": "number",
            "description": "Tax rate as percentage",
            "required": False,
            "validation_rules": None,
            "example_value": "8.00"
        },
        {
            "field_name": "discount_amount",
            "field_type": "currency",
            "description": "Total discount amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$50.00"
        },
        {
            "field_name": "shipping_cost",
            "field_type": "currency",
            "description": "Shipping and handling cost",
            "required": False,
            "validation_rules": None,
            "example_value": "$25.00"
        },
        {
            "field_name": "total_amount",
            "field_type": "currency",
            "description": "Final total amount due",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,595.00"
        },
        {
            "field_name": "currency",
            "field_type": "string",
            "description": "Currency code",
            "required": False,
            "validation_rules": r"^[A-Z]{3}$",
            "example_value": "USD"
        },
        
        # Line Items (Arrays)
        {
            "field_name": "line_items",
            "field_type": "array",
            "description": "Array of line items with details",
            "required": True,
            "validation_rules": None,
            "example_value": '[{"id": "1", "description": "Product A", "quantity": 10, "unit_price": 50.00, "total": 500.00}]'
        },
        {
            "field_name": "line_item_count",
            "field_type": "integer",
            "description": "Total number of line items",
            "required": False,
            "validation_rules": None,
            "example_value": "5"
        },
        
        # Payment Information
        {
            "field_name": "payment_terms",
            "field_type": "string",
            "description": "Payment terms and conditions",
            "required": False,
            "validation_rules": None,
            "example_value": "Net 30"
        },
        {
            "field_name": "payment_method",
            "field_type": "string",
            "description": "Preferred payment method",
            "required": False,
            "validation_rules": None,
            "example_value": "Bank Transfer"
        },
        {
            "field_name": "bank_account_number",
            "field_type": "string",
            "description": "Bank account number for payment",
            "required": False,
            "validation_rules": None,
            "example_value": "1234567890"
        },
        {
            "field_name": "routing_number",
            "field_type": "string",
            "description": "Bank routing number",
            "required": False,
            "validation_rules": r"^[0-9]{9}$",
            "example_value": "123456789"
        },
        
        # Additional Fields
        {
            "field_name": "reference_number",
            "field_type": "string",
            "description": "Additional reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "REF-2024-001"
        },
        {
            "field_name": "project_code",
            "field_type": "string",
            "description": "Project or job code",
            "required": False,
            "validation_rules": None,
            "example_value": "PROJ-2024-001"
        },
        {
            "field_name": "department",
            "field_type": "string",
            "description": "Department or cost center",
            "required": False,
            "validation_rules": None,
            "example_value": "IT Department"
        },
        {
            "field_name": "approval_status",
            "field_type": "string",
            "description": "Invoice approval status",
            "required": False,
            "validation_rules": None,
            "example_value": "Approved"
        },
        {
            "field_name": "notes",
            "field_type": "string",
            "description": "Additional notes or comments",
            "required": False,
            "validation_rules": None,
            "example_value": "Rush order - expedited shipping"
        },
        
        # Compliance and Legal
        {
            "field_name": "contract_number",
            "field_type": "string",
            "description": "Contract reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "CONTRACT-2024-001"
        },
        {
            "field_name": "license_required",
            "field_type": "boolean",
            "description": "Whether special license is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "regulatory_code",
            "field_type": "string",
            "description": "Regulatory or compliance code",
            "required": False,
            "validation_rules": None,
            "example_value": "FDA-2024-001"
        },
        
        # Dates and Timestamps
        {
            "field_name": "delivery_date",
            "field_type": "date",
            "description": "Expected or actual delivery date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-20"
        },
        {
            "field_name": "service_period_start",
            "field_type": "date",
            "description": "Service period start date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-01"
        },
        {
            "field_name": "service_period_end",
            "field_type": "date",
            "description": "Service period end date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-31"
        },
        
        # Quality and Inspection
        {
            "field_name": "quality_inspection_required",
            "field_type": "boolean",
            "description": "Whether quality inspection is required",
            "required": False,
            "validation_rules": None,
            "example_value": "true"
        },
        {
            "field_name": "inspection_certificate",
            "field_type": "string",
            "description": "Inspection certificate number",
            "required": False,
            "validation_rules": None,
            "example_value": "CERT-2024-001"
        },
        
        # International Trade
        {
            "field_name": "country_of_origin",
            "field_type": "string",
            "description": "Country where goods were manufactured",
            "required": False,
            "validation_rules": None,
            "example_value": "United States"
        },
        {
            "field_name": "customs_value",
            "field_type": "currency",
            "description": "Customs declared value",
            "required": False,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "harmonized_code",
            "field_type": "string",
            "description": "Harmonized tariff code",
            "required": False,
            "validation_rules": None,
            "example_value": "8471.30.01"
        },
        
        # Insurance and Warranty
        {
            "field_name": "insurance_required",
            "field_type": "boolean",
            "description": "Whether insurance is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "warranty_period",
            "field_type": "string",
            "description": "Warranty period for products",
            "required": False,
            "validation_rules": None,
            "example_value": "12 months"
        },
        

- **Invoice Number**: `^[A-Z0-9\\-]+import pandas as pd
from typing import List, Dict, Any

def create_invoice_fields_template() -> List[Dict[str, Any]]:
    """
    Create a comprehensive template for invoice field definitions
    
    Returns:
        List of field definitions for the Excel template
    """
    fields = [
        # Basic Invoice Information
        {
            "field_name": "invoice_number",
            "field_type": "string",
            "description": "Unique invoice identifier",
            "required": True,
            "validation_rules": r"^[A-Z0-9\-]+$",
            "example_value": "INV-2024-001"
        },
        {
            "field_name": "invoice_date",
            "field_type": "date",
            "description": "Date when invoice was issued",
            "required": True,
            "validation_rules": None,
            "example_value": "2024-01-15"
        },
        {
            "field_name": "due_date",
            "field_type": "date",
            "description": "Payment due date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-02-15"
        },
        {
            "field_name": "purchase_order_number",
            "field_type": "string",
            "description": "Purchase order reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "PO-2024-100"
        },
        
        # Vendor Information
        {
            "field_name": "vendor_name",
            "field_type": "string",
            "description": "Name of the vendor/supplier",
            "required": True,
            "validation_rules": None,
            "example_value": "ABC Corporation"
        },
        {
            "field_name": "vendor_address",
            "field_type": "string",
            "description": "Vendor's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "123 Business St, City, State 12345"
        },
        {
            "field_name": "vendor_phone",
            "field_type": "string",
            "description": "Vendor's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-123-4567"
        },
        {
            "field_name": "vendor_email",
            "field_type": "string",
            "description": "Vendor's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "billing@abc-corp.com"
        },
        {
            "field_name": "vendor_tax_id",
            "field_type": "string",
            "description": "Vendor's tax identification number",
            "required": False,
            "validation_rules": None,
            "example_value": "12-3456789"
        },
        
        # Customer/Bill To Information
        {
            "field_name": "customer_name",
            "field_type": "string",
            "description": "Name of the customer being billed",
            "required": True,
            "validation_rules": None,
            "example_value": "XYZ Company"
        },
        {
            "field_name": "customer_address",
            "field_type": "string",
            "description": "Customer's billing address",
            "required": False,
            "validation_rules": None,
            "example_value": "456 Main St, City, State 67890"
        },
        {
            "field_name": "customer_phone",
            "field_type": "string",
            "description": "Customer's phone number",
            "required": False,
            "validation_rules": r"^[\+]?[0-9\-\(\)\s]+$",
            "example_value": "+1-555-987-6543"
        },
        {
            "field_name": "customer_email",
            "field_type": "string",
            "description": "Customer's email address",
            "required": False,
            "validation_rules": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "example_value": "accounts@xyz-company.com"
        },
        
        # Shipping Information
        {
            "field_name": "ship_to_name",
            "field_type": "string",
            "description": "Name for shipping recipient",
            "required": False,
            "validation_rules": None,
            "example_value": "XYZ Company Warehouse"
        },
        {
            "field_name": "ship_to_address",
            "field_type": "string",
            "description": "Shipping address",
            "required": False,
            "validation_rules": None,
            "example_value": "789 Warehouse Blvd, City, State 11111"
        },
        {
            "field_name": "shipping_method",
            "field_type": "string",
            "description": "Method of shipping",
            "required": False,
            "validation_rules": None,
            "example_value": "Ground"
        },
        {
            "field_name": "tracking_number",
            "field_type": "string",
            "description": "Shipment tracking number",
            "required": False,
            "validation_rules": None,
            "example_value": "1Z999AA1234567890"
        },
        
        # Financial Information
        {
            "field_name": "subtotal",
            "field_type": "currency",
            "description": "Subtotal amount before tax",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "tax_amount",
            "field_type": "currency",
            "description": "Total tax amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$120.00"
        },
        {
            "field_name": "tax_rate",
            "field_type": "number",
            "description": "Tax rate as percentage",
            "required": False,
            "validation_rules": None,
            "example_value": "8.00"
        },
        {
            "field_name": "discount_amount",
            "field_type": "currency",
            "description": "Total discount amount",
            "required": False,
            "validation_rules": None,
            "example_value": "$50.00"
        },
        {
            "field_name": "shipping_cost",
            "field_type": "currency",
            "description": "Shipping and handling cost",
            "required": False,
            "validation_rules": None,
            "example_value": "$25.00"
        },
        {
            "field_name": "total_amount",
            "field_type": "currency",
            "description": "Final total amount due",
            "required": True,
            "validation_rules": None,
            "example_value": "$1,595.00"
        },
        {
            "field_name": "currency",
            "field_type": "string",
            "description": "Currency code",
            "required": False,
            "validation_rules": r"^[A-Z]{3}$",
            "example_value": "USD"
        },
        
        # Line Items (Arrays)
        {
            "field_name": "line_items",
            "field_type": "array",
            "description": "Array of line items with details",
            "required": True,
            "validation_rules": None,
            "example_value": '[{"id": "1", "description": "Product A", "quantity": 10, "unit_price": 50.00, "total": 500.00}]'
        },
        {
            "field_name": "line_item_count",
            "field_type": "integer",
            "description": "Total number of line items",
            "required": False,
            "validation_rules": None,
            "example_value": "5"
        },
        
        # Payment Information
        {
            "field_name": "payment_terms",
            "field_type": "string",
            "description": "Payment terms and conditions",
            "required": False,
            "validation_rules": None,
            "example_value": "Net 30"
        },
        {
            "field_name": "payment_method",
            "field_type": "string",
            "description": "Preferred payment method",
            "required": False,
            "validation_rules": None,
            "example_value": "Bank Transfer"
        },
        {
            "field_name": "bank_account_number",
            "field_type": "string",
            "description": "Bank account number for payment",
            "required": False,
            "validation_rules": None,
            "example_value": "1234567890"
        },
        {
            "field_name": "routing_number",
            "field_type": "string",
            "description": "Bank routing number",
            "required": False,
            "validation_rules": r"^[0-9]{9}$",
            "example_value": "123456789"
        },
        
        # Additional Fields
        {
            "field_name": "reference_number",
            "field_type": "string",
            "description": "Additional reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "REF-2024-001"
        },
        {
            "field_name": "project_code",
            "field_type": "string",
            "description": "Project or job code",
            "required": False,
            "validation_rules": None,
            "example_value": "PROJ-2024-001"
        },
        {
            "field_name": "department",
            "field_type": "string",
            "description": "Department or cost center",
            "required": False,
            "validation_rules": None,
            "example_value": "IT Department"
        },
        {
            "field_name": "approval_status",
            "field_type": "string",
            "description": "Invoice approval status",
            "required": False,
            "validation_rules": None,
            "example_value": "Approved"
        },
        {
            "field_name": "notes",
            "field_type": "string",
            "description": "Additional notes or comments",
            "required": False,
            "validation_rules": None,
            "example_value": "Rush order - expedited shipping"
        },
        
        # Compliance and Legal
        {
            "field_name": "contract_number",
            "field_type": "string",
            "description": "Contract reference number",
            "required": False,
            "validation_rules": None,
            "example_value": "CONTRACT-2024-001"
        },
        {
            "field_name": "license_required",
            "field_type": "boolean",
            "description": "Whether special license is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "regulatory_code",
            "field_type": "string",
            "description": "Regulatory or compliance code",
            "required": False,
            "validation_rules": None,
            "example_value": "FDA-2024-001"
        },
        
        # Dates and Timestamps
        {
            "field_name": "delivery_date",
            "field_type": "date",
            "description": "Expected or actual delivery date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-20"
        },
        {
            "field_name": "service_period_start",
            "field_type": "date",
            "description": "Service period start date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-01"
        },
        {
            "field_name": "service_period_end",
            "field_type": "date",
            "description": "Service period end date",
            "required": False,
            "validation_rules": None,
            "example_value": "2024-01-31"
        },
        
        # Quality and Inspection
        {
            "field_name": "quality_inspection_required",
            "field_type": "boolean",
            "description": "Whether quality inspection is required",
            "required": False,
            "validation_rules": None,
            "example_value": "true"
        },
        {
            "field_name": "inspection_certificate",
            "field_type": "string",
            "description": "Inspection certificate number",
            "required": False,
            "validation_rules": None,
            "example_value": "CERT-2024-001"
        },
        
        # International Trade
        {
            "field_name": "country_of_origin",
            "field_type": "string",
            "description": "Country where goods were manufactured",
            "required": False,
            "validation_rules": None,
            "example_value": "United States"
        },
        {
            "field_name": "customs_value",
            "field_type": "currency",
            "description": "Customs declared value",
            "required": False,
            "validation_rules": None,
            "example_value": "$1,500.00"
        },
        {
            "field_name": "harmonized_code",
            "field_type": "string",
            "description": "Harmonized tariff code",
            "required": False,
            "validation_rules": None,
            "example_value": "8471.30.01"
        },
        
        # Insurance and Warranty
        {
            "field_name": "insurance_required",
            "field_type": "boolean",
            "description": "Whether insurance is required",
            "required": False,
            "validation_rules": None,
            "example_value": "false"
        },
        {
            "field_name": "warranty_period",
            "field_type": "string",
            "description": "Warranty period for products",
            "required": False,
            "validation_rules": None,
            "example_value": "12 months"
        },
        


## Adding New Fields

1. Open `invoice_fields.xlsx`
2. Add a new row with your field information
3. Save the file
4. Restart your extraction process

## Removing Fields

1. Delete the row from the Excel file
2. Save the file
3. The field will no longer be extracted

## Best Practices

1. **Start Simple**: Begin with required fields only
2. **Test Incrementally**: Add a few fields at a time and test
3. **Use Examples**: Always provide example values
4. **Validate Results**: Check extracted data for accuracy
5. **Document Changes**: Keep track of field modifications

## Common Field Categories

### Basic Invoice Info
- invoice_number, invoice_date, due_date, total_amount

### Vendor Information
- vendor_name, vendor_address, vendor_phone, vendor_email

### Customer Information
- customer_name, customer_address, customer_phone

### Line Items
- line_items (array), line_item_count

### Financial Details
- subtotal, tax_amount, shipping_cost, discount_amount

### Payment Information
- payment_terms, payment_method, bank_account_number

## Troubleshooting

### Field Not Extracted
- Check field name spelling in Excel
- Verify field type is appropriate
- Ensure description is clear
- Add example value

### Validation Errors
- Check regex pattern syntax
- Test regex with sample data
- Make validation rules less restrictive if needed

### Poor Extraction Quality
- Improve field descriptions
- Add more example values
- Adjust LLM prompt if needed
- Ensure invoice text quality is good

## Example Customization

To add a new field for "Project Manager":

1. Add row to Excel:
   - field_name: `project_manager`
   - field_type: `string`
   - description: `Name of the project manager responsible`
   - required: `FALSE`
   - validation_rules: (leave empty)
   - example_value: `John Smith`

2. Save and test with sample invoice containing project manager info

## Support

For technical issues or questions about field customization, refer to the main documentation or contact your system administrator.
'''
    
    try:
        with open(output_file, 'w') as f:
            f.write(guide_content)
        print(f"Field customization guide created: {output_file}")
    except Exception as e:
        print(f"Error creating customization guide: {e}")

# Main execution
if __name__ == "__main__":
    print("Creating Invoice Field Template and Documentation...")
    
    # Create Excel template
    create_excel_template()
    
    # Create sample usage script
    create_sample_usage_script()
    
    # Create customization guide
    create_field_customization_guide()
    
    print("\\nAll files created successfully!")
    print("\\nNext steps:")
    print("1. Review and customize invoice_fields.xlsx")
    print("2. Update your SageMaker endpoint name in the code")
    print("3. Run the sample_usage.py script to test")
    print("4. Refer to field_customization_guide.md for help")
        