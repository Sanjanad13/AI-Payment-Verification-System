import pytesseract
from PIL import Image
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_receipt_data(image_path):
    raw_text = pytesseract.image_to_string(Image.open(image_path))
    
    amount_match = re.search(r'(?:₹|Rs\.?|INR)\s*(\d+(?:\.\d{1,2})?)', raw_text, re.IGNORECASE)
    amount = float(amount_match.group(1)) if amount_match else 0.00
    
    tx_match = re.search(r'(?:Ref|ID)[\s:]*([A-Z0-9]+})', raw_text, re.IGNORECASE)
    tx_id = tx_match.group(1) if tx_match else None
    
    return {
        "extracted_amount": amount,
        "transaction_id": tx_id
    }
