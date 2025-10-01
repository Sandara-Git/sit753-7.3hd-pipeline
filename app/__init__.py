from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def home():
    return jsonify(ok=True, msg="Hello from CI/CD")

@app.get("/health")
def health():
    return jsonify(status="pass")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

