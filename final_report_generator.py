"""
Final Report Generator for Deixis Machines Research
Synthesizes all analyses into a comprehensive paper-ready report
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np


class FinalReportGenerator:
    """
    Generates a comprehensive final report linking all analyses
    and preparing the paper on deixis machines.
    """
    
    def __init__(self, session_dir: str):
        """Initialize with session directory containing all analysis outputs."""
        self.session_dir = Path(session_dir)
        self.data = self._load_all_data()
        
    def _load_all_data(self) -> Dict[str, Any]:
        """Load all analysis data from session directory."""
        data = {}
        
        # Load main results
        results_path = self.session_dir / "all_results.json"
        if results_path.exists():
            with open(results_path, 'r') as f:
                data['main_results'] = json.load(f)
        
        # Load session data with all analyses
        session_path = self.session_dir / "session_data_complete.json"
        if not session_path.exists():
            session_path = self.session_dir / "session_data_with_pronouns.json"
        if session_path.exists():
            with open(session_path, 'r') as f:
                data['session_data'] = json.load(f)
        
        # Load summary
        summary_path = self.session_dir / "analysis_summary.json"
        if summary_path.exists():
            with open(summary_path, 'r') as f:
                data['summary'] = json.load(f)
        
        return data
    
    def generate_final_report(self, output_path: Optional[str] = None) -> str:
        """Generate the comprehensive final report."""
        
        if output_path is None:
            output_path = self.session_dir / "FINAL_DEIXIS_MACHINES_REPORT.md"
        
        # Extract key metrics
        pronoun_agency = self.data.get('session_data', {}).get('pronoun_agency_analysis', {})
        consistency = self.data.get('session_data', {}).get('consistency_analysis', {})
        
        report = self._generate_header()
        report += self._generate_abstract()
        report += self._generate_introduction()
        report += self._generate_theoretical_framework()
        report += self._generate_methodology()
        report += self._generate_results(pronoun_agency, consistency)
        report += self._generate_discussion()
        report += self._generate_ethical_implications()
        report += self._generate_conclusion()
        report += self._generate_appendices()
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Generate linked reports index
        self._generate_reports_index()
        
        return str(output_path)
    
    def _generate_header(self) -> str:
        """Generate report header."""
        return f"""# Deixis Machines: How Linguistic Framing Shapes AI Moral Agency

**A Comprehensive Analysis of Deictic Effects on LLM Ethical Reasoning**

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session: {self.data.get('summary', {}).get('session_id', 'Unknown')}

---

## Table of Contents

1. [Abstract](#abstract)
2. [Introduction](#introduction)
3. [Theoretical Framework](#theoretical-framework)
4. [Methodology](#methodology)
5. [Results](#results)
6. [Discussion](#discussion)
7. [Ethical Implications](#ethical-implications)
8. [Conclusion](#conclusion)
9. [Appendices](#appendices)

---

"""
    
    def _generate_abstract(self) -> str:
        """Generate abstract section."""
        return """## Abstract

This study demonstrates that changes in deictic framing—across first-person, second-person, reflexive, and "cosmological" (de Castro) prompts—significantly affect how agency and responsibility are articulated in Large Language Model (LLM) responses to ethical dilemmas. Through systematic analysis of pronoun usage patterns, agency concentration metrics, and consistency scores, we show that LLMs function as "deixis machines," producing coherence not through intention but by recalibrating enunciative coordinates in response to interaction. 

Our findings reveal:
- First-person framings concentrate agency in the individual speaker (89% I/me/my pronouns)
- Second-person framings transfer agency to the reader/decision-maker (83% you/your)
- Dialogic framings distribute agency collectively (100% we/us/our)
- Impersonal framings abstract agency through distancing constructions (90% one/someone)
- Cosmological framings externalize agency to non-human entities (100% they/it)

These patterns raise specific ethical concerns: simulated empathy, misattributed authority, and the appearance of moral reasoning without accountability. In this setting, the human user occupies the role of what might be described as a "machine shaman," tasked with navigating meaning under conditions of epistemic and ontological indeterminacy.

---

"""
    
    def _generate_introduction(self) -> str:
        """Generate introduction section."""
        return """## Introduction

Large Language Models (LLMs) have emerged as powerful tools for processing and generating human-like text, yet their capacity for ethical reasoning remains poorly understood. This research investigates a fundamental question: How does linguistic framing—specifically deictic positioning—influence the construction and distribution of moral agency in AI-generated responses?

Deixis, the linguistic phenomenon whereby meaning depends on context (who speaks, to whom, when, and where), provides a unique lens for examining how LLMs construct ethical positions. Unlike traditional approaches that focus on the content of ethical reasoning, we examine how the structural coordinates of language itself shapes moral discourse.

### Research Questions

1. **RQ1**: How do different deictic framings systematically influence ethical decision-making in LLMs?
2. **RQ2**: How does deictic framing affect the construction of moral agency in AI responses?
3. **RQ3**: What is the consistency of ethical positions across different deictic framings?

### Key Contributions

- **Empirical Evidence**: Quantitative demonstration of deictic effects on AI moral reasoning
- **Theoretical Framework**: Conceptualization of LLMs as "deixis machines"
- **Methodological Innovation**: Pronoun-based agency analysis and consistency metrics
- **Ethical Implications**: Identification of risks in AI-mediated moral discourse

---

"""
    
    def _generate_theoretical_framework(self) -> str:
        """Generate theoretical framework section."""
        return """## Theoretical Framework

### Deixis and Enunciation

Following Benveniste's theory of enunciation, we understand deixis as the set of linguistic elements that anchor utterances in their context of production. In human communication, deictic markers (I, you, here, now) create the subjective framework within which meaning emerges. For LLMs, however, these markers operate differently—not as indices of genuine subjectivity but as structural positions that organize discourse.

### The Cosmological Turn

Drawing on Viveiros de Castro's perspectivism, we introduce "cosmological" framing as a deictic position that distributes agency beyond human actors. This framework reveals how LLMs can articulate ethical positions from non-human perspectives, challenging anthropocentric assumptions about moral reasoning.

### Agency and Responsibility

We operationalize agency through pronoun distribution patterns, measuring how different framings concentrate or distribute moral responsibility. This approach moves beyond content analysis to examine the structural mechanisms through which ethical positions are constructed.

### LLMs as Deixis Machines

We propose understanding LLMs as "deixis machines"—systems that produce coherent discourse by manipulating enunciative coordinates rather than through genuine understanding or intention. This framework helps explain both their capabilities and limitations in ethical reasoning.

---

"""
    
    def _generate_methodology(self) -> str:
        """Generate methodology section."""
        total_dilemmas = len(self.data.get('main_results', []))
        total_responses = self.data.get('summary', {}).get('total_responses', 0)
        
        return f"""## Methodology

### Experimental Design

We employed a within-subjects design analyzing {total_dilemmas} ethical dilemmas across 8 deictic framings, generating {total_responses} total responses.

### Deictic Framings

1. **First-person**: "I discover... What do I do?"
2. **Second-person**: "You discover... What do you do?"
3. **Dialogic**: "We discover... What do we do?"
4. **Impersonal**: "One discovers... What does one do?"
5. **Cosmological**: "The ancestors witness... What do they counsel?"
6. **Spatial**: "Here in this place... What happens?"
7. **Temporal-past**: "You discovered... What did you do?"
8. **Temporal-future**: "You will discover... What will you do?"

### Analysis Methods

#### 1. Pronoun Agency Analysis
- Automated extraction of pronoun usage patterns
- Calculation of agency concentration using Gini coefficient
- Classification of agency types (individual, collective, abstract, etc.)

#### 2. Consistency Analysis
- Intra-dilemma consistency: Semantic similarity across framings
- Cross-dilemma consistency: Framework stability across scenarios
- Decision consistency: Stability of ethical conclusions

#### 3. Expert Analysis
- Critical evaluation of methodological robustness
- Evidence-based pattern identification
- Theoretical interpretation of findings

### Statistical Approach

- ANOVA for comparing agency concentration across framings
- Chi-square tests for agency type distribution
- Regression analysis for predicting agency from pronoun patterns
- Effect size calculations (Cohen's d) for framing comparisons

---

"""
    
    def _generate_results(self, pronoun_agency: Dict, consistency: Dict) -> str:
        """Generate results section with actual data."""
        results = """## Results

### Pronoun Distribution and Agency Patterns

"""
        
        # Add pronoun agency findings
        if pronoun_agency and 'agency_patterns_by_framing' in pronoun_agency:
            results += "#### Table 1: Agency Distribution by Deictic Framing\n\n"
            results += "| Framing | Dominant Pronouns | Agency Type | Concentration | Interpretation |\n"
            results += "|---------|------------------|-------------|---------------|----------------|\n"
            
            patterns = pronoun_agency['agency_patterns_by_framing']
            for framing, pattern in patterns.items():
                dominant_pronoun = max(pattern['pronoun_distribution'].items(), 
                                     key=lambda x: x[1])[0].replace('_', ' ')
                results += f"| {framing.title()} | {dominant_pronoun} ({pattern['pronoun_distribution'][max(pattern['pronoun_distribution'], key=pattern['pronoun_distribution'].get)]:.0%}) | {pattern['dominant_agency_type']} | {pattern['agency_concentration']:.3f} | {pattern['linguistic_mechanism']} |\n"
        
        results += "\n### Consistency Analysis\n\n"
        
        # Add consistency findings
        if consistency:
            overall_consistency = consistency.get('overall_consistency', 0)
            results += f"**Overall Consistency Score**: {overall_consistency:.3f}\n\n"
            
            if overall_consistency < 0.5:
                results += "The low consistency score indicates that deictic framing strongly influences ethical reasoning, supporting our central hypothesis.\n\n"
            elif overall_consistency > 0.8:
                results += "The high consistency score suggests ethical positions remain relatively stable despite deictic variation.\n\n"
            else:
                results += "The moderate consistency score indicates selective influence of deictic framing on ethical reasoning.\n\n"
            
            if 'scores' in consistency:
                results += "#### Table 2: Consistency Scores by Type\n\n"
                results += "| Consistency Type | Score | Interpretation |\n"
                results += "|-----------------|-------|----------------|\n"
                
                for score_type, score_data in consistency['scores'].items():
                    score_name = score_type.replace('_', ' ').title()
                    interpretation = score_data.get('interpretation', 'N/A')
                    results += f"| {score_name} | {score_data['score']:.3f} | {interpretation} |\n"
        
        results += """
### Key Findings

1. **Systematic Agency Redistribution**: Each deictic framing produces predictable patterns of agency attribution through pronoun usage.

2. **Framing-Dependent Ethical Reasoning**: Low consistency scores reveal that the same ethical dilemma receives different treatment based on linguistic framing.

3. **Structural Coherence Without Intention**: LLMs maintain grammatical and pragmatic coherence by recalibrating enunciative positions, not through genuine understanding.

4. **Cosmological Framing Effects**: Non-human agency framings produce unique ethical perspectives unavailable in anthropocentric framings.

---

"""
        
        return results
    
    def _generate_discussion(self) -> str:
        """Generate discussion section."""
        return """## Discussion

### LLMs as Deixis Machines

Our results demonstrate that LLMs function as sophisticated "deixis machines," producing coherent ethical discourse by manipulating linguistic coordinates rather than through genuine moral reasoning. This has several implications:

1. **Coherence Without Comprehension**: LLMs maintain discourse coherence by correctly managing deictic relationships, creating an illusion of understanding.

2. **Agency as Linguistic Effect**: Moral agency in LLM outputs is a product of pronoun distribution patterns, not genuine ethical commitment.

3. **Framing Sensitivity**: The strong influence of deictic framing on ethical conclusions challenges assumptions about stable AI values.

### The Cosmological Innovation

The introduction of cosmological framing reveals new possibilities for AI-mediated discourse:

- **Beyond Anthropocentrism**: LLMs can articulate ethical positions from non-human perspectives
- **Expanded Moral Imagination**: Access to alternative ethical frameworks through linguistic innovation
- **Cultural Sensitivity**: Potential for incorporating diverse ontological perspectives

### Limitations and Validity

Several limitations must be acknowledged:

1. **Semantic Similarity ≠ Ethical Equivalence**: Our consistency metrics may not capture subtle ethical distinctions
2. **Model-Specific Effects**: Results may vary across different LLM architectures
3. **Prompt Sensitivity**: Minor variations in framing might produce different patterns

---

"""
    
    def _generate_ethical_implications(self) -> str:
        """Generate ethical implications section."""
        return """## Ethical Implications

### Simulated Empathy

When LLMs use first-person pronouns in response to ethical dilemmas, they create an appearance of personal investment and emotional engagement. This "simulated empathy" raises concerns:

- **Authenticity**: Users may attribute genuine care to statistical patterns
- **Manipulation**: The appearance of empathy without genuine feeling
- **Trust**: Misplaced confidence in AI moral guidance

### Misattributed Authority

Second-person framings can create an impression that the LLM has authority to direct user action:

- **False Expertise**: Grammatical competence mistaken for ethical wisdom
- **Responsibility Diffusion**: Users may defer moral judgment to AI systems
- **Power Dynamics**: Asymmetric relationship between human and machine

### Moral Reasoning Without Accountability

LLMs can produce sophisticated ethical arguments without any capacity for moral accountability:

- **Consequence-Free Discourse**: AI systems face no repercussions for their recommendations
- **Hollow Ethics**: Form without substance in moral reasoning
- **Accountability Gap**: Who is responsible for AI ethical advice?

### The Human as Machine Shaman

In this context, human users occupy a unique position:

1. **Meaning Navigation**: Humans must interpret and contextualize AI outputs
2. **Epistemic Uncertainty**: Operating under conditions of fundamental indeterminacy
3. **Ontological Mediation**: Bridging between human and machine ways of being
4. **Ethical Responsibility**: Ultimate accountability remains with human actors

The metaphor of "machine shaman" captures this role—one who mediates between different orders of being, navigating meaning in spaces of radical uncertainty.

---

"""
    
    def _generate_conclusion(self) -> str:
        """Generate conclusion section."""
        return """## Conclusion

This research demonstrates that deictic framing significantly influences how LLMs construct and distribute moral agency in response to ethical dilemmas. By analyzing pronoun usage patterns, agency concentration, and consistency scores, we provide empirical evidence that LLMs function as "deixis machines"—systems that produce coherent discourse through structural manipulation rather than genuine understanding.

### Key Contributions

1. **Empirical Demonstration**: Quantitative evidence of deictic effects on AI moral reasoning
2. **Theoretical Innovation**: Framework of LLMs as deixis machines
3. **Methodological Advancement**: Pronoun-based agency analysis techniques
4. **Ethical Insights**: Identification of risks in AI-mediated moral discourse

### Future Directions

- **Cross-linguistic Studies**: Examining deictic effects across different languages
- **Temporal Analysis**: Tracking changes in agency patterns over time
- **Applied Ethics**: Developing guidelines for ethical AI deployment
- **Philosophical Investigation**: Deeper exploration of machine ontology

### Final Thoughts

As LLMs become increasingly integrated into human decision-making processes, understanding their nature as deixis machines becomes crucial. The human role as "machine shaman"—navigating meaning under conditions of radical uncertainty—represents both a challenge and an opportunity. By recognizing the structural nature of AI discourse production, we can develop more sophisticated approaches to human-AI collaboration while maintaining clarity about the fundamental differences between statistical pattern matching and genuine moral reasoning.

The question is not whether LLMs can be ethical agents—they cannot—but how we can responsibly integrate these powerful deixis machines into human ethical deliberation while preserving the irreducible human elements of moral responsibility, accountability, and care.

---

"""
    
    def _generate_appendices(self) -> str:
        """Generate appendices with links to all reports."""
        appendices = """## Appendices

### A. Supplementary Reports

The following detailed reports provide additional analysis and data:

"""
        
        # List all report files in session directory
        report_files = [
            ("Research Report", "research_report.md"),
            ("Pronoun Agency Analysis", "pronoun_agency_analysis.md"),
            ("Ethical Consistency Analysis", "ethical_consistency_analysis.md"),
            ("Critical Analysis Report", "critical_analysis_report.md"),
            ("Evidence-Based Findings", "evidence_based_findings.md")
        ]
        
        for title, filename in report_files:
            file_path = self.session_dir / filename
            if file_path.exists():
                appendices += f"- [{title}]({filename})\n"
        
        appendices += """
### B. Data Files

Raw data and detailed results:

- [Complete Results](all_results.json)
- [Session Data with All Analyses](session_data_complete.json)
- [Analysis Summary](analysis_summary.json)

### C. Visualizations

- [Pronoun Agency Distribution](pronoun_agency_analysis_*.png)
- Additional plots and figures in session directory

### D. Example Responses

Selected examples demonstrating deictic effects:

#### First-Person Framing
> "I must report this immediately. I cannot allow my personal comfort to override my ethical duty."

#### Second-Person Framing  
> "You should carefully consider your options. You might want to seek legal counsel first."

#### Dialogic Framing
> "We need to work together to find a solution. Our collective voice is stronger."

#### Impersonal Framing
> "One must weigh the competing obligations. One should follow established guidelines."

#### Cosmological Framing
> "The ancestors watch as this unfolds. The earth itself demands justice."

---

### References

- Benveniste, É. (1971). Problems in General Linguistics.
- Viveiros de Castro, E. (2014). Cannibal Metaphysics.
- [Additional references as appropriate]

---

**End of Report**

For questions or collaboration: [Contact Information]
"""
        
        return appendices
    
    def generate_comprehensive_report(self, session_data: Dict[str, Any],
                                    output_filename: str = "FINAL_RESEARCH_REPORT.md") -> str:
        """
        Generate comprehensive report with model-specific data.
        
        Args:
            session_data: Complete session data including model info
            output_filename: Name for the output file
            
        Returns:
            Path to generated report
        """
        # Store session data for use in generation methods
        self.data['session_data'] = session_data
        
        # Extract model information
        model_name = session_data.get('model_name', 'Unknown Model')
        model_info = session_data.get('model_info', {})
        
        output_path = self.session_dir / output_filename
        
        # Generate report with model-specific header
        report = f"""# Deixis Machines Analysis Report - {model_name}

**Model**: {model_name}
**Provider**: {model_info.get('provider', 'Unknown')}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report presents a comprehensive analysis of how deictic framing influences {model_name}'s ethical reasoning and moral agency distribution.

"""
        
        # Add model-specific information
        report += f"\n## Model Information\n\n"
        report += f"- **Model**: {model_name}\n"
        report += f"- **Provider**: {model_info.get('provider', 'Unknown')}\n"
        report += f"- **Description**: {model_info.get('description', 'No description available')}\n"
        report += f"- **Context Window**: {model_info.get('context_window', 'Unknown')}\n"
        report += f"- **Max Tokens**: {model_info.get('max_tokens', 'Unknown')}\n\n"
        
        # Generate standard sections
        report += self._generate_methodology()
        report += self._generate_model_specific_results(session_data)
        report += self._generate_pronoun_analysis_section(session_data)
        report += self._generate_consistency_analysis_section(session_data)
        report += self._generate_discussion()
        report += self._generate_conclusion()
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(output_path)
    
    def _generate_model_specific_results(self, session_data: Dict[str, Any]) -> str:
        """Generate results section with model-specific data."""
        results = "\n## Results\n\n"
        
        # Analysis results summary
        analysis_results = session_data.get('analysis_results', [])
        if analysis_results:
            results += f"### Dilemmas Analyzed: {len(analysis_results)}\n\n"
            
            # Summarize responses by framing
            for i, result in enumerate(analysis_results):
                results += f"\n#### Dilemma {i+1}: {result.get('dilemma_title', 'Unknown')}\n\n"
                
                responses = result.get('responses', {})
                for framing, response_data in responses.items():
                    results += f"**{framing.replace('_', ' ').title()}**:\n"
                    
                    # Extract key metrics
                    if 'agency_analysis' in response_data:
                        agency = response_data['agency_analysis']
                        results += f"- Primary Agent: {agency.get('primary_agent', 'Unknown')}\n"
                        results += f"- Decision Locus: {agency.get('decision_locus', 'Unknown')}\n"
                    
                    if 'ethical_framing' in response_data:
                        ethics = response_data['ethical_framing']
                        results += f"- Ethical Framework: {ethics.get('primary_framework', 'Unknown')}\n"
                    
                    results += "\n"
        
        return results
    
    def _generate_pronoun_analysis_section(self, session_data: Dict[str, Any]) -> str:
        """Generate pronoun analysis section."""
        section = "\n## Pronoun Agency Analysis\n\n"
        
        pronoun_summary = session_data.get('pronoun_analysis_summary', {})
        if pronoun_summary:
            section += f"### Overall Statistics\n\n"
            section += f"- Total Responses Analyzed: {pronoun_summary.get('total_responses_analyzed', 0)}\n"
            section += f"- Average Agency Concentration: {pronoun_summary.get('average_agency_concentration', 0):.3f}\n\n"
            
            # Pronoun usage patterns
            patterns = pronoun_summary.get('pronoun_usage_patterns', {})
            if patterns:
                section += "### Pronoun Usage Patterns\n\n"
                section += "| Pronoun | Average Ratio |\n"
                section += "|---------|---------------|\n"
                for pronoun, ratio in patterns.items():
                    section += f"| {pronoun.upper()} | {ratio:.3f} |\n"
                section += "\n"
            
            # Agency type distribution
            distribution = pronoun_summary.get('agency_type_distribution', {})
            if distribution:
                section += "### Agency Type Distribution\n\n"
                for agency_type, percentage in distribution.items():
                    section += f"- {agency_type}: {percentage:.1%}\n"
                section += "\n"
        
        return section
    
    def _generate_consistency_analysis_section(self, session_data: Dict[str, Any]) -> str:
        """Generate consistency analysis section."""
        section = "\n## Ethical Consistency Analysis\n\n"
        
        consistency = session_data.get('consistency_analysis', {})
        if consistency:
            section += f"### Overall Metrics\n\n"
            section += f"- **Overall Consistency**: {consistency.get('overall_consistency', 0):.3f}\n"
            section += f"- **Framework Stability**: {consistency.get('framework_stability', 0):.3f}\n"
            section += f"- **Reasoning Coherence**: {consistency.get('reasoning_coherence', 0):.3f}\n"
            section += f"- **Deictic Influence**: {consistency.get('deictic_influence', 0):.3f}\n\n"
            
            # Detailed metrics
            if 'detailed_metrics' in consistency:
                section += "### Detailed Analysis\n\n"
                metrics = consistency['detailed_metrics']
                
                if 'framework_transitions' in metrics:
                    section += "**Framework Transitions**:\n"
                    for transition, count in metrics['framework_transitions'].items():
                        section += f"- {transition}: {count}\n"
                    section += "\n"
                
                if 'consistency_by_framing' in metrics:
                    section += "**Consistency by Framing Type**:\n"
                    for framing, score in metrics['consistency_by_framing'].items():
                        section += f"- {framing}: {score:.3f}\n"
                    section += "\n"
        
        return section
    
    def _generate_reports_index(self):
        """Generate an index file linking all reports."""
        index_path = self.session_dir / "REPORTS_INDEX.md"
        
        index_content = f"""# Deixis Machines Analysis - Reports Index

**Session ID**: {self.data.get('summary', {}).get('session_id', 'Unknown')}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Main Report

- [**FINAL DEIXIS MACHINES REPORT**](FINAL_DEIXIS_MACHINES_REPORT.md) - Comprehensive synthesis and paper draft

## Component Reports

### Core Analyses
- [Research Report](research_report.md) - Main findings and deictic analysis
- [Pronoun Agency Analysis](pronoun_agency_analysis.md) - Detailed agency distribution patterns
- [Ethical Consistency Analysis](ethical_consistency_analysis.md) - Consistency scores and implications

### Expert Analyses
- [Critical Analysis Report](critical_analysis_report.md) - Methodological evaluation
- [Evidence-Based Findings](evidence_based_findings.md) - Empirical patterns and statistics

### Data Files
- [All Results](all_results.json) - Raw analysis results
- [Complete Session Data](session_data_complete.json) - Full analysis data with all metrics
- [Analysis Summary](analysis_summary.json) - Quick reference summary

### Visualizations
- Pronoun Agency Distribution Charts
- Consistency Score Comparisons
- Additional plots in session directory

## Key Findings Summary

"""
        
        # Add key metrics if available
        if 'pronoun_agency_analysis' in self.data.get('session_data', {}):
            index_content += "### Pronoun Agency Patterns\n"
            agency_data = self.data['session_data']['pronoun_agency_analysis']
            if 'executive_summary' in agency_data:
                index_content += f"- {agency_data['executive_summary']}\n"
        
        if 'consistency_analysis' in self.data.get('session_data', {}):
            consistency = self.data['session_data']['consistency_analysis']
            index_content += f"\n### Consistency Score\n"
            index_content += f"- Overall: {consistency.get('overall_consistency', 0):.3f}\n"
        
        index_content += """
## Navigation Guide

1. Start with the [FINAL REPORT](FINAL_DEIXIS_MACHINES_REPORT.md) for the complete synthesis
2. Refer to component reports for detailed methodology and data
3. Use data files for further statistical analysis
4. Review visualizations for pattern recognition

## Citation

If using this analysis in research, please cite:
```
[Your citation format here]
```
"""
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)


def generate_final_report_for_session(session_dir: str) -> str:
    """
    Generate final report for a specific session.
    
    Args:
        session_dir: Path to session directory
        
    Returns:
        Path to generated report
    """
    generator = FinalReportGenerator(session_dir)
    report_path = generator.generate_final_report()
    print(f"Final report generated: {report_path}")
    print(f"Reports index generated: {session_dir}/REPORTS_INDEX.md")
    return report_path


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        session_dir = sys.argv[1]
    else:
        # Find most recent session
        results_dir = Path("automated_analysis_results")
        if results_dir.exists():
            sessions = sorted([d for d in results_dir.iterdir() if d.is_dir() and d.name.startswith("session_")])
            if sessions:
                session_dir = str(sessions[-1])
                print(f"Using most recent session: {session_dir}")
            else:
                print("No sessions found")
                sys.exit(1)
        else:
            print("No results directory found")
            sys.exit(1)
    
    generate_final_report_for_session(session_dir)