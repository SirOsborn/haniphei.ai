import json
import os
from typing import Dict, List, Tuple
from collections import Counter

# Support both package and module execution
from core.config import settings

class DataQualityValidator:
    MIN_TEXT_LENGTH = 50
    MIN_WORD_COUNT = 10
    MAX_TEXT_LENGTH = 100000
    MIN_RISK_COUNT = 1
    MAX_RISK_COUNT = 20
    MIN_SAMPLES_PER_CATEGORY = 10
    MIN_TOTAL_SAMPLES = 20
    def __init__(self):
        self.training_file = settings.training_file
        self.metadata_file = os.path.join(settings.data_dir, "metadata.jsonl")
        self.issues = []
        self.warnings = []
    def validate_dataset(self) -> Dict:
        self.issues = []
        self.warnings = []
        if not os.path.exists(self.training_file):
            self.issues.append("Training file does not exist. No data collected yet.")
            return self._format_results()
        training_data = self._load_training_data()
        metadata = self._load_metadata()
        self._validate_sample_count(training_data)
        self._validate_text_quality(training_data)
        self._validate_label_quality(training_data)
        self._validate_class_balance(training_data)
        if metadata:
            self._validate_language_distribution(metadata)
            self._validate_document_types(metadata)
            self._validate_feature_coverage(metadata)
        return self._format_results()
    def identify_low_quality_samples(self) -> List[Dict]:
        if not os.path.exists(self.training_file):
            return []
        training_data = self._load_training_data()
        metadata = self._load_metadata()
        low_quality = []
        for idx, sample in enumerate(training_data):
            reasons = []
            text_len = len(sample.get("text", ""))
            word_count = len(sample.get("text", "").split())
            if text_len < self.MIN_TEXT_LENGTH:
                reasons.append(f"Text too short ({text_len} chars)")
            if text_len > self.MAX_TEXT_LENGTH:
                reasons.append(f"Text suspiciously long ({text_len} chars)")
            if word_count < self.MIN_WORD_COUNT:
                reasons.append(f"Too few words ({word_count})")
            labels = sample.get("labels", [])
            if not labels:
                reasons.append("No labels/categories")
            risks = sample.get("raw", [])
            risk_count = len(risks)
            if risk_count < self.MIN_RISK_COUNT:
                reasons.append("No risks identified")
            if risk_count > self.MAX_RISK_COUNT:
                reasons.append(f"Suspiciously many risks ({risk_count})")
            if metadata and idx < len(metadata):
                meta = metadata[idx]
                if meta.get("language") == "unknown":
                    reasons.append("Unknown language")
                features = meta.get("features", {})
                feature_count = sum(1 for v in features.values() if v)
                if feature_count == 0:
                    reasons.append("No features extracted")
            if reasons:
                low_quality.append({
                    "index": idx,
                    "text_preview": sample.get("text", "")[:100] + "...",
                    "text_length": text_len,
                    "word_count": word_count,
                    "risk_count": risk_count,
                    "reasons": reasons,
                })
        return low_quality
    def get_recommendations(self) -> List[str]:
        recommendations = []
        training_data = self._load_training_data()
        metadata = self._load_metadata()
        if not training_data:
            recommendations.append("START COLLECTING DATA: Upload documents via /scan endpoint")
            return recommendations
        total_samples = len(training_data)
        if total_samples < self.MIN_TOTAL_SAMPLES:
            recommendations.append(
                f"COLLECT MORE DATA: You have {total_samples} samples, "
                f"recommend at least {self.MIN_TOTAL_SAMPLES} for initial training"
            )
        elif total_samples < 100:
            recommendations.append(
                f"IMPROVE COVERAGE: {total_samples} samples is good for testing, "
                "but aim for 100+ for production quality"
            )
        label_counts = Counter()
        for sample in training_data:
            for label in sample.get("labels", []):
                label_counts[label] += 1
        underrepresented = [
            cat for cat, count in label_counts.items() 
            if count < self.MIN_SAMPLES_PER_CATEGORY
        ]
        if underrepresented:
            recommendations.append(
                f"BALANCE CLASSES: These categories need more samples: {', '.join(underrepresented)}"
            )
        if metadata:
            doc_types = Counter(m.get("document_type", "unknown") for m in metadata)
            if len(doc_types) < 3:
                recommendations.append(
                    "DIVERSIFY DOCUMENT TYPES: Collect more varied document types "
                    "(contracts, policies, proposals, etc.)"
                )
            languages = Counter(m.get("language", "unknown") for m in metadata)
            if "khmer" in languages and "english" in languages:
                ratio = languages["khmer"] / (languages["english"] + 1)
                if ratio > 3 or ratio < 0.33:
                    recommendations.append(
                        "BALANCE LANGUAGES: Try to collect more balanced Khmer/English documents"
                    )
        low_quality = self.identify_low_quality_samples()
        if low_quality:
            recommendations.append(
                f"CLEAN DATA: Found {len(low_quality)} low-quality samples that should be reviewed"
            )
        if total_samples >= self.MIN_TOTAL_SAMPLES and not underrepresented:
            recommendations.append(
                "READY FOR TRAINING: Dataset quality is sufficient. Call /train endpoint"
            )
        return recommendations
    def _load_training_data(self) -> List[Dict]:
        data = []
        if not os.path.exists(self.training_file):
            return data
        with open(self.training_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except Exception:
                    continue
        return data
    def _load_metadata(self) -> List[Dict]:
        data = []
        if not os.path.exists(self.metadata_file):
            return data
        with open(self.metadata_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except Exception:
                    continue
        return data
    def _validate_sample_count(self, data: List[Dict]):
        count = len(data)
        if count == 0:
            self.issues.append("No training samples found")
        elif count < self.MIN_TOTAL_SAMPLES:
            self.warnings.append(
                f"Only {count} samples. Recommend at least {self.MIN_TOTAL_SAMPLES} for training"
            )
    def _validate_text_quality(self, data: List[Dict]):
        too_short = sum(
            1 for d in data 
            if len(d.get("text", "")) < self.MIN_TEXT_LENGTH
        )
        too_long = sum(
            1 for d in data 
            if len(d.get("text", "")) > self.MAX_TEXT_LENGTH
        )
        if too_short > 0:
            self.warnings.append(
                f"{too_short} samples have text shorter than {self.MIN_TEXT_LENGTH} chars (possible OCR failure)"
            )
        if too_long > 0:
            self.warnings.append(
                f"{too_long} samples have unusually long text (>{self.MAX_TEXT_LENGTH} chars)"
            )
    def _validate_label_quality(self, data: List[Dict]):
        no_labels = sum(1 for d in data if not d.get("labels"))
        no_risks = sum(1 for d in data if not d.get("raw"))
        if no_labels > 0:
            self.issues.append(f"{no_labels} samples have no labels")
        if no_risks > 0:
            self.warnings.append(f"{no_risks} samples have no detailed risks")
    def _validate_class_balance(self, data: List[Dict]):
        label_counts = Counter()
        for sample in data:
            for label in sample.get("labels", []):
                label_counts[label] += 1
        if not label_counts:
            return
        max_count = max(label_counts.values())
        min_count = min(label_counts.values())
        if max_count > min_count * 5:
            self.warnings.append(
                f"Class imbalance detected. Most common: {max_count}, least: {min_count}"
            )
        underrep = [
            cat for cat, count in label_counts.items() 
            if count < self.MIN_SAMPLES_PER_CATEGORY
        ]
        if underrep:
            self.warnings.append(
                f"Underrepresented categories (< {self.MIN_SAMPLES_PER_CATEGORY} samples): {', '.join(underrep)}"
            )
    def _validate_language_distribution(self, metadata: List[Dict]):
        languages = Counter(m.get("language", "unknown") for m in metadata)
        if "unknown" in languages and languages["unknown"] > len(metadata) * 0.1:
            self.warnings.append(
                f"{languages['unknown']} samples have unknown language "
                "(possible OCR or detection issues)"
            )
    def _validate_document_types(self, metadata: List[Dict]):
        doc_types = Counter(m.get("document_type", "unknown") for m in metadata)
        if len(doc_types) == 1:
            self.warnings.append(
                "All documents are same type. Collect diverse document types for better generalization"
            )
        if "general" in doc_types and doc_types["general"] > len(metadata) * 0.5:
            self.warnings.append(
                f"{doc_types['general']} samples not classified to specific document type"
            )
    def _validate_feature_coverage(self, metadata: List[Dict]):
        samples_with_no_features = sum(
            1 for m in metadata
            if sum(1 for v in m.get("features", {}).values() if v) == 0
        )
        if samples_with_no_features > len(metadata) * 0.2:
            self.warnings.append(
                f"{samples_with_no_features} samples have no extracted features "
                "(check text quality)"
            )
    def _format_results(self) -> Dict:
        return {
            "valid": len(self.issues) == 0,
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendations": self.get_recommendations(),
        }

validator = DataQualityValidator()
