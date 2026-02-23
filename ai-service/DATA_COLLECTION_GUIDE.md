# Data Collection Pipeline - Usage Guide

## Overview
This guide explains how to use the enhanced data collection pipeline to build your own risk analysis model and eventually stop using the Gemini API.

## Quick Start

### Step 1: Initial Setup
```bash
# Ensure AI service is configured
cd ai-service
cp .env.example .env

# Edit .env and set your Gemini API key
# GEMINI_API_KEY=your_key_here

# Make sure LLM is enabled for data collection
# USE_LLM=true
```

### Step 2: Start Collecting Data
```bash
# Start the AI service
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8082
```

Now upload documents through the `/scan` endpoint. Every document processed will be automatically stored with comprehensive metadata.

### Step 3: Monitor Data Collection
```bash
# Check collection statistics
curl http://localhost:8082/data/stats

# Validate data quality
curl http://localhost:8082/data/validate

# Identify quality issues
curl http://localhost:8082/data/quality-issues
```

### Step 4: Train Your Model
Once you have enough data (recommended: 50+ samples with diverse categories):
```bash
# Train the model
curl -X POST http://localhost:8082/train

# Response will show:
# {
#   "accuracy": 0.87,
#   "f1_micro": 0.85,
#   "meets_target": true
# }
```

### Step 5: Switch to Your Model
When accuracy meets your target (default: 0.85):
```bash
# Update .env
USE_LLM=false

# Restart service
# Now all requests will use your trained model instead of Gemini API
```

## Detailed Workflow

### Understanding the Data Flow

```
User Upload → OCR/Text Extraction → LLM Analysis → Multi-Level Storage
                                                    ↓
                                    ┌──────────────┼──────────────┐
                                    ↓              ↓              ↓
                            training.jsonl  metadata.jsonl  dedup_hashes.txt
                              (simple)      (enhanced)       (tracking)
                                    └──────────────┼──────────────┘
                                                   ↓
                                         Model Training Pipeline
                                                   ↓
                                           risk_model.joblib
```

### Data Collection Features

#### 1. Automatic Deduplication
The system prevents duplicate data collection:
- Computes SHA256 hash of normalized text
- Checks against existing hashes before storing
- Prevents reprocessing same document multiple times

#### 2. Language Detection
Automatically detects and tracks:
- Khmer documents (>70% Khmer characters)
- English documents (>70% English characters)
- Mixed language documents (both languages >15%)
- Language ratio tracking

#### 3. Document Classification
Automatically classifies documents into types:
- Construction contracts
- Employment contracts
- Scholarship agreements
- Loan agreements
- Sales contracts
- Rental agreements
- Service agreements
- Partnership agreements
- Policy documents
- Proposals
- General (unclassified)

#### 4. Feature Extraction
Extracts important features for model training:

**Numerical Indicators:**
- Currency presence ($, USD, ៛, រៀល)
- Percentages
- Dates
- Time durations

**Legal Indicators:**
- Legal keywords count
- Risk keywords count
- Numbered clauses
- Party identification

**Financial Indicators:**
- Payment terms
- Installment mentions

**Temporal Indicators:**
- Deadlines
- Timeframes

#### 5. Risk Analysis Storage
Stores comprehensive risk information:
- Risk description
- Risk category
- Supporting context
- Category counts
- Total risk count

### API Endpoints

#### POST /scan
**Primary endpoint for data collection**

Upload documents for risk analysis. Data is automatically collected and stored.

```bash
# Upload PDF
curl -X POST http://localhost:8082/scan \
  -F "file=@contract.pdf"

# Upload DOCX
curl -X POST http://localhost:8082/scan \
  -F "file=@agreement.docx"

# Upload Image (Khmer OCR)
curl -X POST http://localhost:8082/scan \
  -F "file=@scanned_contract.jpg"

# Analyze text directly (Khmer)
curl -X POST http://localhost:8082/scan \
  -F "text=កិច្ចសន្យានេះតម្រូវឱ្យបង់ប្រាក់ក្នុងរយៈពេល ៣០ ថ្ងៃ"

# Analyze text (English)
curl -X POST http://localhost:8082/scan \
  -F "text=Payment required within 30 days with 10% penalty for late payment"
```

#### GET /data/stats
**View collection statistics**

```bash
curl http://localhost:8082/data/stats
```

Response:
```json
{
  "total_samples": 127,
  "document_types": {
    "construction_contract": 45,
    "employment_contract": 32,
    "loan_agreement": 25,
    "sales_contract": 15,
    "general": 10
  },
  "languages": {
    "khmer": 58,
    "english": 42,
    "mixed": 27
  },
  "risk_categories": {
    "Financial": 156,
    "Schedule": 98,
    "Legal": 87,
    "Technical": 65,
    "Operational": 54,
    "Compliance": 32,
    "Other": 18
  },
  "avg_risks_per_doc": 3.5,
  "avg_text_length": 1456,
  "date_range": {
    "earliest": "2026-02-01T10:30:00",
    "latest": "2026-02-22T15:45:00"
  }
}
```

#### GET /data/validate
**Validate dataset quality**

```bash
curl http://localhost:8082/data/validate
```

Response:
```json
{
  "valid": true,
  "issues": [],
  "warnings": [
    "2 samples have text shorter than 50 chars (possible OCR failure)",
    "Underrepresented categories (< 10 samples): Compliance"
  ],
  "recommendations": [
    "BALANCE CLASSES: These categories need more samples: Compliance",
    "READY FOR TRAINING: Dataset quality is sufficient. Call /train endpoint"
  ]
}
```

#### GET /data/quality-issues
**Identify problematic samples**

```bash
curl http://localhost:8082/data/quality-issues
```

Response:
```json
{
  "total_issues": 3,
  "issues": [
    {
      "index": 15,
      "text_preview": "ព្រ...",
      "text_length": 35,
      "word_count": 5,
      "risk_count": 0,
      "reasons": [
        "Text too short (35 chars)",
        "Too few words (5)",
        "No risks identified"
      ]
    }
  ]
}
```

#### POST /train
**Train your model**

```bash
curl -X POST http://localhost:8082/train
```

Response:
```json
{
  "accuracy": 0.87,
  "f1_micro": 0.85,
  "meets_target": true
}
```

### Data Storage Structure

#### Location
All data is stored in `ai-service/data/` directory:
```
ai-service/data/
├── training.jsonl          # Simple format (backward compatible)
├── metadata.jsonl          # Enhanced format with features
└── dedup_hashes.txt        # Deduplication tracking
```

#### Training Data Format (training.jsonl)
```json
{
  "text": "Full document text...",
  "labels": ["Financial", "Schedule"],
  "raw": [
    {
      "risk": "Budget overrun",
      "category": "Financial",
      "context": "Supporting text from document"
    }
  ]
}
```

#### Metadata Format (metadata.jsonl)
See [DATA_SCHEMA.md](DATA_SCHEMA.md) for complete schema documentation.

### Best Practices

#### 1. Data Collection Phase
- **Collect diverse documents**: Mix contract types, languages, industries
- **Aim for 100+ samples** before production use
- **Balance categories**: Each risk category should have 10+ examples
- **Mix languages**: Collect both Khmer and English documents
- **Quality over quantity**: Better to have 50 good samples than 200 poor ones

#### 2. Monitoring Quality
- Check `/data/validate` regularly
- Review quality issues with `/data/quality-issues`
- Monitor statistics with `/data/stats`
- Aim for:
  - Average text length > 500 characters
  - Average risks per document: 2-5
  - Less than 5% "unknown" language detection
  - Less than 10% quality issues

#### 3. Training Strategy
- **First training**: After 50+ diverse samples
- **Check metrics**: Accuracy > 0.70 is good start
- **Iterate**: Continue collecting data, especially for underrepresented categories
- **Retrain regularly**: Every 50-100 new samples
- **Production ready**: Accuracy > 0.85, F1 > 0.80

#### 4. Transitioning from LLM to Model
```bash
# Phase 1: LLM-only (Bootstrapping)
USE_LLM=true
# Collect 50-100 samples

# Phase 2: Hybrid (Testing)
# Train model, keep LLM enabled for comparison
USE_LLM=true
# Test model predictions, collect more data

# Phase 3: Model-only (Production)
# Once accuracy meets target and validated
USE_LLM=false
# Save API costs, use your own model
```

### Data Quality Indicators

#### Good Quality Sample
```json
{
  "text_length": 1500,
  "word_count": 250,
  "risk_count": 3,
  "language": "khmer",
  "document_type": "construction_contract",
  "features": {
    "has_currency": true,
    "has_payment_terms": true,
    "legal_keyword_count": 5,
    "risk_keyword_count": 3
  }
}
```

#### Poor Quality Sample (should be removed)
```json
{
  "text_length": 25,
  "word_count": 4,
  "risk_count": 0,
  "language": "unknown",
  "document_type": "general",
  "features": {
    // All false or 0
  }
}
```

### Troubleshooting

#### Issue: "No training data available"
**Solution**: Upload documents through `/scan` endpoint first

#### Issue: Low accuracy (<0.70)
**Causes**:
- Not enough training data
- Imbalanced categories
- Low-quality samples
**Solutions**:
- Collect more diverse samples (aim for 100+)
- Balance underrepresented categories
- Clean low-quality samples

#### Issue: Model predictions too generic
**Cause**: Training on too similar documents
**Solution**: Diversify document types and risk patterns

#### Issue: Khmer text not recognized
**Causes**:
- Khmer language data not installed
- Poor scan quality
**Solutions**:
- Install `khm.traineddata` for Tesseract
- Use higher quality scans (300+ DPI)
- Ensure TESSERACT_LANG=eng+khm in .env

#### Issue: Duplicate data being collected
**Expected**: System automatically prevents duplicates
**Check**: Verify `dedup_hashes.txt` is being created
**Reset**: Delete `dedup_hashes.txt` to allow recollection

### Performance Optimization

#### For Training Speed
- Use subset of data for quick iterations
- Reduce `max_features` in TF-IDF (currently 20000)
- Adjust `ngram_range` (currently 1-2)

#### For Prediction Speed
- Once model is trained, USE_LLM=false is much faster
- No API calls, instant local prediction
- Can handle high request volume

#### For Storage
- JSONL format is efficient and append-only
- Each line is independent (easy to process)
- Can be compressed with gzip if needed

### Cost Analysis

#### Using Gemini API
- Free tier: 15 requests/min, 1,500/day
- After free tier: $0.15-0.30 per 1,000 requests
- 10,000 documents/month ≈ $1.50-$3.00/month

#### Using Your Model
- One-time training cost: ~5-10 minutes
- Prediction cost: Nearly zero (CPU only)
- 10,000 documents/month ≈ $0.00
- **Savings**: 100% after initial data collection

### Next Steps

1. **Start Collecting**: Upload your first 10-20 documents
2. **Monitor Quality**: Check `/data/validate` regularly
3. **Diversify**: Ensure variety in document types and languages
4. **Train**: When you have 50+ good samples
5. **Evaluate**: Check accuracy and F1 scores
6. **Iterate**: Continue collecting for underrepresented categories
7. **Deploy**: Switch to USE_LLM=false when ready
8. **Maintain**: Periodically retrain with new data

## Support

For detailed technical documentation:
- [DATA_SCHEMA.md](DATA_SCHEMA.md) - Complete data schema reference
- [README.md](README.md) - AI service overview
- [../backend/docs/AI_SERVICE_INTEGRATION.md](../backend/docs/AI_SERVICE_INTEGRATION.md) - Backend integration

## Summary

The enhanced data collection pipeline ensures:
✅ Clean, structured data from day one
✅ No manual cleaning required
✅ Rich metadata for better model training
✅ Automatic deduplication
✅ Quality validation and recommendations
✅ Seamless transition from LLM to your own model
✅ Cost savings and self-sustainability

**Your path to independence from expensive APIs starts with every document you upload!**
