import json
from jsonschema import validate, ValidationError

user_profile_schema = {
    "type ":"object",
    "properties":{
    "name": {"type":"string", "minLength":1},
    "email":{"type":"string", "format":"email"},
    "age":{"type":"integer","minimum":19}
    },
    "required":["name","email","age"]
}

def validate_user_profile(profile_json_string:str, schema:dict)->bool:
    try:
        profile_data = json.loads(profile_json_string)
        validate(instance=profile_data, schema=schema)
        print(f"Profile {profile_json_string} is VALID")
        return True
    except json.JSONDecodeError:
        print(f"Profile {profile_json_string} is NOT VALID JSON")
        return False
    except ValidationError as e:
        print(f"Profile {profile_json_string} FAILED SCHEMA VALIDATION: {e.message}")
        return False
    
## Test Case
valid_profile_str = '{"name": "Alice Wonderland", "email": "alice@example.com", "age": 30}' 
invalid_profile_str_bad_email = '{"name": "Bob The Builder", "email": "bob@com", "age": 25}' # Bad email format 
invalid_profile_str_young_age = '{"name": "Charlie Brown", "email": "charlie@example.com", "age": 18}' # Age too young   
invalid_profile_str_missing_field = '{"name": "Diana Prince", "email": "diana@example.com"}' # Missing age

print("---- Testing User Profile Validation -----")
validate_user_profile(valid_profile_str, user_profile_schema) 
validate_user_profile(invalid_profile_str_bad_email, user_profile_schema) 
validate_user_profile(invalid_profile_str_young_age, user_profile_schema) 
validate_user_profile(invalid_profile_str_missing_field, user_profile_schema) 