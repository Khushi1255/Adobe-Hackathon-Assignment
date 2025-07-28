#!/usr/bin/env python3
"""
Validate all Challenge 1b outputs for schema compliance and problem statement requirements.
"""
import os
import json
from pathlib import Path
import sys

def load_schema(schema_path):
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_json_schema(data, schema):
    try:
        import jsonschema
        jsonschema.validate(instance=data, schema=schema)
        return True, ""
    except ImportError:
        return False, "jsonschema not installed. Install with: pip install jsonschema"
    except jsonschema.ValidationError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def check_required_fields(data, required_fields):
    missing = [field for field in required_fields if field not in data]
    return missing

def check_persona_job(input_data, output_data):
    # Check if persona/job is reflected in output (basic check)
    persona = input_data.get('persona', {}).get('role', '').lower()
    job = input_data.get('job_to_be_done', {}).get('task', '').lower()
    output_text = json.dumps(output_data).lower()
    persona_ok = persona in output_text if persona else True
    job_ok = job in output_text if job else True
    return persona_ok, job_ok

def main():
    base_dir = Path(__file__).parent
    schema_path = base_dir / 'sample_dataset' / 'schema' / 'output_schema.json'
    collections = [f'Collection {i}' for i in range(1, 4)]
    required_fields = ['metadata', 'extracted_sections', 'subsection_analysis']
    
    # Load schema
    if not schema_path.exists():
        print(f"❌ Schema file not found: {schema_path}")
        sys.exit(1)
    schema = load_schema(schema_path)
    
    all_passed = True
    for collection in collections:
        print(f"\n=== Validating {collection} ===")
        input_file = base_dir / collection / 'challenge1b_input.json'
        output_file = base_dir / collection / 'challenge1b_output.json'
        
        if not input_file.exists():
            print(f"❌ Input file missing: {input_file}")
            all_passed = False
            continue
        if not output_file.exists():
            print(f"❌ Output file missing: {output_file}")
            all_passed = False
            continue
        
        with open(input_file, 'r') as f:
            input_data = json.load(f)
        with open(output_file, 'r') as f:
            output_data = json.load(f)
        
        # Check required fields
        missing = check_required_fields(output_data, required_fields)
        if missing:
            print(f"❌ Missing required fields: {missing}")
            all_passed = False
        else:
            print(f"✅ All required fields present")
        
        # Schema validation
        valid, msg = validate_json_schema(output_data, schema)
        if valid:
            print(f"✅ Schema validation passed")
        else:
            print(f"❌ Schema validation failed: {msg}")
            all_passed = False
        
        # Persona/job check
        persona_ok, job_ok = check_persona_job(input_data, output_data)
        if persona_ok:
            print(f"✅ Persona reflected in output")
        else:
            print(f"❌ Persona not found in output")
            all_passed = False
        if job_ok:
            print(f"✅ Job-to-be-done reflected in output")
        else:
            print(f"❌ Job-to-be-done not found in output")
            all_passed = False
    
    print("\n====================================")
    if all_passed:
        print("🎉 All outputs are valid and fulfill the problem statement requirements!")
    else:
        print("❌ Some outputs failed validation. Please review the above messages.")

if __name__ == "__main__":
    main() 