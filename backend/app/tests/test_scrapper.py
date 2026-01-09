# Import your scraper function
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from scraper.mal_scraper import get_manhwa_list
# from  import get_manhwa_list  # Replace with actual filename
    

def validate_manhwa_data(batch_data, expected_schema):
    """
    Validates that each item in the batch matches the expected schema.
    
    Args:
        batch_data: List of dicts from get_manhwa_list
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
    
    # Expected field names
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
        
        # Check if item is a dict
        if not isinstance(item, dict):
            item_result["valid"] = False
            item_result["error"] = f"Item is not a dict, got {type(item).__name__}"
            results["valid"] = False
            results["errors"].append(item_result)
            continue
        
        # Check if dict has all required fields
        missing_fields = [field for field in field_names if field not in item]
        if missing_fields:
            item_result["valid"] = False
            item_result["error"] = f"Missing fields: {missing_fields}"
            results["valid"] = False
            results["errors"].append(item_result)
            continue
        
        # Validate each field
        for field_name in field_names:
            field_value = item[field_name]
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
    
    print("\n"+"=" * 80)
    print("MANHWA SCRAPER VALIDATION TEST")
    print("=" * 80)
    

    # Run the scraper
    print("\tFetching data from scraper...")
    
    batch_count = 0
    for batch in get_manhwa_list(test_phase=True, result_lazy_limit=1):
        batch_count += 1
        print(f"\nValidating batch {batch_count}...")
        
        # Validate the batch
        validation_result = validate_manhwa_data(batch, expected_schema)
        
        # Print results
        if validation_result["valid"]:
            print(f"\tVALIDATION PASSED")
            print(f"\tTotal items validated: {validation_result['total_items']}")
            print(f"\tAll fields match expected schema")
        else:
            print(f"❌ VALIDATION FAILED")
            print(f"   Total items: {validation_result['total_items']}")
            print(f"   Valid items: {len(validation_result['items_validated'])}")
            print(f"   Invalid items: {len(validation_result['errors'])}")
        
        # Always print types for debugging
        item = batch[0]
        
        def truncate(value, length=10):
            s = str(value)
            return s[:length] + "..." if len(s) > length else s
        
        print(f"""
                rank: {type(item['rank']).__name__}, sample: {truncate(item['rank'])}
                title: {type(item['title']).__name__}, sample: {truncate(item['title'])}
                synopsis: {type(item['synopsis']).__name__}, sample: {truncate(item['synopsis'])}
                cover_image_url: {type(item['cover_image_url']).__name__}, sample: {truncate(item['cover_image_url'])}
                rating: {type(item['rating']).__name__}, sample: {truncate(item['rating'])}
                chapters: {type(item['chapters']).__name__}, sample: {truncate(item['chapters'])}
                published_date: {type(item['published_date']).__name__}, sample: {truncate(item['published_date'])}
                tags: {type(item['tags']).__name__}, sample: {item['tags']}
                link: {type(item['link']).__name__}, sample: {truncate(item['link'])}
        """)
        

        
        # Show detailed errors
        if not validation_result["valid"]:
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
    
    print(f"\nTest completed. Processed {batch_count} batch(es)")


if __name__ == "__main__":
    test_manhwa_scraper()