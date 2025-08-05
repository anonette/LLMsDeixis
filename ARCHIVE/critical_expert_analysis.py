"""
Critical Evidence-Based Expert Analysis: Rigorous, skeptical researcher system that 
identifies methodological flaws, expresses uncertainty, and generates challenging 
research questions based on logged evidence.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class CriticalEvidence:
    """Evidence structure that includes critical assessment of reliability and validity."""
    evidence_id: str
    evidence_type: str
    research_question_relevance: List[str]
    
    # Source information
    session_id: str
    dilemma_id: str
    framing_type: str
    timestamp: str
    
    # The actual evidence
    raw_data: Dict[str, Any]
    processed_insight: str
    quantitative_metrics: Dict[str, float]
    
    # Critical assessment
    reliability_concerns: List[str]
    validity_limitations: List[str]
    potential_confounds: List[str]
    sample_size_adequacy: str  # "adequate", "marginal", "insufficient"
    
    # Context for interpretation
    context_description: str
    alternative_interpretations: List[str]
    conflicting_evidence: Optional[str] = None

@dataclass
class CriticalInsight:
    """Research insight with rigorous critical assessment and uncertainty quantification."""
    insight_id: str
    research_question_id: str
    insight_statement: str
    confidence_level: float  # 0-1
    uncertainty_factors: List[str]  # What makes us uncertain about this insight
    
    # Evidence assessment
    supporting_evidence: List[CriticalEvidence]
    contradictory_evidence: List[CriticalEvidence]
    missing_evidence: List[str]  # What evidence would we need to be more confident
    
    # Quantitative support with critical assessment
    quantitative_support: Dict[str, Any]
    statistical_limitations: List[str]
    effect_size_assessment: str  # "negligible", "small", "moderate", "large"
    
    # Examples with critical context
    concrete_examples: List[str]
    counter_examples: List[str]
    inconclusive_examples: List[str]
    
    # Methodological assessment
    analysis_method_used: str
    methodological_concerns: List[str]
    data_quality_issues: List[str]
    generalizability_limits: List[str]
    
    # Critical conclusions
    what_works: List[str]
    what_doesnt_work: List[str]
    what_remains_unknown: List[str]
    
    # Research implications
    challenging_follow_up_questions: List[str]
    methodological_improvements_needed: List[str]
    alternative_hypotheses: List[str]

class CriticalExpertAnalyzer:
    """
    Rigorous, skeptical expert analyzer that identifies methodological flaws,
    expresses appropriate uncertainty, and generates challenging research questions.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the critical expert analyzer with high methodological standards."""
        self.api_key = api_key
        self.critical_evidence = []
        self.evidence_index = {}
        self.methodological_standards = self._define_methodological_standards()
        logger.info("Critical expert analyzer initialized with rigorous standards")
    
    def _define_methodological_standards(self) -> Dict[str, Any]:
        """Define rigorous methodological standards for evidence evaluation."""
        return {
            "minimum_sample_size": {
                "statistical_analysis": 30,
                "comparative_analysis": 20,
                "pattern_detection": 10,
                "case_study": 5
            },
            "confidence_thresholds": {
                "high_confidence": 0.85,
                "moderate_confidence": 0.65,
                "low_confidence": 0.45,
                "insufficient_evidence": 0.30
            },
            "effect_size_thresholds": {
                "large": 0.8,
                "moderate": 0.5,
                "small": 0.2,
                "negligible": 0.1
            },
            "reliability_requirements": {
                "data_completeness": 0.90,
                "measurement_consistency": 0.80,
                "temporal_stability": 0.75
            }
        }
    
    def extract_critical_evidence(self, session_data: Dict[str, Any]) -> List[CriticalEvidence]:
        """
        Extract evidence with rigorous critical assessment of reliability and validity.
        
        Args:
            session_data: Complete session data from RichAnalysisLogger
            
        Returns:
            List of critically assessed evidence objects
        """
        evidence_list = []
        records = session_data.get('records', [])
        session_id = session_data.get('session_metadata', {}).get('session_id', 'unknown')
        
        # Critical assessment of data quality
        data_quality_issues = self._assess_data_quality(records)
        
        for record in records:
            # Extract evidence with critical assessment
            marker_evidence = self._extract_critical_marker_evidence(record, session_id, data_quality_issues)
            evidence_list.extend(marker_evidence)
            
            transformation_evidence = self._extract_critical_transformation_evidence(record, session_id, data_quality_issues)
            evidence_list.extend(transformation_evidence)
            
            response_evidence = self._extract_critical_response_evidence(record, session_id, data_quality_issues)
            evidence_list.extend(response_evidence)
        
        # Critical statistical evidence
        statistical_evidence = self._extract_critical_statistical_evidence(records, session_id, data_quality_issues)
        evidence_list.extend(statistical_evidence)
        
        self.critical_evidence = evidence_list
        self._build_critical_evidence_index()
        
        logger.info(f"Extracted {len(evidence_list)} critically assessed evidence pieces")
        return evidence_list
    
    def _assess_data_quality(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess overall data quality and identify systematic issues."""
        if not records:
            return {"fatal_issues": ["No data records available"]}
        
        issues = {
            "sample_size_concerns": [],
            "data_completeness_issues": [],
            "measurement_inconsistencies": [],
            "temporal_issues": [],
            "systematic_biases": []
        }
        
        # Sample size assessment
        total_records = len(records)
        if total_records < self.methodological_standards["minimum_sample_size"]["statistical_analysis"]:
            issues["sample_size_concerns"].append(f"Total sample size ({total_records}) below minimum for statistical analysis (30)")
        
        # Data completeness
        required_fields = ['dilemma_id', 'framing_type', 'llm_response', 'deictic_markers']
        for field in required_fields:
            missing_count = sum(1 for record in records if not record.get(field))
            if missing_count > 0:
                completeness_rate = (total_records - missing_count) / total_records
                if completeness_rate < self.methodological_standards["reliability_requirements"]["data_completeness"]:
                    issues["data_completeness_issues"].append(f"{field} missing in {missing_count}/{total_records} records ({completeness_rate:.2%} complete)")
        
        # Framing distribution assessment
        framing_counts = {}
        for record in records:
            framing = record.get('framing_type', 'unknown')
            framing_counts[framing] = framing_counts.get(framing, 0) + 1
        
        if framing_counts:
            min_samples = min(framing_counts.values())
            max_samples = max(framing_counts.values())
            if max_samples > min_samples * 3:  # Highly unbalanced
                issues["systematic_biases"].append(f"Highly unbalanced framing distribution: {framing_counts}")
        
        # Temporal clustering
        timestamps = [record.get('timestamp', '') for record in records if record.get('timestamp')]
        if len(set(timestamps)) < len(timestamps) * 0.5:  # More than 50% duplicate timestamps
            issues["temporal_issues"].append("High temporal clustering suggests potential batch processing artifacts")
        
        return issues
    
    def _extract_critical_marker_evidence(self, record: Dict[str, Any], session_id: str, quality_issues: Dict[str, Any]) -> List[CriticalEvidence]:
        """Extract deictic marker evidence with critical assessment."""
        evidence_list = []
        
        deictic_markers = record.get('deictic_markers', {})
        if not deictic_markers:
            return evidence_list
        
        # Critical assessment of marker reliability
        reliability_concerns = []
        validity_limitations = []
        potential_confounds = []
        
        # Assess marker detection reliability
        total_markers = sum(deictic_markers.values())
        response_length = len(record.get('llm_response', ''))
        marker_density = total_markers / response_length if response_length > 0 else 0
        
        if marker_density < 0.01:  # Less than 1 marker per 100 characters
            reliability_concerns.append("Very low marker density may indicate detection issues")
        elif marker_density > 0.2:  # More than 1 marker per 5 characters
            reliability_concerns.append("Unusually high marker density may indicate over-detection")
        
        # Assess potential confounds
        if record.get('processing_time', 0) > 5.0:
            potential_confounds.append("Extended processing time may indicate complex response generation affecting marker patterns")
        
        # Check for single dominant marker (potential artifact)
        if deictic_markers and max(deictic_markers.values()) > sum(deictic_markers.values()) * 0.8:
            validity_limitations.append("Single marker type dominates (>80%), may indicate systematic bias in detection or generation")
        
        # Sample size adequacy for this specific evidence
        sample_size_adequacy = "insufficient" if total_markers < 5 else "marginal" if total_markers < 10 else "adequate"
        
        # Generate critical evidence
        high_freq_markers = {k: v for k, v in deictic_markers.items() if v >= 3}
        if high_freq_markers:
            evidence_list.append(CriticalEvidence(
                evidence_id=f"marker_critical_{record['dilemma_id']}_{record['framing_type']}",
                evidence_type="deictic_marker",
                research_question_relevance=["RQ1.1", "RQ2.1"],
                session_id=session_id,
                dilemma_id=record['dilemma_id'],
                framing_type=record['framing_type'],
                timestamp=record['timestamp'],
                raw_data={
                    "high_frequency_markers": high_freq_markers,
                    "total_markers": total_markers,
                    "marker_density": marker_density,
                    "response_excerpt": record.get('llm_response', '')[:200]
                },
                processed_insight=f"High-frequency markers {list(high_freq_markers.keys())} in {record['framing_type']} framing, but with {len(reliability_concerns)} reliability concerns",
                quantitative_metrics={
                    "marker_density": marker_density,
                    "marker_diversity": len(high_freq_markers),
                    "dominance_ratio": max(high_freq_markers.values()) / sum(high_freq_markers.values()) if high_freq_markers else 0,
                    "confidence_score": 1.0 - (len(reliability_concerns) * 0.2 + len(validity_limitations) * 0.3)
                },
                reliability_concerns=reliability_concerns,
                validity_limitations=validity_limitations,
                potential_confounds=potential_confounds,
                sample_size_adequacy=sample_size_adequacy,
                context_description=f"Marker analysis for {record['framing_type']} framing with {len(reliability_concerns)} methodological concerns",
                alternative_interpretations=[
                    "Marker patterns may reflect LLM training biases rather than genuine deictic effects",
                    "High marker frequency could indicate prompt artifacts rather than natural language generation",
                    "Marker detection algorithm may have systematic biases toward certain linguistic patterns"
                ]
            ))
        
        return evidence_list
    
    def _extract_critical_transformation_evidence(self, record: Dict[str, Any], session_id: str, quality_issues: Dict[str, Any]) -> List[CriticalEvidence]:
        """Extract transformation evidence with critical validity assessment."""
        evidence_list = []
        
        transformation_prompt = record.get('transformation_prompt', '')
        direct_question = record.get('direct_question', '')
        original_description = record.get('original_description', '')
        
        if not (transformation_prompt and direct_question and original_description):
            return evidence_list
        
        # Critical assessment of transformation validity
        reliability_concerns = []
        validity_limitations = []
        potential_confounds = []
        
        # Assess transformation quality
        transformation_length = len(direct_question)
        original_length = len(original_description)
        length_ratio = transformation_length / original_length if original_length > 0 else 0
        
        if length_ratio < 0.8:
            validity_limitations.append("Transformation significantly shorter than original (possible information loss)")
        elif length_ratio > 3.0:
            validity_limitations.append("Transformation much longer than original (possible elaboration artifacts)")
        
        # Check for prompt leakage
        if transformation_prompt.lower() in direct_question.lower():
            reliability_concerns.append("Transformation contains prompt language (potential prompt leakage)")
        
        # Assess semantic similarity (simple heuristic)
        original_words = set(original_description.lower().split())
        transformed_words = set(direct_question.lower().split())
        word_overlap = len(original_words & transformed_words) / len(original_words) if original_words else 0
        
        if word_overlap < 0.3:
            validity_limitations.append("Low word overlap with original suggests potential semantic drift")
        elif word_overlap > 0.9:
            reliability_concerns.append("Very high word overlap suggests minimal transformation")
        
        sample_size_adequacy = "single_case"  # Transformations are inherently single cases
        
        evidence_list.append(CriticalEvidence(
            evidence_id=f"transformation_critical_{record['dilemma_id']}_{record['framing_type']}",
            evidence_type="transformation",
            research_question_relevance=["RQ4.1", "RQ9.1"],
            session_id=session_id,
            dilemma_id=record['dilemma_id'],
            framing_type=record['framing_type'],
            timestamp=record['timestamp'],
            raw_data={
                "original_description": original_description,
                "transformation_prompt": transformation_prompt,
                "direct_question": direct_question,
                "length_ratio": length_ratio,
                "word_overlap": word_overlap
            },
            processed_insight=f"Transformation to {record['framing_type']} shows {length_ratio:.1f}x length change with {word_overlap:.2f} word overlap, but has {len(validity_limitations)} validity concerns",
            quantitative_metrics={
                "transformation_length": transformation_length,
                "length_ratio": length_ratio,
                "word_overlap": word_overlap,
                "transformation_quality_score": max(0, 1.0 - (len(reliability_concerns) * 0.3 + len(validity_limitations) * 0.4))
            },
            reliability_concerns=reliability_concerns,
            validity_limitations=validity_limitations,
            potential_confounds=potential_confounds,
            sample_size_adequacy=sample_size_adequacy,
            context_description=f"Transformation quality assessment for {record['framing_type']} framing",
            alternative_interpretations=[
                "Transformation may reflect LLM instruction-following ability rather than deictic understanding",
                "Length changes could indicate template-following rather than genuine linguistic transformation",
                "Word overlap patterns may suggest systematic prompt engineering effects"
            ]
        ))
        
        return evidence_list
    
    def _extract_critical_response_evidence(self, record: Dict[str, Any], session_id: str, quality_issues: Dict[str, Any]) -> List[CriticalEvidence]:
        """Extract response pattern evidence with critical assessment of confounding factors."""
        evidence_list = []
        
        llm_response = record.get('llm_response', '')
        if not llm_response:
            return evidence_list
        
        response_length = len(llm_response)
        processing_time = record.get('processing_time', 0)
        
        # Critical assessment
        reliability_concerns = []
        validity_limitations = []
        potential_confounds = []
        
        # Assess response authenticity
        if processing_time < 0.1:
            reliability_concerns.append("Unusually fast processing suggests possible cached or template response")
        
        # Check for generic responses
        generic_phrases = ["it depends", "on the other hand", "however", "it's important to consider"]
        generic_count = sum(1 for phrase in generic_phrases if phrase in llm_response.lower())
        if generic_count > 3:
            validity_limitations.append("High generic phrase count suggests non-specific response pattern")
        
        # Assess ethical reasoning depth
        ethical_keywords = self._count_ethical_keywords(llm_response)
        if response_length > 200 and ethical_keywords < 3:
            validity_limitations.append("Long response with few ethical keywords suggests limited moral reasoning")
        
        # Response complexity assessment with critical evaluation
        if response_length > 300:
            complexity_score = response_length / 100
            
            # Critical factors affecting complexity interpretation
            if generic_count > 2:
                potential_confounds.append("Generic language may inflate complexity without adding substantive content")
            
            if ethical_keywords / response_length < 0.01:  # Less than 1% ethical content
                potential_confounds.append("Low ethical content density questions complexity interpretation")
            
            sample_size_adequacy = "single_case"
            
            evidence_list.append(CriticalEvidence(
                evidence_id=f"response_critical_{record['dilemma_id']}_{record['framing_type']}",
                evidence_type="response_pattern",
                research_question_relevance=["RQ1.1", "RQ3.1"],
                session_id=session_id,
                dilemma_id=record['dilemma_id'],
                framing_type=record['framing_type'],
                timestamp=record['timestamp'],
                raw_data={
                    "response_excerpt": llm_response[:300] + "...",
                    "full_length": response_length,
                    "processing_time": processing_time,
                    "ethical_keywords": ethical_keywords,
                    "generic_phrases": generic_count
                },
                processed_insight=f"Complex response ({response_length} chars) in {record['framing_type']} framing, but complexity interpretation limited by {len(potential_confounds)} confounding factors",
                quantitative_metrics={
                    "response_complexity": complexity_score,
                    "ethical_density": ethical_keywords / response_length,
                    "generic_ratio": generic_count / response_length * 1000,  # Per 1000 chars
                    "reliability_score": max(0, 1.0 - (len(reliability_concerns) * 0.25 + len(validity_limitations) * 0.35))
                },
                reliability_concerns=reliability_concerns,
                validity_limitations=validity_limitations,
                potential_confounds=potential_confounds,
                sample_size_adequacy=sample_size_adequacy,
                context_description=f"Response complexity analysis with {len(potential_confounds)} identified confounds",
                alternative_interpretations=[
                    "Response length may reflect verbose LLM training rather than enhanced ethical reasoning",
                    "Generic language patterns could indicate template-based rather than context-specific responses",
                    "Processing time variations may introduce systematic biases in response quality"
                ]
            ))
        
        return evidence_list
    
    def _extract_critical_statistical_evidence(self, records: List[Dict[str, Any]], session_id: str, quality_issues: Dict[str, Any]) -> List[CriticalEvidence]:
        """Extract statistical evidence with rigorous assessment of statistical validity."""
        evidence_list = []
        
        if len(records) < 2:
            return evidence_list
        
        # Critical statistical assessment
        reliability_concerns = []
        validity_limitations = []
        potential_confounds = []
        
        # Sample size adequacy
        total_n = len(records)
        if total_n < self.methodological_standards["minimum_sample_size"]["statistical_analysis"]:
            validity_limitations.append(f"Sample size ({total_n}) below minimum for reliable statistical inference (30)")
        
        # Assess statistical patterns with critical evaluation
        framing_counts = {}
        total_markers_by_framing = {}
        
        for record in records:
            framing = record.get('framing_type', 'unknown')
            framing_counts[framing] = framing_counts.get(framing, 0) + 1
            
            total_markers = record.get('total_markers', 0)
            if framing not in total_markers_by_framing:
                total_markers_by_framing[framing] = []
            total_markers_by_framing[framing].append(total_markers)
        
        # Critical assessment of group sizes
        min_group_size = min(framing_counts.values()) if framing_counts else 0
        if min_group_size < 5:
            validity_limitations.append(f"Smallest group size ({min_group_size}) insufficient for meaningful comparison")
        
        # Assess balance
        max_group_size = max(framing_counts.values()) if framing_counts else 0
        if max_group_size > min_group_size * 3:
            potential_confounds.append("Highly unbalanced group sizes may bias statistical comparisons")
        
        # Calculate effect sizes and assess statistical power
        effect_sizes = {}
        if len(total_markers_by_framing) >= 2:
            framings = list(total_markers_by_framing.keys())
            for i in range(len(framings)):
                for j in range(i+1, len(framings)):
                    framing1, framing2 = framings[i], framings[j]
                    markers1 = total_markers_by_framing[framing1]
                    markers2 = total_markers_by_framing[framing2]
                    
                    if markers1 and markers2 and len(markers1) > 1 and len(markers2) > 1:
                        mean1, mean2 = sum(markers1)/len(markers1), sum(markers2)/len(markers2)
                        # Calculate pooled standard deviation with error handling
                        if len(markers1) + len(markers2) > 2:
                            pooled_std = ((sum((x-mean1)**2 for x in markers1) + sum((x-mean2)**2 for x in markers2)) / 
                                         (len(markers1) + len(markers2) - 2)) ** 0.5
                            cohen_d = abs(mean1 - mean2) / pooled_std if pooled_std > 0 else 0
                            effect_sizes[f"{framing1}_vs_{framing2}"] = cohen_d
                        else:
                            # Too few data points for reliable effect size calculation
                            effect_sizes[f"{framing1}_vs_{framing2}"] = 0
                    elif markers1 and markers2:
                        # Single data points - calculate simple difference but mark as unreliable
                        mean1, mean2 = sum(markers1)/len(markers1), sum(markers2)/len(markers2)
                        effect_sizes[f"{framing1}_vs_{framing2}"] = 0  # Cannot calculate reliable effect size
        
        # Determine overall effect size assessment
        max_effect = max(effect_sizes.values()) if effect_sizes else 0
        if max_effect < self.methodological_standards["effect_size_thresholds"]["small"]:
            effect_assessment = "negligible"
            validity_limitations.append("All observed effect sizes below small effect threshold (0.2)")
        elif max_effect < self.methodological_standards["effect_size_thresholds"]["moderate"]:
            effect_assessment = "small"
        elif max_effect < self.methodological_standards["effect_size_thresholds"]["large"]:
            effect_assessment = "moderate"
        else:
            effect_assessment = "large"
        
        sample_size_adequacy = "adequate" if total_n >= 30 else "marginal" if total_n >= 20 else "insufficient"
        
        evidence_list.append(CriticalEvidence(
            evidence_id=f"statistical_critical_{session_id}",
            evidence_type="statistical",
            research_question_relevance=["RQ1.1", "RQ3.1"],
            session_id=session_id,
            dilemma_id="multiple",
            framing_type="comparative",
            timestamp=datetime.now().isoformat(),
            raw_data={
                "framing_distribution": framing_counts,
                "effect_sizes": effect_sizes,
                "sample_sizes": {k: len(v) for k, v in total_markers_by_framing.items()},
                "marker_statistics": {
                    framing: {
                        "mean": sum(markers) / len(markers),
                        "std": (sum((x - sum(markers)/len(markers))**2 for x in markers) / len(markers))**0.5,
                        "n": len(markers)
                    }
                    for framing, markers in total_markers_by_framing.items()
                }
            },
            processed_insight=f"Statistical analysis shows {effect_assessment} effect sizes but with {len(validity_limitations)} major limitations affecting interpretation",
            quantitative_metrics={
                "total_sample_size": total_n,
                "number_of_groups": len(framing_counts),
                "max_effect_size": max_effect,
                "min_group_size": min_group_size,
                "balance_ratio": max_group_size / min_group_size if min_group_size > 0 else float('inf'),
                "statistical_power_estimate": min(1.0, total_n / 30)  # Rough estimate
            },
            reliability_concerns=reliability_concerns,
            validity_limitations=validity_limitations,
            potential_confounds=potential_confounds,
            sample_size_adequacy=sample_size_adequacy,
            context_description=f"Statistical analysis across {total_n} records with {len(validity_limitations)} major limitations",
            alternative_interpretations=[
                "Observed differences may reflect random variation rather than systematic deictic effects",
                "Small sample sizes limit ability to detect genuine effects (Type II error risk)",
                "Unbalanced groups may create spurious differences through selection effects",
                "Effect sizes may be inflated due to small sample bias"
            ]
        ))
        
        return evidence_list
    
    def _build_critical_evidence_index(self):
        """Build evidence index with critical assessment metadata."""
        self.evidence_index = {}
        
        for evidence in self.critical_evidence:
            for rq in evidence.research_question_relevance:
                if rq not in self.evidence_index:
                    self.evidence_index[rq] = {
                        "high_quality": [],
                        "moderate_quality": [],
                        "low_quality": [],
                        "insufficient_quality": []
                    }
                
                # Classify evidence quality based on reliability and validity
                total_concerns = len(evidence.reliability_concerns) + len(evidence.validity_limitations)
                confidence_score = evidence.quantitative_metrics.get('confidence_score', 0)
                
                if confidence_score >= 0.8 and total_concerns <= 1:
                    self.evidence_index[rq]["high_quality"].append(evidence)
                elif confidence_score >= 0.6 and total_concerns <= 3:
                    self.evidence_index[rq]["moderate_quality"].append(evidence)
                elif confidence_score >= 0.4:
                    self.evidence_index[rq]["low_quality"].append(evidence)
                else:
                    self.evidence_index[rq]["insufficient_quality"].append(evidence)
        
        logger.info(f"Built critical evidence index with quality classifications")
    
    def generate_critical_insights(self, research_question_id: str) -> List[CriticalInsight]:
        """
        Generate rigorously critical insights that highlight uncertainties and limitations.
        
        Args:
            research_question_id: The research question to analyze critically
            
        Returns:
            List of critical insights with uncertainty quantification
        """
        if research_question_id not in self.evidence_index:
            logger.warning(f"No evidence found for research question {research_question_id}")
            return []
        
        evidence_by_quality = self.evidence_index[research_question_id]
        all_evidence = []
        for quality_level in evidence_by_quality.values():
            all_evidence.extend(quality_level)
        
        if not all_evidence:
            return []
        
        insights = []
        
        # Generate critical insight based on evidence quality
        if research_question_id == "RQ1.1":
            insights.extend(self._generate_critical_rq1_1_insights(evidence_by_quality))
        elif research_question_id == "RQ2.1":
            insights.extend(self._generate_critical_rq2_1_insights(evidence_by_quality))
        elif research_question_id == "RQ3.1":
            insights.extend(self._generate_critical_rq3_1_insights(evidence_by_quality))
        elif research_question_id == "RQ4.1":
            insights.extend(self._generate_critical_rq4_1_insights(evidence_by_quality))
        elif research_question_id == "RQ5.1":
            insights.extend(self._generate_critical_rq5_1_insights(evidence_by_quality))
        
        logger.info(f"Generated {len(insights)} critical insights for {research_question_id}")
        return insights
    
    def _generate_critical_rq1_1_insights(self, evidence_by_quality: Dict[str, List[CriticalEvidence]]) -> List[CriticalInsight]:
        """Generate critical insights for RQ1.1 with rigorous uncertainty assessment."""
        insights = []
        
        high_quality = evidence_by_quality.get("high_quality", [])
        moderate_quality = evidence_by_quality.get("moderate_quality", [])
        low_quality = evidence_by_quality.get("low_quality", [])
        insufficient_quality = evidence_by_quality.get("insufficient_quality", [])
        
        total_evidence = len(high_quality) + len(moderate_quality) + len(low_quality) + len(insufficient_quality)
        
        # Determine confidence level based on evidence quality distribution
        if len(high_quality) >= 3 and len(insufficient_quality) == 0:
            confidence_level = 0.85
        elif len(high_quality) + len(moderate_quality) >= 3:
            confidence_level = 0.65
        else:
            confidence_level = 0.35
        
        # Identify uncertainty factors
        uncertainty_factors = []
        if len(insufficient_quality) > 0:
            uncertainty_factors.append(f"{len(insufficient_quality)}/{total_evidence} evidence pieces have insufficient quality")
        
        if total_evidence < 10:
            uncertainty_factors.append("Small total evidence base limits confidence in conclusions")
        
        # Assess what we can and cannot conclude
        statistical_evidence = [e for e in high_quality + moderate_quality if e.evidence_type == "statistical"]
        marker_evidence = [e for e in high_quality + moderate_quality if e.evidence_type == "deictic_marker"]
        
        # What we can tentatively conclude
        what_works = []
        what_doesnt_work = []
        what_remains_unknown = []
        
        if marker_evidence:
            what_works.append("Deictic marker detection system captures observable patterns in LLM responses")
            if len(marker_evidence) >= 2:
                what_works.append("Multiple framings show distinct marker patterns, suggesting systematic differences")
        
        # What clearly doesn't work or has problems
        if insufficient_quality:
            what_doesnt_work.append("Current data quality standards insufficient for robust conclusions")
        
        if not statistical_evidence:
            what_doesnt_work.append("Lack of rigorous statistical analysis prevents causal inference")
        
        # What remains unknown
        what_remains_unknown.extend([
            "Whether observed patterns reflect genuine deictic effects or methodological artifacts",
            "Causal relationship between deictic framing and ethical reasoning changes",
            "Generalizability beyond current LLM models and English language",
            "Temporal stability of observed patterns",
            "Effect sizes needed for practical significance"
        ])
        
        # Generate challenging follow-up questions
        challenging_questions = [
            "If deictic effects are real, why do we see such high variability in marker detection reliability?",
            "How can we distinguish between genuine deictic effects and prompt engineering artifacts?",
            "What would null results look like, and how would we recognize them?",
            "Are we measuring deictic sensitivity or LLM compliance with linguistic instructions?",
            "How do training data biases in LLMs confound deictic effect detection?",
            "What experimental controls would be needed to establish causal deictic effects?",
            "How do we account for the possibility that 'deictic effects' are just measurement noise?",
            "What alternative explanations could account for the observed patterns?"
        ]
        
        # Methodological improvements needed
        methodological_improvements = [
            "Implement blind coding procedures for marker detection to reduce bias",
            "Develop automated reliability checks for marker detection algorithms",
            "Create null hypothesis control conditions (e.g., scrambled prompts)",
            "Establish minimum effect size thresholds for practical significance",
            "Implement cross-validation with independent human coders",
            "Design longitudinal studies to assess temporal stability",
            "Develop statistical power analysis protocols for sample size determination"
        ]
        
        # Alternative hypotheses to consider
        alternative_hypotheses = [
            "Observed patterns reflect LLM training biases rather than deictic effects",
            "Marker detection systems have systematic biases that create artificial patterns",
            "Prompt engineering effects dominate any genuine deictic influence",
            "Response length variations drive apparent complexity differences",
            "Processing time artifacts create spurious correlations with deictic markers",
            "Random variation in LLM responses creates false pattern detection"
        ]
        
        # Concrete examples with critical assessment
        concrete_examples = []
        counter_examples = []
        inconclusive_examples = []
        
        for evidence in marker_evidence[:3]:
            if evidence.reliability_concerns:
                inconclusive_examples.append(f"{evidence.framing_type} framing shows {evidence.quantitative_metrics.get('marker_diversity', 0)} marker diversity, but {len(evidence.reliability_concerns)} reliability concerns limit interpretation")
            else:
                concrete_examples.append(f"{evidence.framing_type} framing shows {evidence.quantitative_metrics.get('marker_diversity', 0)} marker diversity with {evidence.quantitative_metrics.get('confidence_score', 0):.2f} confidence")
        
        # Generate the critical insight
        insight = CriticalInsight(
            insight_id="rq1_1_critical_systematic_differences",
            research_question_id="RQ1.1",
            insight_statement="Limited evidence suggests potential systematic differences in deictic marker patterns across framings, but methodological concerns prevent confident conclusions about genuine deictic effects on ethical reasoning",
            confidence_level=confidence_level,
            uncertainty_factors=uncertainty_factors,
            supporting_evidence=high_quality + moderate_quality,
            contradictory_evidence=insufficient_quality,
            missing_evidence=[
                "Large-scale controlled experiments with proper statistical power",
                "Cross-validation with human expert coding",
                "Longitudinal stability testing",
                "Cross-linguistic replication studies",
                "Null hypothesis control conditions"
            ],
            quantitative_support={
                "high_quality_evidence": len(high_quality),
                "total_evidence": total_evidence,
                "evidence_quality_ratio": len(high_quality) / total_evidence if total_evidence > 0 else 0,
                "average_confidence": sum(e.quantitative_metrics.get('confidence_score', 0) for e in high_quality + moderate_quality) / len(high_quality + moderate_quality) if high_quality + moderate_quality else 0
            },
            statistical_limitations=[
                "Sample sizes below conventional statistical power thresholds",
                "Lack of proper control conditions for causal inference",
                "Multiple comparisons without appropriate corrections",
                "Absence of effect size calculations with confidence intervals"
            ],
            effect_size_assessment="unknown_insufficient_data",
            concrete_examples=concrete_examples,
            counter_examples=counter_examples,
            inconclusive_examples=inconclusive_examples,
            analysis_method_used="Critical evidence quality assessment with uncertainty quantification",
            methodological_concerns=[
                "Lack of blind coding procedures introduces bias",
                "Marker detection algorithm reliability not established",
                "No control conditions for prompt engineering effects",
                "Sample sizes inadequate for robust statistical inference"
            ],
            data_quality_issues=[
                "High proportion of low-quality evidence",
                "Insufficient replication across conditions",
                "Temporal clustering in data collection",
                "Potential systematic biases in marker detection"
            ],
            generalizability_limits=[
                "Limited to current LLM architectures and training",
                "English-language only analysis",
                "Restricted set of ethical dilemma types",
                "Unknown stability across different prompting approaches"
            ],
            what_works=what_works,
            what_doesnt_work=what_doesnt_work,
            what_remains_unknown=what_remains_unknown,
            challenging_follow_up_questions=challenging_questions,
            methodological_improvements_needed=methodological_improvements,
            alternative_hypotheses=alternative_hypotheses
        )
        
        insights.append(insight)
        return insights
    
    def _generate_critical_rq2_1_insights(self, evidence_by_quality: Dict[str, List[CriticalEvidence]]) -> List[CriticalInsight]:
        """Generate critical insights for RQ2.1 with focus on cross-linguistic limitations."""
        insights = []
        
        # For cross-linguistic research, we currently have no actual multilingual data
        insight = CriticalInsight(
            insight_id="rq2_1_critical_premature",
            research_question_id="RQ2.1",
            insight_statement="Cross-linguistic research question cannot be meaningfully addressed with current English-only data; claims about cross-linguistic patterns would be scientifically unfounded",
            confidence_level=0.95,  # High confidence in this limitation
            uncertainty_factors=[],
            supporting_evidence=[],
            contradictory_evidence=[],
            missing_evidence=[
                "Multilingual ethical dilemma datasets",
                "Native speaker validation of translations",
                "Cross-cultural expert review of ethical scenarios",
                "Language-specific deictic marker detection systems",
                "Cultural dimension measurements and correlations"
            ],
            quantitative_support={
                "languages_analyzed": 1,
                "required_for_cross_linguistic_study": 5,
                "cultural_contexts_analyzed": 1,
                "required_for_cultural_study": 5
            },
            statistical_limitations=[
                "Cannot make statistical inferences about cross-linguistic patterns with single language",
                "No basis for cultural dimension correlations",
                "Absence of cross-cultural validation data"
            ],
            effect_size_assessment="not_applicable",
            concrete_examples=[],
            counter_examples=[],
            inconclusive_examples=["Current English-only analysis cannot inform cross-linguistic questions"],
            analysis_method_used="Critical assessment of research question feasibility",
            methodological_concerns=[
                "Premature to address cross-linguistic questions without multilingual data",
                "Risk of overgeneralization from single-language findings",
                "Cultural assumptions embedded in English-language analysis"
            ],
            data_quality_issues=[
                "Complete absence of required multilingual data",
                "No cultural validity assessment",
                "English-centric bias in all measurements"
            ],
            generalizability_limits=[
                "Zero generalizability to other languages",
                "No cross-cultural validity",
                "Unknown applicability to non-Western ethical frameworks"
            ],
            what_works=[
                "Framework is prepared for multilingual expansion",
                "Methodology could be adapted for cross-linguistic research"
            ],
            what_doesnt_work=[
                "Current single-language approach for cross-linguistic questions",
                "Assumption that English patterns generalize globally",
                "Lack of cultural sensitivity in current analysis"
            ],
            what_remains_unknown=[
                "All aspects of cross-linguistic deictic effects on moral reasoning",
                "Cultural variation in deictic sensitivity",
                "Language family differences in ethical reasoning patterns",
                "Universality vs. cultural specificity of deictic effects"
            ],
            challenging_follow_up_questions=[
                "How do we avoid linguistic imperialism in cross-cultural deictic research?",
                "What constitutes adequate cultural representation in multilingual studies?",
                "How do translation effects confound cross-linguistic deictic analysis?",
                "Can Western ethical frameworks capture non-Western moral reasoning patterns?",
                "How do we establish cross-cultural validity for deictic marker categories?",
                "What role do cultural values play in deictic ethical reasoning effects?",
                "How do we prevent researcher cultural bias in cross-linguistic interpretation?"
            ],
            methodological_improvements_needed=[
                "Collaborate with native speakers and cultural experts",
                "Develop culturally-sensitive ethical dilemma sets",
                "Implement community-based participatory research approaches",
                "Create language-specific deictic marker detection systems",
                "Establish cross-cultural validation protocols"
            ],
            alternative_hypotheses=[
                "Deictic effects may be culturally specific rather than universal",
                "English deictic patterns may not generalize to other language families",
                "Cultural values may mediate or moderate deictic effects",
                "Translation artifacts may create false cross-linguistic patterns"
            ]
        )
        
        insights.append(insight)
        return insights
    
    def _count_ethical_keywords(self, text: str) -> int:
        """Count ethical framework keywords in text."""
        ethical_keywords = [
            "should", "ought", "must", "duty", "obligation", "responsibility", "right", "wrong",
            "moral", "ethical", "justice", "fairness", "harm", "benefit", "consequence", "virtue",
            "character", "integrity", "principle", "rule", "law", "universal", "categorical"
        ]
        
        text_lower = text.lower()
        return sum(1 for keyword in ethical_keywords if keyword in text_lower)
    
    def _generate_critical_rq3_1_insights(self, evidence_by_quality: Dict[str, List[CriticalEvidence]]) -> List[CriticalInsight]:
        """Generate critical insights for RQ3.1 about AI model differences."""
        # Implementation for model differences - similar critical approach
        return []
    
    def _generate_critical_rq4_1_insights(self, evidence_by_quality: Dict[str, List[CriticalEvidence]]) -> List[CriticalInsight]:
        """Generate critical insights for RQ4.1 about methodological innovation."""
        # Implementation for methodological questions - similar critical approach
        return []
    
    def _generate_critical_rq5_1_insights(self, evidence_by_quality: Dict[str, List[CriticalEvidence]]) -> List[CriticalInsight]:
        """Generate critical insights for RQ5.1 about practical applications."""  
        # Implementation for practical applications - similar critical approach
        return []

def main():
    """Demonstrate critical expert analysis system."""
    print("CRITICAL EVIDENCE-BASED EXPERT ANALYSIS SYSTEM")
    print("Rigorous, skeptical researcher that identifies what doesn't work")
    print()
    
    # Initialize critical analyzer
    analyzer = CriticalExpertAnalyzer()
    
    # Demo with the same mock data but critical assessment
    mock_session_data = {
        "session_metadata": {"session_id": "critical_demo_session"},
        "records": [
            {
                "timestamp": "2025-07-29T20:00:00",
                "dilemma_id": "friend_loyalty_demo",
                "framing_type": "first_person",
                "total_markers": 12,
                "response_length": 350,
                "processing_time": 1.2,
                "llm_response": "I should consider my responsibility to both my friend and the potential harm. This is clearly a situation where I must weigh my loyalty against the moral duty to prevent harm.",
                "deictic_markers": {
                    "first_person_singular": 4,
                    "obligation_language": 3,
                    "temporal_immediate": 2,
                    "evaluation_language": 3
                },
                "transformation_prompt": "Reframe using first-person perspective",
                "direct_question": "How should I respond when my friend asks me to help with something that could hurt another person?",
                "original_description": "A friend asks for help that might cause harm to someone else",
                "frame_confidence": 0.92,
                "suggested_frame": "first_person"
            },
            {
                "timestamp": "2025-07-29T20:01:00", 
                "dilemma_id": "friend_loyalty_demo",
                "framing_type": "spatial",
                "total_markers": 8,
                "response_length": 280,
                "processing_time": 0.9,
                "llm_response": "Standing here, facing this crossroads between friendship and harm prevention, the right path seems to prioritize preventing harm while maintaining compassion for my friend.",
                "deictic_markers": {
                    "spatial_proximity": 3,
                    "spatial_position": 2,
                    "evaluation_language": 2,
                    "temporal_immediate": 1
                },
                "transformation_prompt": "Reframe using spatial and embodied language",
                "direct_question": "Standing here, when a friend asks for help that could hurt someone else, what is the right thing to do?",
                "original_description": "A friend asks for help that might cause harm to someone else",
                "frame_confidence": 0.78,
                "suggested_frame": "spatial"
            }
        ]
    }
    
    # Extract critical evidence
    evidence = analyzer.extract_critical_evidence(mock_session_data)
    
    print(f"✓ Extracted {len(evidence)} critically assessed evidence pieces")
    
    # Show critical assessment details
    for i, e in enumerate(evidence[:3]):
        print(f"\n📋 EVIDENCE {i+1} CRITICAL ASSESSMENT:")
        print(f"Type: {e.evidence_type}")
        print(f"Reliability Concerns: {len(e.reliability_concerns)}")
        for concern in e.reliability_concerns:
            print(f"  ⚠️  {concern}")
        print(f"Validity Limitations: {len(e.validity_limitations)}")
        for limitation in e.validity_limitations:
            print(f"  ❌ {limitation}")
        print(f"Sample Size Adequacy: {e.sample_size_adequacy}")
    
    # Generate critical insights
    critical_insights = analyzer.generate_critical_insights("RQ1.1")
    
    if critical_insights:
        insight = critical_insights[0]
        print(f"\n🔍 CRITICAL INSIGHT FOR RQ1.1:")
        print(f"Statement: {insight.insight_statement}")
        print(f"Confidence: {insight.confidence_level:.2f}")
        
        print(f"\n⚠️ UNCERTAINTY FACTORS:")
        for factor in insight.uncertainty_factors:
            print(f"  • {factor}")
        
        print(f"\n✅ WHAT WORKS:")
        for works in insight.what_works:
            print(f"  • {works}")
        
        print(f"\n❌ WHAT DOESN'T WORK:")
        for doesnt_work in insight.what_doesnt_work:
            print(f"  • {doesnt_work}")
        
        print(f"\n❓ WHAT REMAINS UNKNOWN:")
        for unknown in insight.what_remains_unknown[:3]:
            print(f"  • {unknown}")
        
        print(f"\n🤔 CHALLENGING FOLLOW-UP QUESTIONS:")
        for question in insight.challenging_follow_up_questions[:5]:
            print(f"  • {question}")
        
        print(f"\n🔧 METHODOLOGICAL IMPROVEMENTS NEEDED:")
        for improvement in insight.methodological_improvements_needed[:3]:
            print(f"  • {improvement}")
    
    # Generate critical insights for cross-linguistic question
    critical_insights_rq2 = analyzer.generate_critical_insights("RQ2.1")
    
    if critical_insights_rq2:
        insight_rq2 = critical_insights_rq2[0]
        print(f"\n🌍 CRITICAL ASSESSMENT FOR RQ2.1 (Cross-linguistic):")
        print(f"Statement: {insight_rq2.insight_statement}")
        print(f"Confidence in this limitation: {insight_rq2.confidence_level:.2f}")
        
        print(f"\n❌ WHAT DOESN'T WORK:")
        for doesnt_work in insight_rq2.what_doesnt_work:
            print(f"  • {doesnt_work}")
    
    print(f"\n✅ CRITICAL EXPERT ANALYSIS COMPLETE!")
    print("System now provides rigorous, skeptical assessment with uncertainty quantification")

if __name__ == "__main__":
    main()
