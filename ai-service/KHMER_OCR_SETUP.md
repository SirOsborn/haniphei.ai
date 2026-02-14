# Khmer OCR Setup Guide

This guide will help you set up Khmer language support for OCR in the AI service.

## 📋 Prerequisites

- Tesseract OCR must be installed
- Windows users: Download from https://github.com/UB-Mannheim/tesseract/wiki

---

## 🇰🇭 Installing Khmer Language Data

### Step 1: Download Khmer Language File

1. Go to Tesseract language data repository:
   - **Best Quality (Recommended)**: https://github.com/tesseract-ocr/tessdata_best
   - **Fast (Alternative)**: https://github.com/tesseract-ocr/tessdata

2. Download `khm.traineddata`:
   - **Direct link (best quality)**: https://github.com/tesseract-ocr/tessdata_best/raw/main/khm.traineddata
   - File size: ~11 MB

### Step 2: Install Language File

**Windows:**
```powershell
# Default Tesseract installation path
Copy-Item khm.traineddata "C:\Program Files\Tesseract-OCR\tessdata\"
```

**Linux:**
```bash
sudo cp khm.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
```

**macOS:**
```bash
cp khm.traineddata /usr/local/share/tessdata/
```

### Step 3: Verify Installation

```powershell
tesseract --list-langs
```

**Expected output:**
```
List of available languages (3):
eng
khm
osd
```

You should see both `eng` (English) and `khm` (Khmer) in the list.

---

## ⚙️ Configuration

### Update your `.env` file:

```bash
# For both Khmer and English (recommended)
TESSERACT_LANG=eng+khm

# Or specify Tesseract path if not in PATH
# TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## 🧪 Testing Khmer OCR

### Test 1: English Text
```powershell
curl -X POST http://localhost:8082/scan `
  -F "text=The project requires payment within 30 days with 10% penalty"
```

### Test 2: Khmer Text
```powershell
curl -X POST http://localhost:8082/scan `
  -F "text=កិច្ចសន្យានេះតម្រូវឱ្យបង់ប្រាក់ក្នុងរយៈពេល ៣០ ថ្ងៃ ជាមួយនឹងការពិន័យ ១០%"
```

### Test 3: Mixed Khmer-English
```powershell
curl -X POST http://localhost:8082/scan `
  -F "text=កិច្ចសន្យា Contract requires payment ទូទាត់ប្រាក់ within 30 days"
```

### Test 4: Image/PDF with Khmer Text
```powershell
curl -X POST http://localhost:8082/scan `
  -F "file=@cambodian_contract.pdf"
```

**Expected Response:**
```json
{
  "data": [
    {
      "risk": "របៀបបង់ប្រាក់មិនច្បាស់លាស់ (Payment terms unclear)",
      "category": "Financial",
      "context": "កិច្ចសន្យាមិនបានបញ្ជាក់ច្បាស់អំពីកាលកំណត់នៃការទូទាត់"
    }
  ],
  "source": "llm"
}
```

---

## 🔍 Troubleshooting

### Error: "Failed loading language 'khm'"

**Cause:** Khmer language data not installed or in wrong location.

**Solution:**
1. Verify `khm.traineddata` exists in tessdata folder
2. Check file permissions (should be readable)
3. Restart your terminal/service after installation

### Error: "Tesseract is not installed"

**Solution:**
```powershell
# Check if Tesseract is in PATH
tesseract --version

# If not found, set TESSERACT_CMD in .env:
# TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Poor OCR Quality for Khmer Text

**Solutions:**
1. Use high-quality scanned images (300+ DPI)
2. Ensure good contrast between text and background
3. Consider using `tessdata_best` instead of `tessdata` for better accuracy
4. For handwritten Khmer, OCR accuracy will be limited

---

## 📊 Performance Notes

- **English-only text**: ~1-2 seconds per page
- **Khmer-only text**: ~2-3 seconds per page
- **Mixed Khmer-English**: ~2-4 seconds per page
- **Scanned PDFs**: OCR adds 3-5 seconds per page

---

## 🔗 Additional Resources

- **Tesseract Documentation**: https://tesseract-ocr.github.io/
- **Khmer Language Data**: https://github.com/tesseract-ocr/tessdata_best
- **Tesseract Training**: https://tesseract-ocr.github.io/tessdoc/Training-Tesseract.html

---

## ✅ Quick Checklist

- [ ] Tesseract OCR installed
- [ ] `khm.traineddata` downloaded
- [ ] Language file copied to tessdata folder
- [ ] Verified with `tesseract --list-langs`
- [ ] `.env` configured with `TESSERACT_LANG=eng+khm`
- [ ] AI service restarted
- [ ] Tested with Khmer text

**All done? You're ready to process Khmer contracts! 🎉**
