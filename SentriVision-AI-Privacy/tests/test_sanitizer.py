from backend.app.sanitizer import AegisSanitizer

def test_sanitizer_normal_text_preservation():
    sanitizer = AegisSanitizer()
    text = "Machine learning is useful for data analysis."
    result = sanitizer.sanitize(text)
    assert result["sanitized_text"] == text
    assert result["detected"] == False
    assert result["protected_count"] == 0

def test_sanitizer_email():
    sanitizer = AegisSanitizer()
    text = "My email is afrin@example.com."
    result = sanitizer.sanitize(text)
    assert "[EMAIL REDACTED]" in result["sanitized_text"]
    assert "afrin@example.com" not in result["sanitized_text"]
    assert result["detected"] == True

def test_sanitizer_phone():
    sanitizer = AegisSanitizer()
    text = "Phone: 9876543210"
    result = sanitizer.sanitize(text)
    assert "[PHONE REDACTED]" in result["sanitized_text"]
    assert "9876543210" not in result["sanitized_text"]

def test_sanitizer_name():
    sanitizer = AegisSanitizer()
    text = "Name: Afrin Banu"
    result = sanitizer.sanitize(text)
    assert "[NAME REDACTED]" in result["sanitized_text"]
    assert "Afrin Banu" not in result["sanitized_text"]

def test_sanitizer_username():
    sanitizer = AegisSanitizer()
    text = "Username: afrin123"
    result = sanitizer.sanitize(text)
    assert "[USERNAME REDACTED]" in result["sanitized_text"]

def test_sanitizer_password():
    sanitizer = AegisSanitizer()
    text = "Password: MyPassword123"
    result = sanitizer.sanitize(text)
    assert "[PASSWORD REDACTED]" in result["sanitized_text"]

def test_sanitizer_bank():
    sanitizer = AegisSanitizer()
    text = "Bank Account: 123456789012"
    result = sanitizer.sanitize(text)
    assert "[BANK ACCOUNT REDACTED]" in result["sanitized_text"]

def test_sanitizer_card():
    sanitizer = AegisSanitizer()
    text = "Card Number: 4111111111111111"
    result = sanitizer.sanitize(text)
    assert "[CARD NUMBER REDACTED]" in result["sanitized_text"]

def test_sanitizer_pan():
    sanitizer = AegisSanitizer()
    text = "PAN: ABCDE1234F"
    result = sanitizer.sanitize(text)
    assert "[PAN REDACTED]" in result["sanitized_text"]

def test_sanitizer_aadhaar():
    sanitizer = AegisSanitizer()
    text = "Aadhaar: 1234 5678 9012"
    result = sanitizer.sanitize(text)
    assert "[AADHAAR REDACTED]" in result["sanitized_text"]

def test_sanitizer_address():
    sanitizer = AegisSanitizer()
    text = "Address: 12 Anna Nagar, Chennai."
    result = sanitizer.sanitize(text)
    assert "[ADDRESS REDACTED]" in result["sanitized_text"]

def test_sanitizer_dob():
    sanitizer = AegisSanitizer()
    text = "Date of Birth: 12/05/2004"
    result = sanitizer.sanitize(text)
    assert "[DOB REDACTED]" in result["sanitized_text"]

def test_sanitizer_ip():
    sanitizer = AegisSanitizer()
    text = "IP Address: 192.168.1.10"
    result = sanitizer.sanitize(text)
    assert "[IP ADDRESS REDACTED]" in result["sanitized_text"]

def test_sanitizer_passport():
    sanitizer = AegisSanitizer()
    text = "Passport: A12345678"
    result = sanitizer.sanitize(text)
    assert "[PASSPORT REDACTED]" in result["sanitized_text"]

def test_sanitizer_id():
    sanitizer = AegisSanitizer()
    text = "Student ID: STU2026001"
    result = sanitizer.sanitize(text)
    assert "[STUDENT ID REDACTED]" in result["sanitized_text"]

def test_sanitizer_license():
    sanitizer = AegisSanitizer()
    text = "Driver License: DL1234567890123"
    result = sanitizer.sanitize(text)
    assert "[DRIVING LICENCE REDACTED]" in result["sanitized_text"]

def test_sanitizer_token():
    sanitizer = AegisSanitizer()
    text = "API Key: abcdefghijklmnopqrstuvwxyz123456"
    result = sanitizer.sanitize(text)
    assert "[API KEY REDACTED]" in result["sanitized_text"]

def test_sanitizer_name_formats():
    sanitizer = AegisSanitizer()
    texts = [
        "Name: John Example",
        "Full Name: John Example",
        "My name is John Example",
        "Account Holder: John Example",
        "Name\nJohn Example"
    ]
    for text in texts:
        result = sanitizer.sanitize(text)
        assert "[NAME REDACTED]" in result["sanitized_text"], f"Failed to redact name in: {text}"

def test_sanitizer_dob_formats():
    sanitizer = AegisSanitizer()
    texts = [
        "DOB: 12/09/2003",
        "DOB: 12-09-2003",
        "DOB: 2003-09-12",
        "DOB: 12 September 2003",
        "DOB: 12 September, 2003",
        "DOB: 12 Sep 2003",
        "Date of Birth: 12 September 2003",
        "Birth Date: 12/09/2003",
        "Born: 12 September 2003",
        "Date of Birth\n12 September 2003"
    ]
    for text in texts:
        result = sanitizer.sanitize(text)
        assert "[DOB REDACTED]" in result["sanitized_text"], f"Failed to redact DOB in: {text}"

def test_sanitizer_ip_formats():
    sanitizer = AegisSanitizer()
    texts = [
        "IP: 192.168.1.100",
        "IP Address: 192.168.1.100",
        "Login IP: 192.168.1.100",
        "Your IP address is 192.168.1.100",
        "192.168.1.100"
    ]
    for text in texts:
        result = sanitizer.sanitize(text)
        assert "[IP ADDRESS REDACTED]" in result["sanitized_text"], f"Failed to redact IP in: {text}"

def test_sanitizer_false_positives():
    sanitizer = AegisSanitizer()
    texts = [
        "Microsoft",
        "Google",
        "Privacy Policy",
        "Security Settings",
        "Dashboard",
        "Order Date: 12/09/2026",
        "Meeting Date: 12 September 2026",
        "123456",
        "123.456",
        "123.456.789"
    ]
    for text in texts:
        result = sanitizer.sanitize(text)
        # It shouldn't redact anything except perhaps things that accidentally trigger, but we designed them not to.
        # Check that none of the texts were modified
        assert result["sanitized_text"] == text, f"False positive matched on: {text}"

def test_sanitizer_end_to_end():
    sanitizer = AegisSanitizer()
    text = (
        "Name: John Example\n"
        "Email: john@example.com\n"
        "Phone: +91 98765 43210\n"
        "DOB: 12 September 2003\n"
        "IP Address: 192.168.1.100\n"
        "Bank Account: 123456789012\n"
        "PAN: ABCDE1234F\n"
        "Username: john123\n"
        "Password: MyPassword123"
    )
    result = sanitizer.sanitize(text)
    
    assert "Name: [NAME REDACTED]" in result["sanitized_text"]
    assert "Email: [EMAIL REDACTED]" in result["sanitized_text"]
    assert "Phone: [PHONE REDACTED]" in result["sanitized_text"]
    assert "DOB: [DOB REDACTED]" in result["sanitized_text"]
    assert "IP Address: [IP ADDRESS REDACTED]" in result["sanitized_text"]
    assert "Bank Account: [BANK ACCOUNT REDACTED]" in result["sanitized_text"]
    assert "PAN: [PAN REDACTED]" in result["sanitized_text"]
    assert "Username: [USERNAME REDACTED]" in result["sanitized_text"]
    assert "Password: [PASSWORD REDACTED]" in result["sanitized_text"]
