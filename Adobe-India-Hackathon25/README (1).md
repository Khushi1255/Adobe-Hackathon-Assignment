# Adobe India Hackathon 2025 - "Connecting the Dots" Challenge

## Welcome to the "Connecting the Dots" Challenge

### Rethink Reading. Rediscover Knowledge

What if every time you opened a PDF, it didn't just sit there—it spoke to you, connected ideas, and narrated meaning across your entire library?

That's the future we're building — and we want you to help shape it.

In the Connecting the Dots Challenge, our mission is to reimagine the humble PDF as an intelligent, interactive experience—one that understands structure, surfaces insights, and responds to you like a trusted research companion.

## What We Have Built

### Complete Round 1 Implementation

We have successfully implemented both phases of Round 1, creating a comprehensive PDF intelligence system that:

1. **Extracts structured outlines** from PDFs with blazing speed and pinpoint accuracy
2. **Provides on-device intelligence** that understands sections and links related ideas together
3. **Delivers persona-driven analysis** that adapts to user roles and specific tasks

### The Journey We've Completed

**Challenge 1a: PDF Structure Extraction**
- Built the foundation by extracting structured outlines from raw PDFs
- Implemented custom heading detection (H1, H2, H3) with multi-strategy classification
- Achieved sub-10-second processing for 50-page PDFs
- Created robust, schema-compliant JSON output

**Challenge 1b: Persona-Driven Document Intelligence**
- Powered up the system with on-device intelligence
- Implemented persona-driven content analysis and relevance scoring
- Created a generic solution that works across diverse domains
- Achieved ≤60-second processing for 3-5 documents

## Why This Matters

In a world flooded with documents, what wins is not more content — it's context. We've built tools that understand the future of how we read, learn, and connect. Our solutions demonstrate:

- **Intelligent Structure Recognition**: Understanding document hierarchy and organization
- **Context-Aware Analysis**: Adapting to user personas and specific job requirements
- **Performance Excellence**: Meeting strict time and resource constraints
- **Generic Architecture**: Working across diverse domains and use cases

## Challenge Solutions

### [Challenge 1a: PDF Structure Extraction](./Challenge_1a/README.md)
**Complete implementation** that extracts structured outlines from PDF documents with hierarchical headings (H1, H2, H3) and page numbers. Built on `pdfstructure` library with custom modifications for optimal performance and accuracy.

**Key Features:**
- Custom multi-strategy heading detection
- Multiple fallback title extraction strategies
- Sub-10-second processing for 50-page PDFs
- Schema-compliant JSON output
- AMD64, CPU-only, offline operation

### [Challenge 1b: Persona-Driven Document Intelligence](./Challenge_1b/README.md)
**Complete implementation** of an intelligent document analyst that extracts and prioritizes relevant sections from document collections based on specific personas and job-to-be-done requirements. Built on Secure-Offline-RAG-System with custom persona-driven analysis.

**Key Features:**
- Custom relevance scoring based on persona/job keywords
- Hybrid retrieval (BM25 + Vector search)
- Generic solution for diverse domains
- ≤60-second processing for 3-5 documents
- Fully offline operation with cached models

## Technical Excellence

### Performance Achievements
- **Challenge 1a**: ≤10 seconds for 50-page PDFs
- **Challenge 1b**: ≤60 seconds for 3-5 documents
- **Model Size**: Challenge 1a <50MB, Challenge 1b <1GB
- **Architecture**: AMD64, CPU-only, no internet access

### Innovation Highlights
- **Custom Heading Detection**: Multi-strategy classification outperforming generic solutions
- **Persona-Driven Scoring**: Unique relevance calculation based on user context
- **Hybrid Retrieval**: Combining keyword and semantic search effectively
- **Generic Architecture**: Adaptable to any domain without hardcoding

## Project Structure
```
Adobe-India-Hackathon25/
├── Challenge_1a/                    # PDF Structure Extraction
│   ├── process_pdfs.py             # Main entry point (191 lines)
│   ├── Dockerfile                  # AMD64, CPU-only container
│   ├── requirements.txt            # Minimal dependencies (3 packages)
│   ├── src/                       # Custom modules (746 lines total)
│   │   ├── heading_detector.py    # H1/H2/H3 classification
│   │   ├── title_extractor.py     # Title extraction
│   │   └── output_generator.py    # JSON output generation
│   └── test_output/               # Actual test results
└── Challenge_1b/                   # Persona-Driven Document Intelligence
    ├── process_challenge1b.py     # Main entry point (423 lines)
    ├── Dockerfile                 # AMD64, CPU-only with OCR support
    ├── requirements.txt           # RAG system dependencies (129 packages)
    ├── download_models.py         # Model downloader for offline operation
    ├── src/                      # RAG system modules
    │   ├── data/                 # Document loading
    │   ├── retrieval/            # Hybrid retrieval system
    │   ├── response/             # Response generation
    │   └── utils/                # Configuration
    └── Collection 1/             # Sample test cases
```

## Ready for Round 2

Our Round 1 implementation provides the perfect foundation for Round 2's webapp development. We have:

1. **Structured Data Foundation**: Challenge 1a provides the document structure and outline extraction
2. **Intelligent Content Analysis**: Challenge 1b provides persona-driven content understanding
3. **Performance-Optimized Backend**: Both solutions meet strict performance constraints
4. **API-Ready Architecture**: Clean, modular design ready for webapp integration

---

**Status**: Both Challenge 1a and Challenge 1b are **complete and ready for submission**. Our implementations fully satisfy all requirements and demonstrate technical excellence in PDF intelligence and document analysis.