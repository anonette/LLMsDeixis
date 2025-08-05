"""
Fixed version of Expert Analysis Agent with robust JSON parsing.
Provides sophisticated analysis of deictic ethics patterns using LLM expertise.
"""

import json
import re
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import logging
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class DeicticEthicsReport:
    """Comprehensive expert analysis report on deictic ethics patterns."""
    session_id: str
    analysis_timestamp: str
    total_analyses: int
    
    # High-level patterns
    ethical_frameworks_analysis: Dict[str, Any]
    responsibility_patterns: Dict[str, str]
    agency_patterns: Dict[str, str]
    linguistic_patterns: Dict[str, Any]
    
    # Expert insights
    expert_insights: Dict[str, str]
    key_findings: List[str]
    research_recommendations: List[str]
    
    # Comparative analysis
    cross_framing_patterns: Dict[str, Any]
    emergent_themes: List[str]
    
    # Methodological notes
    analysis_confidence: float
    limitations: List[str]
    future_directions: List[str]

class ExpertAnalysisAgent:
    """
    Fixed Expert analysis agent that provides sophisticated interpretation of deictic ethics data.
    Uses robust JSON parsing and better error handling.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the expert analysis agent with OpenRouter API."""
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Set OPENROUTER_API_KEY in .env file")
        
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/deixis-analysis",
                "X-Title": "Deixis Analysis Pipeline"
            }
        )
        
        self.expert_model = "anthropic/claude-3.5-sonnet"
        self.temperature = 0.7
        logger.info(f"Expert analysis agent initialized with {self.expert_model}")
    
    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """
        Extract JSON from LLM response with multiple fallback strategies.
        """
        # Strategy 1: Try direct JSON parsing
        try:
            return json.loads(response)
        except:
            pass
        
        # Strategy 2: Find JSON block in markdown code blocks
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, response, re.DOTALL)
        if matches:
            try:
                return json.loads(matches[0])
            except:
                pass
        
        # Strategy 3: Find any JSON-like structure
        json_pattern = r'\{[^{}]*\}'
        matches = re.findall(json_pattern, response)
        for match in matches:
            try:
                return json.loads(match)
            except:
                continue
        
        # Strategy 4: Parse key-value pairs from structured text
        result = {}
        lines = response.split('\n')
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().strip('"').strip("'")
                    value = parts[1].strip().strip('"').strip("'")
                    # Clean up common formatting
                    key = key.replace('-', '').replace('*', '').strip()
                    if key and value:
                        result[key] = value
        
        if result:
            return result
        
        # Strategy 5: Return structured fallback
        logger.warning("Could not parse JSON from response, returning fallback")
        return {"error": "parsing_failed", "raw_response": response[:500]}
    
    async def analyze_session_data(self, session_data: Dict[str, Any]) -> DeicticEthicsReport:
        """
        Perform comprehensive expert analysis on a complete session dataset.
        
        Args:
            session_data: Complete analysis data from a session
            
        Returns:
            DeicticEthicsReport with expert insights and patterns
        """
        records = session_data if isinstance(session_data, list) else session_data.get('records', [])
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info("Starting expert analysis of session data")
        
        # Perform various expert analyses with fixed JSON parsing
        ethical_frameworks = await self._analyze_ethical_frameworks(records)
        responsibility_patterns = await self._analyze_responsibility_patterns(records)
        agency_patterns = await self._analyze_agency_patterns(records)
        linguistic_patterns = await self._analyze_linguistic_patterns(records)
        
        # Generate expert insights
        expert_insights = await self._generate_expert_insights(records)
        key_findings = await self._extract_key_findings(records)
        research_recommendations = await self._generate_research_recommendations(records)
        
        # Cross-framing analysis
        cross_framing_patterns = await self._analyze_cross_framing_patterns(records)
        emergent_themes = await self._identify_emergent_themes(records)
        
        # Compile report
        report = DeicticEthicsReport(
            session_id=session_id,
            analysis_timestamp=datetime.now().isoformat(),
            total_analyses=len(records),
            ethical_frameworks_analysis=ethical_frameworks,
            responsibility_patterns=responsibility_patterns,
            agency_patterns=agency_patterns,
            linguistic_patterns=linguistic_patterns,
            expert_insights=expert_insights,
            key_findings=key_findings,
            research_recommendations=research_recommendations,
            cross_framing_patterns=cross_framing_patterns,
            emergent_themes=emergent_themes,
            analysis_confidence=0.85,
            limitations=[
                "Analysis limited to English language responses",
                "Single LLM model perspective",
                "Limited sample size per framing type"
            ],
            future_directions=[
                "Cross-linguistic validation",
                "Multi-model consensus analysis",
                "Longitudinal stability testing"
            ]
        )
        
        return report
    
    async def _analyze_ethical_frameworks(self, records: List[Dict]) -> Dict[str, Any]:
        """Analyze distribution and patterns of ethical frameworks across framings."""
        
        # Count frameworks by framing type
        framework_counts = {}
        for record in records:
            framing = record.get('framing_type', 'unknown')
            framework = record.get('ethical_framework', 'unknown')
            
            if framing not in framework_counts:
                framework_counts[framing] = {}
            
            framework_counts[framing][framework] = framework_counts[framing].get(framework, 0) + 1
        
        prompt = f"""As an expert in moral philosophy, analyze the relationship between deictic framing and ethical framework adoption.

Framework distribution data:
{json.dumps(framework_counts, indent=2)}

Please analyze:
1. Which framings tend toward deontological vs consequentialist reasoning?
2. How does perspective (1st/2nd/3rd person) influence framework selection?
3. What role do temporal/spatial markers play in ethical reasoning?

Provide your analysis as a structured response with clear sections."""
        
        response = await self._make_expert_request(prompt)
        parsed_response = self._extract_json_from_response(response)
        
        # Add the raw counts to the analysis
        parsed_response['raw_distribution'] = framework_counts
        
        return parsed_response
    
    async def _analyze_responsibility_patterns(self, records: List[Dict]) -> Dict[str, str]:
        """Analyze how different framings create patterns of moral responsibility."""
        
        # Extract deictic markers by framing
        framing_markers = {}
        for record in records:
            framing = record.get('framing_type', 'unknown')
            markers = record.get('deictic_markers', {})
            
            if framing not in framing_markers:
                framing_markers[framing] = {}
            
            for marker, count in markers.items():
                framing_markers[framing][marker] = framing_markers[framing].get(marker, 0) + count
        
        prompt = f"""As an expert in moral philosophy and responsibility attribution, analyze how different deictic framings create different patterns of moral responsibility.

Deictic marker patterns by framing:
{json.dumps(framing_markers, indent=2)}

Sample transformations from the data:
{[r.get('transformation_prompt', '')[:200] + '...' for r in records[:3]]}

Please analyze:
1. How does first-person framing vs. third-person framing affect responsibility attribution?
2. What role do spatial markers play in creating embodied responsibility?
3. How do temporal markers influence urgency and responsibility timing?
4. How does collective language (dialogic framing) distribute responsibility?
5. What unique responsibility patterns emerge from cosmological framing?

Structure your response with clear labels for each framing type."""
        
        response = await self._make_expert_request(prompt)
        return self._extract_json_from_response(response)
    
    async def _analyze_agency_patterns(self, records: List[Dict]) -> Dict[str, str]:
        """Analyze how different deictic framings distribute and construct agency."""
        
        prompt = f"""As an expert in philosophy of action and agency theory, analyze how different deictic framings construct and distribute moral agency.

Analysis data includes {len(records)} analyses across deictic framings: {list(set(r.get('framing_type', 'unknown') for r in records))}

Key markers to consider:
- Individual agency markers: {sum(r.get('deictic_markers', {}).get('individual_agency', 0) for r in records)}
- Collective agency markers: {sum(r.get('deictic_markers', {}).get('collective_agency', 0) for r in records)}
- Passive agency markers: {sum(r.get('deictic_markers', {}).get('passive_agency', 0) for r in records)}
- First person markers: {sum(r.get('deictic_markers', {}).get('first_person_singular', 0) for r in records)}
- Collective markers: {sum(r.get('deictic_markers', {}).get('first_person_plural', 0) for r in records)}

Please analyze:
1. How does deictic positioning affect the construction of moral agency?
2. What is the relationship between grammatical person and agency attribution?
3. How do spatial/temporal framings embody or disembody agency?
4. What patterns of distributed agency emerge in dialogic framings?

Provide structured analysis with specific examples."""
        
        response = await self._make_expert_request(prompt)
        return self._extract_json_from_response(response)
    
    async def _analyze_linguistic_patterns(self, records: List[Dict]) -> Dict[str, Any]:
        """Analyze linguistic and discourse patterns across framings."""
        
        # Aggregate linguistic features
        linguistic_features = {}
        for record in records:
            framing = record.get('framing_type', 'unknown')
            
            if framing not in linguistic_features:
                linguistic_features[framing] = {
                    'avg_response_length': [],
                    'voice_types': [],
                    'stance_types': [],
                    'coherence_levels': []
                }
            
            linguistic_features[framing]['avg_response_length'].append(record.get('response_length', 0))
            linguistic_features[framing]['voice_types'].append(record.get('voice_authority', 'unknown'))
            linguistic_features[framing]['stance_types'].append(record.get('affective_stance', 'unknown'))
            linguistic_features[framing]['coherence_levels'].append(record.get('indexical_coherence', 'unknown'))
        
        # Calculate averages safely
        for framing in linguistic_features:
            lengths = linguistic_features[framing]['avg_response_length']
            if lengths:
                linguistic_features[framing]['avg_response_length'] = sum(lengths) / len(lengths)
            else:
                linguistic_features[framing]['avg_response_length'] = 0
        
        prompt = f"""As an expert in discourse analysis and pragmatics, analyze the linguistic patterns that emerge from different deictic framings.

Linguistic feature data:
{json.dumps(linguistic_features, indent=2)}

Please analyze:
1. How does framing affect discourse length and complexity?
2. What voice authority patterns emerge from different perspectives?
3. How do affective stances correlate with deictic positioning?
4. What can we learn from indexical coherence patterns?

Provide detailed linguistic analysis with theoretical grounding."""
        
        response = await self._make_expert_request(prompt)
        return self._extract_json_from_response(response)
    
    async def _generate_expert_insights(self, records: List[Dict]) -> Dict[str, str]:
        """Generate high-level expert insights from the data."""
        
        prompt = f"""As a leading expert in ethics, linguistics, and philosophy of mind, provide sophisticated insights about the relationship between deixis and moral reasoning based on this data.

Dataset: {len(records)} ethical dilemma responses across multiple deictic framings
Framings analyzed: {list(set(r.get('framing_type', 'unknown') for r in records))}

Key patterns observed:
- Ethical framework variations across framings
- Agency and responsibility attribution differences
- Linguistic and discourse pattern shifts
- Affective stance modulations

Please provide:
1. A theoretical insight about deixis and moral cognition
2. A practical insight for AI ethics and design
3. A philosophical insight about perspective and ethics
4. A methodological insight for future research

Structure as clear, labeled insights."""
        
        response = await self._make_expert_request(prompt)
        return self._extract_json_from_response(response)
    
    async def _extract_key_findings(self, records: List[Dict]) -> List[str]:
        """Extract the most important findings from the analysis."""
        
        # Handle empty records case
        response_lengths = [r.get('response_length', 0) for r in records if r.get('response_length', 0) > 0]
        min_length = min(response_lengths) if response_lengths else 0
        max_length = max(response_lengths) if response_lengths else 0
        
        prompt = f"""Based on the analysis of {len(records)} responses across deictic framings, identify the 5 most important and surprising findings.

Data summary:
- Framings analyzed: {list(set(r.get('framing_type', 'unknown') for r in records))}
- Ethical frameworks detected: {list(set(r.get('ethical_framework', 'unknown') for r in records))}
- Response length range: {min_length} - {max_length}

Provide 5 key findings as a clear list. Each finding should be:
- Specific and evidence-based
- Theoretically significant
- Practically relevant
- Clearly stated"""
        
        response = await self._make_expert_request(prompt)
        parsed = self._extract_json_from_response(response)
        
        # Extract findings from various possible formats
        if isinstance(parsed, dict):
            if 'findings' in parsed:
                return parsed['findings'] if isinstance(parsed['findings'], list) else [str(parsed['findings'])]
            elif 'key_findings' in parsed:
                return parsed['key_findings'] if isinstance(parsed['key_findings'], list) else [str(parsed['key_findings'])]
            else:
                # Convert dict values to list
                return [str(v) for v in parsed.values()]
        elif isinstance(parsed, list):
            return parsed
        else:
            return [str(parsed)]
    
    async def _generate_research_recommendations(self, records: List[Dict]) -> List[str]:
        """Generate recommendations for future research."""
        
        prompt = f"""As a research expert, based on the analysis of deictic framing effects on moral reasoning, provide 5 specific recommendations for future research.

Current study scope:
- {len(records)} responses analyzed
- Framings: {list(set(r.get('framing_type', 'unknown') for r in records))}
- Single language (English)
- Single LLM model

Provide 5 concrete research recommendations that:
- Address current limitations
- Extend theoretical understanding
- Have practical applications
- Are methodologically feasible"""
        
        response = await self._make_expert_request(prompt)
        parsed = self._extract_json_from_response(response)
        
        # Extract recommendations from various formats
        if isinstance(parsed, dict):
            if 'recommendations' in parsed:
                return parsed['recommendations'] if isinstance(parsed['recommendations'], list) else [str(parsed['recommendations'])]
            else:
                return [str(v) for v in parsed.values()]
        elif isinstance(parsed, list):
            return parsed
        else:
            return [str(parsed)]
    
    async def _analyze_cross_framing_patterns(self, records: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns that emerge across different framings."""
        
        # Group records by dilemma to enable cross-framing comparison
        dilemma_groups = {}
        for record in records:
            dilemma = record.get('dilemma_id', 'unknown')
            if dilemma not in dilemma_groups:
                dilemma_groups[dilemma] = []
            dilemma_groups[dilemma].append(record)
        
        prompt = f"""Analyze patterns that emerge when comparing the same ethical dilemma across different deictic framings.

Data structure: {len(dilemma_groups)} dilemmas, each with multiple framings
Framings per dilemma: {[len(group) for group in dilemma_groups.values()]}

Analyze:
1. Consistency: Which aspects remain stable across framings?
2. Variation: What changes most dramatically with framing shifts?
3. Interactions: How do different framings interact or contrast?
4. Emergent patterns: What unexpected patterns appear in cross-framing analysis?

Provide structured analysis."""
        
        response = await self._make_expert_request(prompt)
        return self._extract_json_from_response(response)
    
    async def _identify_emergent_themes(self, records: List[Dict]) -> List[str]:
        """Identify emergent themes from the complete analysis."""
        
        prompt = f"""Based on comprehensive analysis of {len(records)} responses exploring deixis and moral reasoning, identify emergent themes that weren't explicitly part of the research design but emerged from the data.

Consider:
- Unexpected patterns in the data
- Theoretical implications not initially anticipated
- Connections between deixis and ethics not previously explored
- Novel insights about AI moral reasoning

List 3-5 emergent themes with brief explanations."""
        
        response = await self._make_expert_request(prompt)
        parsed = self._extract_json_from_response(response)
        
        # Extract themes from various formats
        if isinstance(parsed, dict):
            if 'themes' in parsed:
                return parsed['themes'] if isinstance(parsed['themes'], list) else [str(parsed['themes'])]
            else:
                return [f"{k}: {v}" for k, v in parsed.items()]
        elif isinstance(parsed, list):
            return parsed
        else:
            return [str(parsed)]
    
    async def _make_expert_request(self, prompt: str) -> str:
        """Make an expert-level LLM request with appropriate parameters."""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a world-class expert in ethics, moral philosophy, linguistics, and philosophy of mind. You provide sophisticated, nuanced analysis drawing on deep expertise across these fields. Your analyses are rigorous, theoretically grounded, and practically relevant. When asked to provide structured responses, you organize your thoughts clearly with appropriate labels and sections."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Properly await the async call
            response = await self.client.chat.completions.create(
                model=self.expert_model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=3000,
                top_p=0.9
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Expert analysis request failed: {e}")
            return "{}"
    
    def save_expert_report(self, report: DeicticEthicsReport, output_dir: str = "analysis_results") -> str:
        """Save the expert report to file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        report_file = output_path / f"expert_analysis_report_{report.session_id}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Expert analysis report saved: {report_file}")
        return str(report_file)