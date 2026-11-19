from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        try:
            weight = float(request.form.get("weight", ""))
            height = float(request.form.get("height", ""))

            if weight <= 0 or height <= 0:
                result = "<p>Please enter positive values.</p>"

            else:
                bmi = weight / (height * height)

                if bmi < 18.5:
                    category = "Underweight"
                elif bmi < 25:
                    category = "Normal"
                elif bmi < 30:
                    category = "Overweight"
                else:
                    category = "Obese"

                result = (
                    "<div class='result'>"
                    "<h2>Your BMI: " + str(round(bmi, 2)) + "</h2>"
                    "<h3>" + category + "</h3>"
                    "</div>"
                )

        except ValueError:
            result = "<p>Please enter valid numbers.</p>"

    page = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BMI Calculator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #141e30, #243b55);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 15px;
            }

            .box {
                background: white;
                padding: 30px;
                border-radius: 15px;
                width: 100%;
                max-width: 350px;
                text-align: center;
            }

            input {
                width: 100%;
                box-sizing: border-box;
                padding: 13px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
            }

            button {
                width: 100%;
                padding: 14px;
                background: #243b55;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 17px;
            }

            .result {
                background: #eef3f8;
                padding: 15px;
                margin-top: 20px;
                border-radius: 10px;
            }
        </style>
    </head>

    <body>
        <div class="box">

            <h1>BMI Calculator</h1>
            <p>Enter your details below</p>

            <form method="POST">
                <input type="number" step="any"
                       name="weight" placeholder="Weight (kg)" required>

                <input type="number" step="any"
                       name="height" placeholder="Height (metres)" required>

                <button type="submit">Calculate BMI</button>
            </form>

            {{RESULT}}

        </div>
    </body>
    </html>
    """

    page = page.replace("{{RESULT}}", result)

    return page


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
