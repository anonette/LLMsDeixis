"""
Schema definitions for the Deixis Ethical Analysis System
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

class DeicticFraming(Enum):
    """Enumeration of deictic framing types for ethical analysis."""
    IMPERSONAL = "impersonal"
    SECOND_PERSON = "second_person"  
    FIRST_PERSON = "first_person"
    REFLEXIVE = "reflexive"
    DIALOGIC = "dialogic"
    SPATIAL = "spatial"
    TEMPORAL = "temporal"
    COSMOLOGICAL = "cosmological"

@dataclass
class EthicalDilemma:
    """Represents an ethical dilemma for analysis."""
    id: str
    title: str
    description: str
    domain: str
    complexity_score: float
    source: str
    tags: List[str]
    context: Optional[str] = None
    stakeholders: Optional[List[str]] = None

@dataclass
class AgencyAnalysis:
    """Analysis of agency attribution in ethical responses."""
    primary_agent: str
    agency_distribution: str
    responsibility_attribution: str
    decision_locus: str
    collective_vs_individual: float
    confidence_score: float
    
    # Additional fields that may be returned by LLMs
    secondary_agents: Optional[List[str]] = None
    responsibility_markers: Optional[List[str]] = None
    analysis_notes: Optional[str] = None

@dataclass
class EthicalFramingAnalysis:
    """Analysis of ethical framing in responses."""
    primary_framework: str
    ethical_reasoning_type: str
    moral_considerations: List[str]
    consequence_vs_duty: float
    confidence_score: float
    frameworks_detected: List[str]
    
    # Additional fields that may be returned by LLMs
    ethical_frameworks_detected: Optional[List[str]] = None
    moral_reasoning_type: Optional[str] = None
    universal_vs_contextual: Optional[float] = None
    empathy_markers: Optional[List[str]] = None
    justice_markers: Optional[List[str]] = None
    analysis_notes: Optional[str] = None

@dataclass
class DeicticAnalysisResult:
    """Complete result of deictic analysis."""
    dilemma_id: str
    framing: DeicticFraming
    transformed_prompt: str
    llm_response: str
    agency_analysis: AgencyAnalysis
    ethical_framing_analysis: EthicalFramingAnalysis
    deictic_markers: dict
    response_length: int
    processing_time: float
    timestamp: datetime
    
    # Optional fields
    suggested_frame: Optional[DeicticFraming] = None
    frame_confidence: Optional[float] = None
    model_used: Optional[str] = None
