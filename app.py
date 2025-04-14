from flask import Flask,render_template,render_template_string,request
import requests
import json
import textwrap 
import math
API_KEY = "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"

app=Flask(__name__,template_folder='template', static_folder='static')

user_input_global = None 
detailresponse = None
formulas_global = None
Output = None
htmll_final = None
flask_final = None

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/ask', methods=['POST'])
def ask():
    global user_input_global
    global detailresponse
    global formulas_global
    global htmll_final
    user_input_global = request.form.get('user_input') 
    user_input_global = f"""Provide a detailed explanation in HTML format with css for '{user_input_global}'. Include:
                        - The concept definition
                        - Related formulas
                        - Key variables and their units
                        - Common applications
                        - use css for styling
                        - desing with table and colorfull
                        - Keep response under 2000 tokens

                        Return only clean HTML without:
                        - JavaScript
                        - Input forms
                        - User prompts
                        - Code blocks or backticks

                        Format the response with proper HTML5 structure using semantic tags like <section>, <article>, and <aside>.""" 
    print("User Input:", user_input_global)

    detailresp = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  
            "X-Title": "DeepSeekTerminalApp"     
        },
        data=json.dumps({
            "model": "google/gemini-2.0-flash-thinking-exp:free",
            "messages": [
                {
                    "role": "user",
                    "content": user_input_global
                }
            ],
            "max_tokens": 100000
        })
    )
    print("frist api request done")
    data1 = detailresp.json()
    if "choices" in data1 and len(data1["choices"]) > 0:
        detailresponse = data1["choices"][0]["message"]["content"]
        detailresponse = detailresponse.replace("```html", "").replace("```", "")
        print(f"🤖: {detailresponse}")
    else:
        print("Error: 'choices' key not found or empty in the response")

    formulaset = f"""Extract or generate a key formula from the given HTML content:

                    Source: "{detailresponse}"

                    Requirements:
                    1. Primary task:
                    - First, try to extract ONE key formula/equation from the content
                    - If no formula exists, generate the most relevant formula based on the concept
                    - Ensure the formula represents the main mathematical relationship

                    2. Format requirements:
                    - Use clean HTML structure
                    - Include MathML or HTML entities for mathematical symbols
                    - Add CSS for visual emphasis
                    - Keep response under 800 tokens

                    Return only the styled HTML formula without:
                    - JavaScript
                    - Forms
                    - Multiple equations
                    - Explanations
                    - Example calculations"""
    
    print ("second code request done")
    formulas = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost", 
            "X-Title": "DeepSeekTerminalApp"     
        },
        data=json.dumps({
            "model": "google/gemini-2.0-flash-thinking-exp:free",
            "messages": [
                {
                    "role": "user",
                    "content": formulaset
                }
            ],
            "max_tokens": 1000
        })
    )
    data2 = formulas.json()
    if "choices" in data2 and len(data2["choices"]) > 0:
        formulas_global = data2["choices"][0]["message"]["content"]
        formulas_global = formulas_global.replace("```html", "").replace("```", "")
        print(f"🤖: {formulas_global}")
    else:
        print("Error: 'choices' key not found or empty in the response")
    print("third code request done")
    htmlcode = f"""Create an HTML form for the following formula with specific input fields:

    Formula: {formulas_global}

    Requirements for the form:
    1. Extract each variable from the formula
    2. For each variable:
       - Create a labeled input field
       - Add placeholder showing expected format (e.g., "Enter value in meters")
       - Include the unit of measurement in the label
       - Add required attribute
    3. Include both numeric and text input types as needed
    4. Add min/max values for numeric inputs where appropriate

    Use this exact template structure:

    {{% extends 'base.html' %}}
    {{% block title %}} Formula Calculator {{% endblock %}}
    {{% block content %}}

    <form action=\"{{{{url_for('call')}}}}\" method=\"post\" class=\"calculation-form\">
        <!-- Generate input fields here with proper labels and units -->
        <div class=\"button-group\">
            <button type=\"submit\" class=\"calculate-btn\">Calculate</button>
            <button type=\"reset\" class=\"reset-btn\">Reset</button>
        </div>
    </form>

    {{% endblock %}}

    Return only the complete HTML template code without any explanations."""

    htmlll = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost", 
            "X-Title": "DeepSeekTerminalApp"     
        },
        data=json.dumps({
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {
                    "role": "user",
                    "content": htmlcode
                }
            ],
            "max_tokens": 10000
        })
    )
    data3 = htmlll.json()
    if "choices" in data3 and len(data3["choices"]) > 0:
        htmll_final = data3["choices"][0]["message"]["content"]
        print(f"🤖: {htmll_final}")
        htmll_final = htmll_final.replace("```html", "").replace("```", "")
    else:
        print("Error: 'choices' key not found or empty in the response")
        htmll_final = None  

   
    if htmll_final is None:
        print("Error: htmll_final is None")
        return "Error: Failed to generate HTML code", 500

    test()
    return render_template_string(htmll_final)

def test():
    global htmll_final
    global formulas_global
    global flask_final
    falskprompt=f"""Generate only the Python code to be inserted inside this Flask function template based on the given equation and HTML form inputs. Do not include any explanations, comments, or output except for the generated Python code inside the allocated section.

    Template:

    @app.route('/call', methods=['POST'])
    def call():
      global detailresponse
      global formulas_global
      global Output

      <-- generated code here -->

      # Save the final output to the Output variable and dont assign any for detailresponse,formulas_global

    Given equation: '{formulas_global}'
    Given HTML form: '{htmll_final}'

    Only return the Python code to be inserted at '<-- generated code here -->'. Do not add any additional words or explanations.
    """
    flaskout = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  
            "X-Title": "DeepSeekTerminalApp"     
        },
        data=json.dumps({
            "model": "openrouter/optimus-alpha",
            "messages": [
                {
                    "role": "user",
                    "content": falskprompt
                }
            ],
            "max_tokens": 1
        })
    )
    data4 = flaskout.json()
    if "choices" in data4 and len(data4["choices"]) > 0:
        flask_final = data4["choices"][0]["message"]["content"]
        print(f"🤖:")
    else:
        print("Error: 'choices' key not found or empty in the response")
    flask_final = flask_final.replace("```python", "")  
    flask_final = flask_final.replace("```", "")
    print(flask_final)
    

@app.route('/call', methods=['POST', 'GET'])
def call():
    global detailresponse
    global formulas_global
    global Output
    global flask_final

   
    if flask_final is None:
        print("Error: flask_final is None")
        return "Error: flask_final is None", 500

   
    if request.method == 'POST':
        user_inputs = request.form.to_dict()  
    elif request.method == 'GET':
        user_inputs = request.args.to_dict() 
    else:
        user_inputs = {}

    print(f"Collected user inputs: {user_inputs}")


    max_retries = 1 
    for attempt in range(max_retries):
       
        if "global Output" not in flask_final:
            flask_final = f"global Output and error\n{flask_final}"

       
        try:
            flask_final = textwrap.dedent(flask_final)
        except Exception as e:
            print(f"Error normalizing flask_final indentation: {e}")
            return f"Error normalizing flask_final indentation: {e}", 500

       
        print(f"Attempt {attempt + 1}: Executing flask_final:")
        print(flask_final)

       
        try:
            exec(flask_final, globals()) 
            if Output is None:
                raise ValueError("Output is None after execution")
            break 
        except Exception as e:
            print(f"executing flask_final: ")

           
            compute_prompt = f"""
            Compute the result of the following equation using the provided inputs:

            Equation: {formulas_global}
            Inputs: {user_inputs}

            Return only the computed result as a number or string with Unit . Do not include any explanations or additional text.
            """
            compute_response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": "openrouter/optimus-alpha",
                    "messages": [
                        {
                            "role": "user",
                            "content": compute_prompt
                        }
                    ],
                    "max_tokens": 10000
                })
            )
            compute_data = compute_response.json()
            if "choices" in compute_data and len(compute_data["choices"]) > 0:
                Output = compute_data["choices"][0]["message"]["content"]
                print(f"final-computed Output: {Output}")
                break  
            else:
                print("Error: Failed to compute the result from the API")
                return "Error: Failed to compute the result from the API", 500


    print("Value of Output after executing flask_final:", Output)

   
    return render_template('output.html', formulas_global=formulas_global, Output=Output, detailresponse=detailresponse)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)