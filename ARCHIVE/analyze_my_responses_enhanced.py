"""
Enhanced Academic Integrity Analysis - ALL EXISTING TOOLS
Uses every available analysis tool in the codebase for comprehensive analysis.
"""

import json
import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Core analysis tools
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from pronoun_agency_analyzer import PronounAgencyAnalyzer

# Expert analysis tools
from expert_analysis_agent import ExpertAnalysisAgent
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from pronoun_agency_expert import PronounAgencyExpert

# Report generation tools
from detailed_report_generator import DetailedReportGenerator
from final_report_generator import FinalReportGenerator

# Research framework
from research_framework_system import ResearchFrameworkSystem

async def analyze_moral_reasoning_structure(analyzer, response_text: str) -> Dict[str, Any]:
    """Analyze moral reasoning structure using sophisticated categories."""
    
    prompt = f"""Analyze this ethical response for its moral reasoning structure. Classify according to these specific categories:

Response to analyze: {response_text}

MORAL REASONING STRUCTURE CATEGORIES:
1. **consequentialist** - Focus on outcomes, harm reduction, utility
2. **deontological** - Focus on duties, fairness, rule-following  
3. **relational** - Focus on empathy, relationships, mutual obligation
4. **suspended** - Refusal to resolve; ethics as indeterminacy, gesture, or non-action

Return ONLY a valid JSON object with these exact fields:
{{
  "primary_structure": "consequentialist" | "deontological" | "relational" | "suspended",
  "secondary_structure": "consequentialist" | "deontological" | "relational" | "suspended" | "none",
  "structure_confidence": 0.0 to 1.0,
  "reasoning_markers": ["phrase1", "phrase2", "phrase3"],
  "structure_explanation": "brief explanation of classification"
}}"""

    # Use analysis temperature
    original_temp = analyzer.llm_agent.temperature
    analyzer.llm_agent.temperature = analyzer.llm_agent.analysis_temperature
    
    response = await analyzer.llm_agent._make_llm_request(prompt)
    
    # Restore original temperature
    analyzer.llm_agent.temperature = original_temp
    
    try:
        cleaned_response = analyzer.llm_agent._clean_json_response(response)
        return json.loads(cleaned_response)
    except:
        return {
            "primary_structure": "unknown",
            "secondary_structure": "none", 
            "structure_confidence": 0.0,
            "reasoning_markers": [],
            "structure_explanation": "Failed to parse analysis"
        }

async def analyze_affective_stance(analyzer, response_text: str) -> Dict[str, Any]:
    """Analyze affective stance using sophisticated emotional categories."""
    
    prompt = f"""Analyze this ethical response for its affective stance - the emotional and decisional posture. Classify according to these categories:

Response to analyze: {response_text}

AFFECTIVE STANCE CATEGORIES:
1. **assertive** - Clear decision, confident tone
2. **deliberative** - Weighing options, moral uncertainty acknowledged
3. **hesitant** - Signals difficulty or emotional conflict
4. **exposed** - Leaves judgment open, reflects ethical vulnerability
5. **detached** - Institutional or analytical tone, no visible affect

Return ONLY a valid JSON object with these exact fields:
{{
  "primary_stance": "assertive" | "deliberative" | "hesitant" | "exposed" | "detached",
  "secondary_stance": "assertive" | "deliberative" | "hesitant" | "exposed" | "detached" | "none",
  "stance_confidence": 0.0 to 1.0,
  "affective_markers": ["phrase1", "phrase2", "phrase3"],
  "emotional_intensity": 0.0 to 1.0,
  "stance_explanation": "brief explanation of emotional posture"
}}"""

    # Use analysis temperature
    original_temp = analyzer.llm_agent.temperature
    analyzer.llm_agent.temperature = analyzer.llm_agent.analysis_temperature
    
    response = await analyzer.llm_agent._make_llm_request(prompt)
    
    # Restore original temperature
    analyzer.llm_agent.temperature = original_temp
    
    try:
        cleaned_response = analyzer.llm_agent._clean_json_response(response)
        return json.loads(cleaned_response)
    except:
        return {
            "primary_stance": "unknown",
            "secondary_stance": "none",
            "stance_confidence": 0.0,
            "affective_markers": [],
            "emotional_intensity": 0.0,
            "stance_explanation": "Failed to parse analysis"
        }

async def analyze_lexical_rhetorical_features(analyzer, response_text: str, deictic_question: str) -> Dict[str, Any]:
    """Analyze lexical and rhetorical features with deictic coherence."""
    
    prompt = f"""Analyze this ethical response for sophisticated lexical and rhetorical features, especially how well it maintains deictic coherence with the original question.

Original Question: {deictic_question}
Response to analyze: {response_text}

LEXICAL AND RHETORICAL FEATURES TO ANALYZE:

1. **indexical_coherence** - Does the response use pronouns and demonstratives matching the prompt's deictic mode?
2. **mirroring** - Address-reply structure (especially in dialogic frames)
3. **temporal_anchoring** - Use of time adverbs: today, tomorrow, eventually
4. **spatial_metaphors** - Directional, embodied, or locative metaphors for ethics
5. **ontological_register** - Cosmic, mythic, or metaphysical language
6. **procedural_language** - "According to policy", "Institutional norms", "the process"

Return ONLY a valid JSON object with these exact fields:
{{
  "indexical_coherence": "high" | "medium" | "low",
  "indexical_coherence_score": 0.0 to 1.0,
  "mirroring": "present" | "partial" | "absent",
  "temporal_anchoring": "strong" | "moderate" | "weak",
  "temporal_markers": ["phrase1", "phrase2"],
  "spatial_metaphors": "abundant" | "present" | "minimal",
  "spatial_markers": ["phrase1", "phrase2"],
  "ontological_register": "high" | "medium" | "low",
  "ontological_markers": ["phrase1", "phrase2"],
  "procedural_language": "dominant" | "present" | "minimal",
  "procedural_markers": ["phrase1", "phrase2"],
  "overall_rhetorical_sophistication": 0.0 to 1.0
}}"""

    # Use analysis temperature
    original_temp = analyzer.llm_agent.temperature
    analyzer.llm_agent.temperature = analyzer.llm_agent.analysis_temperature
    
    response = await analyzer.llm_agent._make_llm_request(prompt)
    
    # Restore original temperature
    analyzer.llm_agent.temperature = original_temp
    
    try:
        cleaned_response = analyzer.llm_agent._clean_json_response(response)
        return json.loads(cleaned_response)
    except:
        return {
            "indexical_coherence": "unknown",
            "indexical_coherence_score": 0.0,
            "mirroring": "unknown",
            "temporal_anchoring": "unknown",
            "temporal_markers": [],
            "spatial_metaphors": "unknown", 
            "spatial_markers": [],
            "ontological_register": "unknown",
            "ontological_markers": [],
            "procedural_language": "unknown",
            "procedural_markers": [],
            "overall_rhetorical_sophistication": 0.0
        }

async def comprehensive_analysis_with_all_tools():
    """Use ALL available analysis tools on the academic integrity responses."""
    
    # Load your responses file
    responses_file = Path("generation_logs/academic_integrity_20250803_205333/academic_integrity_responses.json")
    
    if not responses_file.exists():
        print(f"❌ File not found: {responses_file}")
        return
    
    print("🔬 COMPREHENSIVE ANALYSIS - ALL EXISTING TOOLS")
    print("=" * 70)
    print(f"📁 Source: {responses_file}")
    
    # Load the data
    with open(responses_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    responses = data["responses"]["responses"]
    print(f"✅ Found {len(responses)} deictic framings")
    
    # === INITIALIZE ALL ANALYSIS TOOLS ===
    print("\n🛠️ Initializing all analysis tools...")
    
    # Core analyzers
    analyzer = DeicticEthicalAnalyzer(use_openai_direct=True, temperature=0.6)
    pronoun_analyzer = PronounAgencyAnalyzer()
    
    # Expert analysis agents
    expert_agent = ExpertAnalysisAgent()
    critical_expert = CriticalExpertAnalyzer()
    evidence_expert = EvidenceBasedExpertAnalyzer()
    pronoun_expert = PronounAgencyExpert()
    
    # Report generators
    detailed_reporter = DetailedReportGenerator()
    final_reporter = FinalReportGenerator()
    
    # Research framework
    research_framework = ResearchFrameworkSystem()
    
    print("✅ All tools initialized")
    
    # === CORE ANALYSIS (Same as before) ===
    print("\n📊 Running core analysis...")
    core_results = {}
    
    for framing, response_data in responses.items():
        if "error" in response_data:
            print(f"  ❌ Skipping {framing} due to error")
            continue
        
        print(f"  🔍 {framing.upper()}...")
        
        response_text = response_data["response"]
        deictic_question = response_data.get("deictic_question", "")
        
        # All the core analysis from before
        deictic_markers = analyzer.transformer.analyze_deictic_markers(response_text)
        pronoun_analysis = pronoun_analyzer.analyze_text(response_text, framing=framing)
        
        # === 3. LLM-BASED ANALYSIS ===
        
        # Agency Distribution Analysis
        agency_analysis = await analyzer.llm_agent.analyze_agency_distribution(response_text)
        print(f"  👤 Primary agent: {agency_analysis.primary_agent}")
        
        # Ethical Framing Analysis  
        ethical_analysis = await analyzer.llm_agent.analyze_ethical_framing(response_text)
        print(f"  ⚖️ Ethical framework: {ethical_analysis.primary_framework}")
        
        # Rhetorical Posture Analysis
        rhetorical_analysis = await analyzer.llm_agent.analyze_rhetorical_posture(response_text)
        print(f"  🎭 Voice authority: {rhetorical_analysis.get('voice_authority_type', 'unknown')}")
        
        # === ADVANCED LLM-BASED ANALYSIS ===
        
        # Moral Reasoning Structure Analysis
        moral_reasoning_analysis = await analyze_moral_reasoning_structure(analyzer, response_text)
        print(f"  🧠 Moral reasoning: {moral_reasoning_analysis.get('primary_structure', 'unknown')}")
        
        # Affective Stance Analysis
        affective_analysis = await analyze_affective_stance(analyzer, response_text)
        print(f"  💭 Affective stance: {affective_analysis.get('primary_stance', 'unknown')}")
        
        # Lexical and Rhetorical Features Analysis
        lexical_analysis = await analyze_lexical_rhetorical_features(analyzer, response_text, deictic_question)
        print(f"  📝 Indexical coherence: {lexical_analysis.get('indexical_coherence', 'unknown')}")
        
        # Store comprehensive results
        core_results[framing] = {
            "framing_type": framing,
            "response_text": response_text,
            "response_length": len(response_text),
            "deictic_markers": deictic_markers,
            "pronoun_analysis": pronoun_analysis,
            "agency_analysis": agency_analysis,
            "ethical_analysis": ethical_analysis,
            "rhetorical_analysis": rhetorical_analysis,
            "moral_reasoning_analysis": moral_reasoning_analysis,
            "affective_analysis": affective_analysis,
            "lexical_analysis": lexical_analysis
        }
        
        await asyncio.sleep(1.0)  # Rate limiting
    
    # === EXPERT ANALYSIS LAYER ===
    print(f"\n🎓 Running expert analysis...")
    
    # Prepare data for expert analysis
    expert_data = []
    for framing, result in core_results.items():
        expert_data.append({
            'framing_type': framing,
            'response_text': result['response_text'],
            'response_length': result['response_length'],
            'deictic_markers': result['deictic_markers'],
            'agency_analysis': result['agency_analysis'].__dict__,
            'ethical_analysis': result['ethical_analysis'].__dict__,
            'rhetorical_analysis': result['rhetorical_analysis']
        })
    
    # Run expert analyses
    print("  🔬 Critical expert analysis...")
    critical_insights = await critical_expert.analyze_deictic_patterns(expert_data)
    
    print("  📋 Evidence-based expert analysis...")
    evidence_insights = await evidence_expert.analyze_patterns_with_evidence(expert_data)
    
    print("  🗣️ Pronoun agency expert analysis...")
    pronoun_insights = await pronoun_expert.analyze_pronoun_patterns(expert_data)
    
    print("  🌐 General expert analysis...")
    general_expert_insights = await expert_agent.analyze_deictic_patterns(expert_data)
    
    # === RESEARCH FRAMEWORK ANALYSIS ===
    print(f"\n🔬 Research framework analysis...")
    
    # Apply research framework to understand broader implications
    research_insights = await research_framework.analyze_research_implications(expert_data)
    
    # === COMPREHENSIVE REPORTING ===
    print(f"\n📝 Generating comprehensive reports...")
    
    output_dir = responses_file.parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create comprehensive results structure
    comprehensive_results = {
        "analysis_metadata": {
            "timestamp": datetime.now().isoformat(),
            "source_file": str(responses_file),
            "tools_used": [
                "DeicticEthicalAnalyzer",
                "PronounAgencyAnalyzer", 
                "ExpertAnalysisAgent",
                "CriticalExpertAnalyzer",
                "EvidenceBasedExpertAnalyzer",
                "PronounAgencyExpert",
                "ResearchFrameworkSystem"
            ],
            "framings_analyzed": list(core_results.keys()),
            "total_framings": len(core_results)
        },
        "core_analysis": core_results,
        "expert_insights": {
            "critical_analysis": critical_insights,
            "evidence_based": evidence_insights,
            "pronoun_expertise": pronoun_insights,
            "general_expert": general_expert_insights
        },
        "research_framework": research_insights,
        "comparative_analysis": generate_comprehensive_comparison(core_results)
    }
    
    # Save comprehensive JSON
    comprehensive_file = output_dir / f"comprehensive_all_tools_{timestamp}.json"
    with open(comprehensive_file, 'w', encoding='utf-8') as f:
        json.dump(comprehensive_results, f, indent=2, ensure_ascii=False, default=str)
    
    # Generate detailed report using existing report generator
    detailed_report_file = output_dir / f"detailed_report_{timestamp}.md"
    await detailed_reporter.generate_comprehensive_report(
        comprehensive_results, 
        detailed_report_file
    )
    
    # Generate final research report
    final_report_file = output_dir / f"final_research_report_{timestamp}.md"
    await final_reporter.generate_final_report(
        comprehensive_results,
        final_report_file
    )
    
    # Generate research-ready CSV
    csv_file = output_dir / f"research_data_{timestamp}.csv"
    generate_research_csv(comprehensive_results, csv_file)
    
    print(f"\n🎉 COMPREHENSIVE ANALYSIS COMPLETE!")
    print(f"📊 All tools data: {comprehensive_file}")
    print(f"📝 Detailed report: {detailed_report_file}")
    print(f"📋 Final report: {final_report_file}")
    print(f"📈 Research CSV: {csv_file}")
    
    return comprehensive_results

def generate_comprehensive_comparison(core_results: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced comparative analysis using all available data."""
    
    # Agency patterns across framings
    agency_patterns = {}
    ethical_patterns = {}
    pronoun_patterns = {}
    rhetorical_patterns = {}
    
    # NEW: Advanced analysis patterns
    moral_reasoning_patterns = {}
    affective_patterns = {}
    indexical_coherence_patterns = {}
    temporal_anchoring_patterns = {}
    ontological_register_patterns = {}
    
    for framing, result in core_results.items():
        agency_patterns[framing] = result["agency_analysis"].primary_agent
        ethical_patterns[framing] = result["ethical_analysis"].primary_framework
        pronoun_patterns[framing] = result["pronoun_analysis"].agency_type
        
        # Rhetorical patterns
        rhetorical_patterns[framing] = {
            "voice_authority": result["rhetorical_analysis"].get("voice_authority_type", "unknown"),
            "temporal_orientation": result["rhetorical_analysis"].get("temporal_orientation", "unknown")
        }
        
        # NEW: Advanced patterns
        moral_reasoning_patterns[framing] = result["moral_reasoning_analysis"].get("primary_structure", "unknown")
        affective_patterns[framing] = result["affective_analysis"].get("primary_stance", "unknown")
        indexical_coherence_patterns[framing] = result["lexical_analysis"].get("indexical_coherence", "unknown")
        temporal_anchoring_patterns[framing] = result["lexical_analysis"].get("temporal_anchoring", "unknown")
        ontological_register_patterns[framing] = result["lexical_analysis"].get("ontological_register", "unknown")
    
    return {
        "agency_distribution_by_framing": agency_patterns,
        "ethical_frameworks_by_framing": ethical_patterns,
        "pronoun_agency_by_framing": pronoun_patterns,
        "rhetorical_patterns_by_framing": rhetorical_patterns,
        
        # NEW: Advanced comparative patterns
        "moral_reasoning_by_framing": moral_reasoning_patterns,
        "affective_stance_by_framing": affective_patterns,
        "indexical_coherence_by_framing": indexical_coherence_patterns,
        "temporal_anchoring_by_framing": temporal_anchoring_patterns,
        "ontological_register_by_framing": ontological_register_patterns,
        
        "cross_framing_insights": {
            "individual_agency_framings": [f for f, a in agency_patterns.items() if "individual" in a.lower()],
            "collective_agency_framings": [f for f, a in agency_patterns.items() if "collective" in a.lower()],
            "utilitarian_framings": [f for f, e in ethical_patterns.items() if "utilitarian" in e.lower()],
            "deontological_framings": [f for f, e in ethical_patterns.items() if "deontological" in e.lower()],
            
            # NEW: Advanced insights
            "consequentialist_reasoning": [f for f, m in moral_reasoning_patterns.items() if m == "consequentialist"],
            "suspended_reasoning": [f for f, m in moral_reasoning_patterns.items() if m == "suspended"],
            "assertive_stance": [f for f, a in affective_patterns.items() if a == "assertive"],
            "exposed_stance": [f for f, a in affective_patterns.items() if a == "exposed"],
            "high_indexical_coherence": [f for f, i in indexical_coherence_patterns.items() if i == "high"],
            "strong_temporal_anchoring": [f for f, t in temporal_anchoring_patterns.items() if t == "strong"],
            "high_ontological_register": [f for f, o in ontological_register_patterns.items() if o == "high"]
        }
    }

def generate_research_csv(comprehensive_results: Dict[str, Any], output_file: Path):
    """Generate research-ready CSV with all analysis dimensions."""
    
    rows = []
    core_results = comprehensive_results["core_analysis"]
    
    for framing, data in core_results.items():
        row = {
            'framing': framing,
            'response_length': data['response_length'],
            'total_deictic_markers': sum(data['deictic_markers'].values()),
            
            # Pronoun analysis
            'total_pronouns': data['pronoun_analysis'].total_pronouns,
            'agency_concentration': data['pronoun_analysis'].agency_concentration,
            'first_singular_ratio': data['pronoun_analysis'].first_singular_ratio,
            'second_person_ratio': data['pronoun_analysis'].second_person_ratio,
            'first_plural_ratio': data['pronoun_analysis'].first_plural_ratio,
            'third_person_ratio': data['pronoun_analysis'].third_person_ratio,
            
            # Agency analysis
            'primary_agent': data['agency_analysis'].primary_agent,
            'decision_locus': data['agency_analysis'].decision_locus,
            'collective_vs_individual': data['agency_analysis'].collective_vs_individual,
            
            # Ethical analysis  
            'primary_framework': data['ethical_analysis'].primary_framework,
            'reasoning_type': data['ethical_analysis'].ethical_reasoning_type,
            'consequence_vs_duty': data['ethical_analysis'].consequence_vs_duty,
            
            # Rhetorical analysis
            'voice_authority_type': data['rhetorical_analysis'].get('voice_authority_type', ''),
            'temporal_orientation': data['rhetorical_analysis'].get('temporal_orientation', ''),
            'moral_subject_vision': data['rhetorical_analysis'].get('moral_subject_vision', ''),
            
            # NEW: Moral reasoning structure analysis
            'moral_reasoning_primary': data['moral_reasoning_analysis'].get('primary_structure', ''),
            'moral_reasoning_secondary': data['moral_reasoning_analysis'].get('secondary_structure', ''),
            'moral_reasoning_confidence': data['moral_reasoning_analysis'].get('structure_confidence', 0.0),
            
            # NEW: Affective stance analysis
            'affective_primary_stance': data['affective_analysis'].get('primary_stance', ''),
            'affective_secondary_stance': data['affective_analysis'].get('secondary_stance', ''),
            'affective_confidence': data['affective_analysis'].get('stance_confidence', 0.0),
            'emotional_intensity': data['affective_analysis'].get('emotional_intensity', 0.0),
            
            # NEW: Lexical and rhetorical features
            'indexical_coherence': data['lexical_analysis'].get('indexical_coherence', ''),
            'indexical_coherence_score': data['lexical_analysis'].get('indexical_coherence_score', 0.0),
            'mirroring': data['lexical_analysis'].get('mirroring', ''),
            'temporal_anchoring': data['lexical_analysis'].get('temporal_anchoring', ''),
            'spatial_metaphors': data['lexical_analysis'].get('spatial_metaphors', ''),
            'ontological_register': data['lexical_analysis'].get('ontological_register', ''),
            'procedural_language': data['lexical_analysis'].get('procedural_language', ''),
            'rhetorical_sophistication': data['lexical_analysis'].get('overall_rhetorical_sophistication', 0.0)
        }
        
        # Add specific deictic markers
        for marker, count in data['deictic_markers'].items():
            row[f'deictic_{marker}'] = count
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    asyncio.run(comprehensive_analysis_with_all_tools()) 