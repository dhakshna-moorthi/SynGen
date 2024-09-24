from flask import Flask, request, render_template, send_file
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd 
import os
import re
import json

app = Flask(__name__)

load_dotenv()
token = os.getenv('api_token')

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':

        if 'download' in request.form:
            return send_file(
                'result.csv',
                mimetype='text/csv',
                download_name='result.csv',
                as_attachment=True
            )
            
        user_input = request.form.get('user_input')

        client = OpenAI(
            api_key=f'{token}:my-test-project',
            base_url="https://llmfoundry.straive.com/openai/v1/",
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input+"the response should only data in json format, which can be easily converted to csv file"}],
            model="gpt-4o-mini",
        )
        
        response = chat_completion
        content = response.choices[0].message.content
        
        json_str = re.search(r'```json(.*?)```', content, re.DOTALL).group(1).strip()
        data=json.loads(json_str)

        df = pd.DataFrame(data)
        df.to_csv('result.csv', index=False)
        table_html = df.to_html(classes='table table-striped')

        if 'view' in request.form:
            return render_template('result.html', table_html=table_html)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)