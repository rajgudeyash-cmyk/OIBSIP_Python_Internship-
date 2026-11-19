from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Yash Voice Assistant</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #141e30, #243b55);
            color: white;
            text-align: center;
            padding: 30px 15px;
        }

        .container {
            max-width: 450px;
            margin: 50px auto;
            padding: 25px;
            background: rgba(255,255,255,0.10);
            border-radius: 20px;
        }

        h1 {
            color: #00e5ff;
        }

        button {
            background: #00bcd4;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 30px;
            font-size: 17px;
            margin: 10px;
            cursor: pointer;
        }

        button:active {
            background: #008ba3;
        }

        input {
            width: 85%;
            padding: 12px;
            border-radius: 10px;
            border: none;
            margin-top: 15px;
            font-size: 16px;
        }

        #status {
            margin-top: 20px;
            color: #00e5ff;
            font-size: 16px;
        }

        #response {
            margin-top: 20px;
            font-size: 18px;
            line-height: 1.5;
        }
    </style>
</head>

<body>

    <div class="container">

        <h1>Yash Voice Assistant</h1>

        <p>Welcome! How can I help you?</p>

        <button onclick="listen()">🎤 Start Listening</button>

        <p id="status">Click the microphone and speak.</p>

        <p id="response"></p>

        <hr>

        <p>Or type a command:</p>

        <input
            type="text"
            id="commandInput"
            placeholder="Type something..."
        >

        <br>

        <button onclick="sendText()">Send</button>

    </div>

<script>

    function speak(text) {
        document.getElementById("response").innerText = text;

        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();

            let speech = new SpeechSynthesisUtterance(text);
            speech.lang = "en-US";
            speech.rate = 1;

            window.speechSynthesis.speak(speech);
        }
    }


    function sendCommand(command) {

        document.getElementById("status").innerText =
            "Processing: " + command;

        fetch("/process", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                command: command
            })
        })

        .then(response => response.json())

        .then(data => {
            speak(data.response);
            document.getElementById("status").innerText =
                "Ready for next command.";
        })

        .catch(error => {
            document.getElementById("status").innerText =
                "Server connection error.";
        });
    }


    function listen() {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {

            document.getElementById("status").innerText =
                "Speech recognition is not supported in this browser.";

            return;
        }

        const recognition = new SpeechRecognition();

        recognition.lang = "en-US";
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = function() {

            document.getElementById("status").innerText =
                "Listening... Speak now!";

        };


        recognition.onresult = function(event) {

            const command =
                event.results[0][0].transcript;

            document.getElementById("status").innerText =
                "You said: " + command;

            sendCommand(command);

        };


        recognition.onerror = function(event) {

            document.getElementById("status").innerText =
                "Microphone error: " + event.error;

        };


        recognition.onend = function() {

            console.log("Voice recognition ended.");

        };


        try {

            recognition.start();

        }

        catch(error) {

            document.getElementById("status").innerText =
                "Error starting microphone: " + error.message;

        }

    }


    function sendText() {

        let command =
            document.getElementById("commandInput").value;

        if (command.trim() !== "") {

            sendCommand(command);

            document.getElementById("commandInput").value = "";

        }

    }

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/process", methods=["POST"])
def process():

    data = request.get_json(silent=True) or {}

    command = data.get("command", "").lower().strip()

    if "hello" in command or "hi" in command:
        response = "Hello! How can I help you?"

    elif "your name" in command or "who are you" in command:
        response = "I am Yash Voice Assistant."

    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        response = "The current time is " + current_time

    elif "date" in command or "today" in command:
        current_date = datetime.now().strftime("%d %B %Y")
        response = "Today's date is " + current_date

    elif "how are you" in command:
        response = "I am fine. Thank you for asking!"

    elif "thank you" in command:
        response = "You are welcome!"

    elif "help" in command:
        response = "You can ask me the time, date, or my name."

    elif "bye" in command:
        response = "Goodbye! Have a nice day."

    else:
        response = "Sorry, I did not understand that command."

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
