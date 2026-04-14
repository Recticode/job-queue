import time
import json

def run_submission(payload: str):
    data = json.loads(payload)
    print(f"running submission {data['submission_id']}")
    time.sleep(1)

def generate_report(payload: str):
    data = json.loads(payload)
    print(f"generating report for user {data['user_id']}")
    time.sleep(2)

def send_notification(payload: str):
    data = json.loads(payload)
    print(f"sending notification to {data['email']}")
    time.sleep(1)