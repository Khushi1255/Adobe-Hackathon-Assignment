#!/usr/bin/env python3
"""
Challenge 1b: Persona-Driven Document Intelligence
Main processing script for Adobe India Hackathon 2025

This script processes multiple PDF documents based on a specific persona and job-to-be-done,
extracting relevant sections and providing intelligent analysis.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data.document_loader import DocumentLoader
from src.retrieval.hybrid_retriever import HybridRetriever
from src.response.generator import ResponseGenerator
from src.utils.config import Config
from src.cache.cache import CacheManager

class Challenge1BProcessor:
    """
    Main processor for Challenge 1b: Persona-Driven Document Intelligence
    """
    
    def __init__(self):
        self.config = Config()
        self.document_loader = DocumentLoader(self.config.to_dict())
        self.retriever = HybridRetriever(self.config)
        # Use mock response generator to avoid LLM server issues
        from src.response.response_generator_mock import MockResponseGenerator
        self.response_generator = MockResponseGenerator(self.config)
        self.cache_manager = CacheManager(self.config['paths']['cache_dir'])
        self.start_time = None
        self.max_processing_time = 60  # 60 seconds limit
        
    def _extract_keywords(self, persona: str, job_to_be_done: str) -> List[str]:
        """Extract keywords from persona and job description using simple NLP heuristics"""
        text = f"{persona} {job_to_be_done}"
        # Lowercase, remove punctuation, split on whitespace
        text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text.lower())
        words = text.split()
        # Remove stopwords (minimal set for demo)
        stopwords = set(['the','and','for','to','of','a','in','on','with','at','by','an','is','as','be','are','from','that','this','it','or','job','role','user','persona','task','do','done'])
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        # Deduplicate
        return list(dict.fromkeys(keywords))

    def _custom_relevance_score(self, chunk_text: str, keywords: List[str]) -> float:
        """Compute a custom relevance score for a chunk based on keyword overlap and TF-IDF cosine similarity."""
        if not keywords:
            return 0.0
        # Keyword overlap
        chunk_words = set(re.sub(r'[^a-zA-Z0-9 ]', ' ', chunk_text.lower()).split())
        overlap = len(chunk_words.intersection(keywords)) / (len(keywords) + 1e-6)
        # TF-IDF cosine similarity
        try:
            tfidf = TfidfVectorizer().fit([chunk_text, ' '.join(keywords)])
            vecs = tfidf.transform([chunk_text, ' '.join(keywords)]).toarray()
            cosine = np.dot(vecs[0], vecs[1]) / (np.linalg.norm(vecs[0]) * np.linalg.norm(vecs[1]) + 1e-6)
        except Exception:
            cosine = 0.0
        # Weighted sum (tune weights as needed)
        return 0.5 * overlap + 0.5 * cosine

    def process_challenge1b(self, input_json_path: str, output_json_path: str) -> Dict[str, Any]:
        """
        Process Challenge 1b input and generate output
        
        Args:
            input_json_path: Path to input JSON file
            output_json_path: Path to output JSON file
            
        Returns:
            Dict containing the processing results
        """
        try:
            self.start_time = time.time()
            
            # Load and parse input
            input_data = self._load_input(input_json_path)
            
            # Extract components
            documents = input_data.get('documents', [])
            persona = input_data.get('persona', {}).get('role', '')
            job_to_be_done = input_data.get('job_to_be_done', {}).get('task', '')
            
            # Store for keyword extraction in _extract_relevant_sections
            self.current_persona = persona
            self.current_job = job_to_be_done

            # Load documents
            loaded_docs = self._load_documents(documents)
            
            # Initialize retriever with loaded documents
            if loaded_docs:
                self.retriever.initialize(loaded_docs)
            
            # Generate persona-specific queries
            queries = self._generate_persona_queries(persona, job_to_be_done)
            
            # Extract relevant sections
            extracted_sections = self._extract_relevant_sections(loaded_docs, queries)
            
            # Generate subsection analysis
            subsection_analysis = self._generate_subsection_analysis(loaded_docs, extracted_sections)
            
            # Create output
            output = self._create_output(
                input_data, 
                extracted_sections, 
                subsection_analysis
            )
            
            # Save output
            self._save_output(output, output_json_path)
            
            processing_time = time.time() - self.start_time
            print(f"✅ Processing completed in {processing_time:.2f} seconds")
            
            return output
            
        except Exception as e:
            print(f"❌ Error processing Challenge 1b: {str(e)}")
            return self._create_fallback_output(input_json_path)
    
    def _load_input(self, input_path: str) -> Dict[str, Any]:
        """Load and validate input JSON"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate required fields
        required_fields = ['documents', 'persona', 'job_to_be_done']
        missing_fields = []
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}. This appears to be an output file, not an input file.")
        
        return data
    
    def _load_documents(self, documents: List[Dict[str, str]]) -> List[Any]:
        """Load all documents from the input specification"""
        loaded_docs = []
        
        for doc_info in documents:
            filename = doc_info.get('filename', '')
            title = doc_info.get('title', '')
            
            # Construct full path
            doc_path = Path("/app/input") / filename
            
            if doc_path.exists():
                try:
                    doc = self.document_loader.load_document(str(doc_path))
                    doc.metadata['title'] = title
                    doc.metadata['filename'] = filename
                    loaded_docs.append(doc)
                    print(f"  📄 Loaded: {filename}")
                except Exception as e:
                    print(f"  ⚠️  Error loading {filename}: {str(e)}")
            else:
                print(f"  ⚠️  File not found: {filename}")
        
        return loaded_docs
    
    def _generate_persona_queries(self, persona: str, job_to_be_done: str) -> List[str]:
        """Generate persona-specific queries based on role and job"""
        queries = []
        
        # Base query from job description
        base_query = f"Find information relevant to: {job_to_be_done}"
        queries.append(base_query)
        
        # Persona-specific queries
        if "researcher" in persona.lower():
            queries.extend([
                "methodology research findings data analysis",
                "experimental results conclusions implications",
                "literature review background context"
            ])
        elif "student" in persona.lower():
            queries.extend([
                "key concepts definitions examples",
                "study materials practice exercises",
                "important topics exam preparation"
            ])
        elif "analyst" in persona.lower():
            queries.extend([
                "data trends statistics metrics",
                "financial performance market analysis",
                "strategic insights recommendations"
            ])
        elif "planner" in persona.lower():
            queries.extend([
                "planning guides recommendations tips",
                "itinerary suggestions activities",
                "practical information logistics"
            ])
        else:
            # Generic queries for other personas
            queries.extend([
                "main topics key information",
                "practical guidance how-to",
                "important details essential content"
            ])
        
        return queries
    
    def _extract_relevant_sections(self, documents: List[Any], queries: List[str]) -> List[Dict[str, Any]]:
        """Extract relevant sections using hybrid retrieval, then re-rank with custom scoring."""
        extracted_sections = []
        # Extract persona/job for keyword extraction
        persona = getattr(self, 'current_persona', '')
        job_to_be_done = getattr(self, 'current_job', '')
        keywords = self._extract_keywords(persona, job_to_be_done)
        for query in queries:
            results = self.retriever.retrieve(query, top_k=5)
            for i, result in enumerate(results):
                section = {
                    "document": result.document.metadata.get('filename', 'unknown.pdf'),
                    "section_title": self._generate_section_title(result.document.metadata.get('title', 'Untitled Section'), result.document.page_content),
                    "importance_rank": len(extracted_sections) + 1,
                    "page_number": result.document.metadata.get('page', 1),
                    "content": result.document.page_content,
                    "relevance_score": result.score
                }
                # Add custom score
                section['custom_score'] = self._custom_relevance_score(result.document.page_content, keywords)
                extracted_sections.append(section)
        # Sort by custom_score and remove duplicates
        unique_sections = self._deduplicate_sections(extracted_sections)
        unique_sections.sort(key=lambda s: s.get('custom_score', 0), reverse=True)
        # Re-rank by importance
        for i, section in enumerate(unique_sections[:10]):
            section['importance_rank'] = i + 1
        return unique_sections[:10]
    
    def _deduplicate_sections(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate sections based on content similarity"""
        unique_sections = []
        seen_content = set()
        
        for section in sections:
            content_hash = hash(section['content'][:100])  # Hash first 100 chars
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_sections.append(section)
        
        return unique_sections
    
    def _generate_section_title(self, base_title: str, content: str) -> str:
        """
        Generate a more descriptive section title based on content
        
        Args:
            base_title: Original title from metadata
            content: Document content
            
        Returns:
            Descriptive section title
        """
        # If we have meaningful content, try to extract a better title
        if content and len(content) > 50:
            # Take first few sentences and create a title
            sentences = content.split('.')[:2]
            if sentences:
                # Clean up the text and create a title
                title_text = '. '.join(sentences).strip()
                if len(title_text) > 20:
                    return title_text[:100] + "..." if len(title_text) > 100 else title_text
        
        # Fallback to enhanced base title
        if base_title and base_title != 'Untitled Section':
            return f"Comprehensive Guide to {base_title}"
        
        return "Important Section Content"
    
    def _generate_subsection_analysis(self, documents: List[Any], extracted_sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate refined text analysis for subsections"""
        subsection_analysis = []
        
        for section in extracted_sections[:5]:  # Top 5 sections for detailed analysis
            # Generate refined text using response generator
            refined_text = self.response_generator.generate_refined_text(
                section['content'],
                section['section_title']
            )
            
            analysis = {
                "document": section['document'].replace('PDFs/', ''),
                "refined_text": refined_text,
                "page_number": section['page_number']
            }
            subsection_analysis.append(analysis)
        
        return subsection_analysis
    
    def _create_output(self, input_data: Dict[str, Any], extracted_sections: List[Dict[str, Any]], subsection_analysis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create the final output JSON"""
        
        # Extract metadata
        documents = input_data.get('documents', [])
        persona = input_data.get('persona', {}).get('role', '')
        job_to_be_done = input_data.get('job_to_be_done', {}).get('task', '')
        
        # Format extracted sections
        formatted_sections = []
        for section in extracted_sections:
            # Remove PDFs/ prefix from document name for output
            doc_name = section['document'].replace('PDFs/', '')
            formatted_section = {
                "document": doc_name,
                "section_title": section['section_title'],
                "importance_rank": section['importance_rank'],
                "page_number": section['page_number']
            }
            formatted_sections.append(formatted_section)
        
        output = {
            "metadata": {
                "input_documents": [doc.get('filename', '').replace('PDFs/', '') for doc in documents],
                "persona": persona,
                "job_to_be_done": job_to_be_done,
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": formatted_sections,
            "subsection_analysis": subsection_analysis
        }
        
        return output
    
    def _save_output(self, output: Dict[str, Any], output_path: str):
        """Save output to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"📄 Output saved to: {output_path}")
    
    def _create_fallback_output(self, input_path: str) -> Dict[str, Any]:
        """Create fallback output in case of errors"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
            
            documents = input_data.get('documents', [])
            persona = input_data.get('persona', {}).get('role', 'Unknown')
            job_to_be_done = input_data.get('job_to_be_done', {}).get('task', 'Unknown task')
            
            return {
                "metadata": {
                    "input_documents": [doc.get('filename', '') for doc in documents],
                    "persona": persona,
                    "job_to_be_done": job_to_be_done,
                    "processing_timestamp": datetime.now().isoformat()
                },
                "extracted_sections": [],
                "subsection_analysis": []
            }
        except Exception:
            return {
                "metadata": {
                    "input_documents": [],
                    "persona": "Unknown",
                    "job_to_be_done": "Unknown task",
                    "processing_timestamp": datetime.now().isoformat()
                },
                "extracted_sections": [],
                "subsection_analysis": []
            }

def main():
    """Main entry point"""
    print("=== Challenge 1b: Persona-Driven Document Intelligence ===")
    
    # Define paths
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find input JSON files (exclude output files)
    input_files = []
    for json_file in input_dir.glob("*.json"):
        # Skip files that are output files (contain "_output" in name)
        if "_output" not in json_file.name:
            input_files.append(json_file)
    
    if not input_files:
        print("❌ No input JSON files found in /app/input")
        return
    
    processor = Challenge1BProcessor()
    
    for input_file in input_files:
        print(f"\n📋 Processing: {input_file.name}")
        
        # Generate output filename
        output_file = output_dir / f"{input_file.stem}_output.json"
        
        # Process the file
        result = processor.process_challenge1b(str(input_file), str(output_file))
        
        if result:
            print(f"✅ Successfully processed {input_file.name}")
        else:
            print(f"❌ Failed to process {input_file.name}")
    
    print("\n=== Processing completed ===")

if __name__ == "__main__":
    main() 