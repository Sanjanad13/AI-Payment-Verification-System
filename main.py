from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import shutil
import os
import sqlite3
from forensics import analyze_tampering
from ocr_reader import extract_receipt_data

app = FastAPI(title="Payment Verification API")
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Payment API</title>
        </head>
        <body style="font-family: Arial, sans-serif; margin: 40px; text-align: center;">
            <h2>✅ AI Payment Verification API is Online</h2>
            <p>Welcome to the system. Click the button below to test uploading a receipt.</p>
            <br>
            <a href="/docs" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 5px;">
                Go to Testing Dashboard (/docs)
            </a>
        </body>
    </html>
    """
def setup_database():
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    
    # Create a table for Orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            expected_amount REAL,
            status TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS used_transactions (
            transaction_id TEXT PRIMARY KEY
        )
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO orders (order_id, expected_amount, status) 
        VALUES ('ORD-100', 105000.00, 'awaiting_payment')
    ''')
    
    conn.commit()
    conn.close()

setup_database()

@app.post("/verify-payment/{order_id}")
async def verify_payment(order_id: str, file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    fraud_check = analyze_tampering(file_location)
    
    receipt_data = extract_receipt_data(file_location)
    
    os.remove(file_location)
    
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    
    reasons = []
    
    if fraud_check["is_tampered"]:
        reasons.append(f"Image tampering detected (Score: {fraud_check['tamper_score']})")
        
    extracted_tx_id = receipt_data["transaction_id"]
    if not extracted_tx_id:
        reasons.append("Could not find a valid Transaction ID on receipt.")
    else:
        cursor.execute("SELECT * FROM used_transactions WHERE transaction_id = ?", (extracted_tx_id,))
        if cursor.fetchone():
            reasons.append(f"Duplicate receipt! ID {extracted_tx_id} was already used.")
            
    cursor.execute("SELECT expected_amount FROM orders WHERE order_id = ?", (order_id,))
    order_record = cursor.fetchone()
    
    if order_record:
        expected = order_record[0]
        if receipt_data["extracted_amount"] != expected:
            reasons.append(f"Amount mismatch. Expected ₹{expected}, found ₹{receipt_data['extracted_amount']}")
    else:
        reasons.append("Invalid Order ID.")
        
    if len(reasons) == 0:
        # If approved, save this new transaction ID to the database so it can't be reused!
        cursor.execute("INSERT INTO used_transactions (transaction_id) VALUES (?)", (extracted_tx_id,))
        conn.commit()
        conn.close()
        return {"verdict": "Approved", "trust_score": 99, "details": receipt_data}
    else:
        conn.close()
        return {"verdict": "Rejected", "trust_score": 10, "failures": reasons}
