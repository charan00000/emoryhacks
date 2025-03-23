import pandas as pd
import boto3
import os
from dotenv import load_dotenv
import report_div_maker
load_dotenv('keys/.env')
args = ('Doctor Name', 'Address', 'Location (city, state)', 'Practicing Specialty', 'Calendar Link')

def initialize(upload = True):
    confirm = input("confirm initialize and replace existing database? yes or no?")
    if confirm == 'yes':
        confirm = input("are you sure???????")
        if confirm != 'yes':
            print('aborted')
            return
    else:
        print('aborted')
        return
    data = [
    {"Doctor Name": "Dr. Jane Doe", "Address": "000 xxx", "Location": "New York, NY", "Practicing Specialty": "Oncology", "Calendar Link": "https://www.zocdoc.com/drjanedoe"},
    {"Doctor Name": "Dr. David Lee", "Address": "000 xxx xxx", "Location": "Chicago, IL", "Practicing Specialty": "Gastroenterology", "Calendar Link": "https://www.zocdoc.com/drdavidlee"},
    {"Doctor Name": "Dr. Sophia Patel", "Address": "000 xxx xxx", "Location": "Los Angeles, CA", "Practicing Specialty": "Psychiatry", "Calendar Link": "https://www.zocdoc.com/drsophiapatel"},
    {"Doctor Name": "Dr. Ethan Kim", "Address": "0000 Cexxxdar xxx", "Location": "Houston, TX", "Practicing Specialty": "Urology", "Calendar Link": "https://www.zocdoc.com/drethankim"},
    {"Doctor Name": "Dr. Olivia Martin", "Address": "000 xxx xxx", "Location": "Seattle, WA", "Practicing Specialty": "Endocrinology", "Calendar Link": "https://www.zocdoc.com/droliviamartin"}
]
    df = pd.DataFrame(data)
    df.to_csv('doctor_info.csv')
    if upload:
        upload_doc_file(file = 'doctor_info.csv', bucket = 'emoryhacksdoctors')

def upload_doc_file(file = 'doctor_info.csv', bucket = 'emoryhacksdoctors'):
    s3 = boto3.client('s3')
    s3.upload_file(file, bucket, file)
    print('uploaded to ' + bucket)

def add_doctor(args):
    athena_client = boto3.client('athena')



def update_report(question_answer_string):
    print(question_answer_string)
    divved_string = report_div_maker.wrap_messages_in_divs(question_answer_string)
    print(divved_string)

if __name__ == '__main__':
    #initialize()
    update_report("A")


