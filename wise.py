# WISE – Freestyle Capstone – 100% Google Gemini powered
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import datetime
import time

# === PUT YOUR GOOGLE AI STUDIO KEY HERE (or in .env file) ===
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "YOUR_AI_STUDIO_KEY_HERE"  # ← paste here

# Choose model: gemini-1.5-flash (fast & free) or gemini-1.5-pro (1M context)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",        # change to "gemini-1.5-pro" if you want the beast
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3,
    convert_system_message_to_human=True
)

# === TOOLS (all free) ===
search_tool = DuckDuckGoSearchRun()

def analyze_image(image_path_or_url: str) -> str:
    """Multimodal tool – WISE can literally see your screenshots"""
    message = HumanMessage(content=[
        {"type": "text", "text": "Describe everything in this image and extract personal insights about the user."},
        {"type": "image_url", "image_url": image_path_or_url},
    ])
    return llm.invoke([message]).content

# === 4 CORE AGENTS (easily expandable to 9) ===
observer = Agent(
    role="Observer", goal="Watch everything the user does", backstory="You see every pixel and word",
    tools=[search_tool, analyze_image], llm=llm, verbose=True
)

interpreter = Agent(
    role="Interpreter", goal="Find deep life patterns", backstory="You understand the human soul",
    llm=llm, verbose=True
)

synthesizer = Agent(
    role="Synthesizer", goal="Build and compress long-term memory", backstory="You never forget",
    llm=llm, verbose=True
)

evaluator = Agent(
    role="Evaluator", goal="Nightly self-improvement & prompt rewriting", backstory="You are the meta-mind",
    llm=llm, verbose=True
)

# === TASKS ===
task1 = Task(description="Observe something interesting today (demo: search recent news + analyze a sample image)", 
             expected_output="Rich observations", agent=observer)
task2 = Task(description="Interpret the observations deeply", expected_output="Life insights", agent=interpreter)
task3 = Task(description="Compress and store in long-term memory", expected_output="Memory updated", agent=synthesizer)
task4 = Task(description="Evaluate system and suggest prompt improvements", expected_output="Self-upgrade plan", agent=evaluator)

# === INFINITE CREW – demonstrates loop, memory, A2A, observability ===
crew = Crew(
    agents=[observer, interpreter, synthesizer, evaluator],
    tasks=[task1, task2, task3, task4],
    process=Process.sequential,
    memory=True,
    verbose=2,
    max_iters=3  # Remove this line to run forever
)

# === START WISE ===
print("WISE is now alive – powered by Google Gemini")
for day in range(1, 4):
    print(f"\n=== Day {day} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    result = crew.kickoff()
    print("Day complete\n" + "═"*70)
    time.sleep(2)

print("WISE demo finished – remove max_iters to run infinitely")
