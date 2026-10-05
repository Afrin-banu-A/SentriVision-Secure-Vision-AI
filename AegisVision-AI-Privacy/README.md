# Sentrivision - ML-Based AI-Safe Webpage Privacy Protection
Sentrivision addresses the privacy gap in AI-enabled web browsing. Traditional webpage interaction exposes the same page representation to both the human and an AI system. Sentrivision separates these two views.

The human retains access to the original webpage, while a local privacy gateway uses TF-IDF and Logistic Regression to classify sensitive context. Deterministic entity detection then identifies specific PII and credentials and replaces them with semantic placeholders.

Only the resulting AI-safe representation is forwarded to the AI-facing backend.

## Project Architecture

1.  **Synthetic Dataset:** Generated a custom dataset of normal web text and text containing sensitive PII across multiple categories.
2.  **ML Model Pipeline (TF-IDF & Logistic Regression):** An offline NLP pipeline using `TfidfVectorizer` and `LogisticRegression` to classify text blocks as `NORMAL` or `SENSITIVE`. The model achieved 1.0 accuracy on the synthetic evaluation dataset.
3.  **Local Privacy Gateway (FastAPI):** A local backend containing an ML endpoint and a layered, context-aware `AegisSanitizer` to perform PII detection and strict idempotency checks. It sanitizes 123+ different types of personal, financial, and digital credentials by replacing them with safe placeholders like `[BANK ACCOUNT REDACTED]`.
4.  **AI Simulator:** An endpoint simulating a cloud AI-facing backend that explicitly rejects raw PII to strictly enforce the privacy boundary.
5.  **Chrome Extension:** A browser extension that acts as the Human View. It reads text from the active tab and routes it through the Local Privacy Gateway before it reaches the AI Simulator, preserving the original webpage DOM. The popup exposes both the Human View description and the AI View output.
6.  **Demo Webpage:** A locally hosted mock banking dashboard demonstrating the extension protecting comprehensive credential categories.

## Privacy Boundary

SentriVision sanitizes webpage content before it reaches the demonstrated AI-facing backend. The core principle is **HUMAN VIEW ≠ AI VIEW**. The human sees the original webpage, while the local privacy gateway processes the raw webpage content securely on the client-side. The AI-facing backend receives ONLY the sanitized representation, ensuring credentials, banking details, and secrets never leak to external AI providers.

## Setup Instructions

### Prerequisites
- Python 3.9+
- `uv` (recommended for fast package management)

### 1. Install Dependencies
```bash
uv venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt
```

### 2. Generate Dataset and Train Model
If the `models/` directory does not contain `text_classifier.pkl`, you can regenerate them:
```bash
python data/generate_dataset.py
python ml/train.py
```

### 3. Run the Backend API
Start the FastAPI Local Privacy Gateway:
```bash
uvicorn backend.app.main:app --reload --port 8000
```
*The backend will be available at http://127.0.0.1:8000*

### 4. Run the Demo Page
In a new terminal window, serve the demo page:
```bash
python -m http.server 5500 --directory demo
```
*The demo will be available at http://127.0.0.1:5500/demo.html*

### 5. Install the Chrome Extension
1. Open Google Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** in the top right.
3. Click **Load unpacked**.
4. Select the `extension/` directory in this project.

## How to Demo

1. Ensure the Backend API is running (`uvicorn ...`).
2. Navigate to `http://127.0.0.1:5500/demo.html` in your browser.
3. Click the **SentriVision** extension icon in your Chrome toolbar.
4. The extension will show "Connected" for the Backend Status.
5. Click **SEND PAGE TO AI**.
6. The extension will extract the text, send it to the local gateway, which redacts the PII, and sends the sanitized version to the AI Simulator.
7. The extension popup will display the sanitized output that the AI received (proving no raw PII leaked).

## Automated Testing

This project includes a comprehensive test suite to validate dataset uniqueness, model behavior, sanitizer regex accuracy, API endpoints, and the complete privacy flow.

Run the tests using `pytest`:
```bash
pytest tests/ -v
```

## Supported PII Categories (123+ Items)

SentriVision uses a layered context-aware detection engine to identify and sanitize:
- **Banking Information**: Bank Account, IBAN, IFSC, MICR, SWIFT Code, Routing Number, Account Holder Name, Bank Customer ID.
- **Login Credentials**: Username, Password, Security Question/Answer, Recovery Code, Login IP.
- **Card Information**: Card Number (with Luhn validation), Card Expiry, CVV, Card PIN (ATM PIN, Debit PIN, MPIN, TPIN), OTP.
- **UPI & Payment**: UPI ID, UPI PIN, Transaction ID, UTR, Payment Token, Transaction Amount, Transaction Date.
- **Personal Information**: Name, Email, Phone, Address, Date of Birth, IP Address.
- **Identity & KYC**: PAN, Aadhaar, Passport, Driving Licence, Voter ID, GSTIN, Employee ID, Student ID.
- **Digital Secrets**: API Key, Access Token, Refresh Token, Session Token, JWT, Private Key, Webhook Secret.
- **Financial Information**: Demat ID, Client ID, Policy Number.

## Limitations and Future Work

SentriVision demonstrates protection before content reaches the AI-facing backend in this prototype. It does not claim universal interception of every commercial AI service or browser agent.

Future work includes dynamic interception of browser requests without requiring a popup click, and expanding the ML models beyond traditional TF-IDF + Logistic Regression to Transformer-based NLP pipelines for higher real-world contextual accuracy.
