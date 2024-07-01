from chatbot import chatbot
from multi_agents import dish_recommend, meal_schedule
from feedback_sum import summarization, save_feedback
import re

conversation_history = []

def process_input(user_request, user_document):
    conversation_history.append(f"User: {user_request}")
    bot_response = chatbot(user_request, user_document)
    conversation_history.append(f"Chatbot: {bot_response}")
    return bot_response

def communicate_with_agent(bot_response, feedback_content, report_summary):

    pattern_dish = r"\brecommend.*dish\b"
    pattern_schedule = r"\bmeal.*plan\b"
    match_dish = re.search(pattern_dish, bot_response, flags=re.IGNORECASE)
    match_schedule = re.search(pattern_schedule, bot_response, flags=re.IGNORECASE)

    if match_dish:
        response = dish_recommend(feedback_content, report_summary)['final_output']
    elif match_schedule:
        response = meal_schedule(feedback_content, report_summary)['final_output']
    else:
        response = bot_response

    return response

def summarize_feedback(conversation_history):

    chat_text = " ".join(conversation_history)
    summary = summarization(chat_text)
    return summary


def chat_with_bot(user_document,feedback_content,report_summary):
    # Initialize stopping condition
    for i in range(1): #Only for test
        user_request = input("Input your question: ")
        bot_response = process_input(user_request, user_document)
        response = communicate_with_agent(bot_response, feedback_content, report_summary)
        print(response)

    feedback = summarize_feedback(conversation_history)
    save_feedback("summary_documents/feedback.txt", feedback)

