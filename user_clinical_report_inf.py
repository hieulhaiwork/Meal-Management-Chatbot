import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import re
load_dotenv()

# Retrieve the Google API key from environment variables and initialize the LLM model
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# Read the content of a file
def read_file(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content, file_name

# Remove personal information 
def remove_personal_inf(text):
    patterns = [
        r"\bName:\s?.*",
        r"\bPatient ID:\s?.*",
        r"\bDate of Birth:\s?.*",
        r"\bAddress:\s?.*",
        r"\bPhone:\s?.*",
        r"\bSocial Security Number:\s?.*"
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text)
    return text

# Generate insights 
def generate_insight(content):
    prompt_text = f"""
    ## Instructions
    Process the content to directly extract actionable insights useful for which health problems are caught and nutritional advice.
    Focus on precise, relevant information without introductory or concluding remarks.

    ## Requirements
    - Each insight must be directly applicable to answering specific nutrition-related queries.
    - Keep each insight concise, ideally under 300 words, and ready to be integrated into a nutrition advice platform.
    - The language should be clear and direct, avoiding unnecessary elaborations or thematic introductions.
    - Format insights to ensure they are standalone pieces of information that do not require additional context to be understood.

    ## Content
    {content}
    """
    messages = [HumanMessage(content=prompt_text)]
    insights = llm.invoke(messages).content
    return insights

# Save the generated insights
def save_insight(file_name, file_folder, insights):
    file_path = os.path.join(file_folder, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(insights)
    print(f"Content successfully saved to {file_path}")

# Process the work
def report_insight(input_file_path, output_file_folder):
    content, file_name = read_file(input_file_path)
    content = remove_personal_inf(content)
    insights = generate_insight(content)
    save_insight(f"{file_name}_fix","user_documents", content)
    save_insight(file_name, output_file_folder, insights)