# Challenge 1b: Testing and Validation Scripts

This folder contains all testing and validation scripts for Challenge 1b. Think of this as our quality assurance department - making sure our persona-driven document intelligence system works perfectly in every scenario.

## What We're Testing

Our testing strategy covers every aspect of the system to ensure it meets all requirements:

### 🎯 **Core Functionality Tests**
- Does the system understand different personas correctly?
- Can it extract relevant sections from diverse document types?
- Does the hybrid retrieval (BM25 + Vector) work effectively?
- Is the relevance scoring accurate and meaningful?

### ⚡ **Performance Tests**
- Can it process 3-5 documents within 60 seconds?
- Does it stay within the 1GB memory limit?
- Is it truly CPU-only (no GPU dependencies)?
- Does it work completely offline?

### 📋 **Compliance Tests**
- Does the output format match the required JSON schema?
- Are all input/output requirements satisfied?
- Does the Docker container build and run correctly?
- Is the architecture AMD64 compatible?

## Test Scripts

### Core Testing Scripts

#### `verify_requirements.py`
- **Purpose**: Comprehensive verification of all Challenge 1b requirements
- **Function**: Checks performance constraints, input/output format, architecture, functionality, and deployment requirements
- **Usage**: `python verify_requirements.py`
- **Output**: Detailed compliance report with pass/fail status

#### `test_cpu_setup.py`
- **Purpose**: Validates CPU-only environment setup
- **Function**: Checks for GPU dependencies, model sizes, and CPU compatibility
- **Usage**: `python test_cpu_setup.py`
- **Output**: CPU setup validation results

#### `test_setup.py`
- **Purpose**: Validates overall project setup and dependencies
- **Function**: Checks imports, configurations, and basic functionality
- **Usage**: `python test_setup.py`
- **Output**: Setup validation results

### Processing Tests

#### `test_processing.py`
- **Purpose**: Tests the main processing pipeline
- **Function**: Validates document processing, output generation, and performance
- **Usage**: `python test_processing.py`
- **Output**: Processing test results and performance metrics

#### `test_actual_processing.py`
- **Purpose**: Tests actual document processing with real data
- **Function**: Processes sample collections and validates outputs
- **Usage**: `python test_actual_processing.py`
- **Output**: Processing results and output validation

#### `test_simple.py`
- **Purpose**: Simple functionality tests
- **Function**: Basic component testing without full processing
- **Usage**: `python test_simple.py`
- **Output**: Basic functionality test results

### Validation Scripts

#### `validate_outputs.py`
- **Purpose**: Validates output format and content
- **Function**: Checks JSON schema compliance and content quality
- **Usage**: `python validate_outputs.py`
- **Output**: Output validation results

#### `test_docker_structure.py`
- **Purpose**: Validates Docker container structure
- **Function**: Checks Dockerfile, dependencies, and container setup
- **Usage**: `python test_docker_structure.py`
- **Output**: Docker structure validation results

## Test Directories

### `test_input/`
- Contains test input files for validation
- Sample JSON files for testing different scenarios
- Various persona and job combinations

### `test_output/`
- Contains test output files
- Generated results from test runs
- Expected vs actual output comparison

## Running Tests

### Individual Tests
```bash
cd tests
python verify_requirements.py
python test_cpu_setup.py
python test_processing.py
```

### All Tests (if available)
```bash
cd tests
python -m pytest  # If pytest is configured
```

## Test Categories

### 1. Requirements Verification
- Performance constraints (≤60s, ≤1GB, CPU-only)
- Input/output format compliance
- Architecture requirements
- Functional requirements

### 2. Setup Validation
- CPU-only environment
- Dependencies installation
- Configuration validation
- Import testing

### 3. Processing Tests
- Document loading
- Content extraction
- Output generation
- Performance metrics

### 4. Output Validation
- JSON schema compliance
- Content quality
- Format verification
- Error handling

### 5. Docker Tests
- Container structure
- Build validation
- Runtime testing
- Volume mounting

## Expected Results

All tests should pass with:
- ✅ Performance constraints met
- ✅ Format compliance verified
- ✅ Functionality working correctly
- ✅ Error handling robust
- ✅ Output quality high

## Troubleshooting

If tests fail:
1. Check dependencies: `pip install -r requirements.txt`
2. Verify CPU-only setup
3. Check Docker build
4. Validate input files
5. Review error logs

## Notes

- All tests are designed for CPU-only operation
- Tests run offline (no internet required)
- Output validation includes schema compliance
- Performance tests respect 60-second limit 