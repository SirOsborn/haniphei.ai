"""
Enhanced Data Collection Pipeline for Risk Analysis Model Training

This module provides comprehensive data collection, validation, and storage
for building a production-ready risk analysis model that can eventually replace
the LLM-based approach with a self-sustained, trained model.

Features:
- Structured data format with comprehensive metadata
- Document type classification
- Language detection (Khmer, English, Mixed)
- Feature extraction for ML training
- Data validation and quality checks
- Deduplication
- Versioning and lineage tracking
"""

import json
import os
import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter

# Support both package and module execution
try:
    from .config import settings
except ImportError:
    from config import settings


# Document type patterns for classification
DOCUMENT_TYPE_PATTERNS = {
    "construction_contract": [
        r"construction|building|ការសាងសង់|សំណង់|ម៉ៅការ",
        r"villa|house|ផ្ទះ|វីឡា",
    ],
    "employment_contract": [
        r"employment|work agreement|កិច្ចសន្យាការងារ|ការងារ",
        r"salary|wage|ប្រាក់ខែ|ប្រាក់ឈ្នួល",
    ],
    "scholarship_agreement": [
        r"scholarship|grant|អាហារូបករណ៍|ទុន",
        r"education|study|ការសិក្សា|សិស្ស",
    ],
    "loan_agreement": [
        r"loan|credit|កម្ចី|ប្រាក់កម្ចី",
        r"interest|repayment|ការសងប្រាក់|ការប្រាក់",
    ],
    "sales_contract": [
        r"sale|purchase|លក់|ទិញ",
        r"buyer|seller|អ្នកទិញ|អ្នកលក់",
    ],
    "rental_agreement": [
        r"rent|lease|ជួល|ការជួល",
        r"tenant|landlord|អ្នកជួល|ម្ចាស់ផ្ទះ",
    ],
    "service_agreement": [
        r"service|provide|សេវាកម្ម|ផ្តល់",
        r"client|provider|អតិថិជន|អ្នកផ្តល់សេវា",
    ],
    "partnership_agreement": [
        r"partnership|joint venture|ភាពជាដៃគូ|សហគ្រាស",
        r"partner|collaboration|ដៃគូ|សហការ",
    ],
    "policy_document": [
        r"policy|regulation|គោលនយោបាយ|បទប្បញ្ញត្តិ",
        r"compliance|standard|ការអនុលោម|ស្តង់ដារ",
    ],
    "proposal": [
        r"proposal|plan|សំណើ|គម្រោង",
        r"budget|timeline|ថវិកា|កាលបរិច្ឆេទ",
    ],
}


class DataCollector:
    """Enhanced data collector for training data management."""
    
    def __init__(self):
        self.data_dir = settings.data_dir
        self.training_file = settings.training_file
        self.metadata_file = os.path.join(self.data_dir, "metadata.jsonl")
        self.dedup_file = os.path.join(self.data_dir, "dedup_hashes.txt")
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
    
    def collect(
        self,
        text: str,
        risks: List[Dict],
        source_type: str = "upload",
        filename: Optional[str] = None,
        file_hash: Optional[str] = None,
    ) -> bool:
        """
        Collect and store training data with comprehensive metadata.
        
        Args:
            text: Extracted document text
            risks: List of risk dictionaries from LLM analysis
            source_type: Type of source (upload, api, manual)
            filename: Original filename if available
            file_hash: Hash of original file for deduplication
            
        Returns:
            bool: True if data was stored, False if duplicate or invalid
        """
        # Validate input
        if not text or not text.strip():
            return False
        
        if not risks or not isinstance(risks, list):
            return False
        
        # Check for duplicates
        text_hash = self._compute_text_hash(text)
        if self._is_duplicate(text_hash):
            return False
        
        # Extract features and metadata
        features = self._extract_features(text)
        doc_type = self._classify_document_type(text)
        language_info = self._detect_language(text)
        
        # Prepare training record (backward compatible format)
        labels = sorted({r.get("category", "Other") for r in risks})
        training_record = {
            "text": text,
            "labels": labels,
            "raw": risks,
        }
        
        # Prepare comprehensive metadata record
        metadata_record = {
            "text_hash": text_hash,
            "file_hash": file_hash,
            "timestamp": datetime.utcnow().isoformat(),
            "source_type": source_type,
            "filename": filename,
            "document_type": doc_type,
            "language": language_info["primary_language"],
            "language_mix": language_info["is_mixed"],
            "khmer_ratio": language_info["khmer_ratio"],
            "english_ratio": language_info["english_ratio"],
            "features": features,
            "labels": labels,
            "risk_count": len(risks),
            "risk_categories": Counter([r.get("category", "Other") for r in risks]),
            "text_length": len(text),
            "word_count": len(text.split()),
            "version": "1.0",
        }
        
        # Store data
        try:
            # Append to training file (backward compatible)
            with open(self.training_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(training_record, ensure_ascii=False) + "\n")
            
            # Append to metadata file (enhanced info)
            with open(self.metadata_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(metadata_record, ensure_ascii=False) + "\n")
            
            # Record hash for deduplication
            with open(self.dedup_file, "a", encoding="utf-8") as f:
                f.write(text_hash + "\n")
            
            return True
        except Exception as e:
            print(f"Error storing training data: {e}")
            return False
    
    def _compute_text_hash(self, text: str) -> str:
        """Compute hash of normalized text for deduplication."""
        # Normalize: lowercase, remove extra whitespace
        normalized = re.sub(r'\s+', ' ', text.lower().strip())
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    def _is_duplicate(self, text_hash: str) -> bool:
        """Check if text hash exists in deduplication file."""
        if not os.path.exists(self.dedup_file):
            return False
        
        with open(self.dedup_file, "r", encoding="utf-8") as f:
            existing_hashes = set(line.strip() for line in f)
        
        return text_hash in existing_hashes
    
    def _detect_language(self, text: str) -> Dict:
        """
        Detect language composition of the text.
        
        Returns:
            Dict with primary_language, is_mixed, khmer_ratio, english_ratio
        """
        # Count Khmer characters (Unicode range: 1780-17FF)
        khmer_chars = len(re.findall(r'[\u1780-\u17FF]', text))
        
        # Count English characters (basic Latin alphabet)
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        # Total alphabetic characters
        total_chars = khmer_chars + english_chars
        
        if total_chars == 0:
            return {
                "primary_language": "unknown",
                "is_mixed": False,
                "khmer_ratio": 0.0,
                "english_ratio": 0.0,
            }
        
        khmer_ratio = khmer_chars / total_chars
        english_ratio = english_chars / total_chars
        
        # Determine primary language
        if khmer_ratio > 0.7:
            primary = "khmer"
        elif english_ratio > 0.7:
            primary = "english"
        else:
            primary = "mixed"
        
        # Consider mixed if both languages present significantly
        is_mixed = khmer_ratio > 0.15 and english_ratio > 0.15
        
        return {
            "primary_language": primary,
            "is_mixed": is_mixed,
            "khmer_ratio": round(khmer_ratio, 3),
            "english_ratio": round(english_ratio, 3),
        }
    
    def _classify_document_type(self, text: str) -> str:
        """
        Classify document type based on content patterns.
        
        Returns:
            Document type string or "general" if no match
        """
        text_lower = text.lower()
        
        # Score each document type
        scores = {}
        for doc_type, patterns in DOCUMENT_TYPE_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    score += 1
            scores[doc_type] = score
        
        # Return highest scoring type if score > 0
        if scores:
            best_type = max(scores.items(), key=lambda x: x[1])
            if best_type[1] > 0:
                return best_type[0]
        
        return "general"
    
    def _extract_features(self, text: str) -> Dict:
        """
        Extract important features from text for model training.
        
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Numerical patterns (amounts, percentages, dates)
        features["has_currency"] = bool(re.search(r'\$|USD|៛|រៀល', text))
        features["has_percentage"] = bool(re.search(r'\d+[\s]*%|ភាគរយ', text))
        features["has_date"] = bool(re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|ថ្ងៃទី', text))
        features["has_duration"] = bool(re.search(r'\d+\s*(days?|months?|years?|ថ្ងៃ|ខែ|ឆ្នាំ)', text, re.IGNORECASE))
        
        # Legal/contract keywords
        legal_keywords = [
            r'contract|agreement|កិច្ចសន្យា|កិច្ចព្រមព្រៀង',
            r'party|parties|ភាគី',
            r'obligation|duty|កាតព្វកិច្ច|ភារកិច្ច',
            r'penalty|fine|ពិន័យ|ការពិន័យ',
            r'termination|cancel|បញ្ចប់|លុបចោល',
            r'warranty|guarantee|ធានា|ការធានា',
        ]
        features["legal_keyword_count"] = sum(
            1 for kw in legal_keywords if re.search(kw, text, re.IGNORECASE)
        )
        
        # Risk indicator keywords
        risk_keywords = [
            r'must|shall|required|តម្រូវ|ត្រូវតែ',
            r'penalty|late|delay|ពិន័យ|យឺត|ចាប់',
            r'terminate|void|cease|បញ្ចប់|លុបចោល',
            r'liable|responsible|ទទួលខុសត្រូវ',
            r'dispute|conflict|វិវាទ|ជម្លោះ',
        ]
        features["risk_keyword_count"] = sum(
            1 for kw in risk_keywords if re.search(kw, text, re.IGNORECASE)
        )
        
        # Structural features
        features["has_numbered_clauses"] = bool(re.search(r'(?:Article|Section|Clause|ប្រការ)\s*\d+', text, re.IGNORECASE))
        features["has_party_identification"] = bool(re.search(r'party\s*[(\[]?[a-z]\s*[)\]]?|ភាគី\s*[(\[]?[កខ]\s*[)\]]?', text, re.IGNORECASE))
        
        # Payment-related features
        features["has_payment_terms"] = bool(re.search(r'payment|pay|ទូទាត់|បង់ប្រាក់', text, re.IGNORECASE))
        features["has_installment"] = bool(re.search(r'installment|stage|phase|ដំណាក់កាល|វគ្គ', text, re.IGNORECASE))
        
        # Time-related features
        features["has_deadline"] = bool(re.search(r'deadline|due date|within.*days|ក្នុងរយៈពេល', text, re.IGNORECASE))
        features["has_timeframe"] = bool(re.search(r'\d+\s*days?|\d+\s*months?|\d+\s*years?|\d+\s*ថ្ងៃ|\d+\s*ខែ|\d+\s*ឆ្នាំ', text, re.IGNORECASE))
        
        return features
    
    def get_statistics(self) -> Dict:
        """Get statistics about collected training data."""
        stats = {
            "total_samples": 0,
            "document_types": Counter(),
            "languages": Counter(),
            "risk_categories": Counter(),
            "avg_risks_per_doc": 0.0,
            "avg_text_length": 0.0,
            "date_range": {"earliest": None, "latest": None},
        }
        
        if not os.path.exists(self.metadata_file):
            return stats
        
        total_risks = 0
        total_length = 0
        timestamps = []
        
        with open(self.metadata_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    stats["total_samples"] += 1
                    stats["document_types"][record.get("document_type", "unknown")] += 1
                    stats["languages"][record.get("language", "unknown")] += 1
                    
                    # Risk categories
                    for category, count in record.get("risk_categories", {}).items():
                        stats["risk_categories"][category] += count
                    
                    total_risks += record.get("risk_count", 0)
                    total_length += record.get("text_length", 0)
                    
                    if "timestamp" in record:
                        timestamps.append(record["timestamp"])
                except Exception:
                    continue
        
        if stats["total_samples"] > 0:
            stats["avg_risks_per_doc"] = round(total_risks / stats["total_samples"], 2)
            stats["avg_text_length"] = round(total_length / stats["total_samples"], 0)
        
        if timestamps:
            timestamps.sort()
            stats["date_range"]["earliest"] = timestamps[0]
            stats["date_range"]["latest"] = timestamps[-1]
        
        # Convert Counters to dicts for JSON serialization
        stats["document_types"] = dict(stats["document_types"])
        stats["languages"] = dict(stats["languages"])
        stats["risk_categories"] = dict(stats["risk_categories"])
        
        return stats


# Global instance
collector = DataCollector()
