import pandas as pd

def generate_html(csv_path = 'conversation.csv'):
    # Read the CSV file
    df = pd.read_csv('conversation.csv')

    # Generate HTML content
    html_content = ""
    for index, row in df.iterrows():
        html_content += f"<p>{row['Sender']}: {row['Message']}</p>\n"

    # HTML template
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

    # Save the HTML content to a file
    with open('conversation.html', 'w') as file:
        file.write(html_template)

    print('conversation.html saved successfully.')
