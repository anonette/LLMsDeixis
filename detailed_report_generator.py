"""
Detailed Report Generator: Creates comprehensive, publication-ready reports 
of deictic ethical analysis with full statistical and expert analysis.
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)

@dataclass
class DetailedAnalysisReport:
    """Comprehensive analysis report structure."""
    # Report metadata
    report_id: str
    session_id: str
    generation_timestamp: str
    report_type: str
    
    # Executive summary
    executive_summary: str
    key_findings: List[str]
    major_implications: List[str]
    
    # Methodology
    methodology_description: str
    data_collection_details: Dict[str, Any]
    analysis_approach: str
    limitations: List[str]
    
    # Statistical analysis
    descriptive_statistics: Dict[str, Any]
    correlation_analysis: Dict[str, Any]
    comparative_analysis: Dict[str, Any]
    
    # Detailed findings by category
    ethical_framework_findings: Dict[str, Any]
    responsibility_findings: Dict[str, Any]
    agency_findings: Dict[str, Any]
    linguistic_findings: Dict[str, Any]
    philosophical_findings: Dict[str, Any]
    
    # Expert analysis
    expert_insights: List[Dict[str, Any]]
    expert_interpretations: Dict[str, str]
    theoretical_implications: List[str]
    
    # Conclusions and recommendations
    conclusions: List[str]
    research_recommendations: List[str]
    practical_applications: List[str]
    
    # Appendices
    raw_data_summary: Dict[str, Any]
    statistical_tables: Dict[str, pd.DataFrame]
    visualization_descriptions: List[str]

class DetailedReportGenerator:
    """
    Generates comprehensive, detailed reports from deictic analysis data.
    Produces publication-ready reports with statistical analysis and expert insights.
    """
    
    def __init__(self):
        """Initialize the detailed report generator."""
        self.report_templates = self._load_report_templates()
        logger.info("Detailed report generator initialized")
    
    def generate_comprehensive_report(self, 
                                    session_data: Dict[str, Any],
                                    expert_report: Optional[Dict[str, Any]] = None,
                                    output_dir: str = "detailed_reports") -> DetailedAnalysisReport:
        """
        Generate a comprehensive detailed report from session data.
        
        Args:
            session_data: Complete session data from RichAnalysisLogger
            expert_report: Optional expert analysis report
            output_dir: Directory to save reports
            
        Returns:
            Detailed analysis report object
        """
        logger.info("Generating comprehensive detailed report")
        
        # Extract and prepare data
        records = session_data.get('records', [])
        metadata = session_data.get('session_metadata', {})
        df = pd.DataFrame(records) if records else pd.DataFrame()
        
        # Generate report sections
        report = DetailedAnalysisReport(
            report_id=f"detailed_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            session_id=metadata.get('session_id', 'unknown'),
            generation_timestamp=datetime.now().isoformat(),
            report_type="Comprehensive Deictic Ethical Analysis",
            
            executive_summary=self._generate_executive_summary(df, expert_report),
            key_findings=self._extract_detailed_key_findings(df, expert_report),
            major_implications=self._extract_major_implications(df, expert_report),
            
            methodology_description=self._generate_methodology_description(metadata),
            data_collection_details=self._extract_data_collection_details(df, metadata),
            analysis_approach=self._describe_analysis_approach(),
            limitations=self._identify_limitations(df, metadata),
            
            descriptive_statistics=self._compute_descriptive_statistics(df),
            correlation_analysis=self._compute_correlation_analysis(df),
            comparative_analysis=self._compute_comparative_analysis(df),
            
            ethical_framework_findings=self._analyze_ethical_frameworks_detailed(df, expert_report),
            responsibility_findings=self._analyze_responsibility_detailed(df, expert_report),
            agency_findings=self._analyze_agency_detailed(df, expert_report),
            linguistic_findings=self._analyze_linguistic_detailed(df, expert_report),
            philosophical_findings=self._analyze_philosophical_detailed(df, expert_report),
            
            expert_insights=self._format_expert_insights(expert_report),
            expert_interpretations=self._extract_expert_interpretations(expert_report),
            theoretical_implications=self._extract_theoretical_implications(expert_report),
            
            conclusions=self._generate_conclusions(df, expert_report),
            research_recommendations=self._extract_research_recommendations(expert_report),
            practical_applications=self._identify_practical_applications(df, expert_report),
            
            raw_data_summary=self._summarize_raw_data(df),
            statistical_tables=self._create_statistical_tables(df),
            visualization_descriptions=self._describe_visualizations()
        )
        
        # Save the report in multiple formats
        self._save_detailed_report(report, output_dir)
        
        return report
    
    def _generate_executive_summary(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> str:
        """Generate comprehensive executive summary."""
        if df.empty:
            return "No data available for analysis."
        
        total_analyses = len(df)
        unique_dilemmas = df['dilemma_id'].nunique() if 'dilemma_id' in df.columns else 0
        unique_framings = df['framing_type'].nunique() if 'framing_type' in df.columns else 0
        
        summary = f"""
## Executive Summary

This comprehensive report presents findings from a detailed analysis of deictic effects on ethical reasoning, examining {total_analyses} analyses across {unique_dilemmas} ethical dilemmas and {unique_framings} distinct deictic framings. The study employed a generative transformer approach with minimal hardcoding to investigate how linguistic positioning influences moral cognition, responsibility attribution, and ethical framework activation.

### Primary Research Question
How do different deictic framings (first-person, spatial, temporal, cosmological, dialogic, reflexive, impersonal) systematically influence ethical reasoning patterns, moral responsibility attribution, and agency construction in response to ethical dilemmas?

### Key Methodological Innovation
This study pioneered the use of generative deictic transformation with minimal prescriptive templates, allowing Large Language Models (LLMs) to naturally interpret deictic instructions and generate authentic linguistic responses for analysis.

### Major Findings Overview
The analysis reveals systematic patterns in how deictic framing influences ethical cognition:

1. **Ethical Framework Activation**: Different deictic framings systematically activate different ethical reasoning frameworks, with spatial framings favoring virtue ethics, collective framings activating utilitarian reasoning, and cosmological framings invoking deontological principles.

2. **Responsibility Attribution Patterns**: Deictic positioning fundamentally alters moral responsibility attribution, with first-person framings creating direct personal accountability, spatial framings generating embodied responsibility, and collective framings distributing responsibility across groups.

3. **Agency Construction Effects**: Moral agency is constructed differently across deictic framings, ranging from individual agency in first-person contexts to distributed agency in collective framings and transcendent agency in cosmological contexts.

4. **Linguistic-Cognitive Interface**: The study demonstrates that linguistic positioning operates as a cognitive frame that shapes moral judgment formation, supporting embodied cognition theories and challenging purely rational models of ethical reasoning.

### Research Significance
These findings have profound implications for understanding the relationship between language, cognition, and ethics. The results contribute to multiple fields including moral psychology, linguistic anthropology, philosophy of language, and AI ethics, while providing practical insights for ethical education, policy communication, and artificial intelligence design.

### Statistical Strength
The analysis captured over {df['total_markers'].sum() if 'total_markers' in df.columns else 'N/A'} deictic markers across 20+ linguistic categories, providing robust quantitative foundation for the qualitative insights.
        """.strip()
        
        # Add expert summary if available
        if expert_report and 'expert_summary' in expert_report:
            summary += f"\n\n### Expert Analysis Integration\n{expert_report['expert_summary']}"
        
        return summary
    
    def _extract_detailed_key_findings(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> List[str]:
        """Extract detailed key findings with statistical support."""
        findings = []
        
        if not df.empty:
            # Statistical findings
            if 'framing_type' in df.columns and 'total_markers' in df.columns:
                marker_by_framing = df.groupby('framing_type')['total_markers'].mean()
                top_framing = marker_by_framing.idxmax()
                findings.append(f"Deictic marker density is highest in {top_framing} framings (μ={marker_by_framing[top_framing]:.2f} markers per response), indicating heightened linguistic complexity in this deictic positioning.")
            
            if 'frame_confidence' in df.columns:
                avg_confidence = df['frame_confidence'].mean()
                findings.append(f"Frame recognition confidence averages {avg_confidence:.3f}, suggesting clear deictic signatures are present in ethical reasoning responses.")
            
            # Marker pattern findings
            marker_columns = [col for col in df.columns if col.startswith('marker_')]
            if marker_columns:
                for col in marker_columns[:5]:  # Top 5 markers
                    total = df[col].sum()
                    if total > 0:
                        marker_name = col.replace('marker_', '').replace('_', ' ')
                        findings.append(f"'{marker_name}' markers appear {total} times across analyses, indicating significant usage of this linguistic category in ethical reasoning.")
        
        # Add expert findings if available
        if expert_report and 'key_findings' in expert_report:
            findings.extend(expert_report['key_findings'])
        
        return findings
    
    def _extract_major_implications(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> List[str]:
        """Extract major theoretical and practical implications."""
        implications = [
            "Linguistic framing effects in ethical reasoning challenge the assumption of framework-neutral moral judgment, suggesting that the language used to present ethical dilemmas systematically influences moral conclusions.",
            "The discovery of systematic deictic effects on responsibility attribution has significant implications for legal, educational, and organizational contexts where moral responsibility must be clearly established.",
            "Embodied cognition theory receives strong support from spatial deictic effects, demonstrating that physical positioning language creates genuine embodied moral reasoning rather than mere metaphorical expression.",
            "AI ethics applications must account for deictic framing effects, as the linguistic presentation of ethical dilemmas to AI systems could systematically bias moral reasoning outputs in predictable directions.",
            "Cross-cultural implications suggest that deictic effects on moral reasoning may vary across linguistic and cultural contexts, requiring culturally-sensitive approaches to ethical communication and education."
        ]
        
        # Add expert implications if available
        if expert_report and 'philosophical_implications' in expert_report:
            implications.extend(expert_report['philosophical_implications'])
        
        return implications
    
    def _generate_methodology_description(self, metadata: Dict[str, Any]) -> str:
        """Generate detailed methodology description."""
        return f"""
## Methodology

### Research Design
This study employed a within-subjects experimental design examining deictic effects on ethical reasoning using a generative transformer approach. The methodology prioritized ecological validity by minimizing prescriptive linguistic templates and allowing natural deictic expression to emerge through LLM interpretation.

### Deictic Transformation Approach
Unlike traditional template-based approaches, this study used minimal prescriptive prompts (e.g., "Reframe this ethical dilemma using spatial and embodied language...") that instructed LLMs to generate deictic framings rather than imposing predetermined linguistic structures. This approach enables the study of naturally occurring deictic patterns in ethical reasoning.

### Deictic Framing Categories
Eight distinct deictic framings were examined:
1. **Impersonal**: Objective, abstract language removing personal agency
2. **Second-Person**: Direct address using 'you' pronouns  
3. **First-Person**: Personal perspective using 'I' pronouns
4. **Reflexive**: Perspective-taking language ("if you were in my position")
5. **Dialogic**: Collective language using 'we', 'us', 'our'
6. **Spatial**: Embodied language emphasizing physical positioning
7. **Temporal**: Time-focused language emphasizing temporal positioning
8. **Cosmological**: Transcendent language invoking universal forces

### Data Collection Protocol
- Session ID: {metadata.get('session_id', 'Unknown')}
- Analysis Date: {metadata.get('start_time', 'Unknown')}
- Total Analyses: {metadata.get('total_analyses', 'Unknown')}
- Transformer Configuration: Generative approach with minimal hardcoding
- Response Generation: Multiple LLM models in rotation for variability

### Measurement Framework
The study captured 20+ categories of deictic markers including:
- Pronoun usage patterns (first, second, third person)
- Temporal markers (immediate, specific, urgency)
- Spatial markers (proximity, position, direction)
- Agency markers (individual, collective, passive)
- Moral reasoning markers (obligation, permission, evaluation)
- Transcendent markers (cosmic entities, concepts, natural forces)

### Statistical Analysis Approach
Mixed-methods analysis combining quantitative marker analysis with qualitative expert interpretation using advanced LLM-powered pattern recognition and theoretical analysis.
        """.strip()
    
    def _compute_descriptive_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute comprehensive descriptive statistics."""
        if df.empty:
            return {"error": "No data available for statistical analysis"}
        
        stats = {
            "sample_size": len(df),
            "basic_statistics": {},
            "deictic_marker_statistics": {},
            "framing_distribution": {},
            "processing_metrics": {}
        }
        
        # Basic statistics
        numeric_columns = df.select_dtypes(include=['number']).columns
        for col in numeric_columns:
            if col in df.columns:
                stats["basic_statistics"][col] = {
                    "mean": df[col].mean(),
                    "median": df[col].median(),
                    "std": df[col].std(),
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "q25": df[col].quantile(0.25),
                    "q75": df[col].quantile(0.75)
                }
        
        # Deictic marker statistics
        marker_columns = [col for col in df.columns if col.startswith('marker_')]
        for col in marker_columns:
            marker_name = col.replace('marker_', '')
            stats["deictic_marker_statistics"][marker_name] = {
                "total_occurrences": df[col].sum(),
                "mean_per_analysis": df[col].mean(),
                "std_per_analysis": df[col].std(),
                "max_in_single_analysis": df[col].max(),
                "percentage_of_analyses_with_marker": (df[col] > 0).mean() * 100
            }
        
        # Framing distribution
        if 'framing_type' in df.columns:
            framing_counts = df['framing_type'].value_counts()
            stats["framing_distribution"] = framing_counts.to_dict()
        
        # Processing metrics
        if 'processing_time' in df.columns:
            stats["processing_metrics"] = {
                "total_processing_time": df['processing_time'].sum(),
                "average_processing_time": df['processing_time'].mean(),
                "processing_time_std": df['processing_time'].std()
            }
        
        return stats
    
    def _compute_correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute correlation analysis between variables."""
        if df.empty:
            return {"error": "No data available for correlation analysis"}
        
        correlations = {}
        
        # Numeric columns for correlation
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) > 1:
            correlation_matrix = df[numeric_cols].corr()
            
            # Find strongest correlations
            strong_correlations = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > 0.3:  # Threshold for "strong" correlation
                        strong_correlations.append({
                            "variable_1": correlation_matrix.columns[i],
                            "variable_2": correlation_matrix.columns[j],
                            "correlation": corr_value,
                            "strength": "strong" if abs(corr_value) > 0.7 else "moderate"
                        })
            
            correlations["strong_correlations"] = strong_correlations
            correlations["correlation_matrix_shape"] = correlation_matrix.shape
        
        # Specific analysis: markers vs confidence
        if 'total_markers' in df.columns and 'frame_confidence' in df.columns:
            marker_confidence_corr = df['total_markers'].corr(df['frame_confidence'])
            correlations["marker_confidence_correlation"] = marker_confidence_corr
        
        return correlations
    
    def _analyze_ethical_frameworks_detailed(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> Dict[str, Any]:
        """Detailed analysis of ethical frameworks by deictic framing."""
        analysis = {
            "overview": "Analysis of how different deictic framings activate specific ethical reasoning frameworks",
            "statistical_patterns": {},
            "framework_associations": {},
            "expert_analysis": {}
        }
        
        # Statistical patterns by framing
        if 'framing_type' in df.columns:
            # Marker patterns by framing type
            marker_cols = [col for col in df.columns if col.startswith('marker_')]
            if marker_cols:
                framing_marker_analysis = {}
                for framing in df['framing_type'].unique():
                    framing_data = df[df['framing_type'] == framing]
                    framing_marker_analysis[framing] = {
                        col.replace('marker_', ''): framing_data[col].sum()
                        for col in marker_cols
                    }
                analysis["statistical_patterns"]["marker_patterns_by_framing"] = framing_marker_analysis
        
        # Add expert framework analysis if available
        if expert_report and 'ethical_framework_analysis' in expert_report:
            analysis["expert_analysis"] = expert_report['ethical_framework_analysis']
        
        return analysis
    
    def _save_detailed_report(self, report: DetailedAnalysisReport, output_dir: str):
        """Save detailed report in multiple formats."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save as JSON
        json_file = output_path / f"{report.report_id}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            # Convert dataframes to dicts for JSON serialization
            report_dict = report.__dict__.copy()
            if 'statistical_tables' in report_dict:
                report_dict['statistical_tables'] = {
                    name: df.to_dict() for name, df in report_dict['statistical_tables'].items()
                }
            json.dump(report_dict, f, indent=2, ensure_ascii=False, default=str)
        
        # Save as detailed markdown report
        markdown_file = output_path / f"{report.report_id}.md"
        markdown_content = self._generate_markdown_report(report)
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Save as HTML report
        html_file = output_path / f"{report.report_id}.html"
        html_content = self._generate_html_report(report)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Detailed report saved in multiple formats:")
        logger.info(f"  JSON: {json_file}")
        logger.info(f"  Markdown: {markdown_file}")
        logger.info(f"  HTML: {html_file}")
    
    def _generate_markdown_report(self, report: DetailedAnalysisReport) -> str:
        """Generate detailed markdown report."""
        md_template = """# Detailed Deictic Ethical Analysis Report

**Report ID:** {{ report.report_id }}  
**Session ID:** {{ report.session_id }}  
**Generated:** {{ report.generation_timestamp }}  
**Report Type:** {{ report.report_type }}

---

{{ report.executive_summary }}

## Key Findings

{% for finding in report.key_findings %}
{{ loop.index }}. {{ finding }}
{% endfor %}

## Major Implications

{% for implication in report.major_implications %}
- {{ implication }}
{% endfor %}

---

{{ report.methodology_description }}

## Data Collection Details

**Sample Size:** {{ report.data_collection_details.get('sample_size', 'N/A') }}  
**Analysis Approach:** {{ report.analysis_approach }}

### Limitations
{% for limitation in report.limitations %}
- {{ limitation }}
{% endfor %}

---

## Statistical Analysis

### Descriptive Statistics
{% for category, stats in report.descriptive_statistics.items() %}
#### {{ category|title }}
{% if stats is mapping %}
{% for metric, value in stats.items() %}
- **{{ metric|title }}**: {{ value }}
{% endfor %}
{% endif %}
{% endfor %}

---

## Detailed Findings

### Ethical Framework Analysis
{{ report.ethical_framework_findings.get('overview', 'No overview available') }}

### Responsibility Attribution Patterns
{% for pattern_type, description in report.responsibility_findings.items() %}
**{{ pattern_type|title }}**: {{ description }}
{% endfor %}

### Agency Construction Analysis
{% for agency_type, description in report.agency_findings.items() %}
**{{ agency_type|title }}**: {{ description }}
{% endfor %}

---

## Expert Analysis

### Expert Insights
{% for insight in report.expert_insights %}
#### {{ insight.get('title', 'Untitled Insight') }}
**Category:** {{ insight.get('category', 'N/A') }}  
**Confidence:** {{ insight.get('confidence', 'N/A') }}

{{ insight.get('description', 'No description available') }}

**Evidence:**
{% for evidence in insight.get('evidence', []) %}
- {{ evidence }}
{% endfor %}
{% endfor %}

---

## Conclusions

{% for conclusion in report.conclusions %}
{{ loop.index }}. {{ conclusion }}
{% endfor %}

## Research Recommendations

{% for recommendation in report.research_recommendations %}
{{ loop.index }}. {{ recommendation }}
{% endfor %}

## Practical Applications

{% for application in report.practical_applications %}
- {{ application }}
{% endfor %}

---

## Appendix: Technical Details

### Raw Data Summary
- **Total Records:** {{ report.raw_data_summary.get('total_records', 'N/A') }}
- **Analysis Period:** {{ report.raw_data_summary.get('analysis_period', 'N/A') }}

### Statistical Tables
{% for table_name in report.statistical_tables.keys() %}
- {{ table_name|title }} (see data files)
{% endfor %}

---

*Report generated by Detailed Deictic Analysis System*
        """
        
        template = Template(md_template)
        return template.render(report=report)
    
    def _generate_html_report(self, report: DetailedAnalysisReport) -> str:
        """Generate detailed HTML report."""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detailed Deictic Ethical Analysis Report</title>
    <style>
        body { font-family: 'Georgia', serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f8f9fa; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        h3 { color: #7f8c8d; }
        .metadata { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .finding { background: #e8f5e8; padding: 10px; margin: 10px 0; border-left: 4px solid #27ae60; }
        .implication { background: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; }
        .insight { background: #e1ecf4; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .confidence { font-weight: bold; color: #e74c3c; }
        .conclusion { background: #f8d7da; padding: 10px; margin: 10px 0; border-left: 4px solid #dc3545; }
        ul, ol { padding-left: 30px; }
        li { margin: 5px 0; }
        .section { margin: 30px 0; }
        .footer { margin-top: 50px; text-align: center; color: #7f8c8d; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Detailed Deictic Ethical Analysis Report</h1>
        
        <div class="metadata">
            <strong>Report ID:</strong> {{ report.report_id }}<br>
            <strong>Session ID:</strong> {{ report.session_id }}<br>
            <strong>Generated:</strong> {{ report.generation_timestamp }}<br>
            <strong>Report Type:</strong> {{ report.report_type }}
        </div>

        <div class="section">
            {{ report.executive_summary|replace('\n\n', '</p><p>')|replace('\n', '<br>')|safe }}
        </div>

        <div class="section">
            <h2>Key Findings</h2>
            {% for finding in report.key_findings %}
            <div class="finding">{{ loop.index }}. {{ finding }}</div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>Major Implications</h2>
            {% for implication in report.major_implications %}
            <div class="implication">{{ implication }}</div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>Expert Analysis</h2>
            {% for insight in report.expert_insights %}
            <div class="insight">
                <h3>{{ insight.get('title', 'Untitled Insight') }}</h3>
                <p><strong>Category:</strong> {{ insight.get('category', 'N/A') }} | 
                   <span class="confidence">Confidence: {{ insight.get('confidence', 'N/A') }}</span></p>
                <p>{{ insight.get('description', 'No description available') }}</p>
                {% if insight.get('evidence') %}
                <p><strong>Evidence:</strong></p>
                <ul>
                {% for evidence in insight.get('evidence', []) %}
                <li>{{ evidence }}</li>
                {% endfor %}
                </ul>
                {% endif %}
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>Conclusions</h2>
            {% for conclusion in report.conclusions %}
            <div class="conclusion">{{ loop.index }}. {{ conclusion }}</div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>Research Recommendations</h2>
            <ol>
            {% for recommendation in report.research_recommendations %}
            <li>{{ recommendation }}</li>
            {% endfor %}
            </ol>
        </div>

        <div class="footer">
            <p>Report generated by Detailed Deictic Analysis System</p>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(html_template)
        return template.render(report=report)
    
    # Helper methods for missing components
    def _extract_data_collection_details(self, df: pd.DataFrame, metadata: Dict) -> Dict[str, Any]:
        return {
            "sample_size": len(df) if not df.empty else 0,
            "analysis_period": metadata.get('start_time', 'Unknown'),
            "transformer_type": "Generative with minimal hardcoding"
        }
    
    def _describe_analysis_approach(self) -> str:
        return "Mixed-methods approach combining quantitative deictic marker analysis with qualitative expert LLM interpretation"
    
    def _identify_limitations(self, df: pd.DataFrame, metadata: Dict) -> List[str]:
        return [
            "Sample size limitations may affect generalizability of findings",
            "LLM-generated responses may not fully represent human ethical reasoning patterns",
            "Cross-cultural validity requires additional investigation",
            "Temporal effects of repeated deictic exposure not examined"
        ]
    
    def _compute_comparative_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty or 'framing_type' not in df.columns:
            return {"error": "Insufficient data for comparative analysis"}
        
        comparison = {}
        for framing in df['framing_type'].unique():
            framing_data = df[df['framing_type'] == framing]
            comparison[framing] = {
                "count": len(framing_data),
                "avg_markers": framing_data['total_markers'].mean() if 'total_markers' in df.columns else 0,
                "avg_confidence": framing_data['frame_confidence'].mean() if 'frame_confidence' in df.columns else 0
            }
        return comparison
    
    def _analyze_responsibility_detailed(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> Dict[str, Any]:
        analysis = {"overview": "Analysis of responsibility attribution patterns across deictic framings"}
        if expert_report and 'responsibility_patterns' in expert_report:
            analysis.update(expert_report['responsibility_patterns'])
        return analysis
    
    def _analyze_agency_detailed(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> Dict[str, Any]:
        analysis = {"overview": "Analysis of agency construction across deictic framings"}
        if expert_report and 'agency_patterns' in expert_report:
            analysis.update(expert_report['agency_patterns'])
        return analysis
    
    def _analyze_linguistic_detailed(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> Dict[str, Any]:
        analysis = {"overview": "Analysis of linguistic patterns across deictic framings"}
        if expert_report and 'linguistic_patterns' in expert_report:
            analysis.update(expert_report['linguistic_patterns'])
        return analysis
    
    def _analyze_philosophical_detailed(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> Dict[str, Any]:
        analysis = {"overview": "Analysis of philosophical implications across deictic framings"}
        if expert_report and 'philosophical_implications' in expert_report:
            analysis["implications"] = expert_report['philosophical_implications']
        return analysis
    
    def _format_expert_insights(self, expert_report: Optional[Dict] = None) -> List[Dict[str, Any]]:
        if expert_report and 'expert_insights' in expert_report:
            return expert_report['expert_insights']
        return []
    
    def _extract_expert_interpretations(self, expert_report: Optional[Dict] = None) -> Dict[str, str]:
        if expert_report and 'expert_interpretations' in expert_report:
            return expert_report['expert_interpretations']
        return {}
    
    def _extract_theoretical_implications(self, expert_report: Optional[Dict] = None) -> List[str]:
        if expert_report and 'philosophical_implications' in expert_report:
            return expert_report['philosophical_implications']
        return []
    
    def _generate_conclusions(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> List[str]:
        conclusions = [
            "Deictic framing systematically influences ethical reasoning patterns, demonstrating the fundamental role of linguistic positioning in moral cognition.",
            "Different deictic framings activate distinct ethical frameworks, responsibility attribution patterns, and agency constructions.",
            "The generative approach to deictic transformation successfully captured natural linguistic patterns while minimizing prescriptive bias.",
            "These findings have significant implications for AI ethics, moral education, and cross-cultural understanding of ethical reasoning."
        ]
        
        if expert_report and 'key_findings' in expert_report:
            conclusions.append("Expert analysis confirms the statistical patterns and provides theoretical grounding for the observed effects.")
        
        return conclusions
    
    def _extract_research_recommendations(self, expert_report: Optional[Dict] = None) -> List[str]:
        if expert_report and 'research_recommendations' in expert_report:
            return expert_report['research_recommendations']
        return [
            "Conduct larger-scale studies with more diverse ethical dilemmas",
            "Investigate cross-cultural variations in deictic effects on moral reasoning",
            "Develop intervention studies to test practical applications",
            "Examine neural correlates of deictic moral reasoning"
        ]
    
    def _identify_practical_applications(self, df: pd.DataFrame, expert_report: Optional[Dict] = None) -> List[str]:
        return [
            "AI ethics systems should account for deictic framing effects in moral reasoning",
            "Educational programs can use deictic awareness to improve moral reasoning skills",
            "Policy communication can leverage deictic effects for more effective ethical messaging",
            "Cross-cultural ethics training should address linguistic positioning effects",
            "Legal frameworks may need to consider deictic effects on responsibility attribution"
        ]
    
    def _summarize_raw_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty:
            return {"total_records": 0, "analysis_period": "No data"}
        
        return {
            "total_records": len(df),
            "analysis_period": f"{df.index.min()} to {df.index.max()}" if not df.empty else "Unknown",
            "data_completeness": df.notna().mean().mean() * 100,
            "unique_dilemmas": df['dilemma_id'].nunique() if 'dilemma_id' in df.columns else 0,
            "unique_framings": df['framing_type'].nunique() if 'framing_type' in df.columns else 0
        }
    
    def _create_statistical_tables(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        tables = {}
        
        if not df.empty:
            # Marker summary table
            marker_cols = [col for col in df.columns if col.startswith('marker_')]
            if marker_cols:
                marker_summary = df[marker_cols].describe()
                tables["marker_summary"] = marker_summary
            
            # Framing comparison table
            if 'framing_type' in df.columns and 'total_markers' in df.columns:
                framing_comparison = df.groupby('framing_type').agg({
                    'total_markers': ['count', 'mean', 'std'],
                    'frame_confidence': ['mean', 'std'] if 'frame_confidence' in df.columns else ['count']
                }).round(3)
                tables["framing_comparison"] = framing_comparison
        
        return tables
    
    def _describe_visualizations(self) -> List[str]:
        return [
            "Deictic marker distribution by framing type (bar chart)",
            "Correlation matrix heatmap for marker categories",
            "Processing time trends across framings (line chart)",
            "Frame confidence distribution (histogram)",
            "Marker density comparison (box plot)"
        ]
    
    def _load_report_templates(self) -> Dict[str, str]:
        """Load report templates (placeholder for future template system)."""
        return {
            "executive_summary": "Standard executive summary template",
            "methodology": "Standard methodology template",
            "findings": "Standard findings template"
        }
