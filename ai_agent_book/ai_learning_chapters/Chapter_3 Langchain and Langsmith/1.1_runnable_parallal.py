import sys
import os

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter


# Load API key
config = load_config()
openai_key = config.openai_key

# LangChain setup
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

question_prompt = ChatPromptTemplate.from_template("Generate a concise question about {topic}.")
facts_prompt = ChatPromptTemplate.from_template("List two brief, important facts about {topic}.")

parallel_chain = RunnableParallel(
    question= itemgetter("q_topic")|question_prompt | llm,
    facts=itemgetter("f_topic")|facts_prompt | llm
)

result = parallel_chain.invoke({
    "q_topic": "AI Safety",
    "f_topic":"Ethical Concern"
    })

cleaned_result = {key: value.content for key, value in result.items()}

print(cleaned_result)
