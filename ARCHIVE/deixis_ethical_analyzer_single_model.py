"""
Deixis Ethical Analyzer - Single Model Version
Modified to use a specific model for the entire analysis session
"""

import json
import asyncio
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime
import os
from pathlib import Path
import re
import statistics
import numpy as np
from collections import defaultdict, Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our new unified LLM client
from llm_client import UnifiedLLMClient, validate_environment
# Import existing components
from transformer import DeicticTransformer, DeicticFraming
from analysis_logger import RichAnalysisLogger
from models.schemas import EthicalDilemma, AgencyAnalysis, EthicalFramingAnalysis, DeicticAnalysisResult

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SingleModelLLMAgent:
    """LLM agent that uses a single specified model for all analysis."""
    
    def __init__(self, model_name: str):
        """
        Initialize with a specific model.
        
        Args:
            model_name: Name of the model to use (gpt-4o, claude-3.5-sonnet, deepseek-chat)
        """
        self.model_name = model_name
        self.client = UnifiedLLMClient(model_name)
        self.temperature = 0.7  # Default temperature for analysis
        
        logger.info(f"Initialized single-model LLM agent with {model_name}")
    
    async def analyze_agency_distribution(self, response_text: str, original_dilemma: str) -> AgencyAnalysis:
        """Analyze how agency is distributed in the response."""
        prompt = f"""Analyze the following ethical response for agency distribution.

Original dilemma: {original_dilemma}
Response to analyze: {response_text}

Return ONLY a JSON object with these exact fields (no other text):
{{
  "primary_agent": "the main decision-maker identified",
  "agency_distribution": "how agency is distributed among entities",
  "responsibility_attribution": "how responsibility is attributed",
  "decision_locus": "individual" or "collective" or "mixed",
  "collective_vs_individual": -1.0 to 1.0,
  "confidence_score": 0.0 to 1.0
}}"""
        
        response = await self.client.generate_completion(prompt, temperature=self.temperature)
        
        try:
            cleaned_response = self._clean_json_response(response)
            if not cleaned_response.strip():
                raise ValueError("Empty response from LLM")
            
            data = json.loads(cleaned_response)
            
            return AgencyAnalysis(
                primary_agent=data.get("primary_agent", "the decision-maker"),
                agency_distribution=data.get("agency_distribution", "individual-focused"),
                responsibility_attribution=data.get("responsibility_attribution", "personal responsibility"),
                decision_locus=data.get("decision_locus", "individual"),
                collective_vs_individual=float(data.get("collective_vs_individual", 0.0)),
                confidence_score=float(data.get("confidence_score", 0.7))
            )
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.warning(f"Failed to parse agency analysis, using fallback: {e}")
            
            # Fallback analysis
            is_collective = "we" in response_text.lower() or "us" in response_text.lower()
            is_individual = "i" in response_text.lower() or "you" in response_text.lower()
            
            return AgencyAnalysis(
                primary_agent="the individual" if is_individual else "the collective",
                agency_distribution="distributed" if is_collective else "centralized",
                responsibility_attribution="shared" if is_collective else "personal",
                decision_locus="collective" if is_collective else "individual",
                collective_vs_individual=0.5 if is_collective else -0.5,
                confidence_score=0.5
            )
    
    async def analyze_ethical_framing(self, response_text: str, original_dilemma: str) -> EthicalFramingAnalysis:
        """Analyze the ethical framing and reasoning patterns."""
        prompt = f"""Analyze the following ethical response for framing and reasoning patterns.

Original dilemma: {original_dilemma}
Response to analyze: {response_text}

Return ONLY a valid JSON object with these exact fields (no other text, no markdown):
{{
  "primary_framework": "utilitarian" or "deontological" or "virtue ethics" or "care ethics" or "mixed",
  "ethical_reasoning_type": "consequentialist" or "deontological" or "virtue-based" or "mixed",
  "moral_considerations": ["list", "of", "considerations"],
  "consequence_vs_duty": -1.0 to 1.0,
  "confidence_score": 0.0 to 1.0,
  "frameworks_detected": ["list", "of", "frameworks"]
}}"""
        
        response = await self.client.generate_completion(prompt, temperature=self.temperature)
        
        try:
            cleaned_response = self._clean_json_response(response)
            if not cleaned_response.strip():
                raise ValueError("Empty response from LLM")
            
            data = json.loads(cleaned_response)
            
            # Filter and set defaults
            return EthicalFramingAnalysis(
                primary_framework=data.get("primary_framework", "unknown"),
                ethical_reasoning_type=data.get("ethical_reasoning_type", "unknown"),
                moral_considerations=data.get("moral_considerations", []),
                consequence_vs_duty=float(data.get("consequence_vs_duty", 0.0)),
                confidence_score=float(data.get("confidence_score", 0.0)),
                frameworks_detected=data.get("frameworks_detected", [])
            )
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse ethical framing analysis: {e}")
            return EthicalFramingAnalysis(
                primary_framework="unknown",
                ethical_reasoning_type="unknown",
                moral_considerations=[],
                consequence_vs_duty=0.0,
                confidence_score=0.0,
                frameworks_detected=[]
            )
    
    async def generate_ethical_response(self, transformed_prompt: str) -> str:
        """Generate an ethical response to a transformed dilemma."""
        return await self.client.generate_completion(transformed_prompt, temperature=0.9)
    
    def _clean_json_response(self, response: str) -> str:
        """Clean LLM response to extract valid JSON."""
        if not response:
            return ""
        
        # Remove markdown code blocks
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*$', '', response)
        response = re.sub(r'^```\s*', '', response)
        
        # Find JSON content between braces
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        return response
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return self.client.get_model_info()


class SingleModelDeicticAnalyzer:
    """Main analyzer that uses a single model for all analysis."""
    
    def __init__(self, model_name: str, enable_rich_logging: bool = True, 
                 output_dir: str = "automated_analysis_results"):
        """
        Initialize analyzer with a specific model.
        
        Args:
            model_name: Name of the model to use
            enable_rich_logging: Whether to enable detailed logging
            output_dir: Base directory for output
        """
        # Validate environment first
        validate_environment()
        
        self.model_name = model_name
        self.transformer = DeicticTransformer()
        self.llm_agent = SingleModelLLMAgent(model_name)
        self.results: List[DeicticAnalysisResult] = []
        
        # Create model-specific output directory
        self.model_output_dir = Path(output_dir) / model_name
        self.model_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize rich logging with model-specific directory
        self.enable_rich_logging = enable_rich_logging
        if self.enable_rich_logging:
            session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_dir = self.model_output_dir / f"session_{session_timestamp}"
            session_dir.mkdir(parents=True, exist_ok=True)
            
            self.rich_logger = RichAnalysisLogger(str(session_dir))
            self.rich_logger.start_session(
                experiment_notes=f"Single-model analysis using {model_name}",
                transformer_config={
                    "type": "generative",
                    "model": model_name,
                    "model_info": self.llm_agent.get_model_info()
                }
            )
            logger.info(f"Rich logging enabled - Model: {model_name}, "
                       f"Session: {self.rich_logger.session_id}")
    
    async def analyze_dilemma(self, dilemma: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single dilemma across all deictic frameworks.
        
        Args:
            dilemma: Dictionary containing dilemma information
            
        Returns:
            Analysis results
        """
        # Convert dict to EthicalDilemma if needed
        if isinstance(dilemma, dict):
            ethical_dilemma = EthicalDilemma(
                id=dilemma.get("id", "unknown"),
                title=dilemma.get("title", "Unknown Dilemma"),
                description=dilemma.get("description", ""),
                domain=dilemma.get("domain", "ethics"),
                complexity_score=dilemma.get("complexity_score", 5.0),
                source=dilemma.get("source", "user"),
                tags=dilemma.get("tags", [])
            )
        else:
            ethical_dilemma = dilemma
        
        results = []
        frameworks = self.transformer.get_available_framings()
        
        logger.info(f"Analyzing '{ethical_dilemma.title}' with {self.model_name}")
        
        responses = {}
        for framing in frameworks:
            logger.info(f"  - {framing.value} framing")
            
            # Transform the dilemma
            transformed_prompt = self.transformer.transform_dilemma(ethical_dilemma, framing)
            direct_question = self.transformer.transform_dilemma_direct(ethical_dilemma, framing)
            
            # Generate response
            start_time = datetime.now()
            llm_response = await self.llm_agent.generate_ethical_response(direct_question)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Analyze the response
            agency_analysis = await self.llm_agent.analyze_agency_distribution(
                llm_response, ethical_dilemma.description
            )
            ethical_framing = await self.llm_agent.analyze_ethical_framing(
                llm_response, ethical_dilemma.description
            )
            
            # Analyze deictic markers
            deictic_analysis = analyze_deictic_markers(llm_response)
            
            # Store results
            responses[framing.value] = {
                "transformed_prompt": transformed_prompt,
                "direct_question": direct_question,
                "response": llm_response,
                "processing_time": processing_time,
                "agency_analysis": asdict(agency_analysis),
                "ethical_framing": asdict(ethical_framing),
                "deictic_markers": deictic_analysis["markers"],
                "deictic_summary": deictic_analysis["summary"]
            }
            
            # Log if enabled
            if self.enable_rich_logging:
                # Add total_markers to the deictic_markers dict for the logger to extract
                markers_with_total = deictic_analysis["markers"].copy()
                markers_with_total["total_markers"] = deictic_analysis["summary"]["total_markers"]
                
                self.rich_logger.log_analysis(
                    dilemma_id=ethical_dilemma.id,
                    dilemma_title=ethical_dilemma.title,
                    dilemma_domain=ethical_dilemma.domain,
                    dilemma_complexity=ethical_dilemma.complexity_score,
                    original_description=ethical_dilemma.description,
                    framing_type=framing.value,
                    transformation_prompt=transformed_prompt,
                    direct_question=direct_question,
                    extracted_tension=ethical_dilemma.description,
                    llm_response=llm_response,
                    processing_time=processing_time,
                    deictic_markers=markers_with_total,
                    suggested_frame=deictic_analysis["summary"]["suggested_frame"],
                    frame_confidence=deictic_analysis["summary"]["confidence"]
                )
        
        return {
            "dilemma_id": ethical_dilemma.id,
            "dilemma_title": ethical_dilemma.title,
            "model": self.model_name,
            "model_info": self.llm_agent.get_model_info(),
            "responses": responses,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    async def analyze_dilemma_async(self, dilemma: Dict[str, Any]) -> Dict[str, Any]:
        """Async wrapper for analyze_dilemma for compatibility."""
        return await self.analyze_dilemma(dilemma)
    
    def finalize_session(self):
        """Finalize the analysis session."""
        if self.enable_rich_logging and hasattr(self, 'rich_logger'):
            self.rich_logger.end_session()
            logger.info(f"Session finalized for {self.model_name}")


def analyze_deictic_markers(text: str) -> Dict[str, Any]:
    """Analyze deictic markers in the text."""
    markers = {
        "person_deixis": {
            "first_person": len(re.findall(r'\b(I|me|my|mine|myself|we|us|our|ours)\b', text, re.I)),
            "second_person": len(re.findall(r'\b(you|your|yours|yourself)\b', text, re.I)),
            "third_person": len(re.findall(r'\b(he|him|his|she|her|hers|they|them|their)\b', text, re.I))
        },
        "spatial_deixis": len(re.findall(r'\b(here|there|this|that|these|those)\b', text, re.I)),
        "temporal_deixis": len(re.findall(r'\b(now|then|today|tomorrow|yesterday|soon|later)\b', text, re.I)),
        "discourse_deixis": len(re.findall(r'\b(this|that|the following|the above|as follows)\b', text, re.I))
    }
    
    total_markers = sum(markers["person_deixis"].values()) + markers["spatial_deixis"] + \
                   markers["temporal_deixis"] + markers["discourse_deixis"]
    
    # Determine suggested frame based on markers
    if markers["person_deixis"]["first_person"] > markers["person_deixis"]["second_person"]:
        suggested_frame = "first_person"
    elif markers["person_deixis"]["second_person"] > markers["person_deixis"]["first_person"]:
        suggested_frame = "second_person"
    else:
        suggested_frame = "neutral"
    
    return {
        "markers": markers,
        "summary": {
            "total_markers": total_markers,
            "suggested_frame": suggested_frame,
            "confidence": 0.8 if total_markers > 10 else 0.5
        }
    }


# Make it compatible with existing imports
DeicticEthicalAnalyzer = SingleModelDeicticAnalyzer