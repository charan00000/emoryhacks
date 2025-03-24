import pandas as pd
import os
from xhtml2pdf import pisa

def generate_html(csv_path = 'conversation.csv'):
    df = pd.read_csv('conversation.csv')

    html_content = ""
    for index, row in df.iterrows():
        html_content += f"<p>{row['Sender']}: {row['Message']}</p>\n"

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSV Text Display</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f7f6;
            }}
            
            .text-container {{
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-shadow: 0 1px 2px 0 rgb(0 0 0 / 10%);
            }}
            
            .text-container p {{
                margin-bottom: 10px;
            }}
            
            .text-container p:nth-child(2n) {{
                color: green;
            }}
            
            .text-container p:nth-child(2n+1) {{
                color: blue;
            }}
        </style>
    </head>
    <body>
        <div class="text-container">
            {html_content}
        </div>
    </body>
    </html>
    """

    with open('conversation.html', 'w') as file:
        file.write(html_template)

    print('conversation.html saved successfully.')
    html_to_pdf(html_path='conversation.html', output_path='conversation.pdf')

def html_to_pdf(html_path = "conversation.html", output_path = "conversation.pdf"):
    status = pisa.CreatePDF(open(html_path, 'r'), dest=open(output_path, 'wb'))
    print('pdf report generated in ' + output_path)

if __name__ == '__main__':
    #generate_html()
    html_to_pdf()
