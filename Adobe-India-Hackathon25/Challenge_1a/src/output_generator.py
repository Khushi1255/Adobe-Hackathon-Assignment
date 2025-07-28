"""
Output Generator for Challenge 1a
Converts pdfstructure document format to required JSON schema
"""

import json
from typing import List, Dict, Any
from pdfstructure.model.document import StructuredPdfDocument, Section, TextElement
from pdfstructure.hierarchy.traversal import traverse_in_order


class Challenge1AOutputGenerator:
    """
    Generates output in the exact format required by Challenge 1a
    """
    
    def __init__(self):
        self.required_schema = {
            "title": "string",
            "outline": [
                {
                    "level": "string",  # "H1", "H2", "H3"
                    "text": "string",
                    "page": "integer"
                }
            ]
        }
    
    def generate_output(self, document: StructuredPdfDocument, title: str) -> Dict[str, Any]:
        """
        Generate output in the exact format required by Challenge 1a
        
        Args:
            document: Parsed PDF document
            title: Extracted document title
            
        Returns:
            Dictionary matching the required JSON schema
        """
        outline = []
        
        # Extract headings from all sections
        headings = self._extract_headings(document)
        
        # Sort headings by page number
        headings.sort(key=lambda h: h.get('page', 0))
        
        # Validate hierarchy
        headings = self._validate_hierarchy(headings)
        
        return {
            "title": title,
            "outline": headings
        }
    
    def _extract_headings(self, document: StructuredPdfDocument) -> List[Dict[str, Any]]:
        """
        Extract all headings from the document structure
        """
        headings = []
        
        # Traverse all sections in order
        for section in traverse_in_order(document):
            if section.heading and section.heading.text:
                heading_info = self._create_heading_info(section)
                if heading_info:
                    headings.append(heading_info)
        
        return headings
    
    def _create_heading_info(self, section: Section) -> Dict[str, Any]:
        """
        Create heading information dictionary
        """
        if not section.heading or not section.heading.text:
            return None
        
        text = section.heading.text.strip()
        if not text:
            return None
        
        # Get page number (convert to 1-based indexing)
        page = section.heading.page + 1 if hasattr(section.heading, 'page') and section.heading.page is not None else 1
        
        # Get heading level
        level = getattr(section.heading, 'heading_level', None)
        if not level:
            # Fallback: determine level from section level
            level = self._determine_level_from_section(section)
        
        # Calculate position for sorting (higher y position = higher on page)
        position = 0
        if hasattr(section.heading, '_data') and section.heading._data:
            try:
                position = section.heading._data.y1
            except (AttributeError, TypeError):
                pass
        
        return {
            "level": level,
            "text": text,
            "page": page
        }
    
    def _determine_level_from_section(self, section: Section) -> str:
        """
        Determine heading level from section level if not explicitly set
        """
        section_level = getattr(section, 'level', 0)
        
        if section_level == 0:
            return "H1"
        elif section_level == 1:
            return "H2"
        else:
            return "H3"
    
    def _validate_hierarchy(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate and fix heading hierarchy to ensure proper H1 > H2 > H3 relationship
        """
        if not headings:
            return headings
        
        validated_headings = []
        current_h1 = None
        current_h2 = None
        
        for heading in headings:
            level = heading.get('level', 'H3')
            
            if level == "H1":
                current_h1 = heading
                current_h2 = None
                validated_headings.append(heading)
            elif level == "H2":
                if not current_h1:
                    # If no H1 before H2, promote to H1
                    heading['level'] = "H1"
                    current_h1 = heading
                    current_h2 = None
                else:
                    current_h2 = heading
                validated_headings.append(heading)
            elif level == "H3":
                if not current_h2:
                    # If no H2 before H3, promote to H2
                    heading['level'] = "H2"
                    current_h2 = heading
                validated_headings.append(heading)
        
        return validated_headings
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate output against required schema
        
        Args:
            output: Generated output dictionary
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check required fields
            if 'title' not in output or 'outline' not in output:
                return False
            
            # Check title is string
            if not isinstance(output['title'], str):
                return False
            
            # Check outline is list
            if not isinstance(output['outline'], list):
                return False
            
            # Check each outline item
            for item in output['outline']:
                if not isinstance(item, dict):
                    return False
                
                # Check required fields
                if 'level' not in item or 'text' not in item or 'page' not in item:
                    return False
                
                # Check field types
                if not isinstance(item['level'], str):
                    return False
                if not isinstance(item['text'], str):
                    return False
                if not isinstance(item['page'], int):
                    return False
                
                # Check level values
                if item['level'] not in ['H1', 'H2', 'H3']:
                    return False
                
                # Check page number is positive
                if item['page'] < 1:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def save_output(self, output: Dict[str, Any], output_path: str) -> str:
        """
        Save output to JSON file
        
        Args:
            output: Generated output dictionary
            output_path: Path to save the JSON file
            
        Returns:
            Path to saved file
        """
        # Validate output before saving
        if not self.validate_output(output):
            raise ValueError("Output does not match required schema")
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def get_schema_description(self) -> str:
        """
        Get description of the required schema
        """
        return """
        Required JSON Schema:
        {
            "title": "string",
            "outline": [
                {
                    "level": "string",  // "H1", "H2", or "H3"
                    "text": "string",   // Heading text
                    "page": "integer"   // Page number (1-based)
                }
            ]
        }
        """ 