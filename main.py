from user_clinical_report_inf import *
from conv_control import *
from feedback_sum import *


choice = input('Is this your first time running? (Y/N): ')
if choice.lower() in ['yes', 'y']:
    report_insight("user_documents\diabetes.txt","summary_documents")
elif choice.lower() in ['no','n']:
    user_document = read_file("user_documents/diabetes.txt_fix")
    feedback_content = read_file("summary_documents/feedback.txt")
    report_summary = read_file("summary_documents/diabetes.txt")
    chat_with_bot(user_document, feedback_content, report_summary)
else:
    print('Invalid input!')
