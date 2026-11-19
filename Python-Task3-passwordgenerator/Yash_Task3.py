from flask import Flask, render_template_string, request
import secrets
import string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Password Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial;
            background: #101827;
            color: white;
            text-align: center;
            padding: 20px;
        }

        .box {
            max-width: 400px;
            margin: 40px auto;
            background: #1e293b;
            padding: 25px;
            border-radius: 15px;
        }

        input, button {
            width: 100%;
            padding: 12px;
            margin-top: 15px;
            border: none;
            border-radius: 8px;
            box-sizing: border-box;
        }

        input {
            background: #334155;
            color: white;
        }

        button {
            background: #38bdf8;
            font-weight: bold;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            background: #0f172a;
            border-radius: 10px;
            overflow-wrap: anywhere;
        }

        .password {
            color: #4ade80;
            font-size: 18px;
        }
    </style>
</head>

<body>
    <div class="box">
        <h1>🔐 Password Generator</h1>
        <p>Generate your random password</p>

        <form method="POST">
            <input type="number" name="length"
                   min="8" max="64"
                   placeholder="Enter password length"
                   value="{{ length }}" required>

            <button type="submit">Generate Password</button>
        </form>

        {% if password %}
        <div class="result">
            <h3>Your Password</h3>
            <p class="password">{{ password }}</p>
        </div>
        {% endif %}

        {% if error %}
        <div class="result">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    password = ""
    error = ""
    length = 12

    if request.method == "POST":
        try:
            length = int(request.form.get("length", 12))

            if 8 <= length <= 64:
                characters = (
                    string.ascii_letters
                    + string.digits
                    + string.punctuation
                )

                password = ''.join(
                    secrets.choice(characters)
                    for _ in range(length)
                )
            else:
                error = "Length must be between 8 and 64."

        except ValueError:
            error = "Please enter a valid number."

    return render_template_string(
        HTML,
        password=password,
        error=error,
        length=length
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
