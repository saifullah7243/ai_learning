### Creating the file
import json
example_qa_prompts = {
    "QA_Direct":{
        "user_template":"Context: {context}\n\nQuestion: {question}\n\nAnswer:"

    },
    "QA_RolePlay_Expert":{
         "system": "You are a world-renowned expert in the provided context domain.",
         "user_template": "Given your deep expertise and the following context: {context}\n\nAnswer this question: {question}"
    }
}

with open("my_qa_prompts.json","w") as f:
    json.dump(example_qa_prompts,f,indent=2)

## Function that loads the file
def load_and_print_specific_prompt(filepath,variant_name,field_to_print="user_template"):
    try:
        with open(filepath,"r") as f:
            prompts = json.load(f)

        if variant_name in prompts:
            if field_to_print in prompts[variant_name]:
                print(f"----{field_to_print} for {variant_name}--")
                print(prompts[variant_name][field_to_print])

            else:
                print("Field {field_to_print} not found in {filepath}")
        else:
            print(f"Variant '{variant_name}' not found in '{filepath}'.")

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{filepath}'.")


print(load_and_print_specific_prompt("my_qa_prompts.json", "QA_RolePlay_Expert"))
print(load_and_print_specific_prompt("my_qa_prompts.json", "QA_Direct"))