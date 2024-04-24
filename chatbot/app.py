import json
from flask import Flask, render_template, request, redirect, url_for, session
from langchain_community.llms import Ollama

ollama = Ollama(model="llama3")
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def analyze_code(user_code):
    prompt = "1 : Calculate the complexity of the code,2: Determine the code coverage of the code,3: Identify code duplication in the code,4: Find all the issues in the code" + "Code : " + user_code + "Give the response in the same format 1. 2. 3. 4. only give text-based crisp and short answers for the given 4 prompts\n Give it in dictionary format in python. only generate {} part, no other sentences. Do not use any markdown. the output should be in python format"
    formatted_response = ollama.invoke(prompt)
    return formatted_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code_input = request.form.get('code_input')

    analysis_output = analyze_code(code_input)
    formatted_response = analysis_output

    start_index = formatted_response.find("{")
    end_index = formatted_response.find("}")

    data_str = formatted_response[start_index + 1:end_index]
    pairs = data_str.split("\n")
    result = {}

    for pair in pairs:
        key, value = pair.split(": ", 1)
        result[int(key)] = value.strip('"')

    # Store the analysis result in session storage
    session['analysis_result'] = result

    return redirect(url_for('display_output'))

@app.route('/display_output')
def display_output():
    # Retrieve the analysis result from session storage
    analysis_output = session.pop('analysis_result', {})

    analysis_output_string = {
        'code_complexity': analysis_output.get(1),
        'code_coverage': analysis_output.get(2),
        'duplication_info': analysis_output.get(3),
        'issues': analysis_output.get(4)
    }

    return render_template('output.html', analysis_output=analysis_output_string)

if __name__ == '__main__':
    app.run(debug=True)
