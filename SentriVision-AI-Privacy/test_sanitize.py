import sys
import json
from backend.app.sanitizer import AegisSanitizer

sanitizer = AegisSanitizer()

text = """SentriVision Demo Application
SentriVision Demo Application
User Profile
Name: Afrin
Email: afrin@example.com
Phone: 9876543210
Username: afrin123
Password: MyPassword123
Bank Account: 123456789012
Card Number: 4111111111111111
PAN: ABCDE1234F
Address: 12 Anna Nagar, Chennai
Date of Birth: 12/05/2004
IP Address: 192.168.1.10
Student ID: STU2026001
Application Status
Your application has been approved.
General Information
Machine learning can be used to analyze data."""

res = sanitizer.sanitize(text)
print(res["sanitized_text"])
