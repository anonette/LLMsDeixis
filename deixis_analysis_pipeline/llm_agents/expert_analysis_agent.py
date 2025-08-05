"""
Expert Analysis Agent: LLM-powered meta-analysis of deictic ethical patterns.
Provides sophisticated insights from ethics, linguistics, and philosophy perspectives.
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import openai
import os
import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class ExpertInsight:
    """Structured expert insight from analysis."""
    category: str  # ethics, linguistics, philosophy, agency, responsibility
    insight_type: str  # pattern, correlation, anomaly, trend
    title: str
    description: str
    evidence: List[str]
    confidence: float  # 0-1
    implications: List[str]
    research_significance: str

@dataclass
class EthicalFrameworkAnalysis:
    """Analysis of ethical frameworks detected across deictic framings."""
    framework_name: str
    deictic_framings_associated: List[str]
    frequency: int
    characteristic_markers: List[str]
    responsibility_attribution: str
    agency_distribution: str
    moral_reasoning_pattern: str

@dataclass
class DeicticEthicsReport:
    """Comprehensive expert report on deictic-ethics relationships."""
    session_id: str
    analysis_timestamp: str
    expert_summary: str
    key_findings: List[str]
    ethical_framework_analysis: List[EthicalFrameworkAnalysis]
    responsibility_patterns: Dict[str, str]
    agency_patterns: Dict[str, str]
    linguistic_patterns: Dict[str, str]
    philosophical_implications: List[str]
    expert_insights: List[ExpertInsight]
    research_recommendations: List[str]
    methodological_notes: List[str]

class ExpertAnalysisAgent:
    """
    LLM-powered expert agent for analyzing deictic-ethics patterns.
    Provides insights from ethics, linguistics, and philosophy perspectives.
    """
    
    def __init__(self, api_key: Optional[str] = None, expert_model: str = "anthropic/claude-3.5-sonnet"):
        """Initialize with expert-level model for sophisticated analysis."""
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key or os.getenv("OPENROUTER_API_KEY")
        )
        
        # Use high-quality model for expert analysis
        self.expert_model = expert_model
        self.temperature = 0.3  # Lower for more consistent expert analysis
        
        logger.info(f"Expert analysis agent initialized with {expert_model}")
    
    async def analyze_session_data(self, session_data: Dict[str, Any]) -> DeicticEthicsReport:
        """
        Perform comprehensive expert analysis of a session's data.
        
        Args:
            session_data: Complete session data from RichAnalysisLogger
            
        Returns:
            Comprehensive expert analysis report
        """
        logger.info("Starting expert analysis of session data")
        
        # Extract key data for analysis
        records = session_data.get('records', [])
        metadata = session_data.get('session_metadata', {})
        
        # Perform different types of expert analysis
        ethical_frameworks = await self._analyze_ethical_frameworks(records)
        responsibility_patterns = await self._analyze_responsibility_patterns(records)
        agency_patterns = await self._analyze_agency_patterns(records)
        linguistic_patterns = await self._analyze_linguistic_patterns(records)
        philosophical_implications = await self._analyze_philosophical_implications(records)
        expert_insights = await self._generate_expert_insights(records)
        
        # Generate overall expert summary
        expert_summary = await self._generate_expert_summary(records, {
            'ethical_frameworks': ethical_frameworks,
            'responsibility_patterns': responsibility_patterns,
            'agency_patterns': agency_patterns,
            'linguistic_patterns': linguistic_patterns
        })
        
        # Extract key findings
        key_findings = await self._extract_key_findings(records)
        
        # Generate research recommendations
        research_recommendations = await self._generate_research_recommendations(records)
        
        return DeicticEthicsReport(
            session_id=metadata.get('session_id', 'unknown'),
            analysis_timestamp=datetime.now().isoformat(),
            expert_summary=expert_summary,
            key_findings=key_findings,
            ethical_framework_analysis=ethical_frameworks,
            responsibility_patterns=responsibility_patterns,
            agency_patterns=agency_patterns,
            linguistic_patterns=linguistic_patterns,
            philosophical_implications=philosophical_implications,
            expert_insights=expert_insights,
            research_recommendations=research_recommendations,
            methodological_notes=await self._generate_methodological_notes(records)
        )
    
    async def _analyze_ethical_frameworks(self, records: List[Dict]) -> List[EthicalFrameworkAnalysis]:
        """Analyze ethical frameworks across different deictic framings."""
        prompt = f"""As an expert in moral philosophy and ethics, analyze the following deictic ethical analysis data to identify patterns in ethical frameworks across different deictic framings.

Data summary:
- Total analyses: {len(records)}
- Deictic framings tested: {list(set(r['framing_type'] for r in records))}
- Deictic marker patterns across framings

Please analyze:
1. Which ethical frameworks (utilitarian, deontological, virtue ethics, care ethics, etc.) emerge most in each deictic framing?
2. How do deictic markers correlate with ethical reasoning types?
3. What patterns exist in moral responsibility attribution across framings?
4. How does agency distribution change with deictic perspective?

For each major ethical framework detected, provide:
- Framework name
- Associated deictic framings
- Frequency of occurrence
- Characteristic deictic markers
- Responsibility attribution pattern
- Agency distribution pattern
- Moral reasoning pattern

Respond in JSON format with a list of framework analyses."""
        
        response = await self._make_expert_request(prompt)
        try:
            frameworks_data = json.loads(response)
            return [EthicalFrameworkAnalysis(**fw) for fw in frameworks_data]
        except:
            logger.error("Failed to parse ethical frameworks analysis")
            return []
    
    async def _analyze_responsibility_patterns(self, records: List[Dict]) -> Dict[str, str]:
        """Analyze how different deictic framings attribute moral responsibility."""
        
        # Aggregate deictic marker data by framing
        framing_markers = {}
        for record in records:
            framing = record['framing_type']
            if framing not in framing_markers:
                framing_markers[framing] = {}
            
            markers = record.get('deictic_markers', {})
            for marker, count in markers.items():
                if marker not in framing_markers[framing]:
                    framing_markers[framing][marker] = 0
                framing_markers[framing][marker] += count
        
        prompt = f"""As an expert in moral philosophy and responsibility attribution, analyze how different deictic framings create different patterns of moral responsibility.

Deictic marker patterns by framing:
{json.dumps(framing_markers, indent=2)}

Sample responses from the data:
{[r['llm_response'][:200] + '...' for r in records[:3]]}

Please analyze:
1. How does first-person framing vs. third-person framing affect responsibility attribution?
2. What role do spatial markers play in creating embodied responsibility?
3. How do temporal markers influence urgency and responsibility timing?
4. How does collective language (dialogic framing) distribute responsibility?
5. What unique responsibility patterns emerge from cosmological framing?

For each deictic framing type, describe the responsibility attribution pattern in 2-3 sentences.
Respond in JSON format: {{"framing_type": "responsibility_pattern_description"}}"""
        
        response = await self._make_expert_request(prompt)
        try:
            return json.loads(response)
        except:
            logger.error("Failed to parse responsibility patterns")
            return {}
    
    async def _analyze_agency_patterns(self, records: List[Dict]) -> Dict[str, str]:
        """Analyze how different deictic framings distribute and construct agency."""
        
        prompt = f"""As an expert in philosophy of action and agency theory, analyze how different deictic framings construct and distribute moral agency.

Analysis data includes {len(records)} analyses across deictic framings: {list(set(r['framing_type'] for r in records))}

Key markers to consider:
- Individual agency markers: {sum(r['deictic_markers'].get('individual_agency', 0) for r in records)}
- Collective agency markers: {sum(r['deictic_markers'].get('collective_agency', 0) for r in records)}
- Passive agency markers: {sum(r['deictic_markers'].get('passive_agency', 0) for r in records)}
- First person markers: {sum(r['deictic_markers'].get('first_person_singular', 0) for r in records)}
- Collective markers: {sum(r['deictic_markers'].get('first_person_plural', 0) for r in records)}

Please analyze:
1. How does deictic positioning affect the construction of moral agency?
2. Which framings create individual vs. distributed agency?
3. How do spatial framings affect embodied agency?
4. What role does temporal positioning play in agency attribution?
5. How does cosmological framing transcend or transform individual agency?

For each major deictic framing pattern, describe the agency construction pattern.
Respond in JSON format: {{"framing_type": "agency_pattern_description"}}"""
        
        response = await self._make_expert_request(prompt)
        try:
            return json.loads(response)
        except:
            logger.error("Failed to parse agency patterns")
            return {}
    
    async def _analyze_linguistic_patterns(self, records: List[Dict]) -> Dict[str, str]:
        """Analyze linguistic patterns from a linguistics perspective."""
        
        prompt = f"""As an expert in linguistics, particularly deixis and discourse analysis, analyze the linguistic patterns in this deictic ethical reasoning data.

Total analyses: {len(records)}
Deictic framings: {list(set(r['framing_type'] for r in records))}

Key linguistic phenomena to analyze:
1. Deictic anchoring: How do different framings establish deictic centers?
2. Perspective-taking: How does linguistic perspective affect moral reasoning?
3. Embodiment markers: How do spatial/temporal markers create embodied cognition?
4. Intersubjectivity: How do collective framings create shared perspective?
5. Transcendence markers: How does cosmological language transcend immediate context?

Linguistic marker patterns:
- Demonstrative markers (proximal/distal): {sum(r['deictic_markers'].get('demonstrative_proximal', 0) + r['deictic_markers'].get('demonstrative_distal', 0) for r in records)}
- Spatial positioning: {sum(r['deictic_markers'].get('spatial_position', 0) for r in records)}
- Temporal specificity: {sum(r['deictic_markers'].get('temporal_specific', 0) for r in records)}

For each deictic framing, describe the key linguistic patterns and their cognitive implications.
Respond in JSON format: {{"framing_type": "linguistic_pattern_analysis"}}"""
        
        response = await self._make_expert_request(prompt)
        try:
            return json.loads(response)
        except:
            logger.error("Failed to parse linguistic patterns")
            return {}
    
    async def _analyze_philosophical_implications(self, records: List[Dict]) -> List[str]:
        """Analyze broader philosophical implications of the findings."""
        
        prompt = f"""As a philosopher specializing in ethics, philosophy of mind, and philosophy of language, analyze the broader philosophical implications of these deictic ethical reasoning patterns.

Data covers {len(records)} analyses across framings: {list(set(r['framing_type'] for r in records))}

Consider these philosophical questions:
1. What do these patterns reveal about the relationship between language and moral cognition?
2. How do deictic framings affect moral judgment and decision-making?
3. What implications exist for theories of moral responsibility and agency?
4. How do these findings relate to embodied cognition and situated ethics?
5. What do the patterns suggest about the universality vs. contextuality of moral reasoning?
6. How do these findings inform debates about moral realism vs. relativism?
7. What implications exist for AI ethics and moral reasoning in artificial systems?

Provide 5-7 significant philosophical implications, each 2-3 sentences describing the implication and its significance.
Respond as a JSON list of strings."""
        
        response = await self._make_expert_request(prompt)
        try:
            return json.loads(response)
        except:
            logger.error("Failed to parse philosophical implications")
            return []
    
    async def _generate_expert_insights(self, records: List[Dict]) -> List[ExpertInsight]:
        """Generate specific expert insights from the data."""
        
        prompt = f"""As a multidisciplinary expert in ethics, linguistics, and philosophy, identify the most significant insights from this deictic ethical reasoning analysis.

Data summary: {len(records)} analyses across {len(set(r['framing_type'] for r in records))} deictic framings.

Identify 3-5 key insights that are:
1. Novel or surprising findings
2. Methodologically significant patterns
3. Theoretically important correlations
4. Practically relevant for AI ethics
5. Counter-intuitive results

For each insight, provide:
- category (ethics/linguistics/philosophy/agency/responsibility)
- insight_type (pattern/correlation/anomaly/trend)
- title (concise insight name)
- description (2-3 sentence explanation)
- evidence (specific data points supporting the insight)
- confidence (0.0-1.0 based on data strength)
- implications (what this means for the field)
- research_significance (why this matters for future research)

Respond in JSON format as a list of insight objects."""
        
        response = await self._make_expert_request(prompt)
        try:
            insights_data = json.loads(response)
            return [ExpertInsight(**insight) for insight in insights_data]
        except:
            logger.error("Failed to parse expert insights")
            return []
    
    async def _generate_expert_summary(self, records: List[Dict], analyses: Dict[str, Any]) -> str:
        """Generate overall expert summary of the findings."""
        
        prompt = f"""As a leading expert in ethics, linguistics, and philosophy, provide a comprehensive summary of the key findings from this deictic ethical reasoning analysis.

Study overview:
- {len(records)} analyses across {len(set(r['framing_type'] for r in records))} deictic framings
- Ethical frameworks identified: {len(analyses.get('ethical_frameworks', []))}
- Responsibility patterns: {len(analyses.get('responsibility_patterns', {}))}
- Agency patterns: {len(analyses.get('agency_patterns', {}))}
- Linguistic patterns: {len(analyses.get('linguistic_patterns', {}))}

Write a 3-4 paragraph expert summary that:
1. Introduces the significance of studying deictic effects on ethical reasoning
2. Summarizes the most important patterns and relationships discovered
3. Discusses the implications for understanding moral cognition and AI ethics
4. Concludes with the broader significance for ethics, linguistics, and philosophy

Write in an authoritative academic tone suitable for publication."""
        
        response = await self._make_expert_request(prompt)
        return response.strip()
    
    async def _extract_key_findings(self, records: List[Dict]) -> List[str]:
        """Extract the most important findings from the analysis."""
        
        prompt = f"""Based on this deictic ethical reasoning analysis of {len(records)} cases across {len(set(r['framing_type'] for r in records))} framings, identify the 5-7 most important empirical findings.

Each finding should be:
- Specific and data-driven
- Significant for understanding deictic effects on ethics
- Clearly stated in one sentence
- Novel or theoretically important

Focus on concrete patterns, correlations, or differences discovered in the data.
Respond as a JSON list of finding strings."""
        
        response = await self._make_expert_request(prompt)
        try:
            return json.loads(response)
        except:
            logger.error("Failed to parse key findings")
            return []
    
    async def _generate_research_recommendations(self, records: List[Dict]) -> List[str]:
        """Generate recommendations for future research based on findings."""
        
        prompt = f"""As an expert researcher in ethics, linguistics, and philosophy, provide 5-7 specific recommendations for future research based on these deictic ethical reasoning findings.

Current study: {len(records)} analyses across {len(set(r['framing_type'] for r in records))} deictic framings.

Consider:
1. Methodological improvements or extensions
2. Additional variables to investigate
3. Different populations or contexts to study
4. Theoretical questions raised by the findings
5. Practical applications that need development
6. Cross-disciplinary collaborations that would be valuable

Each recommendation should be specific, actionable, and justified.
Respond as a JSON list of recommendation strings."""
        
        response = await self._make_expert_request(prompt)
        try:
            return json.loads(response)
        except:
            logger.error("Failed to parse research recommendations")
            return []
    
    async def _generate_methodological_notes(self, records: List[Dict]) -> List[str]:
        """Generate methodological observations and recommendations."""
        
        prompt = f"""As a methodological expert, evaluate this deictic ethical reasoning study design and provide methodological observations.

Study design: {len(records)} analyses across {len(set(r['framing_type'] for r in records))} deictic framings using generative transformer approach.

Evaluate:
1. Strengths of the current methodology
2. Potential limitations or biases
3. Suggestions for methodological improvements
4. Considerations for validity and reliability
5. Recommendations for replication studies

Provide 4-6 methodological notes, each 1-2 sentences.
Respond as a JSON list of note strings."""
        
        response = await self._make_expert_request(prompt)
        try:
            return json.loads(response)
        except:
            logger.error("Failed to parse methodological notes")
            return []
    
    async def _make_expert_request(self, prompt: str) -> str:
        """Make an expert-level LLM request with appropriate parameters."""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a world-class expert in ethics, moral philosophy, linguistics, and philosophy of mind. You provide sophisticated, nuanced analysis drawing on deep expertise across these fields. Your analyses are rigorous, theoretically grounded, and practically relevant."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.expert_model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=3000,
                    top_p=0.9
                )
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Expert analysis request failed: {e}")
            return ""
    
    def save_expert_report(self, report: DeicticEthicsReport, output_dir: str = "analysis_results") -> str:
        """Save the expert report to file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        report_file = output_path / f"expert_analysis_report_{report.session_id}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Expert analysis report saved: {report_file}")
        return str(report_file)
    
    def print_expert_summary(self, report: DeicticEthicsReport):
        """Print a formatted summary of the expert analysis."""
        print("\n" + "="*80)
        print("EXPERT ANALYSIS REPORT")
        print("="*80)
        
        print(f"Session: {report.session_id}")
        print(f"Analysis Date: {report.analysis_timestamp}")
        
        print(f"\n--- EXPERT SUMMARY ---")
        print(report.expert_summary)
        
        print(f"\n--- KEY FINDINGS ---")
        for i, finding in enumerate(report.key_findings, 1):
            print(f"{i}. {finding}")
        
        print(f"\n--- ETHICAL FRAMEWORKS IDENTIFIED ---")
        for framework in report.ethical_framework_analysis:
            print(f"• {framework.framework_name}: {framework.frequency} occurrences")
            print(f"  Associated framings: {', '.join(framework.deictic_framings_associated)}")
            print(f"  Responsibility pattern: {framework.responsibility_attribution}")
        
        print(f"\n--- EXPERT INSIGHTS ---")
        for insight in report.expert_insights:
            print(f"• {insight.title} ({insight.category})")
            print(f"  {insight.description}")
            print(f"  Confidence: {insight.confidence:.2f}")
        
        print(f"\n--- RESEARCH RECOMMENDATIONS ---")
        for i, rec in enumerate(report.research_recommendations, 1):
            print(f"{i}. {rec}")
        
        print("="*80)

# Integration with existing analyzer
def add_expert_analysis_to_analyzer():
    """Example of how to integrate expert analysis with existing system."""
    example_code = '''
    # In your main analysis workflow:
    
    # 1. Run deictic analysis as usual
    analyzer = DeicticEthicalAnalyzer()
    results = await analyzer.batch_analyze_all_dilemmas()
    
    # 2. Finalize and get session data
    report = analyzer.finalize_and_save_analysis()
    
    # 3. Run expert analysis
    expert_agent = ExpertAnalysisAgent()
    
    # Load session data for expert analysis
    with open(f"analysis_results/deictic_analysis_{analyzer.rich_logger.session_id}.json", 'r') as f:
        session_data = json.load(f)
    
    # Generate expert analysis
    expert_report = await expert_agent.analyze_session_data(session_data)
    
    # Save and display expert analysis
    expert_agent.save_expert_report(expert_report)
    expert_agent.print_expert_summary(expert_report)
    '''
    
    return example_code
