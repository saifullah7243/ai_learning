import tiktoken

def count_tokens(text: str, model_name: str = "gpt-4o-mini") -> int:
    """
    Returns the number of tokens in a text string for a given model.
    """
    try:
        # Use encoding specific to the model (safe for most OpenAI models)
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        print(f"Warning: Model '{model_name}' not found in tiktoken. Using 'cl100k_base' as fallback.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = len(encoding.encode(text))
    return num_tokens

# Example usage:
my_prompt_text = "What is AI in healthcare, Education and Software domain. Write its pros and cons"
token_count = count_tokens(my_prompt_text)
print(f"The text '{my_prompt_text}' has approximately {token_count} tokens for gpt-4o-mini.")


