import os
from chatbot import chatbot
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
load_dotenv()


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

def summarization(conversation_history):
    prompt_text = f"""
    ## Instructions
    Process the content to determine which dishes the user likes or dislikes and follow the chatbot, it's recommended or not.
    Skip non-revelant subjects, skip dishes chatbot recommend, skip meal plan chatbot provide, only focus on which dishes user like or not.
    Focus on precise, relevant information without introductory or concluding remarks.

    ## Requirements
    - Each insight must be directly applicable to answering specific feeling-related queries.
    - Keep each insight concise, ideally under 300 words, and ready to be integrated into a feedback understanding platform.
    - The language should be clear and direct, avoiding unnecessary elaborations or thematic introductions.
    - Format insights to ensure they are standalone pieces of information that do not require additional context to be understood.

    ## Content
    {conversation_history}
    """
    messages = [HumanMessage(content=prompt_text)]
    insights = llm.invoke(messages).content
    return insights

def save_feedback(file_path, insights):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{insights}\n")
    print(f"Content successfully saved to {file_path}")
