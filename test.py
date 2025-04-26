import requests
import json

API_KEY1 = "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"

# Define the formula HTML
formulas_global = """<div class="formula-container">
    EMI = <span class="fraction">
        <span class="numerator">P × R × (1+R)<sup>N</sup></span>
        <span class="denominator">(1+R)<sup>N</sup> - 1</span>
    </span>
</div>"""

# Define the form HTML
htmll_final = """{% extends 'base.html' %}
{% block title %}Formula Calculator{% endblock %}
{% block content %}
<form action="{{url_for('call')}}" method="post" class="calculation-form">
    <div>
        <label for="P">Principal Loan Amount (₹):</label>
        <input type="number" id="P" name="P" placeholder="Enter principal amount (e.g., 100000)" min="0" required>
    </div>
    <div>
        <label for="R">Interest Rate (Annual %):</label>
        <input type="number" id="R" name="R" placeholder="Enter annual interest rate (e.g., 10.5)" min="0" max="100" step="0.01" required>
    </div>
    <div>
        <label for="N">Loan Tenure (Months):</label>
        <input type="number" id="N" name="N" placeholder="Enter loan tenure in months (e.g., 36)" min="1" required>
    </div>
    <div class="button-group">
        <button type="submit" class="calculate-btn">Calculate</button>
        <button type="reset" class="reset-btn">Reset</button>
    </div>
</form>
{% endblock %}"""

falskprompt = f"""Generate Python code that collects form inputs individually and creates an eval expression.

Template:
@app.route('/call', methods=['POST'])
def call():
    global Output
    
    # Collect inputs individually
    radius = float(request.form.get('radius', 0))
    height = float(request.form.get('height', 0))
    # etc...
    
    # Create eval expression using collected variables
    expression = "3.14159 * radius**2"  # example
    Output = str(eval(expression)) + " units²"

Given equation: '{formulas_global}'
Given HTML form: '{htmll_final}'

Return only the Python code that collects inputs and creates the eval expression. No explanations."""

try:
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
except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
    exit(1)

data4 = flaskout.json()
if "choices" in data4 and len(data4["choices"]) > 0:
    flask_final = data4["choices"][0]["message"]["content"]
    print("🤖: API response received")
else:
    print("Error: 'choices' key not found or empty in the response")
    exit(1)

flask_final = flask_final.replace("```python", "").replace("```", "")
print("\nGenerated Flask code:")
print(flask_final)