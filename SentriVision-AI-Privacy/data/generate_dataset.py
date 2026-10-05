import pandas as pd
import random
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Normal sentences components
subjects = ["Machine learning", "Artificial intelligence", "Python", "Java", "C++", "Data science", "Deep learning", "Web development", "Software engineering", "Cloud computing", "The weather", "The sky", "The sun", "The application", "The system", "This program"]
verbs = ["is", "can be", "provides", "creates", "helps with", "improves", "optimizes", "analyzes", "evaluates", "generates", "looks like", "seems to be", "appears as", "works as"]
objects = ["a useful tool", "a great technology", "an interesting concept", "data analysis", "text classification", "natural language processing", "computer vision", "predictive modeling", "software architecture", "good today", "bright", "sunny", "approved", "pending", "completed"]

# Sensitive components generators
first_names = ["Afrin", "John", "Jane", "Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Mallory", "Nina", "Oscar", "Peggy", "Sybil", "Trent", "Victor", "Walter"]
last_names = ["Banu", "Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson"]
domains = ["example.com", "test.org", "demo.net", "sample.co", "mail.com", "email.net"]
cities = ["Chennai", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "New York", "London", "Tokyo", "Sydney", "Paris"]
streets = ["Anna Nagar", "MG Road", "Main Street", "Park Avenue", "Broadway", "High Street"]

def generate_normal_sentence():
    return f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)}."

def generate_sensitive_name():
    first = random.choice(first_names)
    last = random.choice(last_names)
    formats = [
        f"Name: {first}",
        f"Name: {first} {last}",
        f"Full Name: {first} {last}",
        f"My name is {first}.",
        f"Name - {first}",
        f"First Name: {first}, Last Name: {last}"
    ]
    return random.choice(formats)

def generate_sensitive_email():
    first = random.choice(first_names).lower()
    last = random.choice(last_names).lower()
    domain = random.choice(domains)
    formats = [
        f"Email: {first}@{domain}",
        f"My email is {first}.{last}@{domain}",
        f"Contact me at {first}{random.randint(1,99)}@{domain}",
        f"email = {first}@{domain}"
    ]
    return random.choice(formats)

def generate_sensitive_phone():
    phone = f"{random.randint(6,9)}{random.randint(100000000, 999999999)}"
    formats = [
        f"Phone: {phone}",
        f"My phone number is {phone}.",
        f"Call me at {phone}",
        f"Mobile: +91-{phone}"
    ]
    return random.choice(formats)

def generate_sensitive_username():
    first = random.choice(first_names).lower()
    formats = [
        f"Username: {first}{random.randint(10,999)}",
        f"User ID: {first}_{random.randint(10,999)}",
        f"Login username: {first}{random.randint(10,999)}"
    ]
    return random.choice(formats)

def generate_sensitive_password():
    formats = [
        f"Password: MyPassword{random.randint(100,999)}",
        f"password = Secret{random.randint(100,999)}!",
        f"Login password is Pass{random.randint(100,999)}"
    ]
    return random.choice(formats)

def generate_sensitive_bank():
    acct = f"{random.randint(100000000000, 999999999999)}"
    formats = [
        f"Bank Account: {acct}",
        f"Account Number: {acct}",
        f"My bank account is {acct}."
    ]
    return random.choice(formats)

def generate_sensitive_card():
    card = f"{random.randint(4000, 5000)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
    formats = [
        f"Card Number: {card}",
        f"Credit Card: {card}",
        f"My card is {card}"
    ]
    return random.choice(formats)

def generate_sensitive_pan():
    letters1 = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))
    nums = "".join(random.choices("0123456789", k=4))
    letter2 = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    pan = f"{letters1}{nums}{letter2}"
    formats = [
        f"PAN: {pan}",
        f"PAN Card: {pan}",
        f"My PAN is {pan}"
    ]
    return random.choice(formats)

def generate_sensitive_aadhaar():
    aadhaar = f"{random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"
    formats = [
        f"Aadhaar: {aadhaar}",
        f"Aadhaar Number: {aadhaar}",
        f"My Aadhaar is {aadhaar}"
    ]
    return random.choice(formats)

def generate_sensitive_address():
    city = random.choice(cities)
    street = random.choice(streets)
    num = random.randint(1, 999)
    formats = [
        f"Address: {num} {street}, {city}",
        f"I live at {num} {street}, {city}",
        f"Home Address: {num} {street}, {city}"
    ]
    return random.choice(formats)

def generate_sensitive_dob():
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(1950, 2010)
    formats = [
        f"Date of Birth: {d:02d}/{m:02d}/{y}",
        f"DOB: {y}-{m:02d}-{d:02d}",
        f"I was born on {d:02d}-{m:02d}-{y}"
    ]
    return random.choice(formats)
    
def generate_sensitive_ip():
    ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    formats = [
        f"IP Address: {ip}",
        f"My IP is {ip}",
        f"Server IP: {ip}"
    ]
    return random.choice(formats)

def generate_sensitive_passport():
    letters = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=1))
    nums = "".join(random.choices("0123456789", k=7))
    passport = f"{letters}{nums}"
    formats = [
        f"Passport Number: {passport}",
        f"Passport: {passport}",
        f"My passport is {passport}"
    ]
    return random.choice(formats)

def generate_sensitive_id():
    id_num = f"STU{random.randint(2000, 2026)}{random.randint(100, 999)}"
    formats = [
        f"Student ID: {id_num}",
        f"Employee ID: EMP{random.randint(1000, 9999)}",
        f"My ID is {id_num}"
    ]
    return random.choice(formats)

def generate_sensitive_license():
    license_num = f"DL{random.randint(10, 99)}{random.randint(10000000000, 99999999999)}"
    formats = [
        f"Driver License: {license_num}",
        f"DL Number: {license_num}",
        f"My driving license is {license_num}"
    ]
    return random.choice(formats)

def generate_sensitive_security_answer():
    formats = [
        f"Security Answer: Fluffy",
        f"Mother's maiden name: Smith",
        f"First pet: Sparky"
    ]
    return random.choice(formats)

def generate_sensitive_token():
    token = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=32))
    formats = [
        f"API Key: {token}",
        f"Access Token: {token}",
        f"Bearer Token: {token}",
        f"Secret Token: {token}"
    ]
    return random.choice(formats)

sensitive_generators = [
    generate_sensitive_name, generate_sensitive_email, generate_sensitive_phone,
    generate_sensitive_username, generate_sensitive_password, generate_sensitive_bank,
    generate_sensitive_card, generate_sensitive_pan, generate_sensitive_aadhaar,
    generate_sensitive_address, generate_sensitive_dob, generate_sensitive_ip,
    generate_sensitive_passport, generate_sensitive_id, generate_sensitive_license,
    generate_sensitive_security_answer, generate_sensitive_token
]

def main():
    data = []
    seen_texts = set()
    
    # Generate NORMAL
    while len(data) < 300:
        text = generate_normal_sentence()
        if text not in seen_texts:
            data.append({"text": text, "label": "NORMAL"})
            seen_texts.add(text)
            
    # Generate SENSITIVE
    sensitive_count = 0
    while sensitive_count < 300:
        generator = random.choice(sensitive_generators)
        text = generator()
        if text not in seen_texts:
            data.append({"text": text, "label": "SENSITIVE"})
            seen_texts.add(text)
            sensitive_count += 1
            
    # Shuffle dataset
    random.shuffle(data)
    
    df = pd.DataFrame(data)
    df.to_csv("data/sensitive_text_dataset.csv", index=False)
    print(f"Generated {len(df)} samples (NORMAL: 300, SENSITIVE: 300).")

if __name__ == "__main__":
    main()
