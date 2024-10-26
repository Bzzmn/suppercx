from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai.project import CrewBase, agent, crew, task

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@CrewBase
class CustomerSupportCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def customer_support_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['customer_support_agent'],
            verbose=True,
            llm=llm,
            tools=[
            ]
        )
    

    @task
    def customer_support(self) -> str:
        return Task(
            config=self.tasks_config['customer_support'],
            agent=self.customer_support_agent()
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True, 
            memory=True
        )




