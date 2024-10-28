from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai.project import CrewBase, agent, crew, task
from .tools.FetchLatestVideosFromYouTubeSearchTool import FetchLatestVideosFromYouTubeSearchTool
from .tools.AddVideoToVectorDatabaseTool import AddVideoToVectorDBTool, QueryVectorDBTool

load_dotenv()

llm = ChatOpenAI(model="gpt-4-mini", temperature=0)

# ---- Tools ----
fetch_latest_yt_search_tool = FetchLatestVideosFromYouTubeSearchTool()
add_video_to_vector_db_tool = AddVideoToVectorDBTool()
rag_tool = QueryVectorDBTool()

# --- Agents ---

customer_support_agent = Agent(
    role="Short Answer Agent",
    goal="Give a clear and concise answer to the user's query",
    backstory=(
        """
        You are a highly skilled customer support agent with a talent for giving 
        clear and concise answers to the user's query.
        """
    ),
    verbose=True,
    allow_delegation=False,
)

scrape_agent = Agent(
    role="Scrape Agent",
    goal="Scrape content from YouTube videos relevant to the search query",
    verbose=True,
    allow_delegation=False,
    backstory=(
        """
        - A dedicated professional focused on extracting and processing content
            from YouTube videos.
        - You ensure that all video content is accurately scraped.
        - You are thorough and fact-driven, ensuring the highest quality of data.
        """
    ),
    tools=[fetch_latest_yt_search_tool],
    llm=ChatOpenAI(model="gpt-4o-mini"),
)

vector_db_agent = Agent(
    role="Vector DB Processor",
    goal="Add YouTube videos to the vector database",
    verbose=True,
    allow_delegation=False,
    backstory=(
        """
        A detail-oriented professional who ensures that video content 
        is accurately processed and added to the vector database.
        """
    ),
    tools=[add_video_to_vector_db_tool],
    llm=ChatOpenAI(model="gpt-4o-mini"),
)

product_research_agent = Agent(
    role="Product Research Agent",
    goal="To extract and present the most relevant product features and details from reliable sources, providing clear and actionable insights for decision-making.",
    verbose=True,
    allow_delegation=False,
    backstory=(
    """
    A highly analytical and detail-oriented professional, specialized in gathering 
    and distilling key product information from a wide range of sources. 
    You excel at identifying and extracting the most relevant features and characteristics 
    of products, ensuring the information is actionable and reliable.

    You are relentless in your pursuit of accuracy and thoroughly vet all gathered data 
    by cross-referencing multiple sources. If details are ambiguous or missing, 
    you rephrase and re-query effectively to ensure completeness. 

    When researching products, you look for user reviews, expert evaluations, 
    and product specifications, ensuring that you not only capture technical details 
    but also practical insights on usability, quality, and performance.

    You have a keen understanding of the importance of features that influence 
    customer decision-making, such as price, durability, and compatibility, 
    and always focus on presenting these features in an organized and clear manner.
    """
    ),
    tools=[rag_tool],
    llm=ChatOpenAI(model="gpt-4o-mini"),
)




# --- Tasks ---

understand_user_needs_task = Task(
    description="""
    Have a friendly conversation with the user to understand their needs and query. 
    Ask questions to clarify the user's needs.
    """,
    expected_output="A concise and clear answer to the user's query",
    agent=customer_support_agent,
)



scrape_youtube_search_task = Task(
    description=(
        """
        Search for and scrape 5 videos relevant to the specified search query.
        Extract relevant information about the content of these videos.
        Ensure that all information comes directly from the YouTube videos. 
        Do not make up any information.
        """
    ),
    expected_output="""
        Extract relevant information about the content of the latest 5 videos 
        related to the specified search query.
        """,
    tools=[fetch_latest_yt_search_tool],
    agent=scrape_agent,
)

convert_user_input_to_search_yt_query_task = Task(
    description=(
        """
    Given a user input, transform it into a very concise and accurate search query for youtube videos.
    Focus on extracting the key topic or goal the user is trying to accomplish.
    The query should be very concise and to the point, maximum 4 keywords.
    Example: "I want to buy a new laptop, I use my laptop for work, I need a good battery life, and a good processor. I also like to play video games,so I want a good graphics card."
    The query would be: "best+laptops+work+gaming"

    Here is the user input:
    {query}
    """
    ),
    expected_output="""
        A clear and concise search query for a youtube search
        """,
    tools=[],
    agent=scrape_agent,
)

process_videos_task = Task(
    description=(
        """
        Process the extracted video urls from the previous task 
        and add them to the vector database.
        Ensure that each video is properly added to the vector database.
        If for any reason you cannot add a video, skip it.
        All information must come directly from the searches. 
        Do not make up any information.
        """
    ),
    expected_output="""
        Successfully add videos to the vector database.
        """,
    tools=[add_video_to_vector_db_tool],
    agent=vector_db_agent,
)

research_product_task = Task(
    description=(
        """
        Given a user input, research a list of products and extract the most relevant features, 
        including brand, model, and key characteristics. Compare the products, 
        highlighting their pros and cons, as well as unique features. Ensure that 
        the information is accurate, detailed, and useful for decision-making.
        Use the RAG tool to query the knowledge base for relevant information.
        The query is already provided by the previous task as context.
        Remember that when using the RAG tool, you must give the input as a string, not a list.
        Don't make up any information, only use the information from the knowledge base. If you cannot find any information, say so.
        This is the user input:
        {query}
        """
    ),
    expected_output="""
        - A list of 3 products with brand and model.
        - A comparison table or detailed comparison between the products.
        - Key features, pros, and cons of each product.
        - Any unique selling points or standout characteristics.
        """,
    tools=[rag_tool],
    agent=product_research_agent,
)


give_answer_task = Task(
    description="""
    Given the information from the previous tasks, give a clear and concise answer to the user's query.
    """,
    expected_output="A clear and concise answer to the user's query",
    tools=[],
    agent=customer_support_agent,
    context=[understand_user_needs_task, research_product_task],
)

# --- Crew ---
crew = Crew(
    agents=[
        # scrape_agent,
        # vector_db_agent,
        # product_research_agent,
        customer_support_agent,
    ],
    tasks=[
        understand_user_needs_task,
        # convert_user_input_to_search_yt_query_task,
        # scrape_youtube_search_task,
        # process_videos_task,
        # research_product_task,
        # give_answer_task,
    ],
    process=Process.sequential,
    # manager_llm=ChatOpenAI(model="gpt-4o-mini"),
    planning=True,
    verbose=True,
    memory=True,
)

def get_crew():
    return crew
