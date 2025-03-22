import pandas as pd
df = pd.read_csv('Medical_Intelligence_Dataset.csv')


df = df[(df['input'].str.len() <= 160) & (df['output'].str.len() <= 160)] #remove entries with overly long text

df = df[~df['input'].str.contains('\?')] #remove input questions
df = df[df['output'].str.contains('\?')] #remove output nonquestions
df.to_csv('filtered_medical_data.csv', index=False)
