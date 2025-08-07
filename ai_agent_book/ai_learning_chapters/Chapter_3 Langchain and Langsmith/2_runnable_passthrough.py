import sys
import os

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



# Load API key
config = load_config()
openai_key = config.openai_key

# LangChain setup
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
str_output = StrOutputParser()

question_chain = (
    ChatPromptTemplate.from_template("Generate a concise question about {topic}.") | llm | str_output
    )

facts_chain = (
    ChatPromptTemplate.from_template("List two brief, important facts about {topic}.") | llm | str_output
    )

combined_chain = RunnablePassthrough.assign(
    generated_question=question_chain,
    generated_facts=facts_chain
)

# initial_input = "What is ai"
# result = combined_chain.invoke({"topic":initial_input})
# print(result)

final_prompt = ChatPromptTemplate.from_template(
    "Original Topic: {topic}\n\n"
    "Generated Question: {generated_question}\n\n"
    "Generated Facts: {generated_facts}\n\n"
    "Provide a one-sentence synthesis of this information."
)

full_synthesis_chain = combined_chain | final_prompt | llm | str_output


topic_input = {"topic": "CRISPR gene editing"}
result = full_synthesis_chain.invoke(topic_input)

print("🔍 Final Synthesis:\n", result)
