from crewai import Agent, Task, LLM, Crew, Process


# Example of Defining an Agent in CrewAI
researcher = Agent(
    role="Senior Data Researcher",
    goal="Uncover cutting-edge developments in AI",
    backstory="A seasoned researcher with a knack for uncovering the latest developments in AI.",
    tools=[SerperDevTool()],
    verbose=True
)

# Example of Defining a Task in CrewAI
research_task = Task(
    description="Conduct comprehensive research on the latest AI developments.",
    expected_output="A summary report highlighting key advancements in AI.",
    agent=researcher_agent,
    tools=[search_tool],
    async_execution=True
)


# Connecting to an OpenAI-compatible LLM
openai_llm = LLM(
    model="gpt-4",
    api_key="your-openai-api-key",
    api_base="https://api.openai.com/v1"
)

# Connecting to a local LLM via Ollama
ollama_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# Integrating LLMs with Agents:
researcher = Agent(
    role="Researcher",
    goal="Conduct in-depth research on AI developments.",
    llm=openai_llm
)

# The Crew class orchestrates the collaboration of multiple agents and tasks, enabling the execution of complex workflows
# Agents: A list of Agent instances that define the roles and responsibilities within the crew.
# Tasks: A list of Task instances that outline the specific actions to be executed.
# Process Flow: Determines the execution strategy of tasks, such as sequential or hierarchical processes.
# Verbose Mode: Enables detailed logging of the crew’s operations for monitoring and debugging purposes.
my_crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

# To initiate the workflow defined by the crew: Start the crew's task execution
result = my_crew.kickoff()
print(result)

# Decorators: In CrewAI, decorators like @agent, @task, and @crew are used to define agents, tasks, and crews directly
# within a class that extends CrewBase. These decorators automatically register the components for the workflow.

# @agent: Defines an agent with specific configurations.
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        llm=self.ollama_llm,
        verbose=True
    )

# @task: Defines a task that uses an agent for execution.
@task
def research_task(self) -> Task:
    return Task(
        config=self.tasks_config['research_task']
    )

# @crew: Combines agents and tasks into a crew for execution.
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True
    )

"""
How It Works
The decorators link logic and configurations (from YAML or inline) to the CrewAI framework.
They simplify workflow creation by automatically registering the components in the CrewBase class.
By using these decorators, you can organize and manage agents, tasks, and crews efficiently in a modular way.
"""