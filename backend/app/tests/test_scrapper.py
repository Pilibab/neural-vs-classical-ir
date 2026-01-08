# Import your scraper function
from scraper.mal_scraper import get_manhwa_list
# from  import get_manhwa_list  # Replace with actual filename
    

def validate_manhwa_data(batch_data, expected_schema):
    """
    Validates that each item in the batch matches the expected schema.
    
    Args:
        batch_data: List of tuples from get_manhwa_list
        expected_schema: Dictionary with field names as keys and expected types as values
    
    Returns:
        dict with validation results
    """
    if not isinstance(batch_data, list):
        return {
            "valid": False,
            "error": "batch_data is not a list",
            "batch_data_type": type(batch_data).__name__
        }
    
    if len(batch_data) == 0:
        return {
            "valid": False,
            "error": "batch_data is empty"
        }
    
    results = {
        "valid": True,
        "total_items": len(batch_data),
        "items_validated": [],
        "errors": []
    }
    
    # Expected field names in order
    field_names = [
        "rank",
        "title", 
        "synopsis",
        "cover_image_url",
        "rating",
        "chapters",
        "published_date",
        "tags",
        "link"
    ]
    
    for idx, item in enumerate(batch_data):
        item_result = {
            "index": idx,
            "valid": True,
            "field_errors": []
        }
        
        # Check if item is a tuple
        if not isinstance(item, tuple):
            item_result["valid"] = False
            item_result["error"] = f"Item is not a tuple, got {type(item).__name__}"
            results["valid"] = False
            results["errors"].append(item_result)
            continue
        
        # Check if tuple has correct number of fields
        if len(item) != len(field_names):
            item_result["valid"] = False
            item_result["error"] = f"Expected {len(field_names)} fields, got {len(item)}"
            results["valid"] = False
            results["errors"].append(item_result)
            continue
        
        # Validate each field
        for field_idx, (field_name, field_value) in enumerate(zip(field_names, item)):
            expected_types = expected_schema[field_name]
            
            # Check if value matches any of the expected types
            type_match = False
            actual_type = type(field_value).__name__
            
            for expected_type in expected_types:
                if isinstance(field_value, expected_type):
                    type_match = True
                    break
            
            if not type_match:
                expected_type_names = " | ".join([t.__name__ for t in expected_types])
                item_result["field_errors"].append({
                    "field": field_name,
                    "expected_types": expected_type_names,
                    "actual_type": actual_type,
                    "value": str(field_value)[:100]  # Limit value length for readability
                })
                item_result["valid"] = False
                results["valid"] = False
        
        if item_result["valid"]:
            results["items_validated"].append(idx)
        else:
            results["errors"].append(item_result)
    
    return results


def test_manhwa_scraper():
    """
    Test function to validate manhwa scraper output
    """
    # Define expected schema
    expected_schema = {
        "rank": [int, str],
        "title": [str],
        "synopsis": [str],
        "cover_image_url": [str],
        "rating": [float, str],
        "chapters": [str, int],
        "published_date": [str],
        "tags": [str],
        "link": [str]
    }
    
    print("=" * 80)
    print("MANHWA SCRAPER VALIDATION TEST")
    print("=" * 80)
    

    # Run the scraper
    print("\n📥 Fetching data from scraper...")
    
    batch_count = 0
    for batch in get_manhwa_list(test_phase=True, result_lazy_limit=1):
        batch_count += 1
        print(f"\n🔍 Validating batch {batch_count}...")
        
        # Validate the batch
        validation_result = validate_manhwa_data(batch, expected_schema)
        
        # Print results
        if validation_result["valid"]:
            print(f"✅ VALIDATION PASSED")
            print(f"   Total items validated: {validation_result['total_items']}")
            print(f"   All fields match expected schema")
        else:
            print(f"❌ VALIDATION FAILED")
            print(f"   Total items: {validation_result['total_items']}")
            print(f"   Valid items: {len(validation_result['items_validated'])}")
            print(f"   Invalid items: {len(validation_result['errors'])}")
            
            # Show detailed errors
            for error in validation_result['errors']:
                print(f"\n   Item {error['index']}:")
                if 'error' in error:
                    print(f"      Error: {error['error']}")
                if 'field_errors' in error:
                    for field_error in error['field_errors']:
                        print(f"      ❌ Field '{field_error['field']}':")
                        print(f"         Expected: {field_error['expected_types']}")
                        print(f"         Got: {field_error['actual_type']}")
                        if len(field_error['value']) < 100:
                            print(f"         Value: {field_error['value']}")
        
        print("\n" + "=" * 80)
    
    print(f"\n✨ Test completed. Processed {batch_count} batch(es)")


if __name__ == "__main__":
    test_manhwa_scraper()