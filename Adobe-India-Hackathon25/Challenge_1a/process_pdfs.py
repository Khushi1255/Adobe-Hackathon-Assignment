#!/usr/bin/env python3
"""
Main entry point for Challenge 1a: PDF Structure Extraction
Processes all PDFs in /app/input and generates JSON output in /app/output
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdfstructure.source import FileSource
from pdfstructure.hierarchy.parser import HierarchyParser
from src.heading_detector import CustomHeadingDetector
from src.title_extractor import TitleExtractor
from src.output_generator import Challenge1AOutputGenerator


class PDFProcessor:
    """
    Main PDF processor for Challenge 1a
    """
    
    def __init__(self):
        self.parser = HierarchyParser()
        self.heading_detector = CustomHeadingDetector()
        self.title_extractor = TitleExtractor()
        self.output_generator = Challenge1AOutputGenerator()
    
        # Performance tracking
        self.start_time = None
        self.max_processing_time = 10  # seconds
        
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a single PDF and return the required JSON output
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary matching the required JSON schema
        """
        try:
            print(f"Processing: {os.path.basename(pdf_path)}")
            
            # Check processing time
            if self.start_time and (time.time() - self.start_time) > self.max_processing_time:
                raise TimeoutError(f"Processing time exceeded {self.max_processing_time} seconds")
            
            # Parse PDF using pdfstructure
            source = FileSource(pdf_path)
            document = self.parser.parse_pdf(source)
    
            # Extract title
            title = self.title_extractor.extract_title(document)
            print(f"  Extracted title: {title}")
            
            # Classify headings
            self._classify_headings(document)
            
            # Generate output
            output = self.output_generator.generate_output(document, title)
            
            # Validate output
            if not self.output_generator.validate_output(output):
                raise ValueError("Generated output does not match required schema")
            
            print(f"  Extracted {len(output['outline'])} headings")
            return output
            
        except Exception as e:
            print(f"  Error processing {pdf_path}: {e}")
            # Return fallback output
            return self._create_fallback_output(pdf_path)
    
    def _classify_headings(self, document):
        """
        Add heading level classification to all sections
        """
        def classify_section(section):
            if section.heading:
                level = self.heading_detector.classify_heading_level(
                    section.heading, document.style_distribution
                )
                section.heading.heading_level = level
            
            # Recursively classify children
            for child in section.children:
                classify_section(child)
        
        # Classify all sections
        for section in document.elements:
            classify_section(section)
    
    def _create_fallback_output(self, pdf_path: str) -> Dict[str, Any]:
        """
        Create fallback output when processing fails
        """
        filename = os.path.basename(pdf_path)
        title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        return {
            "title": title,
            "outline": []
        }
    
    def process_all_pdfs(self, input_dir: str, output_dir: str):
        """
        Process all PDFs in the input directory
        
        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory to save JSON output files
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all PDF files
        pdf_files = list(input_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {input_dir}")
            return
        
        print(f"Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF
        for pdf_file in pdf_files:
            try:
                # Start timing for this file
                self.start_time = time.time()
                
                # Process the PDF
                result = self.process_pdf(str(pdf_file))
                
                # Write output
                output_file = output_path / f"{pdf_file.stem}.json"
                self.output_generator.save_output(result, str(output_file))
                
                processing_time = time.time() - self.start_time
                print(f"  Completed in {processing_time:.2f} seconds")
                print(f"  Output: {output_file.name}")
                
            except Exception as e:
                print(f"Failed to process {pdf_file.name}: {e}")
                continue
        
        print(f"Processing complete. Output files saved to {output_dir}")


def main():
    """
    Main function - entry point for the application
    """
    # Define input and output directories
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist")
        sys.exit(1)
    
    print("=== Challenge 1a: PDF Structure Extraction ===")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Create processor and process all PDFs
    processor = PDFProcessor()
    
    try:
        processor.process_all_pdfs(input_dir, output_dir)
        print("\n=== Processing completed successfully ===")
        
    except Exception as e:
        print(f"\nError during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()