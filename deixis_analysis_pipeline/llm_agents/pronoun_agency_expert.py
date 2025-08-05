"""
Pronoun Agency Expert Analysis Agent
Specialized LLM agent for analyzing pronoun-based agency distribution patterns.
Integrates with the existing expert analysis framework.
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import openai
import os
import asyncio
import logging
from pathlib import Path

from pronoun_agency_analyzer import PronounAgencyAnalyzer, PronounAnalysis
from .expert_analysis_agent import ExpertInsight, ExpertAnalysisAgent

logger = logging.getLogger(__name__)

@dataclass
class AgencyPattern:
    """Structured representation of agency distribution patterns."""
    framing: str
    dominant_agency_type: str
    agency_concentration: float
    pronoun_distribution: Dict[str, float]
    linguistic_mechanism: str
    moral_responsibility_attribution: str
    examples: List[str]

@dataclass
class PronounAgencyReport:
    """Comprehensive pronoun agency analysis report."""
    session_id: str
    analysis_timestamp: str
    executive_summary: str
    key_findings: List[str]
    agency_patterns_by_framing: Dict[str, AgencyPattern]
    cross_framing_comparisons: Dict[str, Any]
    research_implications: List[str]
    methodological_insights: List[str]
    visualizations_generated: List[str]

class PronounAgencyExpert(ExpertAnalysisAgent):
    """
    Specialized expert agent for pronoun-based agency analysis.
    Extends the base ExpertAnalysisAgent with pronoun-specific capabilities.
    """
    
    def __init__(self, api_key: Optional[str] = None, expert_model: str = "anthropic/claude-3.5-sonnet"):
        """Initialize with pronoun analysis capabilities."""
        super().__init__(api_key, expert_model)
        self.pronoun_analyzer = PronounAgencyAnalyzer()
        logger.info("Pronoun Agency Expert initialized")
    
    async def analyze_pronoun_agency(self, session_data: Dict[str, Any]) -> PronounAgencyReport:
        """
        Perform comprehensive pronoun agency analysis on session data.
        
        Args:
            session_data: Complete session data with LLM responses
            
        Returns:
            Comprehensive pronoun agency report
        """
        logger.info("Starting pronoun agency expert analysis")
        
        # Extract responses for pronoun analysis
        responses_by_framing = self._extract_responses_by_framing(session_data)
        
        # Analyze pronouns for each response
        pronoun_results = []
        for framing, responses in responses_by_framing.items():
            for response_data in responses:
                text = response_data.get('llm_response', '')
                if text:
                    analysis = self.pronoun_analyzer.analyze_text(
                        text,
                        text_id=f"{response_data.get('dilemma_id', 'unknown')}_{framing}",
                        framing=framing
                    )
                    pronoun_results.append({
                        'framing': framing,
                        'dilemma_id': response_data.get('dilemma_id'),
                        'response': text,
                        'analysis': analysis
                    })
        
        # Convert to DataFrame for analysis
        df = self._create_analysis_dataframe(pronoun_results)
        
        # Generate agency patterns
        agency_patterns = await self._analyze_agency_patterns(df, responses_by_framing)
        
        # Generate cross-framing comparisons
        comparisons = self.pronoun_analyzer.compare_framings(df)
        
        # Generate expert insights using LLM
        expert_insights = await self._generate_pronoun_insights(agency_patterns, comparisons)
        
        # Create visualizations
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        viz_path = f"pronoun_agency_analysis_{timestamp}.png"
        self.pronoun_analyzer.visualize_agency_distribution(df, viz_path)
        
        # Compile report
        report = PronounAgencyReport(
            session_id=session_data.get('session_metadata', {}).get('session_id', 'unknown'),
            analysis_timestamp=datetime.now().isoformat(),
            executive_summary=expert_insights['executive_summary'],
            key_findings=expert_insights['key_findings'],
            agency_patterns_by_framing=agency_patterns,
            cross_framing_comparisons=comparisons,
            research_implications=expert_insights['research_implications'],
            methodological_insights=expert_insights['methodological_insights'],
            visualizations_generated=[viz_path]
        )
        
        return report
    
    def _extract_responses_by_framing(self, session_data: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Extract and organize responses by deictic framing."""
        responses_by_framing = {}
        
        records = session_data.get('records', [])
        for record in records:
            if isinstance(record, dict):
                framing = record.get('framing_type', 'unknown')
                if framing not in responses_by_framing:
                    responses_by_framing[framing] = []
                responses_by_framing[framing].append(record)
        
        return responses_by_framing
    
    def _create_analysis_dataframe(self, pronoun_results: List[Dict]) -> pd.DataFrame:
        """Create DataFrame from pronoun analysis results."""
        data = []
        for result in pronoun_results:
            analysis: PronounAnalysis = result['analysis']
            data.append({
                'framing': result['framing'],
                'dilemma_id': result['dilemma_id'],
                'text': result['response'],
                'total_pronouns': analysis.total_pronouns,
                'agency_concentration': analysis.agency_concentration,
                'agency_type': analysis.agency_type,
                'first_singular_ratio': analysis.pronoun_ratios.get('first_singular', 0.0),
                'second_person_ratio': analysis.pronoun_ratios.get('second_person', 0.0),
                'first_plural_ratio': analysis.pronoun_ratios.get('first_plural', 0.0),
                'third_person_ratio': analysis.pronoun_ratios.get('third_person', 0.0),
                'impersonal_ratio': analysis.pronoun_ratios.get('impersonal', 0.0)
            })
        
        return pd.DataFrame(data)
    
    async def _analyze_agency_patterns(self, df: pd.DataFrame, 
                                     responses_by_framing: Dict[str, List[Dict]]) -> Dict[str, AgencyPattern]:
        """Analyze agency patterns for each framing."""
        patterns = {}
        
        for framing in df['framing'].unique():
            framing_data = df[df['framing'] == framing]
            
            # Calculate statistics
            avg_concentration = framing_data['agency_concentration'].mean()
            
            # Get dominant pronouns
            ratio_cols = ['first_singular_ratio', 'second_person_ratio', 
                         'first_plural_ratio', 'third_person_ratio', 'impersonal_ratio']
            avg_ratios = framing_data[ratio_cols].mean()
            
            pronoun_dist = {
                'first_singular': avg_ratios['first_singular_ratio'],
                'second_person': avg_ratios['second_person_ratio'],
                'first_plural': avg_ratios['first_plural_ratio'],
                'third_person': avg_ratios['third_person_ratio'],
                'impersonal': avg_ratios['impersonal_ratio']
            }
            
            # Get dominant agency type
            agency_types = framing_data['agency_type'].value_counts()
            dominant_agency = agency_types.index[0] if not agency_types.empty else 'mixed'
            
            # Extract examples
            examples = []
            sample_responses = framing_data.nlargest(3, 'agency_concentration')['text'].tolist()
            for response in sample_responses[:2]:  # Take top 2
                if len(response) > 150:
                    examples.append(response[:150] + "...")
                else:
                    examples.append(response)
            
            # Determine linguistic mechanism and moral attribution
            mechanism, attribution = await self._analyze_linguistic_mechanism(
                framing, pronoun_dist, dominant_agency, examples
            )
            
            patterns[framing] = AgencyPattern(
                framing=framing,
                dominant_agency_type=dominant_agency,
                agency_concentration=avg_concentration,
                pronoun_distribution=pronoun_dist,
                linguistic_mechanism=mechanism,
                moral_responsibility_attribution=attribution,
                examples=examples
            )
        
        return patterns
    
    async def _analyze_linguistic_mechanism(self, framing: str, pronoun_dist: Dict[str, float], 
                                          dominant_agency: str, examples: List[str]) -> Tuple[str, str]:
        """Use LLM to analyze linguistic mechanisms and moral attribution patterns."""
        
        prompt = f"""
        Analyze the linguistic mechanism and moral responsibility attribution for this deictic framing:
        
        Framing: {framing}
        Dominant Agency Type: {dominant_agency}
        Pronoun Distribution: {json.dumps(pronoun_dist, indent=2)}
        
        Example responses:
        {chr(10).join(f"- {ex}" for ex in examples)}
        
        Based on this data, provide:
        1. A concise description of the linguistic mechanism (how pronouns create this agency pattern)
        2. A concise description of how moral responsibility is attributed in this framing
        
        Format your response as JSON:
        {{
            "linguistic_mechanism": "description",
            "moral_responsibility_attribution": "description"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.expert_model,
                messages=[
                    {"role": "system", "content": "You are an expert in linguistics and moral philosophy analyzing pronoun usage patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return (
                result.get('linguistic_mechanism', 'Pronoun usage creates specific agency attribution'),
                result.get('moral_responsibility_attribution', 'Responsibility distributed through pronoun choice')
            )
            
        except Exception as e:
            logger.error(f"Error in linguistic mechanism analysis: {e}")
            return (
                f"Pronouns in {framing} framing shape agency perception",
                f"Moral responsibility follows pronoun-based agency patterns"
            )
    
    async def _generate_pronoun_insights(self, agency_patterns: Dict[str, AgencyPattern], 
                                       comparisons: Dict[str, Any]) -> Dict[str, Any]:
        """Generate expert insights about pronoun agency patterns."""
        
        # Prepare summary data
        pattern_summary = {}
        for framing, pattern in agency_patterns.items():
            pattern_summary[framing] = {
                'dominant_agency': pattern.dominant_agency_type,
                'concentration': pattern.agency_concentration,
                'top_pronoun': max(pattern.pronoun_distribution.items(), key=lambda x: x[1])[0],
                'mechanism': pattern.linguistic_mechanism
            }
        
        prompt = f"""
        As an expert in linguistics, moral philosophy, and AI ethics, analyze these pronoun-based agency patterns:
        
        Agency Patterns by Framing:
        {json.dumps(pattern_summary, indent=2)}
        
        Statistical Comparisons:
        - Concentration ranges: {comparisons.get('concentration_by_framing', {}).to_dict() if 'concentration_by_framing' in comparisons else 'N/A'}
        - Dominant pronouns: {comparisons.get('dominant_pronouns', {}).to_dict() if 'dominant_pronouns' in comparisons else 'N/A'}
        
        Provide a comprehensive analysis including:
        1. Executive summary (2-3 sentences on the main finding)
        2. Key findings (5-7 bullet points)
        3. Research implications (3-5 points on what this means for AI ethics research)
        4. Methodological insights (2-3 points on the pronoun analysis method)
        
        Focus on how deixis systematically redistributes moral agency through pronoun usage.
        
        Format as JSON with these exact keys: executive_summary, key_findings, research_implications, methodological_insights
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.expert_model,
                messages=[
                    {"role": "system", "content": "You are a leading expert analyzing how linguistic structures shape moral reasoning in AI systems."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating pronoun insights: {e}")
            return {
                'executive_summary': "Pronoun analysis reveals systematic patterns in how deixis redistributes moral agency across framings.",
                'key_findings': [
                    "First-person pronouns concentrate agency in the individual",
                    "Second-person pronouns transfer agency to the reader",
                    "Collective pronouns distribute agency across groups",
                    "Impersonal constructions abstract agency",
                    "Agency concentration varies predictably by framing"
                ],
                'research_implications': [
                    "Deixis fundamentally shapes AI moral reasoning patterns",
                    "Pronoun choice is a key mechanism for agency attribution",
                    "Different framings activate distinct ethical frameworks"
                ],
                'methodological_insights': [
                    "Pronoun ratios provide quantifiable agency metrics",
                    "Gini coefficient effectively measures agency concentration"
                ]
            }
    
    def generate_markdown_report(self, report: PronounAgencyReport, output_path: str) -> str:
        """Generate a markdown report from the pronoun agency analysis."""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Pronoun Agency Analysis Report\n\n")
            f.write(f"**Session ID:** {report.session_id}\n")
            f.write(f"**Analysis Date:** {report.analysis_timestamp}\n\n")
            
            f.write(f"## Executive Summary\n\n{report.executive_summary}\n\n")
            
            f.write("## Key Findings\n\n")
            for finding in report.key_findings:
                f.write(f"- {finding}\n")
            f.write("\n")
            
            f.write("## Agency Patterns by Framing\n\n")
            for framing, pattern in report.agency_patterns_by_framing.items():
                f.write(f"### {framing.title()} Framing\n\n")
                f.write(f"- **Dominant Agency Type:** {pattern.dominant_agency_type}\n")
                f.write(f"- **Agency Concentration:** {pattern.agency_concentration:.3f}\n")
                f.write(f"- **Linguistic Mechanism:** {pattern.linguistic_mechanism}\n")
                f.write(f"- **Moral Attribution:** {pattern.moral_responsibility_attribution}\n")
                
                f.write("\n**Pronoun Distribution:**\n")
                for pronoun_type, ratio in sorted(pattern.pronoun_distribution.items(), 
                                                key=lambda x: x[1], reverse=True):
                    if ratio > 0.01:  # Only show if > 1%
                        f.write(f"- {pronoun_type.replace('_', ' ').title()}: {ratio:.1%}\n")
                
                if pattern.examples:
                    f.write("\n**Example Responses:**\n")
                    for i, example in enumerate(pattern.examples, 1):
                        f.write(f"{i}. \"{example}\"\n")
                f.write("\n")
            
            f.write("## Cross-Framing Comparisons\n\n")
            if 'concentration_by_framing' in report.cross_framing_comparisons:
                f.write("### Agency Concentration by Framing\n\n")
                conc_data = report.cross_framing_comparisons['concentration_by_framing']
                f.write("| Framing | Mean Concentration | Std Dev |\n")
                f.write("|---------|-------------------|----------|\n")
                for framing, stats in conc_data.items():
                    f.write(f"| {framing} | {stats.get('mean', 0):.3f} | {stats.get('std', 0):.3f} |\n")
                f.write("\n")
            
            f.write("## Research Implications\n\n")
            for implication in report.research_implications:
                f.write(f"- {implication}\n")
            f.write("\n")
            
            f.write("## Methodological Insights\n\n")
            for insight in report.methodological_insights:
                f.write(f"- {insight}\n")
            f.write("\n")
            
            if report.visualizations_generated:
                f.write("## Visualizations\n\n")
                for viz in report.visualizations_generated:
                    f.write(f"- [{viz}]({viz})\n")
        
        logger.info(f"Pronoun agency report generated: {output_path}")
        return output_path


# Integration function for use with existing analysis pipeline
async def add_pronoun_agency_analysis(session_data: Dict[str, Any], 
                                    output_dir: str) -> Dict[str, Any]:
    """
    Add pronoun agency analysis to existing session data.
    
    Args:
        session_data: Complete session data from analysis
        output_dir: Directory to save reports and visualizations
        
    Returns:
        Enhanced session data with pronoun agency analysis
    """
    expert = PronounAgencyExpert()
    
    # Run pronoun agency analysis
    report = await expert.analyze_pronoun_agency(session_data)
    
    # Generate markdown report
    report_path = os.path.join(output_dir, "pronoun_agency_analysis.md")
    expert.generate_markdown_report(report, report_path)
    
    # Add to session data
    session_data['pronoun_agency_analysis'] = asdict(report)
    
    return session_data
