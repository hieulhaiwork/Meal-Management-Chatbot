import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
load_dotenv()


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)


os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')
search_tool = SerperDevTool()


feedback_analyzer = Agent(
    role="Feedback Analyzer",
    goal="Summarize requirements from {feedback} becomes preferences for other agents",
    backstory= "You're a analyzer expert, you can summarize complex information to easilier-understanding information",
    verbose=True,
    llm=llm
)

health_analyzer_agent = Agent(
    role="Health Analyzer",
    goal="Suggest dishes for user's health based on {report_summary} and preferences from Feedback Analyzer agent",
    backstory="You're a health expert and nutrition expert to recommend the best dish for user's health and preferences.",
    tools=[search_tool],
    verbose=True,
    llm=llm
)

# ingredient_optimizer_agent = Agent(
#     role="Ingredient Optimizer",
#     goal="Suggest suitable amount of ingredient of dishes from Health Analyzer Agent for the user caught diabetes",
#     backstory="You're a health expert and nutrition expert, you want user to get enough of nutritions but not waste too much food",
#     tools=[search_tool],
#     verbose=True,
#     llm=llm
# )

meal_planer_agent = Agent(
    role="Meal Planner",
    goal="Suggest suitable an 3-days meal plan for health based on dishes from Health Analyzer Agent suggested",
    backstory="You're a health expert ensuring clients get the best meal plans for their health.",
    tools=[search_tool],
    verbose=True,
    llm=llm
)

feedback_analyze_task = Task(
    description= "Summarize which dishes or taste user likes or not from {feedback} into simple form that other agents can understand quickly.",
    expected_output="A list of preferences",
    agent=health_analyzer_agent
)

health_analyze_task = Task(
    description="Analyze report {report_summary} to understand what user need or prevent. And based on preferences list from Feedback Analyzer agent, search the internet and choose 10 dishes suitable for user satifies both requirements before. Prioritize requirements from report",
    expected_output='A list of dishes that satifies both content in {report_summary} and preferences list',
    agent=health_analyzer_agent,
    tools=[search_tool]
)

# ingredient_optimize_task = Task(
#     description= "Suggest the suitable amount of ingredients to cook one dish from Health Analyzer Agent for diabetes user",
#     expected_output="A list of ingredients with amount of them",
#     tools=[search_tool],
#     agent=ingredient_optimizer_agent
# )

meal_plan_task = Task(
    description= "Generate an 3-days meal plan based on dishes suggest from Health Analyzer Agent, each day should have different dishes, ask Health Analyzer Agent suggest for enough 7 days if necessary",
    expected_output="A table with Day column show Days in a week, other column show names of dishes divided by breakfast, lunch, dinner and extra meal if necessary",
    tools=[search_tool],
    agent=meal_planer_agent,
    context = [health_analyze_task],
    output_file='summary_documents/meal_plan.md'
)

def dish_recommend(feedback_content,report_summary):

    crew = Crew(
            agents=[feedback_analyzer,health_analyzer_agent],
            tasks=[feedback_analyze_task,health_analyze_task],
            process=Process.sequential,
            manager_llm=llm,
            verbose=True,
            cache=True,
            full_output=True,
            share_crew=True,
            max_rpm = os.getenv('MAX_OUTPUT'),
        )
    
    result = crew.kickoff(inputs={"feedback": feedback_content, "report_summary": report_summary})
    return result

def meal_schedule(feedback_content,report_summary):

    crew = Crew(
            agents=[feedback_analyzer,health_analyzer_agent, meal_planer_agent],
            tasks=[feedback_analyze_task, health_analyze_task, meal_plan_task],
            process=Process.sequential,
            manager_llm=llm,
            verbose=True,
            cache=True,
            full_output=True,
            share_crew=True,
            max_rpm=os.getenv('MAX_OUTPUT'),
        )
    
    result = crew.kickoff(inputs={"feedback": feedback_content, "report_summary": report_summary})
    return result