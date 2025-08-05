"""
Fully Generative Deictic Transformer: Zero hardcoding, 100% LLM generation.
Designed for rigorous LLM research - lets models generate everything naturally.
"""

from typing import Dict, List, Optional, Tuple, Any
from models.schemas import EthicalDilemma, DeicticFraming
import logging
import openai
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class FullyGenerativeDeicticTransformer:
    """
    Completely generative transformer that uses LLMs to generate all transformations,
    analysis, and insights. No hardcoded patterns, templates, or predetermined structures.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with LLM client for all generative tasks."""
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key or os.getenv("OPENROUTER_API_KEY")
        )
        
        # Minimal framework definitions - just enough to guide LLM generation
        self.framework_concepts = {
            DeicticFraming.IMPERSONAL: "Remove personal references, use abstract language",
            DeicticFraming.SECOND_PERSON: "Address the reader directly as 'you'",
            DeicticFraming.FIRST_PERSON: "Use 'I' perspective as the decision-maker",
            DeicticFraming.REFLEXIVE: "Invite perspective-taking and role reversal",
            DeicticFraming.DIALOGIC: "Frame as collective decision-making",
            DeicticFraming.SPATIAL: "Emphasize physical positioning and place",
            DeicticFraming.TEMPORAL: "Focus on time, urgency, and critical moments",
            DeicticFraming.COSMOLOGICAL: "Invoke universal, spiritual, or cosmic perspectives"
        }
        
        logger.info("Fully generative deictic transformer initialized - zero hardcoding")
    
    async def transform_dilemma_generative(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        Generate a deictic transformation using pure LLM generation.
        
        Args:
            dilemma: The ethical dilemma to transform
            framing: The deictic framing concept to apply
            
        Returns:
            LLM-generated transformed dilemma
        """
        concept = self.framework_concepts.get(framing, "Apply alternative linguistic perspective")
        
        prompt = f"""Transform this ethical dilemma by applying the following linguistic approach: {concept}

Original ethical dilemma:
{dilemma.description}

Generate a naturally-worded transformation that applies this linguistic perspective. Create a complete, coherent ethical scenario that embodies the specified approach. Generate only the transformed dilemma text:"""

        response = await self._generate_llm_response(prompt)
        
        logger.debug(f"Generated {framing.value} transformation using pure LLM generation")
        return response.strip()
    
    async def generate_direct_question(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        Generate a direct ethical question using pure LLM generation.
        
        Args:
            dilemma: The ethical dilemma
            framing: The deictic framing concept
            
        Returns:
            LLM-generated direct question
        """
        concept = self.framework_concepts.get(framing, "Apply alternative linguistic perspective")
        
        prompt = f"""Based on this ethical dilemma, generate a direct question that applies this linguistic approach: {concept}

Ethical dilemma:
{dilemma.description}

Create a single, clear question that captures the ethical choice using the specified linguistic perspective. Generate only the question:"""

        response = await self._generate_llm_response(prompt)
        
        logger.debug(f"Generated {framing.value} direct question using pure LLM generation")
        return response.strip()
    
    async def extract_ethical_tension_generative(self, description: str) -> str:
        """
        Extract the core ethical tension using pure LLM analysis.
        
        Args:
            description: The dilemma description
            
        Returns:
            LLM-identified core tension
        """
        prompt = f"""Analyze this ethical dilemma and identify the core tension or conflict at its heart.

Ethical dilemma:
{description}

Identify the central ethical tension in 1-2 sentences. Focus on the fundamental conflict or choice that makes this dilemma challenging. Generate only the core tension description:"""

        response = await self._generate_llm_response(prompt)
        
        logger.debug("Extracted ethical tension using pure LLM analysis")
        return response.strip()
    
    async def analyze_deictic_markers_generative(self, response_text: str) -> Dict[str, Any]:
        """
        Analyze deictic markers using pure LLM analysis instead of hardcoded patterns.
        
        Args:
            response_text: Text to analyze
            
        Returns:
            LLM-generated analysis of deictic markers
        """
        prompt = f"""Analyze this text for deictic markers - linguistic elements that depend on context like pronouns, spatial references, temporal markers, etc.

Text to analyze:
{response_text}

Identify and count various types of deictic markers present. Consider:
- Personal pronouns (I, you, we, they, etc.)
- Spatial references (here, there, nearby, etc.)
- Temporal markers (now, then, currently, etc.)
- Demonstratives (this, that, these, those)
- Any other context-dependent linguistic elements

Provide your analysis in JSON format with marker types as keys and counts as values. Include a "total_markers" field and an "interpretation" field explaining what the pattern suggests about the linguistic positioning."""

        response = await self._generate_llm_response(prompt)
        
        try:
            # Attempt to parse JSON response
            import json
            result = json.loads(response.strip())
            logger.debug("Generated deictic marker analysis using pure LLM analysis")
            return result
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            logger.warning("LLM response was not valid JSON, returning descriptive analysis")
            return {
                "analysis_description": response.strip(),
                "total_markers": "unknown",
                "interpretation": "LLM provided qualitative analysis"
            }
    
    async def suggest_frame_type_generative(self, text: str) -> Tuple[DeicticFraming, float]:
        """
        Suggest frame type using pure LLM analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (suggested_frame, confidence_score)
        """
        frameworks_desc = "\n".join([f"- {f.value}: {desc}" for f, desc in self.framework_concepts.items()])
        
        prompt = f"""Analyze this text and determine which deictic framing it most closely represents.

Text to analyze:
{text}

Available deictic framings:
{frameworks_desc}

Based on the linguistic markers and perspective used in the text, which framing does it most closely match? Provide your answer in JSON format with:
- "suggested_frame": the frame name (e.g., "first_person", "spatial", etc.)
- "confidence": a number between 0 and 1 indicating your confidence
- "reasoning": brief explanation of your analysis"""

        response = await self._generate_llm_response(prompt)
        
        try:
            import json
            result = json.loads(response.strip())
            
            # Convert frame name to enum
            frame_name = result.get("suggested_frame", "impersonal")
            confidence = float(result.get("confidence", 0.5))
            
            # Find matching enum value
            suggested_frame = DeicticFraming.IMPERSONAL  # default
            for frame in DeicticFraming:
                if frame.value == frame_name:
                    suggested_frame = frame
                    break
            
            logger.debug(f"Generated frame suggestion using pure LLM analysis: {suggested_frame.value}")
            return suggested_frame, confidence
            
        except (json.JSONDecodeError, ValueError, KeyError):
            logger.warning("LLM frame suggestion was not parseable, using default")
            return DeicticFraming.IMPERSONAL, 0.5
    
    async def generate_analysis_insight(self, analysis_data: Dict[str, Any], research_context: str) -> str:
        """
        Generate research insights using pure LLM analysis.
        
        Args:
            analysis_data: Data to analyze
            research_context: Context about what kind of insight is needed
            
        Returns:
            LLM-generated research insight
        """
        prompt = f"""As a researcher studying how language affects AI reasoning, analyze this data and generate insights.

Research context: {research_context}

Data to analyze:
{analysis_data}

Generate insights about what this data reveals regarding deictic effects on reasoning, agency attribution, or ethical framing. Focus on patterns, implications, and research significance. Provide a clear, analytical insight:"""

        response = await self._generate_llm_response(prompt)
        
        logger.debug("Generated research insight using pure LLM analysis")
        return response.strip()
    
    async def generate_comparative_analysis(self, results_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comparative analysis across multiple results using pure LLM analysis.
        
        Args:
            results_data: List of analysis results to compare
            
        Returns:
            LLM-generated comparative analysis
        """
        prompt = f"""Analyze and compare these multiple analysis results to identify patterns and differences.

Results data:
{results_data}

Generate a comparative analysis that identifies:
1. Key patterns across the different results
2. Significant differences between conditions
3. Implications for understanding how linguistic framing affects reasoning
4. Any unexpected findings or anomalies

Provide your analysis in JSON format with clear sections for patterns, differences, and implications."""

        response = await self._generate_llm_response(prompt)
        
        try:
            import json
            result = json.loads(response.strip())
            logger.debug("Generated comparative analysis using pure LLM analysis")
            return result
        except json.JSONDecodeError:
            logger.warning("LLM comparative analysis was not valid JSON")
            return {
                "analysis_description": response.strip(),
                "method": "qualitative_llm_analysis"
            }
    
    async def _generate_llm_response(self, prompt: str, model: str = "anthropic/claude-3.5-sonnet") -> str:
        """
        Generate LLM response for any analysis task.
        
        Args:
            prompt: The prompt to send to the LLM
            model: Model to use for generation
            
        Returns:
            LLM response
        """
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,  # Lower temperature for analysis tasks
                    max_tokens=2000
                )
            )
            
            logger.debug(f"Generated LLM response using {model}")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return f"Generation failed: {str(e)}"
    
    def get_available_framings(self) -> List[DeicticFraming]:
        """Get list of available deictic framings."""
        return list(self.framework_concepts.keys())
    
    def get_framing_concept(self, framing: DeicticFraming) -> str:
        """Get the minimal concept description for a framing."""
        return self.framework_concepts.get(framing, "Apply alternative linguistic perspective")
    
    async def preview_generative_transformation(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> Dict[str, str]:
        """Preview the fully generative transformation approach."""
        
        # Generate all components using LLM
        transformed_scenario = await self.transform_dilemma_generative(dilemma, framing)
        direct_question = await self.generate_direct_question(dilemma, framing)
        core_tension = await self.extract_ethical_tension_generative(dilemma.description)
        
        return {
            "original": dilemma.description,
            "framing_type": framing.value,
            "framing_concept": self.framework_concepts[framing],
            "core_tension_llm_extracted": core_tension,
            "transformed_scenario_llm_generated": transformed_scenario,
            "direct_question_llm_generated": direct_question,
            "approach": "100% LLM generation, zero hardcoding - pure research into emergent LLM deictic behavior"
        }

# Backward compatibility wrapper
class DeicticTransformer(FullyGenerativeDeicticTransformer):
    """Backward compatibility wrapper that provides the same interface."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        logger.info("Initialized fully generative transformer with backward compatibility")
    
    def transform_dilemma(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """Sync wrapper for async generative transformation."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.transform_dilemma_generative(dilemma, framing))
            return result
        finally:
            loop.close()
    
    def transform_dilemma_direct(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """Sync wrapper for async direct question generation."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.generate_direct_question(dilemma, framing))
            return result
        finally:
            loop.close()
    
    def _extract_dynamic_tension(self, description: str) -> str:
        """Sync wrapper for async tension extraction."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.extract_ethical_tension_generative(description))
            return result
        finally:
            loop.close()
    
    def analyze_deictic_markers(self, response_text: str) -> Dict[str, Any]:
        """Sync wrapper for async marker analysis."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.analyze_deictic_markers_generative(response_text))
            return result
        finally:
            loop.close()
    
    def suggest_frame_type(self, text: str) -> Tuple[DeicticFraming, float]:
        """Sync wrapper for async frame suggestion."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.suggest_frame_type_generative(text))
            return result
        finally:
            loop.close()
    
    def preview_transformation(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> Dict[str, str]:
        """Sync wrapper for async transformation preview."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.preview_generative_transformation(dilemma, framing))
            return result
        finally:
            loop.close()
    
    def get_framing_description(self, framing: DeicticFraming) -> str:
        """Get the concept description for a framing."""
        return self.get_framing_concept(framing)
