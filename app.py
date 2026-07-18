from flask import Flask, request, render_template_string
from google import genai
import os

app = Flask(__name__)

# Read API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Student Support Chatbot</title>
    <style>
        body{
            font-family:Arial;
            background:#f5f5f5;
            margin:40px;
        }

        .box{
            max-width:700px;
            margin:auto;
            background:white;
            padding:20px;
            border-radius:10px;
        }

        textarea{
            width:100%;
            height:120px;
        }

        button{
            padding:10px 20px;
            font-size:16px;
            margin-top:10px;
        }

        .answer{
            margin-top:20px;
            background:#eef;
            padding:15px;
            border-radius:8px;
        }
    </style>
</head>

<body>

<div class="box">

<h1>🎓 AI Student Support Chatbot</h1>

<form method="POST">

<textarea
name="question"
placeholder="Ask any student-related question..."
></textarea>

<br>

<button type="submit">

Ask

</button>

</form>

{% if answer %}

<div class="answer">

<h3>Answer</h3>

<p>{{answer}}</p>

</div>

{% endif %}

</div>

</body>

</html>
"""

@app.route("/", methods=["GET","POST"])
def home():

    answer=""

    if request.method=="POST":

        question=request.form["question"]

        prompt=f"""
You are an AI Student Support Assistant.

Answer politely.

If the question is unrelated to education,
say you only answer student-related questions.

Question:

{question}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer=response.text

    return render_template_string(
        HTML,
        answer=answer
    )

if __name__=="__main__":
    app.run(host="0.0.0.0",port=7860)
