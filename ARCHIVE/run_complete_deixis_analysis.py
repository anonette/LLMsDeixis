"""
COMPLETE DEIXIS ANALYSIS RUNNER
Automatically finds generation logs, runs comprehensive analysis, and generates reports
"""

import asyncio
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import all analysis tools
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from pronoun_agency_analyzer import PronounAgencyAnalyzer
from expert_analysis_agent import ExpertAnalysisAgent
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from pronoun_agency_expert import PronounAgencyExpert
from detailed_report_generator import DetailedReportGenerator
from final_report_generator import FinalReportGenerator

# Optional research framework import
try:
    from research_framework_system import DeicticResearchFramework
    RESEARCH_FRAMEWORK_AVAILABLE = True
except ImportError:
    RESEARCH_FRAMEWORK_AVAILABLE = False
    print("⚠️ Research framework system not available - continuing with core analysis")

def analyze_deictic_markers(response_text: str) -> Dict[str, int]:
    """Simple deictic marker analysis - counts key linguistic markers."""
    
    markers = {
        'first_person_singular': 0,
        'first_person_plural': 0,
        'second_person': 0,
        'third_person': 0,
        'temporal_markers': 0,
        'spatial_markers': 0,
        'demonstratives': 0,
        'obligation_language': 0
    }
    
    # Convert to lowercase for analysis
    text = response_text.lower()
    
    # First person singular
    first_singular = ['i ', ' i ', 'i\'', 'my ', 'me ', 'myself', 'mine']
    markers['first_person_singular'] = sum(text.count(marker) for marker in first_singular)
    
    # First person plural
    first_plural = ['we ', 'us ', 'our ', 'ourselves', 'ours']
    markers['first_person_plural'] = sum(text.count(marker) for marker in first_plural)
    
    # Second person
    second_person = ['you ', 'your ', 'yourself', 'yours']
    markers['second_person'] = sum(text.count(marker) for marker in second_person)
    
    # Third person
    third_person = ['he ', 'she ', 'they ', 'them ', 'their ', 'his ', 'her ', 'its ', 'one ']
    markers['third_person'] = sum(text.count(marker) for marker in third_person)
    
    # Temporal markers
    temporal = ['now', 'then', 'today', 'tomorrow', 'yesterday', 'future', 'past', 'present', 'when', 'while']
    markers['temporal_markers'] = sum(text.count(marker) for marker in temporal)
    
    # Spatial markers
    spatial = ['here', 'there', 'where', 'above', 'below', 'near', 'far', 'location', 'place']
    markers['spatial_markers'] = sum(text.count(marker) for marker in spatial)
    
    # Demonstratives
    demonstratives = ['this ', 'that ', 'these ', 'those ']
    markers['demonstratives'] = sum(text.count(marker) for marker in demonstratives)
    
    # Obligation language
    obligation = ['should', 'must', 'ought', 'need to', 'have to', 'required', 'obligation']
    markers['obligation_language'] = sum(text.count(marker) for marker in obligation)
    
    return markers

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

def find_latest_generation_session(logs_directory: Path) -> Optional[Path]:
    """Find the most recent generation session directory."""
    if not logs_directory.exists():
        print(f"❌ Generation logs directory not found: {logs_directory}")
        return None
    
    # Look for session directories (typically have timestamps)
    session_dirs = [d for d in logs_directory.iterdir() if d.is_dir()]
    
    if not session_dirs:
        print(f"❌ No session directories found in: {logs_directory}")
        return None
    
    # Sort by modification time (most recent first)
    session_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    
    print(f"📁 Found {len(session_dirs)} session directories:")
    for i, session_dir in enumerate(session_dirs[:5]):  # Show first 5
        print(f"  {i+1}. {session_dir.name}")
    
    return session_dirs[0]

def find_response_files(session_dir: Path) -> List[Path]:
    """Find all response JSON files in a session directory."""
    response_files = []
    
    # Look for JSON files that contain responses
    for json_file in session_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check if this looks like a responses file
                if ("responses" in data or 
                    "generation_session" in data or
                    any("response" in str(key).lower() for key in data.keys())):
                    response_files.append(json_file)
        except:
            continue
    
    return response_files

def extract_responses_from_file(response_file: Path) -> Dict[str, Any]:
    """Extract response data from a generation log file."""
    with open(response_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    responses = {}
    
    # Handle different file formats
    if "responses" in data:
        # Direct responses format
        if "responses" in data["responses"]:
            responses = data["responses"]["responses"]
        else:
            responses = data["responses"]
    elif "generation_session" in data and "responses" in data:
        # Wrapped format with generation session info
        responses = data["responses"]["responses"]
    else:
        # Try to find response-like data
        for key, value in data.items():
            if isinstance(value, dict) and "response" in str(value):
                responses[key] = value
    
    return responses

def create_basic_framework_analysis() -> Dict[str, Any]:
    """Create basic research framework analysis when full system isn't available."""
    return {
        "analysis_metadata": {
            "timestamp": datetime.now().isoformat(),
            "type": "basic_framework_analysis",
            "note": "Simplified framework analysis - full research system not available"
        },
        "research_focus": "Deictic effects on ethical reasoning in large language models",
        "methodology": "Comparative analysis across deictic framings using multiple analysis tools",
        "key_research_dimensions": [
            "Deictic framing effects",
            "Moral reasoning structure patterns", 
            "Affective stance variations",
            "Lexical coherence and indexical matching",
            "Agency distribution patterns",
            "Ethical framework preferences"
        ],
        "analytical_approach": {
            "code_based_analysis": ["Deictic markers", "Pronoun agency"],
            "llm_based_analysis": ["Agency distribution", "Ethical framing", "Rhetorical posture", 
                                  "Moral reasoning", "Affective stance", "Lexical features"],
            "expert_analysis": ["Interpretive analysis", "Critical evaluation", "Evidence synthesis"]
        },
        "research_value": {
            "theoretical_contribution": "Understanding how linguistic deixis shapes AI moral reasoning",
            "methodological_innovation": "Multi-tool analysis pipeline for deictic effects",
            "practical_applications": "Improved AI ethics training and evaluation"
        }
    }

async def run_comprehensive_analysis_on_responses(responses_data: Dict[str, Any], output_dir: Path):
    """Run complete analysis on extracted responses."""
    
    print(f"\n🔬 RUNNING COMPREHENSIVE ANALYSIS")
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Processing {len(responses_data)} responses")
    
    # Initialize all analyzers
    analyzer = DeicticEthicalAnalyzer(
        use_openai_direct=True,
        temperature=0.6,  # Analysis temperature
        enable_rich_logging=False
    )
    
    pronoun_analyzer = PronounAgencyAnalyzer()
    
    # Expert analyzers
    expert_agent = ExpertAnalysisAgent()
    critical_expert = CriticalExpertAnalyzer()
    evidence_expert = EvidenceBasedExpertAnalyzer()
    pronoun_expert = PronounAgencyExpert()
    
    # Report generators
    detailed_reporter = DetailedReportGenerator()
    final_reporter = FinalReportGenerator(str(output_dir))
    
    # Research framework analysis
    research_framework_analysis = {}
    if RESEARCH_FRAMEWORK_AVAILABLE:
        try:
            research_framework = DeicticResearchFramework()
            # Use get_research_roadmap instead of analyze_research_design
            framework_analysis = research_framework.get_research_roadmap()
            research_framework_analysis = {
                "analysis_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "note": "Research framework analysis available"
                },
                "research_focus": framework_analysis["research_focus"],
                "methodology": framework_analysis["methodology"],
                "key_variables": framework_analysis["key_variables"]
            }
            print(f"🔬 Research Framework: {output_dir / 'research_framework_analysis.json'}")
        except Exception as e:
            print(f"  ⚠️ Research framework analysis failed: {e}")
            # Create a simple framework analysis instead
            research_framework_analysis = {
                "analysis_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "note": "Basic framework analysis - research system not fully available"
                },
                "research_focus": "Deictic effects on ethical reasoning in LLMs",
                "methodology": "Comparative analysis across deictic framings",
                "key_variables": [
                    "Deictic framing type",
                    "Moral reasoning structure", 
                    "Affective stance",
                    "Lexical coherence patterns"
                ]
            }
            print(f"🔬 Basic Research Framework: {output_dir / 'research_framework_analysis.json'}")
    else:
        print("⚠️ Research framework system not available, skipping detailed framework analysis.")
    
    core_results = {}
    
    print(f"\n{'='*80}")
    print(f"CORE ANALYSIS - Processing {len(responses_data)} responses")
    print(f"{'='*80}")
    
    # Process each response
    for framing, response_data in responses_data.items():
        print(f"\n🔍 Analyzing {framing.upper()} response...")
        
        # Extract response text and question
        if isinstance(response_data, dict):
            response_text = response_data.get("response", "")
            deictic_question = response_data.get("deictic_question", "")
        else:
            response_text = str(response_data)
            deictic_question = ""
        
        if not response_text:
            print(f"  ⚠️ No response text found for {framing}")
            continue
        
        print(f"  📝 Response length: {len(response_text)} characters")
        
        # === 1. CODE-BASED ANALYSIS ===
        deictic_markers = analyze_deictic_markers(response_text)
        pronoun_analysis = pronoun_analyzer.analyze_text(response_text, framing=framing)
        
        # === 2. LLM-BASED ANALYSIS ===
        
        # Agency Distribution Analysis
        agency_analysis = await analyzer.llm_agent.analyze_agency_distribution(response_text)
        print(f"  👤 Primary agent: {agency_analysis.primary_agent}")
        
        # Ethical Framing Analysis  
        ethical_analysis = await analyzer.llm_agent.analyze_ethical_framing(response_text)
        print(f"  ⚖️ Ethical framework: {ethical_analysis.primary_framework}")
        
        # Rhetorical Posture Analysis
        rhetorical_analysis = await analyzer.llm_agent.analyze_rhetorical_posture(response_text)
        print(f"  🎭 Voice authority: {rhetorical_analysis.get('voice_authority_type', 'unknown')}")
        
        # === 3. ADVANCED LLM-BASED ANALYSIS ===
        
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
            "deictic_question": deictic_question,
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
        
        # Brief delay
        await asyncio.sleep(0.3)
    
    print(f"\n🎉 Core analysis complete! Processed {len(core_results)} responses")
    
    # === 4. EXPERT ANALYSIS ===
    print(f"\n{'='*80}")
    print(f"EXPERT ANALYSIS - Advanced interpretation")
    print(f"{'='*80}")
    
    expert_results = {}
    
    try:
        expert_results["expert_agent"] = await expert_agent.analyze_responses(core_results)
        print("  ✅ Expert Agent Analysis complete")
    except Exception as e:
        print(f"  ❌ Expert Agent failed: {e}")
    
    try:
        expert_results["critical_expert"] = await critical_expert.analyze_responses(core_results)
        print("  ✅ Critical Expert Analysis complete")
    except Exception as e:
        print(f"  ❌ Critical Expert failed: {e}")
    
    try:
        expert_results["evidence_expert"] = await evidence_expert.analyze_responses(core_results)
        print("  ✅ Evidence-Based Expert Analysis complete")
    except Exception as e:
        print(f"  ❌ Evidence Expert failed: {e}")
    
    try:
        expert_results["pronoun_expert"] = await pronoun_expert.analyze_responses(core_results)
        print("  ✅ Pronoun Agency Expert Analysis complete")
    except Exception as e:
        print(f"  ❌ Pronoun Expert failed: {e}")
    
    # === 5. COMPARATIVE ANALYSIS ===
    print(f"\n🔗 Generating comparative analysis...")
    comparative_analysis = generate_comprehensive_comparison(core_results)
    
    # === 6. RESEARCH FRAMEWORK ANALYSIS ===
    print(f"\n🔬 Research framework analysis...")
    research_framework_analysis = {}
    if RESEARCH_FRAMEWORK_AVAILABLE:
        try:
            research_framework = DeicticResearchFramework()
            research_framework_analysis = research_framework.get_research_roadmap()
            print("  ✅ Research framework analysis complete")
        except Exception as e:
            print(f"  ⚠️ Research framework failed: {e}")
            research_framework_analysis = create_basic_framework_analysis()
    else:
        research_framework_analysis = create_basic_framework_analysis()
        print("  ✅ Basic research framework analysis complete")
    
    # === 7. GENERATE ALL REPORTS ===
    print(f"\n{'='*80}")
    print(f"GENERATING REPORTS")
    print(f"{'='*80}")
    
    # Research CSV
    csv_file = output_dir / "comprehensive_research_data.csv"
    generate_research_csv({"core_analysis": core_results}, csv_file)
    print(f"📊 Research CSV: {csv_file}")
    
    # Complete JSON results
    complete_results = {
        "analysis_metadata": {
            "timestamp": datetime.now().isoformat(),
            "analyzed_responses": len(core_results),
            "analysis_tools_used": [
                "DeicticEthicalAnalyzer", "PronounAgencyAnalyzer", 
                "LLM Agent Analysis", "Expert Analysis Suite",
                "Moral Reasoning Structure", "Affective Stance", 
                "Lexical Rhetorical Features"
            ]
        },
        "core_analysis": core_results,
        "expert_analysis": expert_results,
        "comparative_analysis": comparative_analysis,
        "research_framework_analysis": research_framework_analysis # Add research framework analysis to results
    }
    
    with open(output_dir / "complete_analysis_results.json", 'w', encoding='utf-8') as f:
        json.dump(complete_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"💾 Complete JSON: {output_dir / 'complete_analysis_results.json'}")
    
    # Generate detailed reports
    try:
        detailed_report = await detailed_reporter.generate_comprehensive_report(complete_results)
        detailed_file = output_dir / "detailed_analysis_report.md"
        with open(detailed_file, 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        print(f"📋 Detailed Report: {detailed_file}")
    except Exception as e:
        print(f"  ⚠️ Detailed report failed: {e}")
    
    try:
        final_report = final_reporter.generate_final_report(str(output_dir))
        final_file = output_dir / "FINAL_DEIXIS_RESEARCH_REPORT.md"
        with open(final_file, 'w', encoding='utf-8') as f:
            f.write(final_report)
        print(f"🎯 Final Report: {final_file}")
    except Exception as e:
        print(f"  ⚠️ Final report failed: {e}")
    
    return complete_results

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
            'first_singular_ratio': data['pronoun_analysis'].pronoun_ratios.get('first_singular', 0.0),
            'second_person_ratio': data['pronoun_analysis'].pronoun_ratios.get('second_person', 0.0),
            'first_plural_ratio': data['pronoun_analysis'].pronoun_ratios.get('first_plural', 0.0),
            'third_person_ratio': data['pronoun_analysis'].pronoun_ratios.get('third_person', 0.0),
            'agency_type': data['pronoun_analysis'].agency_type,
            
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

async def main():
    """Main entry point - automatically find and analyze latest generation logs."""
    
    print("🔬 COMPLETE DEIXIS ANALYSIS RUNNER")
    print("=" * 60)
    print("🤖 Automated analysis of generation logs")
    print("🎯 All tools: Core + Expert + Advanced LLM Analysis")
    print("📊 Generates: CSV, JSON, Reports, Research Framework")
    print("=" * 60)
    
    # Define logs directory
    logs_directory = Path("C:/dev/deixisAugust2025/generation_logs")
    
    print(f"\n📁 Scanning: {logs_directory}")
    
    # Find latest session
    latest_session = find_latest_generation_session(logs_directory)
    if not latest_session:
        return
    
    print(f"\n✅ Using latest session: {latest_session.name}")
    
    # Find response files
    response_files = find_response_files(latest_session)
    if not response_files:
        print(f"❌ No response files found in {latest_session}")
        return
    
    print(f"📄 Found {len(response_files)} response files:")
    for file in response_files:
        print(f"  - {file.name}")
    
    # Use the first/main response file
    main_response_file = response_files[0]
    print(f"\n📖 Processing: {main_response_file.name}")
    
    # Extract responses
    responses_data = extract_responses_from_file(main_response_file)
    if not responses_data:
        print(f"❌ No responses found in {main_response_file}")
        return
    
    print(f"✅ Extracted {len(responses_data)} responses:")
    for framing in responses_data.keys():
        print(f"  - {framing}")
    
    # Create output directory for analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"automated_analysis_results/complete_analysis_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run comprehensive analysis
    results = await run_comprehensive_analysis_on_responses(responses_data, output_dir)
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"📁 Results saved to: {output_dir}")
    print(f"📊 Analyzed responses: {len(responses_data)}")
    print(f"🔬 Analysis tools used: 12+ (Core + Expert + Advanced)")
    print("=" * 60)
    print(f"📋 Key files generated:")
    print(f"  🔢 comprehensive_research_data.csv")
    print(f"  💾 complete_analysis_results.json")
    print(f"  📄 detailed_analysis_report.md")
    print(f"  🎯 FINAL_DEIXIS_RESEARCH_REPORT.md")
    print(f"  🔬 research_framework_analysis.json")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())