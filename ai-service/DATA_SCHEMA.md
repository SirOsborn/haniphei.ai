# Training Data Schema Documentation

## Overview
This document describes the data collection pipeline and storage schema for training the risk analysis model. The system collects comprehensive metadata and features to enable effective model training without extensive data cleaning later.

## Storage Files

### 1. `data/training.jsonl`
**Purpose**: Backward-compatible training data in simple format  
**Format**: JSON Lines (one JSON object per line)

**Schema**:
```json
{
  "text": "Full extracted document text",
  "labels": ["Financial", "Schedule"],  // Unique risk categories
  "raw": [  // Original LLM risk analysis
    {
      "risk": "Budget overrun",
      "category": "Financial",
      "context": "Supporting context from document"
    }
  ]
}
```

### 2. `data/metadata.jsonl`
**Purpose**: Comprehensive metadata for advanced training and analytics  
**Format**: JSON Lines (one JSON object per line)

**Schema**:
```json
{
  "text_hash": "sha256_hash_of_normalized_text",
  "file_hash": "sha256_hash_of_original_file",
  "timestamp": "2026-02-22T10:30:00.000000",
  "source_type": "upload|api|manual",
  "filename": "contract.pdf",
  
  "document_type": "construction_contract|employment_contract|...",
  "language": "khmer|english|mixed|unknown",
  "language_mix": true,
  "khmer_ratio": 0.65,
  "english_ratio": 0.35,
  
  "features": {
    "has_currency": true,
    "has_percentage": true,
    "has_date": true,
    "has_duration": true,
    "legal_keyword_count": 5,
    "risk_keyword_count": 3,
    "has_numbered_clauses": true,
    "has_party_identification": true,
    "has_payment_terms": true,
    "has_installment": true,
    "has_deadline": true,
    "has_timeframe": true
  },
  
  "labels": ["Financial", "Schedule"],
  "risk_count": 3,
  "risk_categories": {
    "Financial": 2,
    "Schedule": 1
  },
  
  "text_length": 1500,
  "word_count": 250,
  "version": "1.0"
}
```

### 3. `data/dedup_hashes.txt`
**Purpose**: Deduplication tracking  
**Format**: Plain text, one hash per line  
**Content**: SHA256 hashes of normalized text to prevent duplicate entries

## Field Descriptions

### Core Identification
- **text_hash**: SHA256 hash of normalized text (lowercase, whitespace normalized) for deduplication
- **file_hash**: SHA256 hash of original uploaded file (if available)
- **timestamp**: UTC timestamp of data collection
- **source_type**: How the data was collected (`upload`, `api`, `manual`)
- **filename**: Original filename if uploaded

### Document Classification
- **document_type**: Classified type of legal document
  - `construction_contract`: Building/construction agreements
  - `employment_contract`: Work agreements
  - `scholarship_agreement`: Educational grants/scholarships
  - `loan_agreement`: Loan/credit agreements
  - `sales_contract`: Purchase agreements
  - `rental_agreement`: Lease/rental agreements
  - `service_agreement`: Service provider contracts
  - `partnership_agreement`: Business partnerships
  - `policy_document`: Organizational policies
  - `proposal`: Project proposals
  - `general`: Unclassified documents

### Language Analysis
- **language**: Primary detected language
  - `khmer`: >70% Khmer characters
  - `english`: >70% English characters
  - `mixed`: Both languages significantly present
  - `unknown`: Unable to determine
- **language_mix**: Boolean indicating if document mixes languages (both >15%)
- **khmer_ratio**: Proportion of Khmer characters (0.0-1.0)
- **english_ratio**: Proportion of English characters (0.0-1.0)

### Extracted Features
Boolean and count features that help the model identify risk patterns:

**Numerical Indicators**:
- `has_currency`: Contains currency symbols ($, USD, ៛, រៀល)
- `has_percentage`: Contains percentage values
- `has_date`: Contains date patterns
- `has_duration`: Contains time duration expressions

**Legal Indicators**:
- `legal_keyword_count`: Count of legal terminology (contract, agreement, party, obligation, etc.)
- `risk_keyword_count`: Count of risk indicators (penalty, terminate, liable, dispute, etc.)

**Structural Indicators**:
- `has_numbered_clauses`: Contains structured clauses (Article 1, Section 2, ប្រការ១, etc.)
- `has_party_identification`: Identifies contracting parties (Party A, ភាគី ក, etc.)

**Financial Indicators**:
- `has_payment_terms`: Contains payment-related terms
- `has_installment`: Mentions staged/installment payments

**Temporal Indicators**:
- `has_deadline`: Contains deadline language
- `has_timeframe`: Specifies time periods

### Risk Analysis
- **labels**: Unique list of risk categories identified
- **risk_count**: Total number of risks identified
- **risk_categories**: Count of risks per category (Counter object)

### Text Statistics
- **text_length**: Character count of extracted text
- **word_count**: Word count of extracted text
- **version**: Schema version for future compatibility

## Risk Categories

The model is trained to identify these risk categories:
1. **Financial**: Budget, cost, payment, pricing risks
2. **Schedule**: Timeline, deadline, delay risks
3. **Technical**: Quality, specification, performance risks
4. **Legal**: Compliance, contract term, liability risks
5. **Operational**: Process, resource, capacity risks
6. **Compliance**: Regulatory, standard adherence risks
7. **Other**: Miscellaneous or uncategorized risks

## Data Collection Workflow

```
1. Document Upload
   ↓
2. Text Extraction (OCR for images/scanned PDFs)
   ↓
3. Deduplication Check (text_hash)
   ↓
4. Language Detection
   ↓
5. Document Type Classification
   ↓
6. Feature Extraction
   ↓
7. LLM Risk Analysis
   ↓
8. Data Storage
   ├── training.jsonl (simple format)
   ├── metadata.jsonl (comprehensive)
   └── dedup_hashes.txt (hash tracking)
```

## Usage for Model Training

### Phase 1: Data Collection
- Set `USE_LLM=true` in configuration
- Users upload documents via `/scan` endpoint
- System automatically collects and stores data
- Monitor with `/data/stats` endpoint

### Phase 2: Feature Engineering
When training the model, utilize these fields:
- **Primary**: `text` field for text vectorization (TF-IDF, embeddings)
- **Metadata features**: Add `features` dict as additional input features
- **Document type**: Use as categorical feature or for stratified training
- **Language info**: Handle Khmer/English/mixed documents differently if needed

### Phase 3: Model Training
```python
# Load training data
df = pd.read_json('data/training.jsonl', lines=True)

# Load metadata for enhanced features
meta_df = pd.read_json('data/metadata.jsonl', lines=True)

# Combine features
df = df.merge(meta_df[['text_hash', 'features', 'document_type', 'language']], 
              left_index=True, right_index=True)

# Your model training code here
```

### Phase 4: Data Quality Checks
Use metadata to:
- Identify underrepresented document types
- Balance language distribution
- Filter low-quality extractions (very short texts)
- Analyze feature distributions

## Deduplication Strategy

The system prevents duplicate training data through:
1. **Text normalization**: Lowercase, whitespace normalization
2. **Hash computation**: SHA256 of normalized text
3. **Hash tracking**: Store in `dedup_hashes.txt`
4. **Pre-storage check**: Reject duplicates before storage

This ensures:
- No redundant training examples
- Better model generalization
- Cleaner dataset metrics

## Data Quality Indicators

### Good Quality Indicators
- `text_length > 100` characters
- `word_count > 20` words
- `risk_count > 0` (LLM found risks)
- `language != "unknown"`
- Multiple features extracted (`has_*` flags)

### Low Quality Indicators
- `text_length < 50` (likely OCR failure)
- `word_count < 10`
- `risk_count == 0` (no risks found)
- Very few extracted features

## Versioning

- **Current Version**: 1.0
- **Version Field**: `metadata.version` tracks schema version
- **Future Changes**: New schema versions will maintain backward compatibility

## Privacy & Security

- **No PII Storage**: System does not attempt to extract or store personally identifiable information
- **Hash-based Deduplication**: Original filenames stored only as metadata reference
- **Text-only Storage**: Original files are not retained, only extracted text
- **Anonymization**: Consider removing party names/addresses before production if required

## Statistics Endpoint

Access data collection statistics via the collector:

```python
from data_collector import collector

stats = collector.get_statistics()
# Returns:
# {
#   "total_samples": 150,
#   "document_types": {"construction_contract": 45, ...},
#   "languages": {"khmer": 60, "english": 50, "mixed": 40},
#   "risk_categories": {"Financial": 180, "Schedule": 120, ...},
#   "avg_risks_per_doc": 2.5,
#   "avg_text_length": 1200,
#   "date_range": {"earliest": "...", "latest": "..."}
# }
```

## Best Practices

1. **Collect Diverse Data**: Ensure variety in document types and languages
2. **Monitor Quality**: Regularly check statistics and sample data
3. **Clean Periodically**: Use metadata to identify and remove low-quality entries
4. **Balance Dataset**: Use `document_type` and `language` to balance training data
5. **Feature Engineering**: Leverage extracted features for better model performance
6. **Version Control**: Track which data was collected with which schema version
7. **Regular Backups**: Back up JSONL files regularly

## Future Enhancements

Potential additions to the schema:
- Entity extraction (party names, amounts, dates)
- Sentiment analysis scores
- Document structure analysis (clause hierarchy)
- Cross-reference detection (references to other documents)
- Risk severity scoring
- Confidence scores from LLM
- Human validation flags
- Annotation corrections
