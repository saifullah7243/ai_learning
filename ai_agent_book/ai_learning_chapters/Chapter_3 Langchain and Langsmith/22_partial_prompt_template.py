from langchain_core.prompts import PromptTemplate

# Create a prompt template with 3 variables
template = PromptTemplate.from_template(
    "Generate a report for {company} in the {quarter} of {year}."
)

# Let's say we always want to generate reports for the current year (2025)
partial_template = template.partial(year="2025")

# Print input variables before and after applying .partial()
print("Original variables:", template.input_variables)         # ['company', 'quarter', 'year']
print("Partial variables:", partial_template.input_variables)  # ['company', 'quarter']

# Format the new template with the remaining variables
formatted_output = partial_template.format(company="QuantumLeap Inc.", quarter="Q2")
print(formatted_output)
