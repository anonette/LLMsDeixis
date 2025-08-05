"""
Multi-Model Data Generation Script
Generate analysis data across GPT-4o, Claude 3.5 Sonnet, and DeepSeek models
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from deixis_ethical_analyzer import DeicticEthicalAnalyzer

async def generate_data_for_models():
    """Generate analysis data for specific models: GPT-4o, Claude 3.5 Sonnet, and DeepSeek."""
    
    print("🚀 MULTI-MODEL DATA GENERATION")
    print("=" * 60)
    print()
    
    # Define the specific models you want
    target_models = [
        "openai/gpt-4o",
        "anthropic/claude-3.5-sonnet", 
        "deepseek/deepseek-chat"
    ]
    
    print("🎯 Target Models:")
    for i, model in enumerate(target_models, 1):
        print(f"   {i}. {model}")
    print()
    
    # Create output directory
    output_dir = Path("multi_model_analysis_results")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = output_dir / f"session_{timestamp}"
    session_dir.mkdir(exist_ok=True)
    
    print(f"📁 Results will be saved to: {session_dir}")
    print()
    
    # Initialize analyzer with specific models
    print("🔧 Initializing analyzer with target models...")
    analyzer = DeicticEthicalAnalyzer(
        models=target_models,
        enable_rich_logging=True, 
        output_dir=str(session_dir)
    )
    
    # Get all dilemmas
    dilemmas = analyzer.get_dilemma_list()
    print(f"📋 Found {len(dilemmas)} ethical dilemmas")
    print()
    
    # Calculate total analyses
    total_analyses = len(dilemmas) * 8 * len(target_models)  # 10 dilemmas × 8 frameworks × 3 models
    print(f"🔄 Will generate {total_analyses} total analyses:")
    print(f"   • {len(dilemmas)} dilemmas")
    print(f"   • 8 deictic frameworks each")
    print(f"   • {len(target_models)} models each")
    print(f"   • Estimated time: {total_analyses * 3 // 60} minutes")
    print()
    
    try:
        # Run batch analysis
        print("🔄 Starting multi-model analysis...")
        all_results = await analyzer.batch_analyze_all_dilemmas()
        
        print(f"✅ Completed {len(all_results)} dilemma analyses")
        print()
        
        # Generate reports for each dilemma
        print("📊 Generating comparative reports...")
        reports = {}
        for dilemma_id in all_results.keys():
            report = analyzer.generate_comparative_report(dilemma_id)
            reports[dilemma_id] = report
            print(f"   ✓ Generated report for {dilemma_id}")
        
        # Save all results
        print("💾 Saving results...")
        
        # Save main results
        analyzer.export_results(str(session_dir / "raw_analysis_results.json"))
        
        # Save comparative reports
        with open(session_dir / "comparative_reports.json", 'w') as f:
            json.dump(reports, f, indent=2, default=str)
        
        # Finalize rich analysis
        final_report = analyzer.finalize_and_save_analysis(include_responses=True)
        
        # Generate summary with model information
        summary = {
            "session_info": {
                "timestamp": timestamp,
                "models_used": target_models,
                "total_dilemmas_analyzed": len(all_results),
                "total_framework_analyses": sum(len(results) for results in all_results.values()),
                "output_directory": str(session_dir)
            },
            "model_breakdown": {
                model: {
                    "analyses_per_model": len(all_results) * 8,  # 5 dilemmas × 8 frameworks
                    "model_description": _get_model_description(model)
                }
                for model in target_models
            },
            "files_generated": {
                "raw_analysis_results.json": "Complete analysis data from all models",
                "comparative_reports.json": "Cross-framework comparisons",
                "session_data.json": "Rich logging data with model information",
                "analysis_report.json": "Comprehensive analysis report",
                "deictic_analysis_TIMESTAMP.csv": "Spreadsheet format for analysis",
                "for_python_analysis_TIMESTAMP.pkl": "Python pickle format",
                "for_R_analysis_TIMESTAMP.csv": "R-compatible CSV format"
            },
            "next_steps": [
                "Review raw_analysis_results.json for model-specific patterns",
                "Compare responses across models using comparative_reports.json",
                "Analyze model differences in session_data.json",
                "Use CSV files for statistical analysis in R/Python"
            ]
        }
        
        with open(session_dir / "multi_model_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Print final summary
        print("🎉 MULTI-MODEL ANALYSIS COMPLETE!")
        print("=" * 60)
        print()
        print(f"📁 All results saved to: {session_dir}")
        print()
        print("📊 Generated Files:")
        for filename, description in summary["files_generated"].items():
            print(f"   • {filename} - {description}")
        print()
        print("🔍 Model Breakdown:")
        for model, info in summary["model_breakdown"].items():
            print(f"   • {model}: {info['analyses_per_model']} analyses")
            print(f"     {info['model_description']}")
        print()
        print("📋 Next Steps:")
        for step in summary["next_steps"]:
            print(f"   • {step}")
        print()
        print("✨ Ready for cross-model analysis!")
        
        return session_dir
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("Check your API keys in .env file and try again")
        return None

def _get_model_description(model: str) -> str:
    """Get description for each model."""
    descriptions = {
        "openai/gpt-4o": "OpenAI's latest GPT-4 Omni model with multimodal capabilities",
        "anthropic/claude-3.5-sonnet": "Anthropic's Claude 3.5 Sonnet with enhanced reasoning",
        "deepseek/deepseek-chat": "DeepSeek's conversational AI model with strong analytical capabilities"
    }
    return descriptions.get(model, "Advanced language model")

def main():
    """Run the multi-model data generation."""
    print("Starting multi-model deictic research analysis...")
    print("This will generate data across GPT-4o, Claude 3.5 Sonnet, and DeepSeek.")
    print()
    
    result = asyncio.run(generate_data_for_models())
    
    if result:
        print(f"\n🎯 SUCCESS: Multi-model data generated in {result}")
        print("\nYou can now:")
        print("1. Analyze model differences in the generated files")
        print("2. Compare ethical reasoning patterns across models")
        print("3. Study how different models handle deictic transformations")
    else:
        print("\n❌ FAILED: Check error messages above")

if __name__ == "__main__":
    main()