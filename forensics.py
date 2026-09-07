from PIL import Image, ImageChops, ImageEnhance
import os

def analyze_tampering(image_path, quality=90):
    try:
        original = Image.open(image_path).convert('RGB')
        temp_filename = 'temp_ela.jpg'
        
        original.save(temp_filename, 'JPEG', quality=quality)
        temporary = Image.open(temp_filename)
        
        diff = ImageChops.difference(original, temporary)
        
        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        
        if max_diff == 0:
            max_diff = 1
            
       
        score = (max_diff / 255.0) * 100
        
        os.remove(temp_filename) # Cleanup
        
        is_tampered = score > 95.0 
        
        return {
            "is_tampered": is_tampered,
            "tamper_score": round(score, 2)
        }
    except Exception as e:
        return {"is_tampered": True, "error": str(e)}
