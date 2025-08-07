from langchain import hub

# Pull a prompt from LangSmith Hub
prompt = hub.pull("hardkothari/prompt-maker")

# now we can use the prompt in our code
chain = prompt | model | StrOutputParser()

