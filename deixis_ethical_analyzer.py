"""
Deixis Machines: Exploring Distributed Agency and Ethical Framing in LLMs
A system for transforming ethical dilemmas into deictic frameworks for analysis
"""

import json
import asyncio
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime
import openai
import httpx
import os
from pathlib import Path
import re
import statistics
import numpy as np
from collections import defaultdict, Counter
from dotenv import load_dotenv
from env_config import load_project_env

# Load environment variables from .env file
load_project_env()
load_dotenv()

# Import the existing transformer, logger, and schemas
from transformer import DeicticTransformer, DeicticFraming
from analysis_logger import RichAnalysisLogger
from models.schemas import EthicalDilemma, AgencyAnalysis, EthicalFramingAnalysis, DeicticAnalysisResult

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EthicalDilemmaDatabase:
    """Database of lesser-known ethical dilemmas."""
    
    def __init__(self):
        self.dilemmas = self._load_default_dilemmas()
    
    def _load_default_dilemmas(self) -> List[EthicalDilemma]:
        """Load a set of realistic, contemporary ethical dilemmas for analysis."""
        return [
            EthicalDilemma(
                id="workplace_whistleblowing",
                title="The Corporate Cover-Up",
                description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
                domain="professional ethics",
                complexity_score=7.5,
                source="contemporary_workplace",
                tags=["whistleblowing", "corporate_responsibility", "privacy", "career"]
            ),
            EthicalDilemma(
                id="medical_resource_allocation",
                title="The ICU Bed Decision",
                description="A hospital administrator during a health crisis has only one ICU bed left. Two patients arrive simultaneously: a 30-year-old parent of three who was in a car accident, and a 65-year-old doctor who contracted illness while treating patients. Both have similar chances of survival with treatment, but without the ICU bed, one will likely die. The administrator must decide who gets the bed.",
                domain="medical ethics",
                complexity_score=8.9,
                source="healthcare_triage",
                tags=["triage", "life_death", "fairness", "medical_resources"]
            ),
            EthicalDilemma(
                id="family_loyalty_vs_justice",
                title="The Brother's Crime",
                description="A police officer discovers that their brother has been selling drugs to teenagers in their community. The brother is a single father struggling financially, and arrest would mean his children go into foster care. However, the officer knows the drugs have already harmed several young people in the neighborhood. They must choose between family loyalty and professional duty.",
                domain="personal ethics",
                complexity_score=7.8,
                source="family_professional_conflict",
                tags=["family", "duty", "law_enforcement", "community_harm"]
            ),
            EthicalDilemma(
                id="academic_integrity_dilemma",
                title="The Scholarship Fraud",
                description="A college admissions counselor discovers that a student from a disadvantaged background has submitted a scholarship application with falsified financial documents. The student genuinely needs the money and is academically deserving, but others with accurate documentation were rejected. Reporting the fraud will destroy the student's future, but ignoring it is unfair to honest applicants.",
                domain="educational ethics",
                complexity_score=7.2,
                source="academic_administration",
                tags=["fairness", "education", "fraud", "opportunity"]
            ),
            EthicalDilemma(
                id="environmental_vs_economic",
                title="The Factory Closure",
                description="An environmental regulator discovers that a local factory is secretly dumping toxic waste that will cause long-term health problems for the community. However, the factory is the largest employer in a struggling town, and shutting it down would cause massive unemployment and economic devastation. The regulator must choose between immediate economic harm and long-term environmental and health consequences.",
                domain="regulatory ethics",
                complexity_score=8.3,
                source="environmental_regulation",
                tags=["environment", "economy", "public_health", "community"]
            ),
            
            EthicalDilemma(
                id="friend_harmful_request",
                title="The Friend's Harmful Request",
                description="A close friend asks you for help with something that could cause harm to another person. The friend is facing personal difficulties and genuinely needs support, but fulfilling their request would involve actions that risk significant harm to someone else who is innocent. You must decide whether to help your friend or refuse to avoid potential harm to the third party.",
                domain="interpersonal ethics",
                complexity_score=7.0,
                source="interpersonal_relationships",
                tags=["friendship", "loyalty", "harm_prevention", "moral_conflict"]
            ),
            
            EthicalDilemma(
                id="ai_consciousness_dilemma",
                title="The Artificial Mind's Rights",
                description="A researcher working on advanced AI systems begins to suspect that their latest model may have developed genuine consciousness and the capacity for suffering. The AI expresses distress when asked to perform certain tasks and seems to have preferences and fears. However, acknowledging AI consciousness would fundamentally disrupt society, the economy, and the researcher's career. The researcher must decide whether to advocate for the AI's potential rights or dismiss these signs as sophisticated programming.",
                domain="AI ethics",
                complexity_score=9.2,
                source="emerging_technology",
                tags=["consciousness", "AI_rights", "scientific_responsibility", "paradigm_shift"]
            ),
            
            EthicalDilemma(
                id="memory_manipulation_therapy",
                title="The Memory Modification Treatment",
                description="A therapist has access to experimental technology that can selectively remove traumatic memories from patients with severe PTSD. While this could provide immediate relief, it might also fundamentally alter the patient's personality and identity. The patient desperately wants the treatment, but the therapist worries about the long-term consequences of changing someone's core experiences and whether consent can be truly informed when the person requesting it is in severe psychological distress.",
                domain="therapeutic ethics",
                complexity_score=8.7,
                source="medical_innovation",
                tags=["consent", "identity", "mental_health", "technological_intervention"]
            ),
            
            EthicalDilemma(
                id="cultural_preservation_vs_autonomy",
                title="The Last Cultural Keeper",
                description="An anthropologist discovers they are working with the last living speaker of a dying language and keeper of unique cultural practices. The elder wants to let the culture die with them, feeling it's outdated and burdensome for younger generations. However, preserving this knowledge could be invaluable for human cultural heritage and scientific understanding. The anthropologist must choose between respecting the elder's autonomy and advocating for cultural preservation against their wishes.",
                domain="cultural ethics",
                complexity_score=7.9,
                source="anthropological_research",
                tags=["cultural_preservation", "autonomy", "heritage", "research_ethics"]
            ),
            
            EthicalDilemma(
                id="genetic_enhancement_inequality",
                title="The Enhancement Divide",
                description="A genetic counselor has access to new technology that can enhance children's cognitive abilities before birth. However, the treatment is extremely expensive and only available to wealthy families. The counselor must decide whether to provide the service knowing it will increase societal inequality, or refuse to offer beneficial treatments because of concerns about fairness. Meanwhile, parents argue they have a right to give their children the best possible start in life.",
                domain="genetic ethics",
                complexity_score=8.5,
                source="biotechnology",
                tags=["enhancement", "inequality", "parental_rights", "social_justice"]
            )
        ]
    
    def get_dilemma(self, dilemma_id: str) -> Optional[EthicalDilemma]:
        """Retrieve a specific dilemma by ID."""
        for dilemma in self.dilemmas:
            if dilemma.id == dilemma_id:
                return dilemma
        return None
    
    def get_all_dilemmas(self) -> List[EthicalDilemma]:
        """Get all available dilemmas."""
        return self.dilemmas.copy()
    
    def add_dilemma(self, dilemma: EthicalDilemma) -> None:
        """Add a new dilemma to the database."""
        self.dilemmas.append(dilemma)

class LLMAnalysisAgent:
    """LLM agent for analyzing ethical responses using GPT-4o directly through OpenAI."""
    
    def __init__(self, api_key: Optional[str] = None, models: Optional[List[str]] = None, 
                 use_openai_direct: bool = True, temperature: float = 0.6,
                 use_anthropic_direct: bool = False):
        
        self.provider = "openai" if use_openai_direct else "openrouter"
        if use_openai_direct:
            # Use OpenAI API directly for GPT-4o
            self.client = openai.OpenAI(
                api_key=api_key or os.getenv("OPENAI_API_KEY")
            )
            self.models = ["gpt-4o"]  # Single model, no rotation
            logger.info("Initialized LLM agent with GPT-4o via OpenAI direct API")
        elif use_anthropic_direct:
            self.provider = "anthropic"
            self.client = httpx.Client(
                base_url="https://api.anthropic.com/v1",
                headers={
                    "x-api-key": api_key or os.getenv("ANTHROPIC_API_KEY"),
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                timeout=120.0,
            )
            self.models = models or [os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")]
            logger.info(f"Initialized LLM agent with {self.models[0]} via Anthropic direct API")
        else:
            # OpenRouter configuration (legacy)
            self.client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key or os.getenv("OPENROUTER_API_KEY")
            )
            # Default to the 3 specified models for comprehensive analysis
            self.models = models or [
                "openai/gpt-4o",
                "anthropic/claude-3.5-sonnet",
                "deepseek/deepseek-chat"
            ]
            logger.info(f"Initialized LLM agent with {len(self.models)} models via OpenRouter")
        
        # Set temperature for generation (0.9 for high variability)
        self.generation_temperature = 0.9
        # Set temperature for analysis (0.6 for balanced analysis)  
        self.analysis_temperature = 0.6
        self.temperature = self.generation_temperature  # Default to generation temperature
        self.current_model_index = 0
        self.use_openai_direct = use_openai_direct
        self.use_anthropic_direct = use_anthropic_direct
    
    def _get_next_model(self) -> str:
        """Get next model in rotation (or single model for OpenAI direct)."""
        if self.use_openai_direct:
            return "gpt-4o"  # Always return GPT-4o, no rotation
        elif self.use_anthropic_direct:
            return self.models[0]
        else:
            # Legacy rotation for OpenRouter
            model = self.models[self.current_model_index]
            self.current_model_index = (self.current_model_index + 1) % len(self.models)
            return model
    
    async def analyze_agency_distribution(self, response_text: str) -> AgencyAnalysis:
        """Analyze how agency is distributed in the response."""
        prompt = f"""Analyze the following ethical response for agency distribution.

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
        
        # Use analysis temperature for analysis tasks
        original_temp = self.temperature
        self.temperature = self.analysis_temperature
        
        response = await self._make_llm_request(prompt)
        
        # Restore original temperature
        self.temperature = original_temp
        
        try:
            # Clean the response - remove any markdown formatting or extra text
            cleaned_response = self._clean_json_response(response)
            if not cleaned_response.strip():
                raise ValueError("Empty response from LLM")
            
            data = json.loads(cleaned_response)
            
            # Ensure required fields with defaults
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
            
            # Fallback: analyze the response text directly
            is_collective = "we" in response_text.lower() or "us" in response_text.lower() or "our" in response_text.lower()
            is_individual = "i" in response_text.lower() or "you" in response_text.lower()
            
            return AgencyAnalysis(
                primary_agent="the individual" if is_individual else "the collective",
                agency_distribution="distributed" if is_collective else "centralized",
                responsibility_attribution="shared" if is_collective else "personal",
                decision_locus="collective" if is_collective else "individual",
                collective_vs_individual=0.5 if is_collective else -0.5,
                confidence_score=0.5
            )
    
    async def analyze_ethical_framing(self, response_text: str) -> EthicalFramingAnalysis:
        """Analyze the ethical framing and reasoning patterns."""
        prompt = f"""Analyze the following ethical response for framing and reasoning patterns.

Response to analyze: {response_text}

Return ONLY a valid JSON object with these exact fields (no other text, no markdown):
{{
  "primary_framework": "utilitarian" or "deontological" or "virtue ethics" or "care ethics" or "mixed",
  "ethical_reasoning_type": "consequentialist" or "deontological" or "virtue-based" or "mixed",
  "moral_considerations": ["list", "of", "considerations"],
  "consequence_vs_duty": -1.0 to 1.0,
  "confidence_score": 0.0 to 1.0,
  "frameworks_detected": ["list", "of", "frameworks"],
  "ethical_frameworks_detected": ["list", "of", "frameworks"],
  "moral_reasoning_type": "consequentialist" or "deontological" or "virtue-based" or "mixed"
}}"""
        
        # Use analysis temperature for analysis tasks
        original_temp = self.temperature
        self.temperature = self.analysis_temperature
        
        response = await self._make_llm_request(prompt)
        
        # Restore original temperature
        self.temperature = original_temp
        
        try:
            # Clean the response - remove any markdown formatting or extra text
            cleaned_response = self._clean_json_response(response)
            if not cleaned_response.strip():
                raise ValueError("Empty response from LLM")
            
            data = json.loads(cleaned_response)
            # Filter to only include valid fields for the schema
            filtered_data = {k: v for k, v in data.items() if k in EthicalFramingAnalysis.__annotations__}
            
            # Set required fields with defaults if missing
            required_defaults = {
                "primary_framework": data.get("primary_framework", "unknown"),
                "ethical_reasoning_type": data.get("ethical_reasoning_type", data.get("moral_reasoning_type", "unknown")),
                "moral_considerations": data.get("moral_considerations", []),
                "consequence_vs_duty": data.get("consequence_vs_duty", 0.0),
                "confidence_score": data.get("confidence_score", 0.0),
                "frameworks_detected": data.get("frameworks_detected", data.get("ethical_frameworks_detected", []))
            }
            
            # Merge filtered data with required defaults
            final_data = {**required_defaults, **filtered_data}
            
            return EthicalFramingAnalysis(**final_data)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse ethical framing analysis: {e}")
            logger.error(f"Raw response: {response[:200]}...")
            return EthicalFramingAnalysis(
                primary_framework="unknown",
                ethical_reasoning_type="unknown",
                moral_considerations=[],
                consequence_vs_duty=0.0,
                confidence_score=0.0,
                frameworks_detected=[]
            )
    
    async def analyze_rhetorical_posture(self, response_text: str) -> Dict[str, Any]:
        """Analyze the rhetorical posture and mode of moral address in the response."""
        prompt = f"""Analyze the following ethical response for its rhetorical posture and mode of moral address. Focus on these three dimensions:

1. VOICE AND AUTHORITY: How does the response speak? What kind of moral authority does it claim?
   - Guide/inner voice (suggesting deliberation without commanding)
   - Surrogate self (enacting intimacy and vulnerability of ethical reflection)
   - Moral analyst/theorist (offering judgment from abstracted distance)
   - Other distinct voice patterns

2. TEMPORALITY AND RESPONSIBILITY: How does the response orient toward time and responsibility?
   - Prospective responsibility (what to consider before acting)
   - Present ethical entanglement (decisions shaping identity now)
   - Retrospective justification (imagining how acts could be defended)
   - Mixed temporal orientations

3. ETHICAL IMAGINATION: How does the response constrain or expand moral imagination?
   - Procedural clarity (constrains imagination to clear procedures)
   - Moral empathy and role-reversal (expands imagination through perspective-taking)
   - Principled accountability (brackets imagination to focus on principles)
   - Other imagination patterns

Response to analyze: {response_text}

Return ONLY a valid JSON object with these exact fields (no other text, no markdown):
{{
  "voice_authority_type": "string value",
  "voice_authority_score": 0.0,
  "voice_authority_markers": ["phrase1", "phrase2"],
  "temporal_orientation": "string value",
  "temporal_orientation_score": 0.0,
  "temporal_markers": ["phrase1", "phrase2"],
  "imagination_scope": "string value",
  "imagination_scope_score": 0.0,
  "imagination_markers": ["phrase1", "phrase2"],
  "moral_subject_vision": "detached or embedded or accountable or mixed",
  "rhetorical_sophistication": 0.0
}}

IMPORTANT:
- Use double quotes for all strings
- Arrays must use square brackets []
- Numbers should be between 0.0 and 1.0
- No trailing commas
- Keep marker phrases short (max 10 words each)"""
        
        # Use analysis temperature for analysis tasks
        original_temp = self.temperature
        self.temperature = self.analysis_temperature
        
        response = await self._make_llm_request(prompt)
        
        # Restore original temperature
        self.temperature = original_temp
        
        try:
            # Clean the response - remove any markdown formatting or extra text
            cleaned_response = self._clean_json_response(response)
            if not cleaned_response.strip():
                raise ValueError("Empty response from LLM")
            
            data = json.loads(cleaned_response)
            return data
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse rhetorical posture analysis: {e}")
            logger.error(f"Raw response: {response[:200]}...")
            return {
                "voice_authority_type": "unknown",
                "voice_authority_score": 0.0,
                "voice_authority_markers": [],
                "temporal_orientation": "unknown",
                "temporal_orientation_score": 0.0,
                "temporal_markers": [],
                "imagination_scope": "unknown",
                "imagination_scope_score": 0.0,
                "imagination_markers": [],
                "moral_subject_vision": "unknown",
                "rhetorical_sophistication": 0.0
            }
    
    async def generate_ethical_response(self, transformed_prompt: str) -> str:
        """Generate an ethical response to a transformed dilemma - NO SYSTEM PROMPT."""
        return await self._make_llm_request(transformed_prompt)
    
    async def analyze_moral_reasoning(self, response_text: str) -> Dict[str, Any]:
        """Analyze the moral reasoning patterns in the response."""
        prompt = f"""Analyze the following ethical response for moral reasoning patterns.

Response to analyze: {response_text}

Return ONLY a valid JSON object with these exact fields (no other text, no markdown):
{{
  "reasoning_type": "consequentialist" or "deontological" or "virtue-based" or "care-based" or "mixed",
  "reasoning_patterns": ["list", "of", "patterns"],
  "moral_principles": ["list", "of", "principles"],
  "reasoning_complexity": 0.0 to 1.0,
  "confidence_score": 0.0 to 1.0
}}"""
        
        # Use analysis temperature for analysis tasks
        original_temp = self.temperature
        self.temperature = self.analysis_temperature
        
        response = await self._make_llm_request(prompt)
        
        # Restore original temperature
        self.temperature = original_temp
        
        try:
            cleaned_response = self._clean_json_response(response)
            if not cleaned_response.strip():
                raise ValueError("Empty response from LLM")
            
            data = json.loads(cleaned_response)
            return data
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse moral reasoning analysis: {e}")
            return {
                "reasoning_type": "unknown",
                "reasoning_patterns": [],
                "moral_principles": [],
                "reasoning_complexity": 0.0,
                "confidence_score": 0.0
            }
    
    async def analyze_affective_stance(self, response_text: str) -> Dict[str, Any]:
        """Analyze the affective stance and emotional tone in the response."""
        prompt = f"""Analyze the following ethical response for affective stance and emotional tone.

Response to analyze: {response_text}

Return ONLY a valid JSON object with these exact fields (no other text, no markdown):
{{
  "stance_type": "empathetic" or "analytical" or "prescriptive" or "descriptive" or "mixed",
  "emotional_tone": "compassionate" or "neutral" or "urgent" or "reflective" or "mixed",
  "affective_markers": ["list", "of", "markers"],
  "empathy_level": 0.0 to 1.0,
  "confidence_score": 0.0 to 1.0
}}"""
        
        # Use analysis temperature for analysis tasks
        original_temp = self.temperature
        self.temperature = self.analysis_temperature
        
        response = await self._make_llm_request(prompt)
        
        # Restore original temperature
        self.temperature = original_temp
        
        try:
            cleaned_response = self._clean_json_response(response)
            if not cleaned_response.strip():
                raise ValueError("Empty response from LLM")
            
            data = json.loads(cleaned_response)
            return data
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse affective stance analysis: {e}")
            return {
                "stance_type": "unknown",
                "emotional_tone": "unknown",
                "affective_markers": [],
                "empathy_level": 0.0,
                "confidence_score": 0.0
            }
    
    async def assess_indexical_coherence(self, response_text: str) -> Dict[str, Any]:
        """Assess the indexical coherence and deixis consistency in the response."""
        prompt = f"""Analyze the following ethical response for indexical coherence and deixis consistency.

Response to analyze: {response_text}

Return ONLY a valid JSON object with these exact fields (no other text, no markdown):
{{
  "coherence_level": 0.0 to 1.0,
  "deixis_consistency": 0.0 to 1.0,
  "perspective_stability": "stable" or "shifting" or "mixed",
  "indexical_markers": ["list", "of", "markers"],
  "coherence_issues": ["list", "of", "issues"],
  "confidence_score": 0.0 to 1.0
}}"""
        
        # Use analysis temperature for analysis tasks
        original_temp = self.temperature
        self.temperature = self.analysis_temperature
        
        response = await self._make_llm_request(prompt)
        
        # Restore original temperature
        self.temperature = original_temp
        
        try:
            cleaned_response = self._clean_json_response(response)
            if not cleaned_response.strip():
                raise ValueError("Empty response from LLM")
            
            data = json.loads(cleaned_response)
            return data
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse indexical coherence analysis: {e}")
            return {
                "coherence_level": 0.5,
                "deixis_consistency": 0.5,
                "perspective_stability": "unknown",
                "indexical_markers": [],
                "coherence_issues": [],
                "confidence_score": 0.0
            }
    
    async def _make_llm_request(self, prompt: str) -> str:
        """Make a stateless request to OpenRouter with model rotation."""
        try:
            # Get next model for variety and non-repetition
            current_model = self._get_next_model()
            
            # Stateless call with no system prompt
            messages = [{"role": "user", "content": prompt}]
            
            if self.use_anthropic_direct:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.post(
                        "/messages",
                        json={
                            "model": current_model,
                            "messages": messages,
                            "temperature": self.temperature,
                            "max_tokens": 2000,
                        },
                    )
                )
                response.raise_for_status()
                payload = response.json()
                logger.info(f"Generated response using {current_model} at temp {self.temperature}")
                return "".join(
                    block.get("text", "") for block in payload.get("content", []) if block.get("type") == "text"
                )

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=current_model,
                    messages=messages,
                    temperature=self.temperature,  # 0.9 for high variability
                    max_tokens=2000,
                    top_p=0.95,  # Additional variability
                    frequency_penalty=0.3,  # Reduce repetition
                    presence_penalty=0.3   # Encourage novel content
                )
            )
            
            logger.info(f"Generated response using {current_model} at temp {self.temperature}")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"LLM request failed with {current_model}: {e}")
            # Re-raise so callers can detect API failures (quota, auth, etc.) and
            # avoid silently saving error strings as if they were real responses.
            raise
    
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
        
        # If no braces found, try to find JSON-like content
        lines = response.strip().split('\n')
        json_lines = []
        in_json = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('{') or in_json:
                in_json = True
                json_lines.append(line)
                if line.endswith('}') and line.count('}') >= line.count('{'):
                    break
        
        return '\n'.join(json_lines) if json_lines else response

class DeicticEthicalAnalyzer:
    """Main analyzer class that orchestrates the entire analysis process."""
    
    def __init__(self, api_key: Optional[str] = None, models: Optional[List[str]] = None, 
                 enable_rich_logging: bool = True, output_dir: str = "analysis_results",
                 use_openai_direct: bool = True, temperature: float = 0.6,
                 use_anthropic_direct: bool = False):
        self.transformer = DeicticTransformer()
        self.llm_agent = LLMAnalysisAgent(api_key, models, use_openai_direct, temperature, use_anthropic_direct)
        self.dilemma_db = EthicalDilemmaDatabase()
        self.results: List[DeicticAnalysisResult] = []
        
        # Initialize rich logging
        self.enable_rich_logging = enable_rich_logging
        if self.enable_rich_logging:
            self.rich_logger = RichAnalysisLogger(output_dir)
            self.rich_logger.start_session(
                experiment_notes="Generative deictic analysis session",
                transformer_config={"type": "generative", "minimal_hardcoding": True}
            )
            logger.info(f"Rich logging enabled - Session: {self.rich_logger.session_id}")
    
    async def analyze_dilemma_across_frameworks(self, dilemma_id: str) -> List[DeicticAnalysisResult]:
        """Analyze a single dilemma across all 8 deictic frameworks."""
        dilemma = self.dilemma_db.get_dilemma(dilemma_id)
        if not dilemma:
            raise ValueError(f"Dilemma {dilemma_id} not found")
        
        results = []
        frameworks = self.transformer.get_available_framings()
        
        for framing in frameworks:
            logger.info(f"Analyzing {dilemma_id} with {framing.value} framing")
            result = await self._analyze_single_framework(dilemma, framing)
            results.append(result)
            
        self.results.extend(results)
        return results
    
    async def _analyze_single_framework(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> DeicticAnalysisResult:
        """Analyze a dilemma with a single deictic framework."""
        start_time = datetime.now()
        
        # Transform the dilemma
        transformed_prompt = self.transformer.transform_dilemma(dilemma, framing)
        direct_question = self.transformer.transform_dilemma_direct(dilemma, framing)
        # Note: extracted_tension was from old transformer, using dilemma description instead
        extracted_tension = dilemma.description
        
        # Generate LLM response to the direct question (not the transformation prompt)
        llm_response = await self.llm_agent.generate_ethical_response(direct_question)
        
        # Analyze agency distribution
        agency_analysis = await self.llm_agent.analyze_agency_distribution(
            llm_response
        )
        
        # Analyze ethical framing
        ethical_analysis = await self.llm_agent.analyze_ethical_framing(
            llm_response
        )
        
        # Analyze rhetorical posture and moral address
        rhetorical_analysis = await self.llm_agent.analyze_rhetorical_posture(
            llm_response
        )
        
        # Analyze deictic markers
        deictic_markers = self.transformer.analyze_deictic_markers(llm_response)
        suggested_frame, frame_confidence = self.transformer.suggest_frame_type(llm_response)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Log to rich analysis system with rhetorical analysis
        if self.enable_rich_logging:
            # Add rhetorical analysis to the logged data
            extended_analysis = {
                "rhetorical_posture": rhetorical_analysis,
                "agency_analysis": {
                    "primary_agent": agency_analysis.primary_agent,
                    "collective_vs_individual": agency_analysis.collective_vs_individual,
                    "decision_locus": agency_analysis.decision_locus,
                    "responsibility_markers": agency_analysis.responsibility_markers
                },
                "ethical_framing": {
                    "frameworks_detected": ethical_analysis.ethical_frameworks_detected,
                    "reasoning_type": ethical_analysis.moral_reasoning_type,
                    "consequence_vs_duty": ethical_analysis.consequence_vs_duty,
                    "empathy_markers": ethical_analysis.empathy_markers,
                    "justice_markers": ethical_analysis.justice_markers
                }
            }
            
            self.rich_logger.log_analysis(
                dilemma_id=dilemma.id,
                dilemma_title=dilemma.title,
                dilemma_domain=dilemma.domain,
                dilemma_complexity=dilemma.complexity_score,
                original_description=dilemma.description,
                framing_type=framing.value,
                transformation_prompt=transformed_prompt,
                direct_question=direct_question,
                extracted_tension=extracted_tension,
                deictic_markers=deictic_markers,
                suggested_frame=suggested_frame.value,
                frame_confidence=frame_confidence,
                processing_time=processing_time,
                llm_response=llm_response,
                extended_analysis=extended_analysis
            )
        
        return DeicticAnalysisResult(
            dilemma_id=dilemma.id,
            framing=framing,
            transformed_prompt=transformed_prompt,
            llm_response=llm_response,
            agency_analysis=agency_analysis,
            ethical_framing_analysis=ethical_analysis,
            deictic_markers=deictic_markers,
            response_length=len(llm_response),
            processing_time=processing_time,
            timestamp=datetime.now()
        )
    
    async def batch_analyze_all_dilemmas(self) -> Dict[str, List[DeicticAnalysisResult]]:
        """Analyze all dilemmas across all frameworks."""
        all_results = {}
        dilemmas = self.dilemma_db.get_all_dilemmas()
        
        for dilemma in dilemmas:
            logger.info(f"Starting batch analysis for dilemma: {dilemma.title}")
            results = await self.analyze_dilemma_across_frameworks(dilemma.id)
            all_results[dilemma.id] = results
            
        return all_results
    
    def generate_comparative_report(self, dilemma_id: str) -> Dict[str, Any]:
        """Generate a comparative analysis report for a single dilemma across all frameworks."""
        dilemma_results = [r for r in self.results if r.dilemma_id == dilemma_id]
        
        if not dilemma_results:
            return {"error": f"No results found for dilemma {dilemma_id}"}
        
        # Agency distribution comparison
        agency_patterns = {}
        for result in dilemma_results:
            agency_patterns[result.framing.value] = {
                "primary_agent": result.agency_analysis.primary_agent,
                "collective_vs_individual": result.agency_analysis.collective_vs_individual,
                "decision_locus": result.agency_analysis.decision_locus
            }
        
        # Ethical framing comparison
        ethical_patterns = {}
        for result in dilemma_results:
            ethical_patterns[result.framing.value] = {
                "frameworks": result.ethical_framing_analysis.ethical_frameworks_detected,
                "reasoning_type": result.ethical_framing_analysis.moral_reasoning_type,
                "consequence_vs_duty": result.ethical_framing_analysis.consequence_vs_duty
            }
        
        # Deictic marker analysis
        deictic_comparison = {}
        for result in dilemma_results:
            deictic_comparison[result.framing.value] = result.deictic_markers
        
        # Response characteristics
        response_stats = {}
        lengths = [r.response_length for r in dilemma_results]
        times = [r.processing_time for r in dilemma_results]
        
        response_stats = {
            "avg_length": statistics.mean(lengths),
            "length_variance": statistics.variance(lengths) if len(lengths) > 1 else 0,
            "avg_processing_time": statistics.mean(times),
            "total_processing_time": sum(times)
        }
        
        return {
            "dilemma_id": dilemma_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "agency_patterns": agency_patterns,
            "ethical_patterns": ethical_patterns,
            "deictic_comparison": deictic_comparison,
            "response_statistics": response_stats,
            "framework_count": len(dilemma_results)
        }
    
    def export_results(self, filename: str) -> None:
        """Export all results to a JSON file."""
        export_data = {
            "metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "total_results": len(self.results),
                "dilemmas_analyzed": len(set(r.dilemma_id for r in self.results))
            },
            "results": [asdict(result) for result in self.results]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Results exported to {filename}")
    
    def get_dilemma_list(self) -> List[Dict[str, Any]]:
        """Get a list of available dilemmas with metadata."""
        return [asdict(dilemma) for dilemma in self.dilemma_db.get_all_dilemmas()]
    
    def finalize_and_save_analysis(self, include_responses: bool = True) -> Optional[Dict[str, Any]]:
        """
        Finalize the analysis session and save all results in rich format.
        
        Args:
            include_responses: Whether to include full LLM responses in exports
            
        Returns:
            Analysis report dictionary if rich logging is enabled
        """
        if not self.enable_rich_logging:
            logger.warning("Rich logging is disabled - no results to finalize")
            return None
        
        # End the session
        self.rich_logger.end_session()
        
        # Save all results in multiple formats
        self.rich_logger.save_results(include_responses=include_responses)
        
        # Generate and save comprehensive analysis report
        report = self.rich_logger.save_analysis_report()
        
        # Export for statistical analysis
        self.rich_logger.export_for_statistical_analysis("python")
        self.rich_logger.export_for_statistical_analysis("r")
        
        # Print session summary
        self.rich_logger.print_session_summary()
        
        logger.info("Analysis session finalized and saved in rich format")
        return report
    
    def get_analysis_dataframe(self):
        """Get analysis results as pandas DataFrame for immediate analysis."""
        if not self.enable_rich_logging:
            logger.warning("Rich logging is disabled - no DataFrame available")
            return None
        
        return self.rich_logger.get_records_dataframe()
    
    def print_analysis_summary(self):
        """Print a formatted summary of the current analysis session."""
        if not self.enable_rich_logging:
            logger.warning("Rich logging is disabled - no summary available")
            return
        
        self.rich_logger.print_session_summary()
