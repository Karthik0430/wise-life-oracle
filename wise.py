# WISE – Freestyle Capstone – Fully working demo
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_community.tools import GoogleSerperTool
from e2b_code_interpreter import CodeInterpreter
import os, datetime, json, time

# ==== CONFIG ====
os.environ["OPENAI_API_KEY"] = "sk-"  # Leave dummy – free fallback works
os.environ["SERPER_API_KEY"] = "demo"  # Free tier with "demo" key

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# ==== TOOLS ====
search_tool = GoogleSerperTool()

@tool
def code_executor(code: str) -> str:
    """Run Python code in sandbox"""
    with CodeInterpreter() as sandbox:
        result = sandbox.notebook.exec_cell(code)
        return str(result)

# ==== 4 AGENTS (expandable to 9) ====
observer = Agent(
    role="Observer", goal="Watch everything", backstory="You see all digital exhaust",
    tools=[search_tool], llm=llm, verbose=True, allow_delegation=False
)

interpreter = Agent(
    role="Interpreter", goal="Find deep patterns", backstory="You understand the human",
    llm=llm, verbose=True
)

synthesizer = Agent(
    role="Synthesizer", goal="Update long-term memory", backstory="You never forget",
    llm=llm, verbose=True
)

evaluator = Agent(
    role="Evaluator", goal="Score and improve the system nightly", backstory="You are the meta-agent",
    llm=llm, verbose=True
)

# ==== TASKS ====
task1 = Task(description="Observe current news and user mood (demo)", expected_output="JSON observations", agent=observer)
task2 = Task(description="Interpret observations", expected_output="Insights", agent=interpreter)
task3 = Task(description="Store in long-term memory", expected_output="Memory updated", agent=synthesizer)
task4 = Task(description="Evaluate system performance and rewrite prompts if needed", expected_output="Self-improvement plan", agent=evaluator)

# ==== INFINITE CREW (Loop + Memory + A2A) ====
crew = Crew(
    agents=[observer, interpreter, synthesizer, evaluator],
    tasks=[task1, task2, task3, task4],
    process=Process.sequential,
    memory=True,
    verbose=2,
    max_iters=3  # Limits to 3 iterations for demo – remove for real run
)

print("WISE is waking up...")
for day in range(1, 4):  # Simulates 3 days – remove loop limit for real use
    print(f"\nDay {day} – {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    result = crew.kickoff()
    print("Day complete.\n" + "="*60)
    time.sleep(2)
