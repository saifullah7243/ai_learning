from langchain_core.prompts import PromptTemplate

#Define a prompt template with single input topic
template_string = "Write a one sentence, witty summary of the following topic:{topic}"
llm_prompt_template = PromptTemplate.from_template(template_string)

# We can inspect its input variables
print(f"Input variables: {llm_prompt_template.input_variables}") 

# Format the prompt with an input value 
formatted_prompt = llm_prompt_template.format(topic="Quantum Physics") 
print(formatted_prompt) 