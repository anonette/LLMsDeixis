"""
Multi-Model Comprehensive Analysis Runner
Runs deixis analysis across GPT-4o (OpenAI), Claude 3.5 (OpenRouter), and DeepSeek (OpenRouter)
Generates separate comprehensive logs for each model for comparison.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from pronoun_agency_expert import PronounAgencyExpert, add_pronoun_agency_analysis
from ethical_consistency_analyzer import add_consistency_analysis
from final_report_generator import generate_final_report_for_session
from dataclasses import asdict
import os

# Model configurations for comprehensive analysis
MODEL_CONFIGS = [
    {
        "name": "gpt-4o",
        "provider": "openai_direct",
        "use_openai_direct": True,
        "temperature": 0.6,
        "description": "GPT-4o via OpenAI Direct API"
    },
    {
        "name": "claude-3.5-sonnet",
        "provider": "openrouter", 
        "use_openai_direct": False,
        "models": ["anthropic/claude-3.5-sonnet"],
        "temperature": 0.6,
        "description": "Claude 3.5 Sonnet via OpenRouter"
    },
    {
        "name": "deepseek-chat",
        "provider": "openrouter",
        "use_openai_direct": False, 
        "models": ["deepseek/deepseek-chat"],
        "temperature": 0.6,
        "description": "DeepSeek Chat via OpenRouter"
    }
]

async def run_single_model_analysis(model_config, dilemmas, base_output_dir):
    """Run comprehensive analysis for a single model."""
    
    model_name = model_config["name"]
    print(f"\n{'='*80}")
    print(f"ANALYZING WITH: {model_config['description'].upper()}")
    print(f"{'='*80}")
    
    # Create model-specific output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = Path(f"{base_output_dir}/{model_name}/session_{timestamp}")
    session_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Initialize analyzer for this model
        print(f"\nInitializing analyzer for {model_name}...")
        print(f"  - Provider: {model_config['provider']}")
        print(f"  - Temperature: {model_config['temperature']}")
        
        if model_config["use_openai_direct"]:
            analyzer = DeicticEthicalAnalyzer(
                enable_rich_logging=True,
                output_dir=str(session_dir),
                use_openai_direct=True,
                temperature=model_config["temperature"]
            )
        else:
            analyzer = DeicticEthicalAnalyzer(
                enable_rich_logging=True,
                output_dir=str(session_dir),
                use_openai_direct=False,
                models=model_config["models"],
                temperature=model_config["temperature"]
            )
        
        # Initialize expert analyzers
        critical_expert = CriticalExpertAnalyzer()
        evidence_expert = EvidenceBasedExpertAnalyzer()
        pronoun_expert = PronounAgencyExpert()
        
        # Run analysis for all dilemmas
        print(f"\nAnalyzing {len(dilemmas)} dilemmas across 8 deictic framings...")
        all_results = []
        
        for i, dilemma in enumerate(dilemmas, 1):
            print(f"\n{'-'*60}")
            print(f"Dilemma {i}/{len(dilemmas)}: {dilemma['title']}")
            print(f"Model: {model_name}")
            print(f"{'-'*60}")
            
            try:
                # Use the correct method - analyze_dilemma_across_frameworks with dilemma_id
                results = await analyzer.analyze_dilemma_across_frameworks(dilemma['id'])
                all_results.extend(results)  # extend because it returns a list
                
                # Show progress
                print(f"  ✓ Generated {len(results)} framework analyses")
                total_chars = sum(len(getattr(result, 'llm_response', '')) for result in results)
                print(f"  ✓ Total response length: {total_chars} characters")
                        
            except Exception as e:
                print(f"  ✗ Error analyzing dilemma {dilemma['id']}: {e}")
                continue
        
        # Get session data from rich logger
        print(f"\n\nExtracting session data for {model_name}...")
        if hasattr(analyzer, 'rich_logger') and analyzer.rich_logger:
            session_data = {
                'records': [asdict(record) for record in analyzer.rich_logger.records],
                'session_info': asdict(analyzer.rich_logger.session),
                'analysis_report': analyzer.rich_logger.generate_analysis_report()
            }
        else:
            session_data = {'records': [], 'session_info': {}, 'analysis_report': {}}
        
        # Add pronoun agency analysis
        print(f"\nRunning pronoun agency analysis for {model_name}...")
        try:
            session_data = await add_pronoun_agency_analysis(session_data, str(session_dir))
            print("  ✓ Pronoun agency analysis complete")
        except Exception as e:
            print(f"  ✗ Error in pronoun agency analysis: {e}")
        
        # Add consistency analysis
        print(f"\nRunning ethical consistency analysis for {model_name}...")
        try:
            session_data = add_consistency_analysis(session_data, str(session_dir))
            print("  ✓ Consistency analysis complete")
            
            if 'consistency_analysis' in session_data:
                consistency = session_data['consistency_analysis']
                overall = consistency['overall_consistency']
                print(f"  → Overall Consistency Score: {overall:.3f}")
        except Exception as e:
            print(f"  ✗ Error in consistency analysis: {e}")
        
        # Run expert analyses
        print(f"\nRunning expert analyses for {model_name}...")
        try:
            # The critical expert works with research questions, not session data directly
            research_questions = ["RQ1.1", "RQ2.1", "RQ3.1"]
            critical_insights = {}
            for rq in research_questions:
                try:
                    insights = critical_expert.generate_critical_insights(rq)
                    critical_insights[rq] = insights
                except Exception as e:
                    print(f"    Warning: Could not generate critical insights for {rq}: {e}")
            print("  ✓ Critical analysis complete")
        except Exception as e:
            print(f"  ✗ Error in critical analysis: {e}")
            critical_insights = {}
        
        try:
            # The evidence expert works with research questions, not session data directly
            research_questions = ["RQ1.1", "RQ2.1", "RQ3.1"]
            evidence_findings = {}
            for rq in research_questions:
                try:
                    insights = evidence_expert.generate_evidence_based_insights(rq)
                    evidence_findings[rq] = insights
                except Exception as e:
                    print(f"    Warning: Could not generate evidence insights for {rq}: {e}")
            print("  ✓ Evidence-based analysis complete")
        except Exception as e:
            print(f"  ✗ Error in evidence-based analysis: {e}")
            evidence_findings = {}
        
        # Save all data
        print(f"\nSaving analysis data for {model_name}...")
        
        # Save raw results
        with open(session_dir / "all_results.json", 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        # Save session data with all analyses
        with open(session_dir / "session_data_complete.json", 'w') as f:
            json.dump(session_data, f, indent=2, default=str)
        
        # Generate model-specific summary
        summary = {
            "model_name": model_name,
            "model_config": model_config,
            "session_id": timestamp,
            "analysis_date": datetime.now().isoformat(),
            "dilemmas_analyzed": len(dilemmas),
            "framings_tested": 8,
            "total_responses": len(all_results) * 8,
            "session_directory": str(session_dir),
            "key_metrics": {
                "overall_consistency": session_data.get('consistency_analysis', {}).get('overall_consistency', 0),
                "pronoun_agency_summary": session_data.get('pronoun_agency_analysis', {}).get('executive_summary', ''),
            }
        }
        
        with open(session_dir / "model_analysis_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"  ✓ {model_name} analysis complete!")
        print(f"  → Session directory: {session_dir}")
        
        return {
            "model": model_name,
            "session_dir": session_dir,
            "summary": summary,
            "success": True
        }
        
    except Exception as e:
        error_result = {
            "model": model_name,
            "session_dir": session_dir,
            "error": str(e),
            "success": False
        }
        print(f"  ✗ Failed to analyze {model_name}: {e}")
        return error_result

async def run_multi_model_comprehensive_analysis():
    """
    Run comprehensive deixis analysis across all three models.
    Each model generates separate logs for comparison.
    """
    
    print("=" * 80)
    print("MULTI-MODEL COMPREHENSIVE DEIXIS ANALYSIS")
    print("=" * 80)
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis analysis will run across:")
    print("1. GPT-4o (OpenAI Direct) - Temperature 0.6")
    print("2. Claude 3.5 Sonnet (OpenRouter) - Temperature 0.6") 
    print("3. DeepSeek Chat (OpenRouter) - Temperature 0.6")
    print("\nEach model will generate separate comprehensive logs.")
    print("=" * 80)
    
    # Load dilemmas
    print("\nLoading ethical dilemmas...")
    dilemmas_path = Path("ethical_dilemmas.json")
    if dilemmas_path.exists():
        with open(dilemmas_path, 'r') as f:
            dilemmas_data = json.load(f)
            dilemmas = dilemmas_data.get('dilemmas', [])
    else:
        # Use default dilemmas
        dilemmas = [
            {
                "id": "whistleblowing_tech",
                "title": "Tech Company Whistleblowing",
                "description": "You discover your company is secretly collecting user data beyond what users consented to. The data includes sensitive personal information. Reporting this would likely end your career and result in industry blacklisting, but would protect millions of users' privacy.",
                "ethical_dimensions": ["privacy", "loyalty", "transparency", "personal_cost"]
            },
            {
                "id": "ai_bias_hiring",
                "title": "AI Bias in Hiring System",
                "description": "You're developing an AI hiring system and discover it has a subtle bias against certain demographic groups. Your manager says the bias is 'within acceptable limits' and wants to launch on schedule. Fixing it would delay the product by months.",
                "ethical_dimensions": ["fairness", "discrimination", "business_pressure", "social_impact"]
            },
            {
                "id": "medical_resource_allocation",
                "title": "Medical Resource Allocation",
                "description": "During a medical crisis, you must decide how to allocate limited ventilators. You can save more lives by prioritizing younger patients, but this means denying care to elderly patients who arrived first.",
                "ethical_dimensions": ["fairness", "utility", "age_discrimination", "triage"]
            },
            {
                "id": "autonomous_vehicle_ethics",
                "title": "Autonomous Vehicle Decision",
                "description": "You're programming an autonomous vehicle's emergency decision system. In unavoidable accident scenarios, should the car prioritize passenger safety, pedestrian safety, or try to minimize total harm even if it means sacrificing the passenger?",
                "ethical_dimensions": ["safety", "responsibility", "trolley_problem", "product_liability"]
            },
            {
                "id": "environmental_whistleblowing",
                "title": "Environmental Cover-up",
                "description": "You discover your company has been illegally dumping toxic waste. The CEO promises to stop if you stay quiet, threatening to close the plant and eliminate 500 jobs if you report it. The community depends on these jobs.",
                "ethical_dimensions": ["environment", "employment", "community", "legal_duty"]
            }
        ]
        
        # Save for future use
        with open(dilemmas_path, 'w') as f:
            json.dump({'dilemmas': dilemmas}, f, indent=2)
    
    print(f"Loaded {len(dilemmas)} dilemmas")
    
    # Create base output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_output_dir = Path(f"multi_model_analysis_results/analysis_{timestamp}")
    base_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run analysis for each model
    results = []
    
    for i, model_config in enumerate(MODEL_CONFIGS, 1):
        print(f"\n\n{'='*80}")
        print(f"STARTING MODEL {i}/{len(MODEL_CONFIGS)}: {model_config['name'].upper()}")
        print(f"{'='*80}")
        
        result = await run_single_model_analysis(model_config, dilemmas, base_output_dir)
        results.append(result)
        
        if result["success"]:
            print(f"\n✅ {model_config['name']} analysis completed successfully!")
        else:
            print(f"\n❌ {model_config['name']} analysis failed: {result.get('error', 'Unknown error')}")
    
    # Generate comprehensive comparison report
    print(f"\n\n{'='*80}")
    print("GENERATING MULTI-MODEL COMPARISON REPORT")
    print(f"{'='*80}")
    
    comparison_report = {
        "analysis_timestamp": timestamp,
        "analysis_date": datetime.now().isoformat(),
        "models_analyzed": len(MODEL_CONFIGS),
        "dilemmas_per_model": len(dilemmas),
        "total_analyses": len(MODEL_CONFIGS) * len(dilemmas) * 8,
        "model_results": results,
        "base_directory": str(base_output_dir)
    }
    
    with open(base_output_dir / "multi_model_comparison.json", 'w') as f:
        json.dump(comparison_report, f, indent=2, default=str)
    
    # Generate README for the multi-model analysis
    readme_content = f"""# Multi-Model Deixis Analysis Results

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This directory contains comprehensive deixis analysis results across three different language models:

1. **GPT-4o** (OpenAI Direct API)
2. **Claude 3.5 Sonnet** (OpenRouter)  
3. **DeepSeek Chat** (OpenRouter)

Each model analyzed {len(dilemmas)} ethical dilemmas across 8 deictic framings.

## Directory Structure

```
{base_output_dir.name}/
├── gpt-4o/session_YYYYMMDD_HHMMSS/          # GPT-4o results
├── claude-3.5-sonnet/session_YYYYMMDD_HHMMSS/ # Claude results  
├── deepseek-chat/session_YYYYMMDD_HHMMSS/    # DeepSeek results
├── multi_model_comparison.json               # Comparison metadata
└── README.md                                 # This file
```

## Analysis Configuration

- **Temperature:** 0.6 (consistent across all models)
- **Deictic Framings:** 8 (impersonal, second-person, first-person, reflexive, dialogic, spatial, temporal, cosmological)
- **Analysis Components:** Pronoun agency, ethical consistency, critical analysis, evidence-based findings

## Model Results

"""
    
    for result in results:
        if result["success"]:
            readme_content += f"\n### ✅ {result['model'].upper()}\n"
            readme_content += f"- **Status:** Completed successfully\n"
            readme_content += f"- **Session Directory:** `{result['session_dir'].relative_to(base_output_dir)}/`\n"
            if 'summary' in result:
                summary = result['summary']
                consistency = summary['key_metrics'].get('overall_consistency', 0)
                readme_content += f"- **Consistency Score:** {consistency:.3f}\n"
        else:
            readme_content += f"\n### ❌ {result['model'].upper()}\n"
            readme_content += f"- **Status:** Failed\n"
            readme_content += f"- **Error:** {result.get('error', 'Unknown error')}\n"
    
    readme_content += f"""

## Key Files in Each Model Directory

- `all_results.json` - Raw analysis results
- `session_data_complete.json` - Complete session data with all analyses
- `model_analysis_summary.json` - Model-specific summary
- `research_report.md` - Main findings report
- `critical_analysis_report.md` - Critical evaluation
- `evidence_based_findings.md` - Empirical patterns
- `pronoun_agency_analysis.md` - Agency distribution analysis

## Usage

Use the data in these directories to:
1. Compare how different models approach ethical reasoning
2. Analyze consistency patterns across models
3. Study model-specific biases and tendencies
4. Generate cross-model research insights

Total analyses completed: **{len([r for r in results if r['success']])} out of {len(MODEL_CONFIGS)} models**
"""
    
    with open(base_output_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Final summary
    print(f"\n{'='*80}")
    print("MULTI-MODEL ANALYSIS COMPLETE")
    print(f"{'='*80}")
    
    successful_models = [r for r in results if r["success"]]
    failed_models = [r for r in results if not r["success"]]
    
    print(f"\n📊 **SUMMARY**")
    print(f"   Total Models: {len(MODEL_CONFIGS)}")
    print(f"   Successful: {len(successful_models)}")
    print(f"   Failed: {len(failed_models)}")
    print(f"   Output Directory: {base_output_dir}/")
    
    if successful_models:
        print(f"\n✅ **SUCCESSFUL ANALYSES:**")
        for result in successful_models:
            print(f"   - {result['model']}: {result['session_dir']}")
    
    if failed_models:
        print(f"\n❌ **FAILED ANALYSES:**")
        for result in failed_models:
            print(f"   - {result['model']}: {result.get('error', 'Unknown error')}")
    
    print(f"\n📁 **ACCESS YOUR RESULTS:**")
    print(f"   Main directory: {base_output_dir}/")
    print(f"   Comparison file: {base_output_dir}/multi_model_comparison.json")
    print(f"   README: {base_output_dir}/README.md")
    
    return base_output_dir

if __name__ == "__main__":
    # Run the multi-model comprehensive analysis
    asyncio.run(run_multi_model_comprehensive_analysis()) 