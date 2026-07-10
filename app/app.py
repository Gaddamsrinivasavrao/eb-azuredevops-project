from flask import Flask, jsonify
application = Flask(__name__)
# NOTE: AWS Elastic Beanstalk (Python platform) looks for a variable
# named "application" by default. That is why it is not called "app".
@application.route("/")
def home():
 return jsonify(
 message="Hello from SentinelOps-Lite!",
 status="running"
 )
@application.route("/health")
def health():
 return jsonify(status="healthy"), 200
if __name__ == "__main__":
 application.run(host="0.0.0.0", port=5000)