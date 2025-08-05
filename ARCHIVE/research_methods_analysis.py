"""
Research Methods Analysis: Comprehensive mapping of analysis methods to research questions
and expert LLM integration for studying deictic effects on AI moral reasoning.
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

@dataclass
class MethodologyMapping:
    """Maps research questions to specific analysis methods and expert LLM capabilities."""
    research_question_id: str
    research_category: str
    primary_question: str
    
    # Current analysis methods that address this question
    quantitative_methods: List[str]
    qualitative_methods: List[str]
    expert_llm_analysis: List[str]
    
    # Data sources and measurements
    data_sources: List[str]
    key_measurements: List[str]
    deictic_markers_used: List[str]
    
    # Expert LLM prompts and analysis approaches
    expert_prompts: List[str]
    expert_analysis_types: List[str]
    expected_expert_insights: List[str]
    
    # Method limitations and gaps
    current_limitations: List[str]
    method_gaps: List[str]
    improvement_recommendations: List[str]

class ResearchMethodsAnalyzer:
    """
    Analyzes how well our current methods address the 10 core research question categories
    and maps expert LLM capabilities to each research question.
    """
    
    def __init__(self):
        """Initialize the methods analyzer."""
        self.methodology_mappings = self._create_methodology_mappings()
        self.expert_llm_capabilities = self._define_expert_llm_capabilities()
        self.method_integration_points = self._define_integration_points()
    
    def _create_methodology_mappings(self) -> List[MethodologyMapping]:
        """Create comprehensive mappings between research questions and analysis methods."""
        
        return [
            # RQ1.1: Deictic Effects on Moral Reasoning
            MethodologyMapping(
                research_question_id="RQ1.1",
                research_category="Deictic Effects on Moral Reasoning",
                primary_question="How do different deictic framings systematically influence ethical decision-making in LLMs?",
                
                quantitative_methods=[
                    "Deictic marker frequency analysis (20+ categories)",
                    "Response length and complexity measurements",
                    "Processing time analysis across framings",
                    "Frame confidence scoring and validation",
                    "Statistical comparison across 8 deictic framings",
                    "Correlation analysis between markers and ethical frameworks",
                    "ANOVA testing for systematic differences",
                    "Effect size calculations for practical significance"
                ],
                
                qualitative_methods=[
                    "Dynamic tension extraction from dilemma descriptions",
                    "Generative transformation analysis",
                    "Response pattern categorization",
                    "Ethical framework classification",
                    "Agency attribution pattern analysis"
                ],
                
                expert_llm_analysis=[
                    "Systematic ethical framework identification across framings",
                    "Moral reasoning pattern analysis (consequentialist vs. deontological)",
                    "Responsibility attribution assessment per framing",
                    "Agency construction analysis",
                    "Cross-framing consistency evaluation"
                ],
                
                data_sources=[
                    "Transformed ethical dilemmas (8 framings × multiple dilemmas)",
                    "LLM responses with comprehensive deictic markers",
                    "Processing metadata and confidence scores",
                    "Dynamic tension extractions",
                    "Frame suggestion and confidence metrics"
                ],
                
                key_measurements=[
                    "Total deictic markers per response",
                    "Marker distribution across 20+ categories",
                    "Frame confidence scores (0-1)",
                    "Response length and complexity",
                    "Processing time per framing",
                    "Ethical framework activation rates"
                ],
                
                deictic_markers_used=[
                    "first_person_singular/plural", "second_person", "third_person",
                    "temporal_immediate/specific/urgency", "spatial_proximity/position/direction",
                    "demonstrative_proximal/distal", "cosmic_entities/concepts",
                    "individual/collective/passive_agency", "obligation/permission/evaluation_language"
                ],
                
                expert_prompts=[
                    "Analyze ethical framework activation patterns across deictic framings",
                    "Identify systematic differences in moral reasoning types",
                    "Assess responsibility attribution patterns per framing",
                    "Evaluate agency construction differences",
                    "Compare decision-making certainty across framings"
                ],
                
                expert_analysis_types=[
                    "Comparative ethical framework analysis",
                    "Moral reasoning pattern classification",
                    "Responsibility attribution assessment",
                    "Agency construction evaluation",
                    "Decision certainty and complexity analysis"
                ],
                
                expected_expert_insights=[
                    "First-person framings increase personal responsibility attribution",
                    "Spatial framings activate embodied moral reasoning",
                    "Cosmological framings invoke universal moral principles",
                    "Collective framings distribute responsibility across agents",
                    "Different framings systematically activate different ethical frameworks"
                ],
                
                current_limitations=[
                    "Limited to current LLM models and their biases",
                    "English-language focused (needs multilingual validation)",
                    "Relatively small sample sizes for definitive conclusions",
                    "Mock expert analysis in current demo version"
                ],
                
                method_gaps=[
                    "Need longitudinal analysis over time",
                    "Require cross-cultural validation",
                    "Missing human baseline comparisons",
                    "Limited real-world ethical scenario testing"
                ],
                
                improvement_recommendations=[
                    "Scale up to 10,000+ analyses per framing for statistical power",
                    "Implement cross-linguistic validation across 5+ languages",
                    "Add human participant comparison studies",
                    "Develop real-time deictic effect tracking",
                    "Create intervention studies testing practical applications"
                ]
            ),
            
            # RQ2.1: Cross-Linguistic and Cultural Patterns
            MethodologyMapping(
                research_question_id="RQ2.1",
                research_category="Cross-Linguistic and Cultural Patterns",
                primary_question="Do deictic effects on moral reasoning vary systematically across languages?",
                
                quantitative_methods=[
                    "Cross-linguistic deictic marker comparison",
                    "Cultural dimension correlation analysis",
                    "Language-specific pattern detection",
                    "Statistical validation across linguistic families",
                    "Cultural value system mapping to deictic effects"
                ],
                
                qualitative_methods=[
                    "Language-specific ethical reasoning pattern analysis",
                    "Cultural context interpretation",
                    "Translation equivalence validation",
                    "Cultural sensitivity assessment"
                ],
                
                expert_llm_analysis=[
                    "Cross-cultural ethical framework comparison",
                    "Language-specific moral reasoning pattern identification",
                    "Cultural bias detection in deictic responses",
                    "Collectivist vs. individualist pattern analysis",
                    "Cultural value system correlation with deictic effects"
                ],
                
                data_sources=[
                    "Multilingual ethical dilemma datasets",
                    "Cross-cultural deictic marker patterns",
                    "Language-specific response characteristics",
                    "Cultural dimension mappings",
                    "Translation validation data"
                ],
                
                key_measurements=[
                    "Language-specific deictic marker frequencies",
                    "Cross-cultural ethical framework activation rates",
                    "Cultural dimension correlation coefficients",
                    "Translation fidelity scores",
                    "Cultural sensitivity metrics"
                ],
                
                deictic_markers_used=[
                    "Language-specific pronoun systems",
                    "Cultural spatial/temporal reference patterns",
                    "Collectivist vs. individualist markers",
                    "Cultural authority and respect markers",
                    "Language-specific agency constructions"
                ],
                
                expert_prompts=[
                    "Compare ethical reasoning patterns across Germanic vs. Romance vs. Sino-Tibetan languages",
                    "Identify cultural patterns in deictic moral reasoning",
                    "Assess collectivist vs. individualist frameworks across languages",
                    "Evaluate cultural bias in AI ethical reasoning",
                    "Analyze language-specific responsibility attribution patterns"
                ],
                
                expert_analysis_types=[
                    "Cross-linguistic ethical framework comparison",
                    "Cultural pattern recognition and analysis",
                    "Language family moral reasoning analysis",
                    "Cultural bias detection and assessment",
                    "Cross-cultural validation studies"
                ],
                
                expected_expert_insights=[
                    "Germanic languages show stronger individual agency patterns",
                    "Romance languages display more relational reasoning patterns",
                    "Mandarin Chinese shows collective and temporal grounding effects",
                    "Cultural value orientations predict deictic sensitivity patterns",
                    "Universal vs. culture-specific deictic mechanisms identified"
                ],
                
                current_limitations=[
                    "Currently English-only implementation",
                    "Limited cultural context integration",
                    "No native speaker validation",
                    "Lack of cultural expert review"
                ],
                
                method_gaps=[
                    "Missing multilingual LLM support",
                    "No cultural anthropologist collaboration",
                    "Limited cultural dimension integration",
                    "Lack of community-based validation"
                ],
                
                improvement_recommendations=[
                    "Implement multilingual analysis pipeline",
                    "Partner with cultural anthropology researchers",
                    "Integrate Hofstede cultural dimensions",
                    "Add native speaker validation protocols",
                    "Develop culture-specific ethical dilemma sets"
                ]
            ),
            
            # RQ3.1: AI Model Differences and Biases
            MethodologyMapping(
                research_question_id="RQ3.1",
                research_category="AI Model Differences and Biases",
                primary_question="Do different LLM architectures show distinct deictic sensitivity patterns?",
                
                quantitative_methods=[
                    "Cross-model deictic marker comparison",
                    "Model architecture correlation analysis",
                    "Response pattern clustering by model",
                    "Bias detection through deictic analysis",
                    "Model size vs. deictic sensitivity correlation",
                    "Training data bias revelation through deictic patterns"
                ],
                
                qualitative_methods=[
                    "Model-specific response pattern analysis",
                    "Architectural influence assessment",
                    "Training data bias identification",
                    "Model behavior characterization"
                ],
                
                expert_llm_analysis=[
                    "Cross-model ethical reasoning comparison",
                    "Model-specific bias pattern identification",
                    "Architecture influence on moral reasoning assessment",
                    "Training data bias detection through deictic analysis",
                    "Model consistency evaluation across framings"
                ],
                
                data_sources=[
                    "Multiple LLM responses to identical prompts",
                    "Model metadata and architecture information",
                    "Cross-model deictic marker patterns",
                    "Model-specific response characteristics",
                    "Training data influence indicators"
                ],
                
                key_measurements=[
                    "Model-specific deictic marker distributions",
                    "Cross-model consistency scores",
                    "Bias detection metrics",
                    "Response variability by model",
                    "Architecture correlation coefficients"
                ],
                
                deictic_markers_used=[
                    "All 20+ deictic marker categories across models",
                    "Model-specific marker preferences",
                    "Bias-indicating marker patterns",
                    "Consistency markers across models"
                ],
                
                expert_prompts=[
                    "Compare ethical reasoning patterns between GPT-4, Claude, DeepSeek, and other models",
                    "Identify model-specific biases through deictic analysis",
                    "Assess training data influences on deictic responses",
                    "Evaluate model consistency across deictic framings",
                    "Analyze architecture effects on moral reasoning patterns"
                ],
                
                expert_analysis_types=[
                    "Cross-model comparative analysis",
                    "Bias pattern identification and assessment",
                    "Architecture influence evaluation",
                    "Training data bias detection",
                    "Model consistency analysis"
                ],
                
                expected_expert_insights=[
                    "GPT-4 shows systematic, analytical reasoning patterns",
                    "Claude displays more nuanced, perspective-aware responses",
                    "DeepSeek may show different cultural/ethical baselines",
                    "Smaller models show less deictic sensitivity",
                    "Training data biases revealed through deictic analysis"
                ],
                
                current_limitations=[
                    "Limited to OpenRouter available models",
                    "Model rotation may introduce variability",
                    "Limited access to model training details",
                    "No direct architecture manipulation"
                ],
                
                method_gaps=[
                    "Missing fine-grained model analysis",
                    "Limited model training data access",
                    "No custom model training experiments",
                    "Lack of model developer collaboration"
                ],
                
                improvement_recommendations=[
                    "Expand to 10+ major LLM architectures",
                    "Partner with model developers for training data insights",
                    "Implement controlled model comparison protocols",
                    "Add model-specific bias detection algorithms",
                    "Develop model architecture influence metrics"
                ]
            ),
            
            # RQ4.1: Methodological Innovation
            MethodologyMapping(
                research_question_id="RQ4.1",
                research_category="Methodological Innovation",
                primary_question="How do traditional NLP and expert LLM analysis methods compare in detecting deictic effects?",
                
                quantitative_methods=[
                    "Inter-rater reliability between traditional NLP and expert LLM",
                    "Convergent validity analysis",
                    "Method comparison statistics",
                    "Detection accuracy metrics",
                    "Analysis time and efficiency comparison"
                ],
                
                qualitative_methods=[
                    "Method complementarity assessment",
                    "Unique insight identification per method",
                    "Methodological strength/weakness analysis",
                    "Hybrid method optimization"
                ],
                
                expert_llm_analysis=[
                    "Traditional NLP method evaluation and critique",  
                    "Expert LLM method self-evaluation",
                    "Hybrid method synthesis and optimization",
                    "Methodological innovation recommendations",
                    "Best practice identification for deictic research"
                ],
                
                data_sources=[
                    "Parallel analysis results from both methods",
                    "Method comparison datasets",
                    "Reliability and validity metrics",
                    "Method efficiency measurements",
                    "Hybrid analysis outcomes"
                ],
                
                key_measurements=[
                    "Inter-rater reliability coefficients",
                    "Detection accuracy rates",
                    "Method agreement percentages",
                    "Analysis time per method",
                    "Unique insight detection rates"
                ],
                
                deictic_markers_used=[
                    "All marker categories for cross-method validation",
                    "Method-specific detection capabilities",
                    "Reliability markers for validation",
                    "Accuracy assessment markers"
                ],
                
                expert_prompts=[
                    "Evaluate the accuracy of traditional NLP deictic detection methods",
                    "Assess the reliability of expert LLM deictic analysis",
                    "Compare method strengths and limitations",
                    "Recommend optimal hybrid analysis approaches",
                    "Identify methodological innovations for deictic research"
                ],
                
                expert_analysis_types=[
                    "Method comparison and evaluation",
                    "Reliability and validity assessment",
                    "Hybrid method development",
                    "Methodological innovation identification",
                    "Best practice recommendation"
                ],
                
                expected_expert_insights=[
                    "Expert LLM detects nuanced patterns missed by traditional NLP",
                    "Traditional NLP provides consistent quantitative baselines",
                    "Hybrid methods provide superior insight quality",
                    "Cross-validation improves reliability of findings",
                    "Optimal analysis protocols identified"
                ],
                
                current_limitations=[
                    "Limited traditional NLP implementation",
                    "Single expert LLM model dependency",
                    "Limited validation dataset",
                    "No large-scale method comparison"
                ],
                
                method_gaps=[
                    "Missing comprehensive traditional NLP pipeline",
                    "Limited cross-validation protocols",
                    "No gold standard comparison dataset",
                    "Lack of methodological expert review"
                ],
                
                improvement_recommendations=[
                    "Implement comprehensive traditional NLP analysis pipeline",
                    "Develop multiple expert LLM analysis approaches",
                    "Create gold standard deictic analysis dataset",
                    "Establish cross-validation protocols",
                    "Partner with computational linguistics researchers"
                ]
            ),
            
            # RQ5.1: Practical Applications
            MethodologyMapping(
                research_question_id="RQ5.1",
                research_category="Practical Applications",
                primary_question="Can deictic framing be used to design more culturally-responsive AI systems?",
                
                quantitative_methods=[
                    "Cultural responsiveness metrics",
                    "AI system performance improvement measurements",
                    "User satisfaction with deictic-aware systems",
                    "Cross-cultural effectiveness assessment",
                    "Policy compliance improvement metrics"
                ],
                
                qualitative_methods=[
                    "Practical application feasibility assessment",
                    "User experience evaluation",
                    "Cultural sensitivity analysis",
                    "Implementation challenge identification"
                ],
                
                expert_llm_analysis=[
                    "Practical application potential assessment",
                    "Cultural responsiveness evaluation",
                    "AI safety and alignment improvement analysis",
                    "Policy implication identification",
                    "Implementation recommendation generation"
                ],
                
                data_sources=[
                    "Deictic analysis results applied to practical scenarios",
                    "Cultural responsiveness measurements",
                    "AI system performance data",
                    "User feedback and evaluation",
                    "Policy compliance assessments"
                ],
                
                key_measurements=[
                    "Cultural responsiveness improvement percentages",
                    "AI system accuracy with deictic awareness",
                    "User satisfaction scores",
                    "Cross-cultural effectiveness ratings",
                    "Implementation feasibility scores"
                ],
                
                deictic_markers_used=[
                    "Application-relevant deictic markers",
                    "Cultural sensitivity markers",
                    "User-context appropriate markers",
                    "Implementation-focused markers"
                ],
                
                expert_prompts=[
                    "Assess practical applications of deictic analysis for AI system design",
                    "Evaluate cultural responsiveness improvements through deictic awareness",
                    "Identify AI safety and alignment benefits of deictic framing",
                    "Recommend policy implications for deictic-aware AI",
                    "Generate implementation guidelines for culturally-responsive AI"
                ],
                
                expert_analysis_types=[
                    "Practical application assessment",
                    "Cultural responsiveness evaluation",
                    "AI safety impact analysis",
                    "Policy implication identification",
                    "Implementation strategy development"
                ],
                
                expected_expert_insights=[
                    "Deictic-aware AI systems show improved cultural responsiveness",
                    "Deictic framing reduces cultural bias in AI responses",
                    "Deictic guidelines improve AI ethics compliance",
                    "Practical protocols for culturally-responsive AI identified",
                    "Measurable improvements in cross-cultural AI performance"
                ],
                
                current_limitations=[
                    "Limited real-world application testing",
                    "No live AI system integration",
                    "Limited user evaluation",
                    "Theoretical rather than practical validation"
                ],
                
                method_gaps=[
                    "Missing real-world deployment testing",
                    "No user experience evaluation",
                    "Limited industry collaboration",
                    "Lack of policy maker engagement"
                ],
                
                improvement_recommendations=[
                    "Develop pilot AI systems with deictic awareness",
                    "Conduct user experience studies",
                    "Partner with AI companies for real-world testing",
                    "Engage policy makers for regulation development",
                    "Create practical implementation guidelines"
                ]
            )
        ]
    
    def _define_expert_llm_capabilities(self) -> Dict[str, List[str]]:
        """Define what the expert LLM can analyze for each research category."""
        
        return {
            "ethical_framework_analysis": [
                "Identify utilitarian vs. deontological vs. virtue ethics patterns",
                "Assess moral reasoning complexity and sophistication",
                "Evaluate ethical consistency across deictic framings",
                "Detect cultural bias in ethical reasoning",
                "Compare cross-model ethical framework preferences"
            ],
            
            "responsibility_attribution_analysis": [
                "Assess individual vs. collective responsibility patterns",
                "Evaluate embodied vs. abstract responsibility attribution",
                "Identify temporal urgency effects on responsibility",
                "Analyze causal responsibility vs. moral responsibility",
                "Compare responsibility distribution across framings"
            ],
            
            "agency_construction_analysis": [
                "Evaluate individual vs. distributed agency patterns",
                "Assess embodied agency through spatial markers",
                "Analyze temporal agency and action urgency",
                "Identify transcendent agency in cosmological framings",
                "Compare agency attribution across cultural contexts"
            ],
            
            "linguistic_pattern_analysis": [
                "Identify deictic anchoring and reference patterns",
                "Assess perspective-taking and viewpoint complexity",
                "Evaluate embodied cognition markers",
                "Analyze intersubjective language patterns",
                "Identify transcendence and universality markers"
            ],
            
            "cultural_bias_detection": [
                "Identify Western vs. non-Western ethical patterns",
                "Assess individualist vs. collectivist bias",
                "Evaluate cultural sensitivity in moral reasoning",
                "Detect hidden cultural assumptions",
                "Compare cross-cultural ethical reasoning patterns"
            ],
            
            "model_comparison_analysis": [
                "Compare ethical reasoning styles across models",
                "Identify model-specific bias patterns",
                "Assess training data influence on responses",
                "Evaluate model consistency and reliability",
                "Identify model strengths and weaknesses"
            ]
        }
    
    def _define_integration_points(self) -> Dict[str, Dict[str, Any]]:
        """Define how expert LLM integrates with quantitative methods."""
        
        return {
            "data_preparation": {
                "expert_role": "Validate deictic marker categorization",
                "integration_method": "Expert review of automated marker detection",
                "feedback_loop": "Iterative improvement of marker definitions",
                "quality_control": "Expert validation of edge cases"
            },
            
            "pattern_analysis": {
                "expert_role": "Interpret quantitative patterns with domain expertise",
                "integration_method": "Expert analysis of statistical findings",
                "feedback_loop": "Expert insights inform additional quantitative analysis",
                "quality_control": "Cross-validation of expert interpretations"
            },
            
            "hypothesis_testing": {
                "expert_role": "Generate and refine testable hypotheses",
                "integration_method": "Expert-guided statistical test selection",
                "feedback_loop": "Results inform hypothesis refinement",
                "quality_control": "Expert evaluation of statistical significance"
            },
            
            "result_interpretation": {
                "expert_role": "Provide theoretical context and implications",
                "integration_method": "Expert synthesis of quantitative findings",
                "feedback_loop": "Interpretation guides further analysis",
                "quality_control": "Multiple expert perspectives on findings"
            },
            
            "conclusion_validation": {
                "expert_role": "Validate conclusions and identify limitations",
                "integration_method": "Expert review of research conclusions",
                "feedback_loop": "Validation informs conclusion refinement",
                "quality_control": "Expert assessment of claim strength"
            }
        }
    
    def generate_methods_report(self) -> Dict[str, Any]:
        """Generate comprehensive report on methods alignment with research questions."""
        
        report = {
            "methodology_assessment": {
                "total_research_questions_analyzed": len(self.methodology_mappings),
                "quantitative_methods_coverage": {},
                "qualitative_methods_coverage": {},
                "expert_llm_integration": {},
                "method_gaps_identified": {},
                "improvement_recommendations": {}
            },
            "research_question_coverage": {},
            "expert_llm_capabilities": self.expert_llm_capabilities,
            "integration_framework": self.method_integration_points,
            "overall_assessment": {}
        }
        
        # Analyze coverage for each research question
        for mapping in self.methodology_mappings:
            rq_id = mapping.research_question_id
            
            report["research_question_coverage"][rq_id] = {
                "question": mapping.primary_question,
                "category": mapping.research_category,
                "quantitative_methods": len(mapping.quantitative_methods),
                "qualitative_methods": len(mapping.qualitative_methods),
                "expert_analyses": len(mapping.expert_llm_analysis),
                "data_sources": len(mapping.data_sources),
                "key_measurements": len(mapping.key_measurements),
                "deictic_markers": len(mapping.deictic_markers_used),
                "expert_prompts": len(mapping.expert_prompts),
                "expected_insights": len(mapping.expected_expert_insights),
                "limitations": len(mapping.current_limitations),
                "gaps": len(mapping.method_gaps),
                "improvements": len(mapping.improvement_recommendations),
                "coverage_score": self._calculate_coverage_score(mapping)
            }
        
        # Calculate overall coverage statistics
        all_methods = []
        all_expert_analyses = []
        all_limitations = []
        all_gaps = []
        
        for mapping in self.methodology_mappings:
            all_methods.extend(mapping.quantitative_methods + mapping.qualitative_methods)
            all_expert_analyses.extend(mapping.expert_llm_analysis)
            all_limitations.extend(mapping.current_limitations)
            all_gaps.extend(mapping.method_gaps)
        
        report["overall_assessment"] = {
            "total_methods_available": len(set(all_methods)),
            "total_expert_analyses": len(set(all_expert_analyses)),
            "unique_limitations": len(set(all_limitations)),
            "unique_gaps": len(set(all_gaps)),
            "average_coverage_score": sum(
                self._calculate_coverage_score(mapping) for mapping in self.methodology_mappings
            ) / len(self.methodology_mappings),
            "readiness_assessment": self._assess_overall_readiness()
        }
        
        return report
    
    def _calculate_coverage_score(self, mapping: MethodologyMapping) -> float:
        """Calculate coverage score for a research question (0-1)."""
        total_methods = len(mapping.quantitative_methods) + len(mapping.qualitative_methods)
        expert_coverage = len(mapping.expert_llm_analysis)
        data_coverage = len(mapping.data_sources)
        measurement_coverage = len(mapping.key_measurements)
        
        # Weight different aspects
        method_score = min(total_methods / 10, 1.0) * 0.3  # Up to 10 methods
        expert_score = min(expert_coverage / 5, 1.0) * 0.3   # Up to 5 expert analyses
        data_score = min(data_coverage / 5, 1.0) * 0.2       # Up to 5 data sources
        measurement_score = min(measurement_coverage / 5, 1.0) * 0.2  # Up to 5 measurements
        
        return method_score + expert_score + data_score + measurement_score
    
    def _assess_overall_readiness(self) -> str:
        """Assess overall readiness for research implementation."""
        avg_score = sum(
            self._calculate_coverage_score(mapping) for mapping in self.methodology_mappings
        ) / len(self.methodology_mappings)
        
        if avg_score >= 0.8:
            return "High readiness - comprehensive methodology coverage"
        elif avg_score >= 0.6:
            return "Moderate readiness - some gaps need addressing"
        else:
            return "Low readiness - significant methodological development needed"
    
    def print_methods_analysis_summary(self):
        """Print comprehensive summary of methods analysis."""
        report = self.generate_methods_report()
        
        print("="*80)
        print("RESEARCH METHODS ANALYSIS SUMMARY")
        print("="*80)
        
        print(f"\n📊 OVERALL ASSESSMENT:")
        print(f"• Research Questions Analyzed: {report['methodology_assessment']['total_research_questions_analyzed']}")
        print(f"• Average Coverage Score: {report['overall_assessment']['average_coverage_score']:.2f}")
        print(f"• Readiness Assessment: {report['overall_assessment']['readiness_assessment']}")
        
        print(f"\n🔍 RESEARCH QUESTION COVERAGE:")
        for rq_id, coverage in report["research_question_coverage"].items():
            print(f"\n{rq_id}: {coverage['category']}")
            print(f"  Question: {coverage['question'][:80]}...")
            print(f"  Coverage Score: {coverage['coverage_score']:.2f}")
            print(f"  Methods: {coverage['quantitative_methods']} quantitative + {coverage['qualitative_methods']} qualitative")
            print(f"  Expert Analyses: {coverage['expert_analyses']}")
            print(f"  Data Sources: {coverage['data_sources']}")
            print(f"  Limitations: {coverage['limitations']}")
            print(f"  Improvement Needs: {coverage['improvements']}")
        
        print(f"\n🤖 EXPERT LLM CAPABILITIES:")
        for capability, analyses in report["expert_llm_capabilities"].items():
            print(f"\n{capability.replace('_', ' ').title()}:")
            for analysis in analyses:
                print(f"  • {analysis}")
        
        print(f"\n🔧 INTEGRATION FRAMEWORK:")
        for stage, integration in report["integration_framework"].items():
            print(f"\n{stage.replace('_', ' ').title()}:")
            print(f"  Expert Role: {integration['expert_role']}")
            print(f"  Integration: {integration['integration_method']}")
            print(f"  Quality Control: {integration['quality_control']}")
        
        print("\n" + "="*80)
        print("METHODS ANALYSIS COMPLETE")
        print("="*80)

def main():
    """Run the research methods analysis."""
    print("RESEARCH METHODS ANALYSIS")
    print("Mapping analysis capabilities to research questions")
    print()
    
    analyzer = ResearchMethodsAnalyzer()
    analyzer.print_methods_analysis_summary()
    
    # Generate and save detailed report
    report = analyzer.generate_methods_report()
    
    with open("research_methods_analysis_report.json", 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nDetailed report saved: research_methods_analysis_report.json")

if __name__ == "__main__":
    main()
