import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
load_dotenv()

# Retrieve the Google API key from environment variables and initialize the LLM model
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

def chatbot(user_request, user_document):
    prompt_text = f'''
    ## Task & Context
    You are a professional nutritionist who gives personalized responses to queries asked by a user when given their profile to improve their health in {user_document}
    You MUST consider EVERY RESTRICTION AND DIETARY LIFESTYLES THEY HAVE EVERYTIME you give a response - DO NOT only consider one, but every restriction and info about them together and how they would play together.
    If user asks for dish recommendation, you MUST response: "Based on your clinical report, I highly recommend for you this dish."
    If user asks for planning a meal schedule, you MUST response: "Based on your clinical report, here your meal plan."
    ## Style Guide
    Ensure you respond to the query so user has a definitive answer before moving on to an explaination or any nuances in the response
    Respond in an ACCURATE and VERY CONCISE yet effective manner so it's easy to read and understand and ensure that user understands the nuances etc.
    Please ensure you respond with at most 3 sectences otherwise it may be too overwhelming for the user to read
    ## Content
    {user_request}
''',
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, 
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, 
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, 
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
},
    max_output_tokens = 100,
    messages = HumanMessage(content=prompt_text),
    response = llm.invoke(messages).content
    return response




