from flask import Flask,render_template,render_template_string,request
import requests
import json
import textwrap 
import math
import mysql.connector
from rake_nltk import Rake
import nltk
import ssl
import os

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
r = Rake()

API_KEY1 = "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"
API_KEY2 = "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"
API_KEY3 = "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"
API_KEY4 = "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"
API_KEY5 = "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"

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="shinkansen.proxy.rlwy.net",
            user="root",
            password="iLpIQVLOCeeFKjITaGomktzXxJXwIBdn",
            port=13002,
            database="railway",
            auth_plugin='mysql_native_password',
            connect_timeout=30,
            allow_local_infile=True
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

mydb = get_db_connection()
if mydb:
    cursor = mydb.cursor()
    print("Database connected successfully!")
else:
    print("Failed to connect to database")


app=Flask(__name__,template_folder='template', static_folder='static')

user_input_global = None 
detailresponse = None
formulas_global = None
Output = None
htmll_final = None
flask_final = None

@app.route('/')
def index():
    global user_input_global
    global detailresponse
    global formulas_global
    global Output
    global htmll_final
    global flask_final
    user_input_global = None
    detailresponse = None
    formulas_global = None
    Output = None
    htmll_final = None
    flask_final = None
    keywords = None
    return render_template('base.html')

@app.route('/ask', methods=['POST'])
def ask():
    global user_input_global
    global detailresponse
    global formulas_global
    global htmll_final
    global flask_final
    global keywords
    user_input_global = request.form.get('user_input') 
    r.extract_keywords_from_text(user_input_global)
    keywords = r.get_ranked_phrases()
    print("keywords:", keywords)
    result = find_matching_calculation(keywords)
    if result:
        print("Found matching calculation in database")
        detailresponse = result['htmlpage']
        formulas_global = result['formula']
        htmll_final = result['formpage']
        flask_final = result['python']
        return render_template_string(htmll_final)
    else: 
        print("No matching calculation found in database")   
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
                "Authorization": f"Bearer {API_KEY1}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",  
                "X-Title": "DeepSeekTerminalApp"     
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-exp:free",
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
                "Authorization": f"Bearer {API_KEY2}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost", 
                "X-Title": "DeepSeekTerminalApp"     
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-exp:free",
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
                "Authorization": f"Bearer {API_KEY3}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost", 
                "X-Title": "DeepSeekTerminalApp"     
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-exp:free",
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
    global keywords
    global detailresponse
    falskprompt = f"""Generate Python code that collects form inputs and assigns the final result to Output variable.

            Given equation: '{formulas_global}'
            Given HTML form: '{htmll_final}'

            IMPORTANT: The code MUST assign the final result to 'Output' variable with proper units.

            Format requirements:
            1. Collect all form inputs as variables
            2. Create calculation expression
            3. Assign result to Output with units

            Example format:
            # Collect inputs individually
            radius = float(request.form.get('radius', 0))
            height = float(request.form.get('height', 0))

            # Calculate result
            result = 3.14159 * radius * height

            # REQUIRED: Assign to Output with units
            Output = f"{{result:.2f}} cubic meters"

            Return only the Python code that collects inputs and assigns to Output. No decorators or explanations."""
    flaskout = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY4}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  
            "X-Title": "DeepSeekTerminalApp"     
        },
        data=json.dumps({
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [
                {
                    "role": "user",
                    "content": falskprompt
                }
            ],
            "max_tokens": 1000
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
    print("flask code :")
    print(flask_final)
    if detailresponse and formulas_global and htmll_final and flask_final:
        try:
            # Get fresh connection
            db = get_db_connection()
            if not db:
                print("Failed to connect to database")
                return
                
            cursor = db.cursor()
            context = ', '.join(keywords)
            query = """
            INSERT INTO calculations 
            (context, htmlpage, formula, formpage, python) 
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (context, detailresponse, formulas_global, htmll_final, flask_final))
            db.commit()
            print("Data inserted successfully")
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")    
            if db:
                db.rollback()
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    

@app.route('/call', methods=['POST', 'GET'])
def call():
    global detailresponse
    global formulas_global
    global Output
    global flask_final
    global keywords

    try:
        if not flask_final:
            return "Error: No calculation code available", 400

        # Clean up the code string by removing extra indentation
        cleaned_code = "\n".join(line.strip() for line in str(flask_final).splitlines())

        # Create namespace for execution
        namespace = {
            'request': request,
            'float': float,
            'math': math,
            'Output': None
        }

        # Execute the cleaned code
        exec(cleaned_code, namespace)
        
        # Get the result
        Output = namespace.get('Output', 'Calculation failed')
        print(f"Calculation result: {Output}")

    except Exception as e:
        if request.method == 'POST':
             user_inputs = request.form.to_dict()  
        elif request.method == 'GET':
             user_inputs = request.args.to_dict() 
        else:
             user_inputs = {}
        print(f"Collected user inputs: {user_inputs}")
        compute_prompt = f"""
            Compute the result of the following equation using the provided inputs:

            Equation: {formulas_global}
            Inputs: {user_inputs}

            Return only the computed result as a number or string with Unit . Do not include any explanations or additional text.
            """
        print("the pycode is not working")
        compute_response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY5}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": "google/gemini-2.0-flash-exp:free",
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
        else:
            print("Error: Failed to compute the result from the API")
            return "Error: Failed to compute the result from the API", 500    

    return render_template('output.html', 
                         formulas_global=formulas_global, 
                         Output=Output, 
                         detailresponse=detailresponse)

def find_matching_calculation(keywords):
    db = get_db_connection()
    if not db:
        print("Failed to connect to database")
        return None
        
    cursor = db.cursor(dictionary=True)
    try:
        print(f"Searching for keywords: {keywords}")
        
        case_statements = []
        where_conditions = []
        
        primary_keywords = keywords[:3]
        secondary_keywords = keywords[3:]
        
        # Add primary keyword conditions with SOUNDEX for similar word matching
        for kw in primary_keywords:
            safe_kw = kw.replace("'", "''")
            case_statements.append(f"""
                (CASE WHEN 
                    LOWER(context) LIKE '%{safe_kw}%' 
                    OR SOUNDEX(context) = SOUNDEX('{safe_kw}')
                THEN 1.0 ELSE 0 END)
            """)
            where_conditions.append(f"""
                LOWER(context) LIKE '%{safe_kw}%'
                OR SOUNDEX(context) = SOUNDEX('{safe_kw}')
            """)
        
        # Secondary keywords with similar word matching
        for kw in secondary_keywords:
            safe_kw = kw.replace("'", "''")
            case_statements.append(f"""
                (CASE WHEN 
                    LOWER(context) LIKE '%{safe_kw}%'
                    OR SOUNDEX(context) = SOUNDEX('{safe_kw}')
                THEN 0.5 ELSE 0 END)
            """)
        
        query = f"""
        SELECT 
            htmlpage,
            context,
            formula,
            formpage,
            python,
            ({' + '.join(case_statements)}) as match_score
        FROM 
            calculations
        WHERE 
            {' OR '.join(where_conditions)}
        HAVING 
            match_score >= 2.5
        ORDER BY 
            match_score DESC,
            LENGTH(context) ASC
        LIMIT 1
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            print(f"Found match with score: {result['match_score']}")
            print(f"Matching context: {result['context']}")
            return result
        
        print("No matching calculation found")
        return None
        
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)