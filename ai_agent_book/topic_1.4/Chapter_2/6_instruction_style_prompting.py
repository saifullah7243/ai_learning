import sys
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# Rich console setup
console = Console()

# Load environment variables (optional but safe practice)
load_dotenv()

# Go 3 levels up from this file to reach ai_agent_course/
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_path)

# Now import from llm/config.py at root
from llm.config import openai_key

# Setup OpenAI client
client = AsyncOpenAI(api_key=openai_key)

messages_instruction_style = [ 
{ 
"role": "system", 
"content": "You are 'SummaryBot', an AI skilled in extracting key information and summarizing technical documents for a non-technical audience. Your summaries should be concise, in bullet points, and under 150 words." 
}, 
{ 
"role": "user", 
"content": """ 
Please summarize the following research paper abstract. 
Focus on the main objective, method, and key findings. 
Abstract Title: "The Impact of Quantum Entanglement on Data Transmission Speeds" 
Abstract Text: 
"Recent advancements in quantum physics have opened new avenues for revolutionizing data 
communication. This paper investigates the potential of leveraging quantum entanglement to 
achieve faster-than-light (FTL) data transmission, a concept previously confined to theoretical 
speculation. We propose a novel experimental setup involving entangled particle pairs 
generated via spontaneous parametric down-conversion. One particle of each pair is modulated 
based on the input data stream, while its entangled counterpart, located at a distant receiver, 
instantaneously reflects this modulation. Our preliminary results indicate a statistically significant 
correlation in state changes across distances up to 10 kilometers, with transmission latencies 
independent of this distance. While challenges related to decoherence and scalable particle 
generation persist, these findings suggest a foundational step towards practical FTL 
communication systems, potentially transforming global networking and deep-space 
communication." 
Ensure your summary is clear and avoids heavy jargon. 
""" 
} 
] 

async def main():
    response = await client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages_instruction_style,
        temperature=0.3
    )
    console.print(Markdown(response.choices[0].message.content))

# Run the async function
asyncio.run(main())