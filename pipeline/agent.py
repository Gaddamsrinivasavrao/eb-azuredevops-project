"""
SentinelOps-Lite AI Agent Gate
-------------------------------
Runs after unit tests finish. Reads the test result summary, sends it
to Gemini (Google AI Studio API key), and gets a simple APPROVE /
REJECT decision.
"""
import os
import sys
from google import genai
RESULTS_FILE = "test_results.txt"
if not os.path.exists(RESULTS_FILE):
 print(f"ERROR: {RESULTS_FILE} not found. Did the test step run first?")
 sys.exit(1)
with open(RESULTS_FILE, "r") as f:
 test_output = f.read()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
 print("ERROR: GEMINI_API_KEY environment variable is not set.")
 sys.exit(1)
client = genai.Client(api_key=api_key)
prompt = f"""
You are a release-approval agent for a CI/CD pipeline.
Below is the raw output of the automated test suite.
Rules:
- If ALL tests passed, respond APPROVE.
- If ANY test failed, respond REJECT.
- Respond with a single word only: APPROVE or REJECT.
- On a second line, give a one-sentence reason.
Test output:
{test_output}
"""
response = client.models.generate_content(
 model="gemini-2.5-flash",
 contents=prompt,
)
decision_text = response.text.strip()
print("----- AI Agent Decision -----")
print(decision_text)
print("------------------------------")
decision_word = decision_text.splitlines()[0].strip().upper()
with open("agent_decision.txt", "w") as f:
 f.write(decision_word)
if decision_word != "APPROVE":
 print("Agent rejected the release. Stopping pipeline.")
 sys.exit(1)
print("Agent approved the release. Continuing to deployment.")
sys.exit(0)