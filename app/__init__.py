from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def home():
    return jsonify(ok=True, msg="Hello from CI/CD")

@app.get("/")
def index():
    return "OK", 200

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

