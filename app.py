from flask import Flask
app = Flask(__name__)
# AKIAUTBJDBVSZFCNE4AK

@app.route('/')
def hello_world():
    return "Secure GitOps with CheckPoint v95\n"
