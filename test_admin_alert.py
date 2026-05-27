import requests
import json
import time

time.sleep(2)  # Give server time to reload if watch detected change

response = requests.get('http://localhost:8000/api/email/debug-env?show_values=true', timeout=10)
print('=== Environment Variables ===')
env_data = response.json()
print(f"ADMIN_EMAIL: {env_data['env']['ADMIN_EMAIL']}")

print('\n=== Testing Admin Alert Auto Endpoint ===')
payload = {
    'user_email': 'newuser@example.com',
    'user_name': 'John Doe',
    'details': {'source': 'web_signup', 'signup_date': '2026-05-27'}
}

response = requests.post(
    'http://localhost:8000/api/email/send-admin-alert-auto',
    json=payload,
    timeout=10
)

print(f'Status Code: {response.status_code}')
print(f'Response: {json.dumps(response.json(), indent=2)}')
