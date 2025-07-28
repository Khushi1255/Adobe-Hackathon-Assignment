"""
Custom Heading Detector for Challenge 1a
Classifies headings as H1, H2, H3 based on multiple heuristics
"""

import re
from typing import Optional
from pdfstructure.model.document import TextElement
from pdfstructure.analysis.styledistribution import StyleDistribution


class CustomHeadingDetector:
    """
    Custom heading detector that classifies headings as H1, H2, H3
    Uses multiple heuristics to ensure accuracy
    """
    
    def __init__(self):
        # Font size thresholds (can be adjusted based on document analysis)
        self.h1_threshold = 14.0  # Largest font size
        self.h2_threshold = 12.0  # Medium font size  
        self.h3_threshold = 10.0  # Smaller font size
        
        # Common heading patterns
        self.heading_patterns = {
            'numbered': r'^\d+\.?\s+',  # 1. or 1 
            'lettered': r'^[A-Z]\.?\s+',  # A. or A 
            'roman': r'^[IVX]+\.?\s+',  # I. II. III.
            'chapter': r'^chapter\s+\d+',  # Chapter 1
            'section': r'^section\s+\d+',  # Section 1
        }
        
        # Words that indicate headings
        self.heading_indicators = {
            'introduction', 'conclusion', 'summary', 'overview', 'background',
            'methodology', 'results', 'discussion', 'references', 'appendix',
            'chapter', 'section', 'subsection', 'part', 'unit'
        }
    
    def classify_heading_level(self, element: TextElement, style_distribution) -> Optional[str]:
        """
        Classify heading as H1, H2, or H3 based on multiple heuristics
        
        Args:
            element: TextElement to classify
            style_distribution: Style distribution for context
            
        Returns:
            "H1", "H2", "H3", or None if not a heading
        """
        if not element or not element.text:
            return None
            
        text = element.text.strip()
        style = element.style
        
        # Skip very short text
        if len(text) < 3:
            return None
            
        # Check if this looks like a heading
        if not self._is_likely_heading(text, style, style_distribution):
            return None
        
        # Primary classification based on font size
        level = self._classify_by_font_size(style, style_distribution)
        
        # Refine classification based on additional heuristics
        level = self._refine_classification(level, text, style, element)
        
        return level
    
    def _is_likely_heading(self, text: str, style, style_distribution) -> bool:
        """
        Determine if text is likely to be a heading
        """
        # Check font size threshold
        if style.max_size < style_distribution.body_size + 1:
            return False
            
        # Check for bold formatting
        if style.bold:
            return True
            
        # Check for ALL CAPS
        if text.isupper() and len(text) > 2:
            return True
            
        # Check for heading patterns
        for pattern in self.heading_patterns.values():
            if re.match(pattern, text, re.IGNORECASE):
                return True
                
        # Check for heading indicator words
        text_lower = text.lower()
        for indicator in self.heading_indicators:
            if indicator in text_lower:
                return True
                
        # Check if text is short (headings are usually short)
        if len(text.split()) <= 10:
            return True
            
        return False
    
    def _classify_by_font_size(self, style, style_distribution) -> str:
        """
        Primary classification based on font size
        """
        font_size = style.max_size
        
        # Normalize font size relative to body text
        relative_size = font_size / style_distribution.body_size
        
        if relative_size >= 1.5 or font_size >= self.h1_threshold:
            return "H1"
        elif relative_size >= 1.3 or font_size >= self.h2_threshold:
            return "H2"
        elif relative_size >= 1.1 or font_size >= self.h3_threshold:
            return "H3"
        else:
            return "H3"  # Default to H3 for smaller headings
    
    def _refine_classification(self, level: str, text: str, style, element: TextElement) -> str:
        """
        Refine classification based on additional heuristics
        """
        # ALL CAPS detection - likely H1
        if text.isupper() and len(text) > 2:
            if level == "H2":
                return "H1"
            elif level == "H3":
                return "H2"
        
        # Bold formatting - likely higher level
        if style.bold:
            if level == "H3":
                return "H2"
            elif level == "H2":
                return "H1"
        
        # Numbered patterns - adjust level based on numbering depth
        numbered_level = self._classify_by_numbering(text)
        if numbered_level:
            return numbered_level
        
        # Position-based refinement (if position data is available)
        if hasattr(element, '_data') and element._data:
            position_level = self._classify_by_position(element._data)
            if position_level:
                return position_level
        
        return level
    
    def _classify_by_numbering(self, text: str) -> Optional[str]:
        """
        Classify based on numbering patterns
        """
        # Main chapter numbers (1, 2, 3...) - likely H1
        if re.match(r'^\d+\.?\s+[A-Z]', text):
            return "H1"
        
        # Subsection numbers (1.1, 1.2, 2.1...) - likely H2
        if re.match(r'^\d+\.\d+\.?\s+', text):
            return "H2"
        
        # Sub-subsection numbers (1.1.1, 1.1.2...) - likely H3
        if re.match(r'^\d+\.\d+\.\d+\.?\s+', text):
            return "H3"
        
        # Lettered subsections (A, B, C...) - likely H2
        if re.match(r'^[A-Z]\.?\s+', text):
            return "H2"
        
        return None
    
    def _classify_by_position(self, text_container) -> Optional[str]:
        """
        Classify based on position on page
        """
        try:
            # Get page dimensions
            page_width = text_container.page.width if hasattr(text_container, 'page') else 612
            page_height = text_container.page.height if hasattr(text_container, 'page') else 792
            
            # Get text position
            x0, y0 = text_container.x0, text_container.y0
            x1, y1 = text_container.x1, text_container.y1
            
            # Calculate center position
            text_center_x = (x0 + x1) / 2
            page_center_x = page_width / 2
            
            # Check if text is centered (within 10% of page center)
            is_centered = abs(text_center_x - page_center_x) < (page_width * 0.1)
            
            # Check if text is at top of page (first 20% of page)
            is_at_top = y1 > (page_height * 0.8)
            
            if is_centered and is_at_top:
                return "H1"
            elif is_centered:
                return "H2"
            elif is_at_top:
                return "H2"
            
        except (AttributeError, TypeError):
            pass
        
        return None
    
    def validate_hierarchy(self, headings: list) -> list:
        """
        Validate and fix heading hierarchy
        Ensure proper H1 > H2 > H3 relationship
        """
        if not headings:
            return headings
        
        # Sort by page and position
        sorted_headings = sorted(headings, key=lambda h: (h.get('page', 0), h.get('position', 0)))
        
        current_h1 = None
        current_h2 = None
        
        for heading in sorted_headings:
            level = heading.get('level')
            
            if level == "H1":
                current_h1 = heading
                current_h2 = None
            elif level == "H2":
                if not current_h1:
                    # If no H1 before H2, promote to H1
                    heading['level'] = "H1"
                    current_h1 = heading
                else:
                    current_h2 = heading
            elif level == "H3":
                if not current_h2:
                    # If no H2 before H3, promote to H2
                    heading['level'] = "H2"
                    current_h2 = heading
        
        return sorted_headings 