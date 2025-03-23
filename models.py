import pandas as pd
import boto3
import os
from dotenv import load_dotenv
import conversation_formatter
load_dotenv('keys/.env')
args = ("Doctor Name","Specialty","City","State","Rating")

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
    df = pd.DataFrame("doctor_info.csv")
    df.to_csv('doctor_info.csv')
    if upload:
        upload_doc_file(file = 'doctor_info.csv', bucket = 'emoryhacksdoctors')

def upload_doc_file(file = 'doctor_info.csv', bucket = 'emoryhacksdoctors'):
    s3 = boto3.client('s3')
    s3.upload_file(file, bucket, file)
    print('doc file uploaded to ' + bucket)

def upload_conversation(file = 'conversation.csv', bucket = 'emoryhacksconversation'):
    s3 = boto3.client('s3')
    s3.upload_file(file, bucket, file)
    print('convo csv uploaded to ' + bucket)

def add_doctor(args):
    athena_client = boto3.client('athena')




if __name__ == '__main__':
    initialize()


