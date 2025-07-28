# Challenge 1b: Persona-Driven Document Intelligence

## Overview
This is a **complete implementation** for Challenge 1b of the Adobe India Hackathon 2025. The solution implements an intelligent document analyst that extracts and prioritizes relevant sections from a collection of documents based on a specific persona and their job-to-be-done. Built on the Secure-Offline-RAG-System with custom modifications for persona-driven analysis.

## The Problem We Solved

Imagine you're a travel planner with 7 different travel guides about the South of France, and a client asks you to plan a 4-day trip for 10 college friends. How do you quickly find the most relevant information across all those documents?

Or imagine you're an HR professional with 15 Adobe Acrobat guides, and you need to create fillable forms for onboarding. How do you extract just the relevant sections from all those technical documents?

Our challenge was to build a system that could:

1. **Understand user context** - Who is the user and what are they trying to accomplish?
2. **Analyze multiple documents** - Process 3-10 related PDFs efficiently
3. **Extract relevant sections** - Find the most important information for the specific task
4. **Prioritize content** - Rank sections by importance and relevance
5. **Work completely offline** - No internet dependencies during processing

## How Our Solution Works

### The Magic Behind Persona-Driven Intelligence

Our system doesn't just search for keywords - it understands context and user intent:

#### 1. **Keyword Extraction** (Understanding the User)
```python
def _extract_keywords(self, persona: str, job_to_be_done: str) -> List[str]:
    """
    Extract meaningful keywords from persona and job description
    """
    text = f"{persona} {job_to_be_done}"
    # Remove stopwords and common terms
    # Create focused keyword set for targeted retrieval
    return keywords
```

**Example**: For a "Travel Planner" planning a "4-day trip for 10 college friends", we extract keywords like: `["travel", "planner", "trip", "college", "friends", "planning", "itinerary"]`

#### 2. **Custom Relevance Scoring** (The Smart Ranking)
```python
def _custom_relevance_score(self, chunk_text: str, keywords: List[str]) -> float:
    """
    Compute relevance score using keyword overlap and TF-IDF similarity
    """
    # Keyword overlap: Direct matches in document sections
    overlap = len(chunk_words.intersection(keywords)) / len(keywords)
    
    # TF-IDF cosine similarity: Semantic similarity
    cosine = compute_semantic_similarity(chunk_text, keywords)
    
    # Weighted combination (50/50 weight)
    return 0.5 * overlap + 0.5 * cosine
```

#### 3. **Persona-Driven Query Generation** (Multiple Perspectives)
```python
def _generate_persona_queries(self, persona: str, job_to_be_done: str) -> List[str]:
    """
    Generate multiple queries covering different aspects of the task
    """
    queries = [
        f"{persona} {job_to_be_done}",
        f"requirements for {job_to_be_done}",
        f"best practices for {persona}",
        f"step-by-step {job_to_be_done}"
    ]
    return queries
```

### Hybrid Retrieval: The Best of Both Worlds

We combine two powerful search approaches:

#### **BM25 Retriever** (The Keyword Detective)
- Finds exact keyword matches
- Great for technical terms and specific concepts
- Fast and efficient for direct matches

#### **Vector Retriever** (The Semantic Detective)
- Understands meaning and context
- Finds related concepts even without exact keyword matches
- Uses sentence transformers for semantic similarity

#### **Result Fusion** (The Smart Combiner)
```python
def retrieve(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
    """
    Combine BM25 and vector results with custom scoring
    """
    bm25_results = self.bm25_retriever.retrieve(query, top_k)
    vector_results = self.vector_retriever.retrieve(query, top_k)
    
    # Combine and re-rank using custom persona-driven scoring
    combined_results = self._combine_results(bm25_results, vector_results)
    return combined_results
```

## Implementation Details

### Core Processing Pipeline

```python
class Challenge1BProcessor:
    def __init__(self):
        self.config = Config()
        self.document_loader = DocumentLoader(self.config.to_dict())
        self.retriever = HybridRetriever(self.config)
        self.response_generator = MockResponseGenerator(self.config)
        self.max_processing_time = 60  # seconds
```

### Custom Relevance Scoring Strategy

Our system implements sophisticated relevance calculation:

```python
def _custom_relevance_score(self, chunk_text: str, keywords: List[str]) -> float:
    """
    Compute a custom relevance score for a chunk based on keyword overlap 
    and TF-IDF cosine similarity.
    """
    if not keywords:
        return 0.0
    
    # Keyword overlap calculation
    chunk_words = set(re.sub(r'[^a-zA-Z0-9 ]', ' ', chunk_text.lower()).split())
    overlap = len(chunk_words.intersection(keywords)) / (len(keywords) + 1e-6)
    
    # TF-IDF cosine similarity
    try:
        tfidf = TfidfVectorizer().fit([chunk_text, ' '.join(keywords)])
        vecs = tfidf.transform([chunk_text, ' '.join(keywords)]).toarray()
        cosine = np.dot(vecs[0], vecs[1]) / (np.linalg.norm(vecs[0]) * np.linalg.norm(vecs[1]) + 1e-6)
    except Exception:
        cosine = 0.0
    
    # Weighted combination (50/50 weight)
    return 0.5 * overlap + 0.5 * cosine
```

### Error Handling and Robustness

We've built a system that never fails completely:

- **Graceful degradation**: If retrieval fails, we provide fallback output
- **Schema compliance**: All outputs conform to the required JSON structure
- **Timeout protection**: Processing stops if it exceeds 60 seconds
- **Memory protection**: Efficient memory usage prevents crashes

## Project Structure
```
Challenge_1b/
├── process_challenge1b.py         # Main processing script (423 lines)
├── download_models.py             # Model downloader for offline operation
├── Dockerfile                    # AMD64, CPU-only container
├── requirements.txt              # RAG system dependencies (129 packages)
├── src/                         # RAG system modules
│   ├── data/                   # Document loading and processing
│   ├── retrieval/              # Hybrid retrieval system
│   │   ├── hybrid_retriever.py # BM25 + Vector fusion
│   │   ├── bm25_retriever.py   # Keyword-based search
│   │   └── vector_retriever.py # Semantic search
│   ├── response/               # Response generation
│   └── utils/                  # Configuration and utilities
├── Collection 1/               # Travel Planning test case
├── Collection 2/               # Adobe Acrobat Learning test case
├── Collection 3/               # Recipe Collection test case
└── README.md                   # This file
```

## Results and Performance

### Test Collections Analysis
Our implementation has been tested with three diverse collections:

#### **Collection 1: Travel Planning**
- **Persona**: Travel Planner
- **Task**: Plan a 4-day trip for 10 college friends to South of France
- **Documents**: 7 travel guides (South of France - Cities, Cuisine, History, etc.)
- **Results**: Successfully extracted relevant sections with importance ranking
- **Performance**: Processed within 60-second limit

#### **Collection 2: Adobe Acrobat Learning**
- **Persona**: HR Professional
- **Task**: Create and manage fillable forms for onboarding and compliance
- **Documents**: 15 Acrobat guides (Create and Convert, Edit, Export, etc.)
- **Results**: Extracted relevant form creation and management sections
- **Performance**: Efficient processing of technical documentation

#### **Collection 3: Recipe Collection**
- **Persona**: Food Contractor
- **Task**: Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents**: 9 cooking guides (Breakfast, Dinner Mains, Sides, etc.)
- **Results**: Identified relevant vegetarian and buffet-style recipes
- **Performance**: Successfully processed culinary content

### Key Achievements
1. **Generic Solution**: Works across diverse domains (travel, technical, culinary)
2. **Persona-Driven**: Custom scoring adapts to different user roles and tasks
3. **Performance**: ≤60 seconds processing for 3-5 documents
4. **Accuracy**: Relevant section extraction with proper importance ranking
5. **Robustness**: Handles various document types and formats

## Input/Output Format

### Input JSON Structure
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [{"filename": "doc.pdf", "title": "Title"}],
  "persona": {"role": "User Persona"},
  "job_to_be_done": {"task": "Use case description"}
}
```

### Output JSON Structure
```json
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description",
    "processing_timestamp": "2025-01-XX..."
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

## Installation & Usage

### Docker Build
```bash
docker build --platform linux/amd64 -t challenge1b-persona-rag .
```

### Docker Run
```bash
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  challenge1b-persona-rag
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Download models (first time only)
python download_models.py

# Run with sample data
python process_challenge1b.py
```

## Why This Approach Works

### Benefits of Our Approach

1. **Persona-Driven**: Custom scoring based on user role and task requirements
2. **Generic Architecture**: Adaptable to any domain or persona without hardcoding
3. **Hybrid Retrieval**: Combines strengths of keyword and semantic search
4. **Offline Operation**: No internet dependencies during runtime
5. **Performance Optimized**: Meets all time and resource constraints

### Technical Advantages
- **Custom Scoring**: Unique relevance calculation based on persona/job keywords
- **Generic Solution**: No domain-specific or persona-specific hardcoding
- **Robust Architecture**: Graceful error handling and fallback mechanisms
- **Scalable Design**: Efficient processing of multiple documents

## Conclusion

Our Challenge 1b implementation successfully demonstrates:

1. **Persona-Driven Intelligence**: Custom relevance scoring based on user roles and tasks
2. **Generic Architecture**: Adaptable to any domain without hardcoding
3. **Hybrid Retrieval**: Combines keyword and semantic search effectively
4. **Performance Excellence**: ≤60 seconds processing for multiple documents
5. **Offline Operation**: Fully self-contained with cached models

The solution provides intelligent document analysis capabilities that understand context and user intent, making it a powerful tool for knowledge discovery and content prioritization.

---
