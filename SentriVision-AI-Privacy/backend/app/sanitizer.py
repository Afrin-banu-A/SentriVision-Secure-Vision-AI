import re

def validate_luhn(card_number):
    # Remove non-digits
    digits = [int(c) for c in card_number if c.isdigit()]
    if not digits or len(digits) < 13: return False
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9: d -= 9
        checksum += d
    return checksum % 10 == 0

class AegisSanitizer:
    def __init__(self):
        # We define explicit regex patterns for different PII types with their target capture groups.
        # This covers Personal, Identity, Banking, Cards, UPI, Transaction, and Digital Secrets.
        self.patterns = [
            # ---------------- PERSONAL INFORMATION ----------------
            {
                "type": "NAME",
                "pattern": r"(?i)(?:\bName\b|\bFull Name\b|\bCustomer Name\b|\bAccount Holder\b|\bBeneficiary Name\b|\bFirst Name\b|\bLast Name\b)[\s]*:?[\s]*([A-Z][a-zA-Z\-\'.]*(?:[ \t]+[A-Z][a-zA-Z\-\'.]*)*)",
                "group": 1
            },
            {
                "type": "EMAIL",
                "pattern": r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b",
                "group": 0
            },
            {
                "type": "PHONE",
                "pattern": r"(?i)(?:\bPhone\b|\bMobile\b|\bContact\b|\bCall\b)[\s]*:?[\s]*(\+?\d{1,3}[\s-]?\d{4,5}[\s-]?\d{4,5}|\d{10})",
                "group": 1
            },
            {
                "type": "ADDRESS",
                "pattern": r"(?i)(?<!\bip\s)(?<!\bemail\s)(?:\bAddress\b|\bHome Address\b|\bLive At\b)[\s]*:[\s]*([^\r\n]+)",
                "group": 1
            },
            {
                "type": "DOB",
                "pattern": r"(?i)(?:\bDate of Birth\b|\bDOB\b|\bBirth Date\b|\bBorn\b)[\s]*:?[\s]*([0-9]{1,4}[-/. ][a-zA-Z0-9, \-/.]{2,15}[0-9]{1,4})",
                "group": 1
            },
            {
                "type": "IP ADDRESS",
                "pattern": r"(?i)(?:(?:\bIP Address\b|\bIP\b)(?:[\s]*:?[\s]*|\s+is\s+))?((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))",
                "group": 1
            },
            {
                "type": "STUDENT ID",
                "pattern": r"(?i)(?:\bStudent ID\b)[\s]*:?[\s]*([a-zA-Z0-9_-]+)",
                "group": 1
            },
            {
                "type": "EMPLOYEE ID",
                "pattern": r"(?i)(?:\bEmployee ID\b)[\s]*:?[\s]*([a-zA-Z0-9_-]+)",
                "group": 1
            },

            # ---------------- INDIAN IDENTITY / KYC ----------------
            {
                "type": "PAN",
                "pattern": r"(?i)(?:\bPAN\b|\bPAN Number\b|\bPermanent Account Number\b)[\s]*:?[\s]*([A-Z]{5}[0-9]{4}[A-Z]{1})",
                "group": 1
            },
            {
                "type": "AADHAAR",
                "pattern": r"(?i)(?:\bAadhaar\b|\bAadhar\b|\bAadhaar Number\b)[\s]*:?[\s]*([0-9]{4}[\s-]*[0-9]{4}[\s-]*[0-9]{4})",
                "group": 1
            },
            {
                "type": "PASSPORT",
                "pattern": r"(?i)(?:\bPassport\b|\bPassport Number\b)[\s]*:?[\s]*([A-Z]{1,2}[0-9]{7,8})",
                "group": 1
            },
            {
                "type": "DRIVING LICENCE",
                "pattern": r"(?i)(?:\bDriving Licence\b|\bDriving License\b|\bDriver License\b|\bDL Number\b)[\s]*:?[\s]*([A-Z0-9\s-]{10,20})",
                "group": 1
            },
            {
                "type": "VOTER ID",
                "pattern": r"(?i)(?:\bVoter ID\b|\bEPIC\b|\bEPIC Number\b)[\s]*:?[\s]*([A-Z0-9]{10,15})",
                "group": 1
            },
            {
                "type": "GSTIN",
                "pattern": r"(?i)(?:\bGSTIN\b|\bGST Number\b|\bTax Identification Number\b)[\s]*:?[\s]*([0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1})",
                "group": 1
            },
            {
                "type": "CUSTOMER ID",
                "pattern": r"(?i)(?:\bCustomer ID\b|\bCIF Number\b|\bCIF\b|\bKYC ID\b|\bBank Customer ID\b)[\s]*:?[\s]*([a-zA-Z0-9_-]+)",
                "group": 1
            },

            # ---------------- BANKING INFORMATION ----------------
            {
                "type": "BANK ACCOUNT",
                "pattern": r"(?i)(?:\bAccount Number\b|\bAccount No\b|\bA/C Number\b|\bA/C No\b|\bBank Account\b|\bSavings Account\b|\bCurrent Account\b|\bLoan Account\b|\bCredit Account\b|\bFixed Deposit\b|\bRecurring Deposit\b|\bBeneficiary Account\b|\bSender Account\b|\bReceiver Account\b)[\s]*:?[\s]*([0-9]{8,18})",
                "group": 1
            },
            {
                "type": "IBAN",
                "pattern": r"(?i)(?:\bIBAN\b)[\s]*:?[\s]*([A-Z]{2}[0-9]{2}[\sA-Z0-9]{11,30})",
                "group": 1
            },
            {
                "type": "IFSC",
                "pattern": r"(?i)(?:\bIFSC\b|\bIFSC Code\b)[\s]*:?[\s]*([A-Z]{4}0[A-Z0-9]{6})",
                "group": 1
            },
            {
                "type": "MICR",
                "pattern": r"(?i)(?:\bMICR\b|\bMICR Code\b)[\s]*:?[\s]*([0-9]{9})",
                "group": 1
            },
            {
                "type": "SWIFT CODE",
                "pattern": r"(?i)(?:\bSWIFT\b|\bBIC\b|\bSWIFT Code\b)[\s]*:?[\s]*([A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?)",
                "group": 1
            },
            {
                "type": "ROUTING NUMBER",
                "pattern": r"(?i)(?:\bRouting Number\b|\bSort Code\b|\bBranch Code\b)[\s]*:?[\s]*([0-9]{6,9})",
                "group": 1
            },

            # ---------------- LOGIN CREDENTIALS ----------------
            {
                "type": "USERNAME",
                "pattern": r"(?i)(?:\bUsername\b|\bUser ID\b|\bLogin ID\b|\bInternet Banking Username\b)[\s]*:[\s]*([a-zA-Z0-9_.-]+)",
                "group": 1
            },
            {
                "type": "PASSWORD",
                "pattern": r"(?i)(?:\bPassword\b|\bBanking Password\b|\bTransaction Password\b|\bPasscode\b)[\s]*:[\s]*([^\s]+)",
                "group": 1
            },
            {
                "type": "CARD PIN",
                "pattern": r"(?i)(?:\bPIN\b|\bATM PIN\b|\bDebit Card PIN\b|\bCredit Card PIN\b|\bSecurity PIN\b|\bMPIN\b|\bTPIN\b|\bTransaction PIN\b)[\s]*:?[\s]*([0-9]{4,6})",
                "group": 1
            },
            {
                "type": "OTP",
                "pattern": r"(?i)(?:\bOTP\b|\bTransaction OTP\b|\bVerification Code\b)[\s]*:?[\s]*([a-zA-Z0-9]{4,8})",
                "group": 1
            },
            {
                "type": "SECURITY QUESTION",
                "pattern": r"(?i)(?:\bSecurity Answer\b|\bMother's maiden name\b|\bFirst pet\b|\bSecurity Question\b)[\s]*:[\s]*([^\n]+)",
                "group": 1
            },
            {
                "type": "RECOVERY CODE",
                "pattern": r"(?i)(?:\bRecovery Code\b|\bRecovery Token\b)[\s]*:?[\s]*([a-zA-Z0-9_.-]{6,})",
                "group": 1
            },
            
            # ---------------- CARD INFORMATION ----------------
            {
                "type": "CARD NUMBER",
                "pattern": r"(?i)(?:\bCard Number\b|\bCard No\b|\bCredit Card\b|\bDebit Card\b|\bATM Card\b|\bVirtual Card\b)[\s]*:?[\s]*([0-9]{4}[\s-]*[0-9]{4}[\s-]*[0-9]{4}[\s-]*[0-9]{4,7})",
                "group": 1,
                "validator": validate_luhn
            },
            {
                "type": "CARD EXPIRY",
                "pattern": r"(?i)(?:\bExpiry\b|\bCard Expiry\b|\bExpiration\b|\bExpiration Date\b)[\s]*:?[\s]*([0-9]{2}/[0-9]{2,4})",
                "group": 1
            },
            {
                "type": "CVV",
                "pattern": r"(?i)(?:\bCVV\b|\bCVC\b|\bCID\b)[\s]*:?[\s]*([0-9]{3,4})",
                "group": 1
            },

            # ---------------- UPI / PAYMENT ----------------
            {
                "type": "UPI ID",
                "pattern": r"(?i)(?:\bUPI ID\b|\bVPA\b|\bUPI\b)[\s]*:?[\s]*([a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64})",
                "group": 1
            },
            {
                "type": "UPI PIN",
                "pattern": r"(?i)(?:\bUPI PIN\b)[\s]*:?[\s]*([0-9]{4,6})",
                "group": 1
            },
            {
                "type": "TRANSACTION ID",
                "pattern": r"(?i)(?:\bTransaction ID\b|\bTransaction Reference\b|\bUPI Transaction ID\b|\bUPI Reference Number\b|\bPayment ID\b|\bTransfer Reference\b|\bOrder Number\b|\bPayment Number\b|\bPayment Authorization Code\b)[\s]*:?[\s]*([a-zA-Z0-9_-]{8,30})",
                "group": 1
            },
            {
                "type": "UTR",
                "pattern": r"(?i)(?:\bUTR\b|\bRRN\b|\bUPI RRN\b|\bPayment Reference\b)[\s]*:?[\s]*([a-zA-Z0-9]{12,22})",
                "group": 1
            },
            {
                "type": "PAYMENT TOKEN",
                "pattern": r"(?i)(?:\bPayment Token\b|\bWallet ID\b|\bWallet Account\b)[\s]*:?[\s]*([a-zA-Z0-9_-]+)",
                "group": 1
            },
            {
                "type": "TRANSACTION AMOUNT",
                "pattern": r"(?i)(?:\bTransaction Amount\b|\bLast Transaction\b|\bLoan Amount\b|\bCredit Limit\b|\bIncome\b|\bSalary\b)[\s]*:?[\s]*([₹$€£]?\s*[0-9.,]+)",
                "group": 1
            },
            {
                "type": "TRANSACTION DATE",
                "pattern": r"(?i)(?:\bTransaction Date\b|\bTransaction Time\b)[\s]*:?[\s]*([0-9]{1,4}[-/. ][a-zA-Z0-9, \-/.]{2,15}[0-9]{1,4})",
                "group": 1
            },

            # ---------------- FINANCIAL INFORMATION ----------------
            {
                "type": "FINANCIAL ID",
                "pattern": r"(?i)(?:\bDemat ID\b|\bClient ID\b|\bPolicy Number\b|\bInvestment Account\b)[\s]*:?[\s]*([a-zA-Z0-9_-]+)",
                "group": 1
            },

            # ---------------- DIGITAL SECRETS ----------------
            {
                "type": "API KEY",
                "pattern": r"(?i)(?:\bAPI Key\b|\bCloud Access Key\b)[\s]*:?[\s]*([a-zA-Z0-9_-]{16,64})",
                "group": 1
            },
            {
                "type": "ACCESS TOKEN",
                "pattern": r"(?i)(?:\bAccess Token\b|\bAuthorization Token\b|\bBearer Token\b)[\s]*:?[\s]*([a-zA-Z0-9_.-]{20,})",
                "group": 1
            },
            {
                "type": "REFRESH TOKEN",
                "pattern": r"(?i)(?:\bRefresh Token\b)[\s]*:?[\s]*([a-zA-Z0-9_.-]{20,})",
                "group": 1
            },
            {
                "type": "SESSION TOKEN",
                "pattern": r"(?i)(?:\bSession ID\b|\bSession Token\b)[\s]*:?[\s]*([a-zA-Z0-9_.-]{16,})",
                "group": 1
            },
            {
                "type": "JWT",
                "pattern": r"(?i)(?:\bJWT\b)[\s]*:?[\s]*([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)",
                "group": 1
            },
            {
                "type": "PRIVATE KEY",
                "pattern": r"(?i)(?:\bPrivate Key\b|\bSecret Key\b|\bSecret\b|\bWebhook Secret\b)[\s]*:?[\s]*([a-zA-Z0-9_.-]{16,})",
                "group": 1
            }
        ]

    def sanitize(self, text: str):
        original_text = text
        sanitized_text = text
        detected_entities = []
        
        # Stopwords to prevent false positive matches on context-aware boundaries
        stopwords = {'is', 'are', 'was', 'were', 'the', 'a', 'an', 'and', 'or', 'of', 'in', 'to'}
        
        for p in self.patterns:
            # 1. Find all existing placeholders to prevent overlapping matches (Idempotency fix)
            placeholder_spans = []
            for m in re.finditer(r'\[[A-Z\s]+ REDACTED\]', sanitized_text):
                placeholder_spans.append(m.span())

            matches = re.finditer(p["pattern"], sanitized_text, flags=re.IGNORECASE)
            
            valid_matches = []
            for match in matches:
                target_val = match.group(p["group"]).strip()
                if not target_val or target_val.lower() in stopwords:
                    continue
                
                # Layer 4/5: Check validation if any (e.g., Luhn check)
                if "validator" in p and not p["validator"](target_val):
                    continue
                
                # Check overlap: if target value overlaps with an already-redacted placeholder, skip it.
                overlap = False
                start, end = match.span(p["group"])
                for p_start, p_end in placeholder_spans:
                    if max(start, p_start) < min(end, p_end):
                        overlap = True
                        break
                
                if not overlap:
                    valid_matches.append((start, end, target_val))
            
            # 2. Reverse sort matches by start index to allow safe substring replacement
            valid_matches.sort(key=lambda x: x[0], reverse=True)
            for start, end, target_val in valid_matches:
                placeholder = f"[{p['type']} REDACTED]"
                sanitized_text = sanitized_text[:start] + placeholder + sanitized_text[end:]
                
                # Avoid duplicate entity logging for the same placeholder in the same position
                # (though reverse replacement intrinsically handles it well)
                detected_entities.append({"type": p["type"], "placeholder": placeholder})
                        
        return {
            "detected": len(detected_entities) > 0,
            "original_length": len(original_text),
            "sanitized_length": len(sanitized_text),
            "sanitized_text": sanitized_text,
            "entities": detected_entities,
            "protected_count": len(detected_entities)
        }
