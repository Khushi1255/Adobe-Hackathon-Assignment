"""
Title Extractor for Challenge 1a
Extracts document title from first few pages using multiple strategies
"""

import re
from typing import List, Optional
from pdfstructure.model.document import StructuredPdfDocument, Section, TextElement


class TitleExtractor:
    """
    Extracts document title using multiple strategies to ensure accuracy
    """
    
    def __init__(self):
        # Common title patterns
        self.title_patterns = [
            r'^[A-Z][A-Z\s]{3,}$',  # ALL CAPS titles
            r'^[A-Z][a-z\s]{3,}$',  # Title Case
            r'^[A-Z][a-z\s]{3,}[:.]',  # Title with colon or period
        ]
        
        # Words that indicate this is NOT a title
        self.non_title_indicators = {
            'page', 'copyright', 'all rights reserved', 'confidential',
            'draft', 'version', 'date', 'author', 'abstract', 'table of contents'
        }
        
        # Maximum pages to search for title
        self.max_title_search_pages = 3
        
    def extract_title(self, document: StructuredPdfDocument) -> str:
        """
        Extract document title using multiple strategies
        
        Args:
            document: Parsed PDF document
            
        Returns:
            Extracted title string
        """
        if not document or not document.elements:
            return "Untitled Document"
        
        # Strategy 1: Look for title in first few pages
        title = self._find_title_in_first_pages(document)
        if title:
            return title
        
        # Strategy 2: Look for largest font text
        title = self._find_largest_font_text(document)
        if title:
            return title
        
        # Strategy 3: Look for centered, prominent text
        title = self._find_centered_prominent_text(document)
        if title:
            return title
        
        # Strategy 4: Use first significant text block
        title = self._get_first_significant_text(document)
        if title:
            return title
        
        # Fallback: Use filename or default
        return self._get_fallback_title(document)
    
    def _find_title_in_first_pages(self, document: StructuredPdfDocument) -> Optional[str]:
        """
        Look for title in the first few pages
        """
        first_pages_elements = []
        
        # Collect elements from first few pages
        for section in self._traverse_sections(document.elements):
            if section.heading and section.heading.page < self.max_title_search_pages:
                first_pages_elements.append(section.heading)
        
        # Sort by page number and position
        first_pages_elements.sort(key=lambda e: (e.page, -e._data.y1 if hasattr(e, '_data') and e._data else 0))
        
        # Look for title candidates
        for element in first_pages_elements:
            text = element.text.strip()
            if self._is_likely_title(text, element):
                return text
        
        return None
    
    def _find_largest_font_text(self, document: StructuredPdfDocument) -> Optional[str]:
        """
        Find text with the largest font size
        """
        largest_font_element = None
        largest_font_size = 0
        
        for section in self._traverse_sections(document.elements):
            if section.heading:
                element = section.heading
                font_size = element.style.max_size if hasattr(element.style, 'max_size') else 0
                
                if font_size > largest_font_size:
                    text = element.text.strip()
                    if self._is_likely_title(text, element):
                        largest_font_size = font_size
                        largest_font_element = element
        
        if largest_font_element:
            return largest_font_element.text.strip()
        
        return None
    
    def _find_centered_prominent_text(self, document: StructuredPdfDocument) -> Optional[str]:
        """
        Find centered, prominent text that could be a title
        """
        for section in self._traverse_sections(document.elements):
            if section.heading:
                element = section.heading
                if self._is_centered(element) and self._is_prominent(element):
                    text = element.text.strip()
                    if self._is_likely_title(text, element):
                        return text
        
        return None
    
    def _get_first_significant_text(self, document: StructuredPdfDocument) -> Optional[str]:
        """
        Get the first significant text block as title
        """
        for section in self._traverse_sections(document.elements):
            if section.heading:
                text = section.heading.text.strip()
                if len(text) > 3 and not self._is_obviously_not_title(text):
                    return text
        
        return None
    
    def _is_likely_title(self, text: str, element: TextElement) -> bool:
        """
        Determine if text is likely to be a title
        """
        if not text or len(text) < 3:
            return False
        
        # Check for non-title indicators
        text_lower = text.lower()
        for indicator in self.non_title_indicators:
            if indicator in text_lower:
                return False
        
        # Check for title patterns
        for pattern in self.title_patterns:
            if re.match(pattern, text):
                return True
        
        # Check if text is reasonable length for a title
        if 3 <= len(text.split()) <= 15:
            return True
        
        return False
    
    def _is_obviously_not_title(self, text: str) -> bool:
        """
        Check if text is obviously not a title
        """
        text_lower = text.lower()
        
        # Check for non-title indicators
        for indicator in self.non_title_indicators:
            if indicator in text_lower:
                return True
        
        # Check if it's too short or too long
        if len(text) < 3 or len(text.split()) > 20:
            return True
        
        # Check if it's just numbers or special characters
        if text.isdigit() or not any(c.isalpha() for c in text):
            return True
        
        return False
    
    def _is_centered(self, element: TextElement) -> bool:
        """
        Check if text element is centered on the page
        """
        try:
            if not hasattr(element, '_data') or not element._data:
                return False
            
            text_container = element._data
            
            # Get page dimensions
            page_width = text_container.page.width if hasattr(text_container, 'page') else 612
            
            # Get text position
            x0, x1 = text_container.x0, text_container.x1
            text_width = x1 - x0
            
            # Calculate center position
            text_center_x = (x0 + x1) / 2
            page_center_x = page_width / 2
            
            # Check if text is centered (within 15% of page center)
            return abs(text_center_x - page_center_x) < (page_width * 0.15)
            
        except (AttributeError, TypeError):
            return False
    
    def _is_prominent(self, element: TextElement) -> bool:
        """
        Check if text element is prominent (large font, bold, etc.)
        """
        try:
            style = element.style
            
            # Check for bold formatting
            if hasattr(style, 'bold') and style.bold:
                return True
            
            # Check for large font size
            if hasattr(style, 'max_size') and style.max_size > 12:
                return True
            
            # Check for ALL CAPS
            text = element.text.strip()
            if text.isupper() and len(text) > 2:
                return True
            
        except (AttributeError, TypeError):
            pass
        
        return False
    
    def _traverse_sections(self, sections: List[Section]):
        """
        Traverse all sections recursively
        """
        for section in sections:
            yield section
            yield from self._traverse_sections(section.children)
    
    def _get_fallback_title(self, document: StructuredPdfDocument) -> str:
        """
        Get fallback title from filename or default
        """
        # Try to get filename from metadata
        filename = document.metadata.get('filename', '')
        if filename:
            # Remove extension and clean up
            title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
            if title:
                return title
        
        return "Untitled Document" 