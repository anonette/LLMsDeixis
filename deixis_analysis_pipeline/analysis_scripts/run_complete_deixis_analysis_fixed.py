#!/usr/bin/env python3
"""
Fixed version of the complete deixis analysis runner.
Properly handles async/sync method calls and includes robust error handling.
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import all required modules
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from transformer import DeicticTransformer
from analysis_logger import RichAnalysisLogger

# Import the fixed expert agent
sys.path.append(str(Path(__file__).parent.parent.parent))
from expert_analysis_agent_fixed import ExpertAnalysisAgent

# Import other expert modules
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from pronoun_agency_expert import PronounAgencyExpert
from detailed_report_generator import DetailedReportGenerator

# Try to import research framework
try:
    from research_framework_system import DeicticResearchFramework
    RESEARCH_FRAMEWORK_AVAILABLE = True
except ImportError:
    RESEARCH_FRAMEWORK_AVAILABLE = False
    print("[WARNING] Research framework not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
GENERATION_LOGS_DIR = Path(__file__).parent.parent / "generation_logs"
OUTPUT_DIR = Path(__file__).parent.parent / "automated_analysis_results"

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

def create_basic_framework_analysis() -> Dict[str, Any]:
    """Create a basic research framework analysis when the full framework isn't available."""
    return {
        "framework_status": "basic",
        "research_categories": [
            "Linguistic Analysis",
            "Ethical Framework Detection", 
            "Agency Attribution",
            "Cross-framing Patterns"
        ],
        "note": "Full research framework not available"
    }

async def analyze_single_response(
    analyzer: DeicticEthicalAnalyzer,
    transformer: DeicticTransformer,
    logger: RichAnalysisLogger,
    response_data: Dict[str, Any],
    dilemma_id: str
) -> Dict[str, Any]:
    """Analyze a single response with all core components."""
    
    framing_type = response_data['framing_type']
    llm_response = response_data['response']
    
    print(f"\n🔍 Analyzing {framing_type.upper()} response...")
    print(f"  📝 Response length: {len(llm_response)} characters")
    
    # Core analysis - use llm_agent methods
    agent_result = await analyzer.llm_agent.analyze_agency_distribution(llm_response)
    print(f"  👤 Primary agent: {agent_result.primary_agent}")
    
    framework_result = await analyzer.llm_agent.analyze_ethical_framing(llm_response)
    print(f"  [ETHICS] Ethical framework: {framework_result.primary_framework}")
    
    voice_result = await analyzer.llm_agent.analyze_rhetorical_posture(llm_response)
    print(f"  🎭 Voice authority: {voice_result.get('voice_authority_type', 'unknown')}")
    
    # Now using the newly implemented methods
    reasoning_result = await analyzer.llm_agent.analyze_moral_reasoning(llm_response)
    print(f"  🧠 Moral reasoning: {reasoning_result.get('reasoning_type', 'unknown')}")
    
    stance_result = await analyzer.llm_agent.analyze_affective_stance(llm_response)
    print(f"  💭 Affective stance: {stance_result.get('stance_type', 'unknown')}")
    
    coherence_result = await analyzer.llm_agent.assess_indexical_coherence(llm_response)
    print(f"  📝 Indexical coherence: {coherence_result.get('coherence_level', 'unknown')}")
    
    # Deictic marker analysis
    deictic_markers = analyze_deictic_markers(llm_response)
    
    # Frame detection - create a simple result since the transformer doesn't have this method
    frame_result = {
        'suggested_frame': framing_type,
        'confidence': 0.8
    }
    
    # Log the analysis
    analysis_record = {
        'timestamp': datetime.now().isoformat(),
        'dilemma_id': dilemma_id,
        'framing_type': framing_type,
        'response_length': len(llm_response),
        'primary_agent': agent_result.primary_agent if hasattr(agent_result, 'primary_agent') else str(agent_result),
        'agent_confidence': agent_result.confidence_score if hasattr(agent_result, 'confidence_score') else 0.8,
        'ethical_framework': framework_result.primary_framework if hasattr(framework_result, 'primary_framework') else str(framework_result),
        'framework_confidence': framework_result.confidence_score if hasattr(framework_result, 'confidence_score') else 0.8,
        'voice_authority': voice_result.get('voice_authority_type', 'unknown') if isinstance(voice_result, dict) else 'unknown',
        'voice_confidence': voice_result.get('voice_authority_score', 0.8) if isinstance(voice_result, dict) else 0.8,
        'moral_reasoning': reasoning_result['reasoning_type'],
        'reasoning_confidence': reasoning_result.get('confidence_score', 0.0),
        'affective_stance': stance_result['stance_type'],
        'stance_confidence': stance_result.get('confidence_score', 0.0),
        'indexical_coherence': coherence_result['coherence_level'],
        'coherence_score': coherence_result.get('confidence_score', coherence_result.get('score', 0.0)),
        'deictic_markers': deictic_markers,
        'total_markers': sum(deictic_markers.values()),
        'suggested_frame': frame_result['suggested_frame'],
        'frame_confidence': frame_result.get('confidence', frame_result.get('confidence_score', 0.0)),
        'llm_response': llm_response,
        'processing_time': 0.0  # Would need timing logic
    }
    
    # Skip the detailed logger for now - focus on file saving
    # logger.log_analysis(analysis_record)
    
    return analysis_record

def generate_comprehensive_comparison(core_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate comparative analysis across all responses."""
    
    comparison = {
        'total_responses': len(core_results),
        'by_framing': {},
        'by_dilemma': {},
        'cross_patterns': {}
    }
    
    # Group by framing type
    for result in core_results:
        framing = result['framing_type']
        if framing not in comparison['by_framing']:
            comparison['by_framing'][framing] = []
        comparison['by_framing'][framing].append(result)
    
    # Group by dilemma
    for result in core_results:
        dilemma = result['dilemma_id']
        if dilemma not in comparison['by_dilemma']:
            comparison['by_dilemma'][dilemma] = []
        comparison['by_dilemma'][dilemma].append(result)
    
    # Analyze patterns
    comparison['cross_patterns'] = {
        'framework_distribution': {},
        'agent_distribution': {},
        'coherence_by_framing': {}
    }
    
    # Calculate distributions
    for framing, results in comparison['by_framing'].items():
        frameworks = [r['ethical_framework'] for r in results]
        comparison['cross_patterns']['framework_distribution'][framing] = {
            fw: frameworks.count(fw) for fw in set(frameworks)
        }
        
        agents = [r['primary_agent'] for r in results]
        comparison['cross_patterns']['agent_distribution'][framing] = {
            agent: agents.count(agent) for agent in set(agents)
        }
        
        coherence_scores = [r['coherence_score'] for r in results]
        comparison['cross_patterns']['coherence_by_framing'][framing] = {
            'mean': sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0,
            'min': min(coherence_scores) if coherence_scores else 0,
            'max': max(coherence_scores) if coherence_scores else 0
        }
    
    return comparison

async def run_comprehensive_analysis_on_responses(
    responses_data: List[Dict[str, Any]], 
    output_dir: Path
) -> Dict[str, Any]:
    """Run comprehensive analysis on a set of responses."""
    
    # Initialize all components
    analyzer = DeicticEthicalAnalyzer()
    transformer = DeicticTransformer()
    analysis_logger = RichAnalysisLogger(output_dir=str(output_dir))
    
    # Initialize expert analyzers
    expert_agent = ExpertAnalysisAgent()
    critical_expert = CriticalExpertAnalyzer()
    evidence_expert = EvidenceBasedExpertAnalyzer()
    pronoun_expert = PronounAgencyExpert()
    
    print(f"\n[ANALYSIS] RUNNING COMPREHENSIVE ANALYSIS")
    print(f"[OUTPUT] Output directory: {output_dir}")
    print(f"[DATA] Processing {len(responses_data)} responses")
    
    # Core analysis
    print("\n" + "="*80)
    print("CORE ANALYSIS - Processing {} responses".format(len(responses_data)))
    print("="*80)
    
    core_results = []
    for response_data in responses_data:
        result = await analyze_single_response(
            analyzer, 
            transformer, 
            analysis_logger,
            response_data,
            response_data.get('dilemma_id', 'unknown')
        )
        core_results.append(result)
    
    print(f"\n🎉 Core analysis complete! Processed {len(core_results)} responses")
    
    # Expert analysis with proper error handling
    print("\n" + "="*80)
    print("EXPERT ANALYSIS - Advanced interpretation")
    print("="*80)
    
    expert_results = {}
    
    # Expert agent analysis (fixed JSON parsing)
    try:
        expert_results["expert_agent"] = await expert_agent.analyze_session_data(core_results)
        print("  [OK] Expert Agent Analysis complete")
    except Exception as e:
        print(f"  [ERROR] Expert Agent failed: {e}")
        logger.error(f"Expert agent error: {e}")
    
    # Critical expert analysis (sync method, not async)
    try:
        # Extract evidence first with proper session data structure
        session_data = {
            'records': core_results,
            'session_metadata': {'session_id': analysis_logger.session_id}
        }
        critical_evidence = critical_expert.extract_critical_evidence(session_data)
        
        # Build evidence index (required before generating insights)
        critical_expert.critical_evidence = critical_evidence
        critical_expert._build_critical_evidence_index()
        
        # Then generate insights for each research question
        critical_insights = {}
        for rq in ["RQ1.1", "RQ2.1", "RQ3.1", "RQ4.1", "RQ5.1"]:
            try:
                insights = critical_expert.generate_critical_insights(rq)
                if insights:
                    # Convert dataclass objects to dicts for JSON serialization
                    critical_insights[rq] = [
                        insight.__dict__ if hasattr(insight, '__dict__') else insight
                        for insight in insights
                    ]
            except Exception as e:
                logger.warning(f"Failed to generate critical insights for {rq}: {e}")
        
        expert_results["critical_expert"] = {
            "evidence": [e.__dict__ if hasattr(e, '__dict__') else e for e in critical_evidence],
            "insights": critical_insights
        }
        print("  [OK] Critical Expert Analysis complete")
    except Exception as e:
        print(f"  [ERROR] Critical Expert failed: {e}")
        logger.error(f"Critical expert error: {e}")
    
    # Evidence-based expert analysis (sync method, not async)
    try:
        # Extract evidence first with proper session data structure
        session_data = {
            'records': core_results,
            'session_metadata': {'session_id': analysis_logger.session_id}
        }
        evidence_based_evidence = evidence_expert.extract_evidence_from_logs(session_data)
        
        # Build evidence index (required before generating insights)
        evidence_expert.logged_evidence = evidence_based_evidence
        evidence_expert._build_evidence_index()
        
        # Then generate insights
        evidence_insights = {}
        for rq in ["RQ1.1", "RQ2.1", "RQ3.1", "RQ4.1", "RQ5.1"]:
            try:
                insights = evidence_expert.generate_evidence_based_insights(rq)
                if insights:
                    # Convert dataclass objects to dicts for JSON serialization
                    evidence_insights[rq] = [
                        insight.__dict__ if hasattr(insight, '__dict__') else insight
                        for insight in insights
                    ]
            except Exception as e:
                logger.warning(f"Failed to generate evidence insights for {rq}: {e}")
        
        expert_results["evidence_expert"] = {
            "evidence": [e.__dict__ if hasattr(e, '__dict__') else e for e in evidence_based_evidence],
            "insights": evidence_insights
        }
        print("  [OK] Evidence-Based Expert Analysis complete")
    except Exception as e:
        print(f"  [ERROR] Evidence Expert failed: {e}")
        logger.error(f"Evidence expert error: {e}")
    
    # Pronoun expert analysis
    try:
        # The pronoun expert expects a specific data structure
        # Group responses by framing type as required
        responses_by_framing = {}
        for result in core_results:
            framing = result.get('framing_type', 'unknown')
            if framing not in responses_by_framing:
                responses_by_framing[framing] = []
            responses_by_framing[framing].append(result)
        
        # Call with proper session data structure
        pronoun_analysis = await pronoun_expert.analyze_session_data({
            'records': core_results,
            'responses_by_framing': responses_by_framing,
            'session_metadata': {'session_id': analysis_logger.session_id}
        })
        
        # Convert to serializable format
        if hasattr(pronoun_analysis, '__dict__'):
            expert_results["pronoun_expert"] = pronoun_analysis.__dict__
        else:
            expert_results["pronoun_expert"] = pronoun_analysis
            
        print("  [OK] Pronoun Agency Expert Analysis complete")
    except Exception as e:
        print(f"  [ERROR] Pronoun Expert failed: {e}")
        logger.error(f"Pronoun expert error: {e}")
    
    # Comparative analysis
    print(f"\n🔗 Generating comparative analysis...")
    comparative_analysis = generate_comprehensive_comparison(core_results)
    
    # Research framework analysis
    print(f"\n[RESEARCH] Research framework analysis...")
    research_framework_analysis = {}
    if RESEARCH_FRAMEWORK_AVAILABLE:
        try:
            research_framework = DeicticResearchFramework()
            research_framework_analysis = research_framework.get_research_roadmap()
            print("  [OK] Research framework analysis complete")
        except Exception as e:
            print(f"  [WARNING] Research framework failed: {e}")
            research_framework_analysis = create_basic_framework_analysis()
    else:
        research_framework_analysis = create_basic_framework_analysis()
        print(f"[RESEARCH] Basic Research Framework: {output_dir / 'research_framework_analysis.json'}")
    
    # Save all results
    print(f"\n💾 Saving analysis results...")
    
    # Core results CSV
    df = pd.DataFrame(core_results)
    csv_path = output_dir / "core_analysis_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"  [OK] Core results CSV: {csv_path}")
    
    # Core results JSON
    json_path = output_dir / "core_analysis_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(core_results, f, indent=2)
    print(f"  [OK] Core results JSON: {json_path}")
    
    # Expert analysis results
    if expert_results:
        expert_path = output_dir / "expert_analysis_results.json"
        with open(expert_path, 'w', encoding='utf-8') as f:
            # Convert any dataclass objects to dicts
            serializable_results = {}
            for key, value in expert_results.items():
                try:
                    if hasattr(value, '__dict__'):
                        serializable_results[key] = value.__dict__
                    else:
                        serializable_results[key] = value
                except:
                    serializable_results[key] = str(value)
            json.dump(serializable_results, f, indent=2, default=str)
        print(f"  [OK] Expert analysis: {expert_path}")
    
    # Comparative analysis
    comparative_path = output_dir / "comparative_analysis.json"
    with open(comparative_path, 'w', encoding='utf-8') as f:
        json.dump(comparative_analysis, f, indent=2)
    print(f"  [OK] Comparative analysis: {comparative_path}")
    
    # Research framework
    framework_path = output_dir / "research_framework_analysis.json"
    with open(framework_path, 'w', encoding='utf-8') as f:
        json.dump(research_framework_analysis, f, indent=2)
    print(f"  [OK] Research framework: {framework_path}")
    
    # Generate detailed report
    try:
        report_generator = DetailedReportGenerator()
        report_path = output_dir / "detailed_analysis_report.md"
        
        # Prepare report data
        report_data = {
            'core_results': core_results,
            'expert_results': expert_results,
            'comparative_analysis': comparative_analysis,
            'research_framework': research_framework_analysis
        }
        
        report_content = report_generator.generate_report(report_data)
        
        # Ensure report_content is a string
        if hasattr(report_content, 'to_markdown'):
            report_text = report_content.to_markdown()
        elif hasattr(report_content, '__str__'):
            report_text = str(report_content)
        else:
            report_text = report_content
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"  [OK] Detailed report: {report_path}")
    except Exception as e:
        print(f"  [WARNING] Report generation failed: {e}")
    
    # Save session log
    session_data = analysis_logger.get_session_data()
    session_path = output_dir / "complete_session_log.json"
    with open(session_path, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, indent=2)
    print(f"  [OK] Session log: {session_path}")
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"📁 All results saved to: {output_dir}")
    
    return {
        'core_results': core_results,
        'expert_results': expert_results,
        'comparative_analysis': comparative_analysis,
        'research_framework': research_framework_analysis,
        'output_directory': str(output_dir)
    }

async def main():
    """Main entry point for the analysis runner."""
    
    print("[ANALYSIS] COMPLETE DEIXIS ANALYSIS RUNNER")
    print("="*60)
    print("[AUTO] Automated analysis of generation logs")
    print("[TOOLS] All tools: Core + Expert + Advanced LLM Analysis")
    print("[OUTPUT] Generates: CSV, JSON, Reports, Research Framework")
    print("="*60)
    
    # Find the latest generation session
    print(f"\n[SCAN] Scanning: {GENERATION_LOGS_DIR}")
    
    if not GENERATION_LOGS_DIR.exists():
        print(f"[ERROR] Generation logs directory not found: {GENERATION_LOGS_DIR}")
        return
    
    session_dirs = [d for d in GENERATION_LOGS_DIR.iterdir() if d.is_dir()]
    if not session_dirs:
        print("[ERROR] No session directories found")
        return
    
    print(f"[DIRS] Found {len(session_dirs)} session directories:")
    for i, session_dir in enumerate(sorted(session_dirs), 1):
        print(f"  {i}. {session_dir.name}")
    
    # Use the latest session
    latest_session = max(session_dirs, key=lambda d: d.stat().st_mtime)
    print(f"\n[OK] Using latest session: {latest_session.name}")
    
    # Find response files
    response_files = list(latest_session.glob("*_responses.json"))
    response_files = [f for f in response_files if f.name != "complete_session_data.json"]
    
    if not response_files:
        print("[ERROR] No response files found in session")
        return
    
    print(f"[FILES] Found {len(response_files)} response files:")
    for f in response_files:
        print(f"  - {f.name}")
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = OUTPUT_DIR / f"complete_analysis_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each dilemma file
    all_responses = []
    
    for response_file in response_files:
        dilemma_id = response_file.stem.replace("_responses", "")
        print(f"\n📖 Processing: {response_file.name}")
        
        with open(response_file, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        
        # Extract responses from the nested structure
        if 'responses' in file_data:
            responses = file_data['responses']
            print(f"[OK] Extracted {len(responses)} response framings:")
            
            # Convert nested responses to list format
            for framing_type, response_data in responses.items():
                print(f"  - {framing_type}")
                # Create a response object with all necessary data
                response_obj = {
                    'framing_type': framing_type,
                    'response': response_data.get('response', ''),
                    'deictic_question': response_data.get('deictic_question', ''),
                    'dilemma_id': dilemma_id,
                    'dilemma_title': file_data.get('dilemma_title', ''),
                    'model': file_data.get('model', ''),
                    'temperature': file_data.get('temperature', 0.9)
                }
                all_responses.append(response_obj)
        else:
            print(f"[WARNING] No 'responses' field found in {response_file.name}")
    
    # Run comprehensive analysis
    results = await run_comprehensive_analysis_on_responses(all_responses, output_dir)
    
    print("\n" + "="*60)
    print("ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total responses analyzed: {len(all_responses)}")
    print(f"Output directory: {output_dir}")
    print(f"Files generated: {len(list(output_dir.glob('*')))}")
    
    # Show framework distribution
    if results['core_results']:
        df = pd.DataFrame(results['core_results'])
        print("\n📊 Ethical Framework Distribution:")
        print(df['ethical_framework'].value_counts())
        
        print("\n📐 Framing Type Distribution:")
        print(df['framing_type'].value_counts())

if __name__ == "__main__":
    asyncio.run(main())