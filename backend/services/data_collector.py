import json
import os
import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter

# Support both package and module execution
try:
    from ..core.config import settings
except ImportError:
    from core.config import settings

DOCUMENT_TYPE_PATTERNS = {
    "construction_contract": [
        r"construction|building|\u1780\u17b6\u179a\u179f\u17b6\u1784\u179f\u1784\u17cb|\u179f\u17c6\u178e\u1784\u17cb|\u1798\u17c9\u17c5\u1780\u17b6\u179a",
        r"villa|house|\u1795\u17d2\u1791\u17c7|\u179c\u17b8\u17a1\u17b6",
    ],
    "employment_contract": [
        r"employment|work agreement|\u1780\u17b7\u1785\u17d2\u1785\u179f\u1793\u17d2\u1799\u17b6\u1780\u17b6\u179a\u1784\u17b6\u179a|\u1780\u17b6\u179a\u1784\u17b6\u179a",
        r"salary|wage|\u1794\u17d2\u179a\u17b6\u1780\u17cb\u1781\u17c2|\u1794\u17d2\u179a\u17b6\u1780\u17cb\u1788\u17d2\u1793\u17bd\u179b",
    ],
    "scholarship_agreement": [
        r"scholarship|grant|\u17a2\u17b6\u17a0\u17b6\u179a\u17bc\u1794\u1780\u179a\u178e\u17cd|\u1791\u17bb\u1793",
        r"education|study|\u1780\u17b6\u179a\u179f\u17b7\u1780\u17d2\u179f\u17b6|\u179f\u17b7\u179f\u17d2\u179f",
    ],
    "loan_agreement": [
        r"loan|credit|\u1780\u1798\u17d2\u1785\u17b8|\u1794\u17d2\u179a\u17b6\u1780\u17cb\u1780\u1798\u17d2\u1785\u17b8",
        r"interest|repayment|\u1780\u17b6\u179a\u179f\u1784\u1794\u17d2\u179a\u17b6\u1780\u17cb|\u1780\u17b6\u179a\u1794\u17d2\u179a\u17b6\u1780\u17cb",
    ],
    "sales_contract": [
        r"sale|purchase|\u179b\u1780\u17cb|\u1791\u17b7\u1789",
        r"buyer|seller|\u17a2\u17d2\u1793\u1780\u1791\u17b7\u1789|\u17a2\u17d2\u1793\u1780\u179b\u1780\u17cb",
    ],
    "rental_agreement": [
        r"rent|lease|\u1787\u17bd\u179b|\u1780\u17b6\u179a\u1787\u17bd\u179b",
        r"tenant|landlord|\u17a2\u17d2\u1793\u1780\u1787\u17bd\u179b|\u1798\u17d2\u1785\u17b6\u179f\u17cb\u1795\u17d2\u1791\u17c7",
    ],
    "service_agreement": [
        r"service|provide|\u179f\u17c1\u179c\u17b6\u1780\u1798\u17d2\u1798|\u1795\u17d2\u178f\u179b\u17cb",
        r"client|provider|\u17a2\u178f\u17b7\u1790\u17b7\u1787\u1793|\u17a2\u17d2\u1793\u1780\u1795\u17d2\u178f\u179b\u17cb\u179f\u17c1\u179c\u17b6",
    ],
    "partnership_agreement": [
        r"partnership|joint venture|\u1797\u17b6\u1796\u1787\u17b6\u178a\u17c3\u1782\u17bc|\u179f\u17a0\u1782\u17d2\u179a\u17b6\u179f",
        r"partner|collaboration|\u178a\u17c3\u1782\u17bc|\u179f\u17a0\u1780\u17b6\u179a",
    ],
    "policy_document": [
        r"policy|regulation|\u1782\u17c4\u179b\u1793\u1799\u17c4\u1794\u17b6\u1799|\u1794\u1791\u1794\u17d2\u1794\u1789\u17d2\u1789\u178f\u17d2\u178f\u17b7",
        r"compliance|standard|\u1780\u17b6\u179a\u17a2\u1793\u17bb\u179b\u17c4\u1798|\u179f\u17d2\u178f\u1784\u17cb\u178a\u17b6\u179a",
    ],
    "proposal": [
        r"proposal|plan|\u179f\u17c6\u178e\u17be|\u1782\u1798\u17d2\u179a\u17c4\u1784",
        r"budget|timeline|\u1790\u179c\u17b7\u1780\u17b6|\u1780\u17b6\u179b\u1794\u179a\u17b7\u1785\u17d2\u1786\u17c1\u1791",
    ],
}

class DataCollector:
    def __init__(self):
        self.data_dir = settings.data_dir
        self.training_file = settings.training_file
        self.metadata_file = os.path.join(self.data_dir, "metadata.jsonl")
        self.dedup_file = os.path.join(self.data_dir, "dedup_hashes.txt")
        os.makedirs(self.data_dir, exist_ok=True)
    def collect(
        self,
        text: str,
        risks: List[Dict],
        source_type: str = "upload",
        filename: Optional[str] = None,
        file_hash: Optional[str] = None,
    ) -> bool:
        if not text or not text.strip():
            return False
        if not risks or not isinstance(risks, list):
            return False
        text_hash = self._compute_text_hash(text)
        if self._is_duplicate(text_hash):
            return False
        features = self._extract_features(text)
        doc_type = self._classify_document_type(text)
        language_info = self._detect_language(text)
        labels = sorted({r.get("category", "Other") for r in risks})
        training_record = {
            "text": text,
            "labels": labels,
            "raw": risks,
        }
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
        try:
            with open(self.training_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(training_record, ensure_ascii=False) + "\n")
            with open(self.metadata_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(metadata_record, ensure_ascii=False) + "\n")
            with open(self.dedup_file, "a", encoding="utf-8") as f:
                f.write(text_hash + "\n")
            return True
        except Exception as e:
            print(f"Error storing training data: {e}")
            return False
    def _compute_text_hash(self, text: str) -> str:
        normalized = re.sub(r'\s+', ' ', text.lower().strip())
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    def _is_duplicate(self, text_hash: str) -> bool:
        if not os.path.exists(self.dedup_file):
            return False
        with open(self.dedup_file, "r", encoding="utf-8") as f:
            existing_hashes = set(line.strip() for line in f)
        return text_hash in existing_hashes
    def _detect_language(self, text: str) -> Dict:
        khmer_chars = len(re.findall(r'[\u1780-\u17FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
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
        if khmer_ratio > 0.7:
            primary = "khmer"
        elif english_ratio > 0.7:
            primary = "english"
        else:
            primary = "mixed"
        is_mixed = khmer_ratio > 0.15 and english_ratio > 0.15
        return {
            "primary_language": primary,
            "is_mixed": is_mixed,
            "khmer_ratio": round(khmer_ratio, 3),
            "english_ratio": round(english_ratio, 3),
        }
    def _classify_document_type(self, text: str) -> str:
        text_lower = text.lower()
        scores = {}
        for doc_type, patterns in DOCUMENT_TYPE_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    score += 1
            scores[doc_type] = score
        if scores:
            best_type = max(scores.items(), key=lambda x: x[1])
            if best_type[1] > 0:
                return best_type[0]
        return "general"
    def _extract_features(self, text: str) -> Dict:
        features = {}
        features["has_currency"] = bool(re.search(r'\$|USD|\u17db|\u179a\u17c0\u179b', text))
        features["has_percentage"] = bool(re.search(r'\d+[\s]*%|\u1797\u17b6\u1782\u179a\u1799', text))
        features["has_date"] = bool(re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\u1790\u17d2\u1784\u17c3\u1791\u17b8', text))
        features["has_duration"] = bool(re.search(r'\d+\s*(days?|months?|years?|\u1790\u17d2\u1784\u17c3|\u1781\u17c2|\u1786\u17d2\u1793\u17b6\u17c6)', text, re.IGNORECASE))
        legal_keywords = [
            r'contract|agreement|\u1780\u17b7\u1785\u17d2\u1785\u179f\u1793\u17d2\u1799\u17b6|\u1780\u17b7\u1785\u17d2\u1785\u1796\u17d2\u179a\u1798\u1796\u17d2\u179a\u17c0\u1784',
            r'party|parties|\u1797\u17b6\u1782\u17b8',
            r'obligation|duty|\u1780\u17b6\u178f\u1796\u17d2\u179c\u1780\u17b7\u1785\u17d2\u1785|\u1797\u17b6\u179a\u1780\u17b7\u1785\u17d2\u1785',
            r'penalty|fine|\u1796\u17b7\u1793\u17d0\u1799|\u1780\u17b6\u179a\u1796\u17b7\u1793\u17d0\u1799',
            r'termination|cancel|\u1794\u1789\u17d2\u1785\u1794\u17cb|\u179b\u17bb\u1794\u1785\u17c4\u179b',
            r'warranty|guarantee|\u1792\u17b6\u1793\u17b6|\u1780\u17b6\u179a\u1792\u17b6\u1793\u17b6',
        ]
        features["legal_keyword_count"] = sum(
            1 for kw in legal_keywords if re.search(kw, text, re.IGNORECASE)
        )
        risk_keywords = [
            r'must|shall|required|\u178f\u1798\u17d2\u179a\u17bc\u179c|\u178f\u17d2\u179a\u17bc\u179c\u178f\u17c2',
            r'penalty|late|delay|\u1796\u17b7\u1793\u17d0\u1799|\u1799\u17ba\u178f|\u1785\u17b6\u1794\u17cb',
            r'terminate|void|cease|\u1794\u1789\u17d2\u1785\u1794\u17cb|\u179b\u17bb\u1794\u1785\u17c4\u179b',
            r'liable|responsible|\u1791\u1791\u17bd\u179b\u1781\u17bb\u179f\u178f\u17d2\u179a\u17bc\u179c',
            r'dispute|conflict|\u179c\u17b7\u179c\u17b6\u1791|\u1787\u1798\u17d2\u179b\u17c4\u17c7',
        ]
        features["risk_keyword_count"] = sum(
            1 for kw in risk_keywords if re.search(kw, text, re.IGNORECASE)
        )
        features["has_numbered_clauses"] = bool(re.search(r'(?:Article|Section|Clause|\u1794\u17d2\u179a\u1780\u17b6\u179a)\s*\d+', text, re.IGNORECASE))
        features["has_party_identification"] = bool(re.search(r'party\s*[(\[]?[a-z]\s*[)\]]?|\u1797\u17b6\u1782\u17b8\s*[(\[]?[\u1780\u1781]\s*[)\]]?', text, re.IGNORECASE))
        features["has_payment_terms"] = bool(re.search(r'payment|pay|\u1791\u17bc\u1791\u17b6\u178f\u17cb|\u1794\u1784\u17cb\u1794\u17d2\u179a\u17b6\u1780\u17cb', text, re.IGNORECASE))
        features["has_installment"] = bool(re.search(r'installment|stage|phase|\u178a\u17c6\u178e\u17b6\u1780\u17cb\u1780\u17b6\u179b|\u179c\u1782\u17d2\u1782', text, re.IGNORECASE))
        features["has_deadline"] = bool(re.search(r'deadline|due date|within.*days|\u1780\u17d2\u1793\u17bb\u1784\u179a\u1799\u17c8\u1796\u17c1\u179b', text, re.IGNORECASE))
        features["has_timeframe"] = bool(re.search(r'\d+\s*days?|\d+\s*months?|\d+\s*years?|\d+\s*\u1790\u17d2\u1784\u17c3|\d+\s*\u1781\u17c2|\d+\s*\u1786\u17d2\u1793\u17b6\u17c6', text, re.IGNORECASE))
        return features
    def get_statistics(self) -> Dict:
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
        stats["document_types"] = dict(stats["document_types"])
        stats["languages"] = dict(stats["languages"])
        stats["risk_categories"] = dict(stats["risk_categories"])
        return stats

collector = DataCollector()
