# AI-Payment-Verification-System
An AI-powered FastAPI microservice that extracts text via OCR and detects tampered payment receipts.
# AI-Automated Payment Proof Verification System 🚀

## Business Problem
Retail businesses that accept manual bank transfers frequently fall victim to transactional fraud. Bad actors submit tampered payment screenshots (altering the amount or date via Photoshop) or reuse old transaction IDs to claim high-value goods without paying.

## Solution
This project is an AI-powered automated verification pipeline built with **Python** and **FastAPI**. It ingests customer-submitted payment proofs, extracts text data using OCR, runs forensic checks for image tampering, and validates the transaction against an SQLite database in real-time.

##  Technology Stack
* **Framework:** FastAPI / Python
* **Data Extraction:** Tesseract OCR / Regex
* **Image Forensics:** Pillow (PIL) / Error Level Analysis (ELA)
* **Database:** SQLite
* **Server:** Uvicorn

##  Key Features
1. **Optical Character Recognition (OCR):** Automatically reads the Total Amount and Reference ID from uploaded receipts.
2. **Fraud Forensics:** Detects pixel inconsistencies and copy-pasted text indicating Photoshop manipulation.
3. **Cross-Verification Database:** Blocks duplicate transaction IDs and rejects orders if the extracted amount does not exactly match the expected database amount.

##  How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Sanjanad13/AI-Payment-Verification-System.git](https://github.com/Sanjanad13/AI-Payment-Verification-System.git)
