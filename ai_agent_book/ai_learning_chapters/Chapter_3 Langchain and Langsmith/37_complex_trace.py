import sys
import os
import asyncio
from dotenv import load_dotenv

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

async def run_complex_chain():
    # 1 MODEL
     model = ChatOpenAI(
          model="gpt-4.1-nano",
          temperature=0.1,
          max_tokens=1024
     )

     # 2 PROMPT for sentiment analysis
     sentiment_prompt = ChatPromptTemplate.from_template(
             "Analyze the sentiment of the following email. Respond with a single word: Positive, Negative, or Neutral.\n\nEmail: {email_text}"
     )

     # 3 PROMPT for summarization
     summary_prompt = ChatPromptTemplate.from_template(
             "Summarize the following email in a single, concise sentence.\n\nEmail: {email_text}"
     )
     
     # subchain for sentiment analysis
     sentiment_chain = sentiment_prompt | model | StrOutputParser()

     # subchain for summarization
     summary_chain = summary_prompt | model | StrOutputParser()

     # The main chain that runs both subchains in parallel
     main_chain = RunnableParallel(
          sentiment = RunnablePassthrough.assign(email_text=lambda x:x["email_text"]) | sentiment_chain,
          summary = RunnablePassthrough.assign(email_text=lambda x:x["email_text"]) | summary_chain
     )

     ## test input
     email_content = "Hi team, I just wanted to say thank you for all the hard work on the recent launch. The results have been phenomenal and I'm so proud of what we've accomplished together. Let's keep up the great momentum!"

     ## invoking chaing
     print("Running complex chain...")
     response = await main_chain.ainvoke({"email_text": email_content})
     print("Chain response:", response)

if __name__ == "__main__":
    asyncio.run(run_complex_chain())