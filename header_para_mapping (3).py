from typing import Dict, List, Tuple, Optional
from markitdown import MarkItDown
import json

# Option 1: Using mistune for proper markdown parsing
try:
    import mistune
    MISTUNE_AVAILABLE = True
except ImportError:
    MISTUNE_AVAILABLE = False

# Option 2: Using markdown-analysis for structure extraction
try:
    from mrkdwn_analysis import MarkdownAnalyzer
    MARKDOWN_ANALYSIS_AVAILABLE = True
except ImportError:
    MARKDOWN_ANALYSIS_AVAILABLE = False

# Option 3: Using standard markdown library
try:
    import markdown
    from markdown.extensions.toc import TocExtension
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

class HeaderParagraphMapper:
    def __init__(self, parser_preference: str = "auto"):
        """
        Initialize the mapper with a preferred parser.
        
        Args:
            parser_preference: "mistune", "markdown_analysis", "markdown", or "auto"
        """
        self.md = MarkItDown()
        self.parser_preference = parser_preference
        self._setup_parser()
    
    def _setup_parser(self):
        """Setup the best available parser based on preference and availability."""
        if self.parser_preference == "auto":
            if MARKDOWN_ANALYSIS_AVAILABLE:
                self.parser_type = "markdown_analysis"
            elif MISTUNE_AVAILABLE:
                self.parser_type = "mistune"
            elif MARKDOWN_AVAILABLE:
                self.parser_type = "markdown"
            else:
                raise ImportError("No suitable markdown parser found. Install mistune, markdown-analysis, or markdown.")
        else:
            self.parser_type = self.parser_preference
    
    def extract_headers_and_paragraphs(self, file_path: str) -> Dict[str, List[str]]:
        """
        Extract headers and map them to their corresponding paragraphs from a file.
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            Dict[str, List[str]]: Dictionary mapping headers to their paragraphs
        """
        try:
            # Convert document to markdown using markitdown
            result = self.md.convert(file_path)
            markdown_content = result.text_content
            
            return self.parse_with_library(markdown_content)
            
        except Exception as e:
            print(f"Error processing file: {e}")
            return {}
    
    def parse_with_library(self, markdown_text: str) -> Dict[str, List[str]]:
        """
        Parse markdown using the best available library.
        
        Args:
            markdown_text (str): Markdown formatted text
            
        Returns:
            Dict[str, List[str]]: Dictionary mapping headers to paragraphs
        """
        if self.parser_type == "markdown_analysis":
            return self._parse_with_markdown_analysis(markdown_text)
        elif self.parser_type == "mistune":
            return self._parse_with_mistune(markdown_text)
        elif self.parser_type == "markdown":
            return self._parse_with_markdown(markdown_text)
        else:
            raise ValueError(f"Unsupported parser type: {self.parser_type}")
    
    def _parse_with_markdown_analysis(self, markdown_text: str) -> Dict[str, List[str]]:
        """Parse using markdown-analysis library."""
        if not MARKDOWN_ANALYSIS_AVAILABLE:
            raise ImportError("markdown-analysis library not available")
        
        import tempfile
        import os
        
        # Create a temporary file with the markdown content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(markdown_text)
            temp_file_path = temp_file.name
        
        try:
            # Now use the file path with MarkdownAnalyzer
            analyzer = MarkdownAnalyzer(temp_file_path)
            
            # Use the library's methods to identify elements
            headers = analyzer.identify_headers()
            paragraphs = analyzer.identify_paragraphs()
            
            # Try to get lists if the method exists
            lists = []
            try:
                if hasattr(analyzer, 'identify_lists'):
                    lists = analyzer.identify_lists()
                elif hasattr(analyzer, 'identify_list_items'):
                    lists = analyzer.identify_list_items()
            except:
                pass
            
            header_para_map = {}
            
            if not headers:
                return header_para_map
            
            # Create a mapping based on line positions
            # Get all elements with their positions
            all_elements = []
            
            # Add headers with their positions
            for header in headers:
                if isinstance(header, dict) and 'line' in header:
                    all_elements.append({
                        'type': 'header',
                        'line': header['line'],
                        'text': header.get('text', ''),
                        'level': header.get('level', 1),
                        'data': header
                    })
            
            # Add paragraphs with their positions
            for para in paragraphs:
                if isinstance(para, dict) and 'line' in para:
                    all_elements.append({
                        'type': 'paragraph',
                        'line': para['line'],
                        'text': para.get('text', ''),
                        'data': para
                    })
            
            # Add lists with their positions
            for list_item in lists:
                if isinstance(list_item, dict) and 'line' in list_item:
                    all_elements.append({
                        'type': 'list',
                        'line': list_item['line'],
                        'text': list_item.get('text', ''),
                        'data': list_item
                    })
            
            # Sort all elements by their line position
            all_elements.sort(key=lambda x: x['line'])
            
            # Group content under headers
            current_header = None
            current_content = []
            
            for element in all_elements:
                if element['type'] == 'header':
                    # Save previous header's content
                    if current_header and current_content:
                        header_para_map[current_header] = [item['text'] for item in current_content if item['text'].strip()]
                    
                    # Start new header
                    current_header = element['text']
                    current_content = []
                
                elif element['type'] in ['paragraph', 'list']:
                    # Add content to current header
                    if current_header:
                        current_content.append(element)
            
            # Don't forget the last header
            if current_header and current_content:
                header_para_map[current_header] = [item['text'] for item in current_content if item['text'].strip()]
            
            return header_para_map
            
        except Exception as e:
            print(f"Error in markdown-analysis parsing: {e}")
            # Fallback to a simpler approach using just the extracted elements
            try:
                analyzer = MarkdownAnalyzer(temp_file_path)
                headers = analyzer.identify_headers()
                
                if headers:
                    # Simple fallback: just extract header text
                    header_para_map = {}
                    for header in headers:
                        if isinstance(header, dict):
                            header_text = header.get('text', 'Unknown Header')
                            header_para_map[header_text] = []  # Empty for now
                    return header_para_map
                
            except Exception as e2:
                print(f"Fallback parsing also failed: {e2}")
                return {}
            
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
    
    def _parse_with_mistune(self, markdown_text: str) -> Dict[str, List[str]]:
        """Parse using mistune library with custom renderer."""
        if not MISTUNE_AVAILABLE:
            raise ImportError("mistune library not available")
        
        class HeaderExtractor(mistune.HTMLRenderer):
            def __init__(self):
                super().__init__()
                self.structure = []
                self.current_section = None
                self.content_buffer = []
            
            def heading(self, text, level):
                # Save previous section if exists
                if self.current_section:
                    self.current_section['paragraphs'] = self.content_buffer.copy()
                    self.structure.append(self.current_section)
                
                # Start new section
                self.current_section = {
                    'level': level,
                    'text': text,
                    'paragraphs': []
                }
                self.content_buffer = []
                return f"<h{level}>{text}</h{level}>"
            
            def paragraph(self, text):
                self.content_buffer.append(text)
                return f"<p>{text}</p>"
            
            def finalize(self):
                # Don't forget the last section
                if self.current_section:
                    self.current_section['paragraphs'] = self.content_buffer.copy()
                    self.structure.append(self.current_section)
                return self.structure
        
        renderer = HeaderExtractor()
        markdown_parser = mistune.create_markdown(renderer=renderer)
        
        # Parse the markdown
        markdown_parser(markdown_text)
        structure = renderer.finalize()
        
        # Convert to header-paragraph mapping
        header_para_map = {}
        for section in structure:
            header_text = section['text']
            paragraphs = section['paragraphs']
            header_para_map[header_text] = paragraphs
        
        return header_para_map
    
    def _parse_with_markdown(self, markdown_text: str) -> Dict[str, List[str]]:
        """Parse using standard markdown library with TOC extension."""
        if not MARKDOWN_AVAILABLE:
            raise ImportError("markdown library not available")
        
        # Use TOC extension to extract headers
        toc_extension = TocExtension()
        md_parser = markdown.Markdown(extensions=[toc_extension])
        
        # Parse markdown
        html_output = md_parser.convert(markdown_text)
        toc = toc_extension.toc
        
        # Extract structure from TOC
        header_para_map = {}
        lines = markdown_text.split('\n')
        current_header = None
        current_paragraphs = []
        
        for line in lines:
            line = line.strip()
            
            # Check if it's a header using markdown parser's detected headers
            if line.startswith('#'):
                # Save previous header's content
                if current_header and current_paragraphs:
                    header_para_map[current_header] = current_paragraphs.copy()
                
                # Extract header text (remove # symbols)
                current_header = line.lstrip('#').strip()
                current_paragraphs = []
            elif line and not line.startswith('#'):
                # This is content, add to current section
                if line:  # Non-empty content
                    current_paragraphs.append(line)
            elif not line and current_paragraphs:
                # Empty line - end current paragraph if we have content
                pass
        
        # Don't forget the last header
        if current_header and current_paragraphs:
            # Join lines that belong to the same paragraph
            paragraphs = []
            current_para = []
            
            for line in current_paragraphs:
                if line.strip():
                    current_para.append(line)
                else:
                    if current_para:
                        paragraphs.append(' '.join(current_para))
                        current_para = []
            
            if current_para:
                paragraphs.append(' '.join(current_para))
            
            header_para_map[current_header] = paragraphs
        
        return header_para_map
    
    def get_document_structure(self, file_path: str) -> List[Dict]:
        """
        Get complete document structure with hierarchy.
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            List[Dict]: List of sections with level, header, and paragraphs
        """
        try:
            result = self.md.convert(file_path)
            markdown_content = result.text_content
            
            if self.parser_type == "markdown_analysis" and MARKDOWN_ANALYSIS_AVAILABLE:
                import tempfile
                import os
                
                # Create temporary file for markdown-analysis
                with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
                    temp_file.write(markdown_content)
                    temp_file_path = temp_file.name
                
                try:
                    analyzer = MarkdownAnalyzer(temp_file_path)
                    headers = analyzer.identify_headers()
                    
                    structure = []
                    
                    for header in headers:
                        structure.append({
                            'level': header.get('level', 1),
                            'header': header.get('text', ''),
                            'paragraphs': []  # Would need additional processing for paragraph mapping
                        })
                    
                    return structure
                    
                finally:
                    # Clean up temp file
                    try:
                        os.unlink(temp_file_path)
                    except OSError:
                        pass
            else:
                # Fallback to basic parsing
                header_para_map = self.parse_with_library(markdown_content)
                structure = []
                
                for header, paragraphs in header_para_map.items():
                    structure.append({
                        'level': 1,  # Default level
                        'header': header,
                        'paragraphs': paragraphs
                    })
                
                return structure
                
        except Exception as e:
            print(f"Error getting document structure: {e}")
            return []

def main():
    """Example usage with different parsers"""
    
    print("Available parsers:")
    print(f"- mistune: {'✓' if MISTUNE_AVAILABLE else '✗'}")
    print(f"- markdown-analysis: {'✓' if MARKDOWN_ANALYSIS_AVAILABLE else '✗'}")
    print(f"- markdown: {'✓' if MARKDOWN_AVAILABLE else '✗'}")
    print()
    
    # Sample markdown for testing
    sample_markdown = """# Introduction
This is the introduction paragraph explaining the document's purpose.

Another paragraph in the introduction with more details.

## Background Information
Here we provide essential background context.

Multiple sentences can form a single paragraph. This continues the same paragraph.

### Technical Specifications
Detailed technical information goes here.

Performance metrics and benchmarks.

## Methodology
Our approach involves several key steps.

Each step builds upon the previous one.

### Data Collection
Information about data gathering procedures.

### Analysis Techniques
Statistical methods and algorithms used.

# Results and Findings
The experimental results show significant improvements.

Detailed analysis reveals important patterns.

## Performance Metrics
Quantitative results and measurements.

# Conclusion
Summary of key findings and implications.

Recommendations for future research directions."""
    
    try:
        # Test with auto-detection
        mapper = HeaderParagraphMapper(parser_preference="auto")
        print(f"Using parser: {mapper.parser_type}")
        print("="*60)
        
        # Parse the sample markdown
        header_map = mapper.parse_with_library(sample_markdown)
        
        print("HEADER-PARAGRAPH MAPPING:")
        print("="*60)
        for header, paragraphs in header_map.items():
            print(f"\n📋 Header: {header}")
            print(f"   Paragraphs: {len(paragraphs)}")
            for i, para in enumerate(paragraphs, 1):
                print(f"   {i}. {para[:100]}{'...' if len(para) > 100 else ''}")
        
        print(f"\n{'='*60}")
        print("USAGE EXAMPLES:")
        print("="*60)
        print("# Process a document file:")
        print("mapper = HeaderParagraphMapper()")
        print("result = mapper.extract_headers_and_paragraphs('document.pdf')")
        print()
        print("# Get document structure:")
        print("structure = mapper.get_document_structure('document.docx')")
        print()
        print("# Use specific parser:")
        print("mapper = HeaderParagraphMapper(parser_preference='mistune')")
        
        print(f"\n{'='*60}")
        print("INSTALLATION:")
        print("="*60)
        print("pip install markitdown")
        print("pip install mistune  # For mistune parser")
        print("pip install markdown-analysis  # For advanced analysis")
        print("pip install markdown  # For standard parser")
        
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install required libraries:")
        print("pip install markitdown mistune")

if __name__ == "__main__":
    main()
