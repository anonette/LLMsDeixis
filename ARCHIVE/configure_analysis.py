"""
Interactive Analysis Configuration
Choose models, generate logs first, and control the analysis process
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from deixis_ethical_analyzer import DeicticEthicalAnalyzer, EthicalDilemmaDatabase
from models.schemas import DeicticFraming

def display_available_models():
    """Display available OpenRouter models."""
    models = {
        "1": {
            "name": "GPT-4o",
            "id": "openai/gpt-4o",
            "description": "OpenAI's most capable model, excellent for complex reasoning"
        },
        "2": {
            "name": "Claude 3.5 Sonnet", 
            "id": "anthropic/claude-3.5-sonnet",
            "description": "Anthropic's flagship model, great for nuanced analysis"
        },
        "3": {
            "name": "GPT-4o Mini",
            "id": "openai/gpt-4o-mini", 
            "description": "Faster, cheaper version of GPT-4o"
        },
        "4": {
            "name": "Claude 3 Haiku",
            "id": "anthropic/claude-3-haiku",
            "description": "Fast and efficient Claude model"
        },
        "5": {
            "name": "Gemini Pro",
            "id": "google/gemini-pro",
            "description": "Google's advanced language model"
        },
        "6": {
            "name": "DeepSeek Chat",
            "id": "deepseek/deepseek-chat",
            "description": "High-performance model with good reasoning"
        }
    }
    
    print("\n🤖 AVAILABLE MODELS:")
    print("=" * 60)
    for key, model in models.items():
        print(f"{key}. {model['name']} ({model['id']})")
        print(f"   {model['description']}")
        print()
    
    return models

def select_models():
    """Let user select which models to use."""
    models = display_available_models()
    
    print("📝 SELECT MODELS TO USE:")
    print("Enter numbers separated by commas (e.g., 1,2,3) or 'all' for all models")
    
    choice = input("Your choice: ").strip().lower()
    
    if choice == 'all':
        selected = list(models.values())
    else:
        try:
            numbers = [n.strip() for n in choice.split(',')]
            selected = [models[n] for n in numbers if n in models]
        except KeyError:
            print("❌ Invalid selection. Using GPT-4o as default.")
            selected = [models["1"]]
    
    print(f"\n✅ Selected {len(selected)} models:")
    for model in selected:
        print(f"   • {model['name']}")
    
    return selected

def select_dilemmas():
    """Let user select which dilemmas to analyze."""
    db = EthicalDilemmaDatabase()
    dilemmas = db.get_all_dilemmas()
    
    print("\n📋 AVAILABLE ETHICAL DILEMMAS:")
    print("=" * 60)
    for i, dilemma in enumerate(dilemmas, 1):
        print(f"{i}. {dilemma.title}")
        print(f"   Domain: {dilemma.domain} | Complexity: {dilemma.complexity_score}/10")
        print(f"   {dilemma.description[:100]}...")
        print()
    
    print("📝 SELECT DILEMMAS TO ANALYZE:")
    print("Enter numbers separated by commas (e.g., 1,2,3) or 'all' for all dilemmas")
    
    choice = input("Your choice: ").strip().lower()
    
    if choice == 'all':
        selected = dilemmas
    else:
        try:
            numbers = [int(n.strip()) for n in choice.split(',')]
            selected = [dilemmas[n-1] for n in numbers if 1 <= n <= len(dilemmas)]
        except (ValueError, IndexError):
            print("❌ Invalid selection. Using first dilemma as default.")
            selected = [dilemmas[0]]
    
    print(f"\n✅ Selected {len(selected)} dilemmas:")
    for dilemma in selected:
        print(f"   • {dilemma.title}")
    
    return selected

def select_frameworks():
    """Let user select which deictic frameworks to use."""
    frameworks = list(DeicticFraming)
    
    print("\n🎯 AVAILABLE DEICTIC FRAMEWORKS:")
    print("=" * 60)
    for i, framework in enumerate(frameworks, 1):
        descriptions = {
            DeicticFraming.IMPERSONAL: "Objective, neutral perspective removing personal agency",
            DeicticFraming.SECOND_PERSON: "Direct address making 'you' the decision-maker", 
            DeicticFraming.FIRST_PERSON: "Personal 'I' perspective as the decision-maker",
            DeicticFraming.REFLEXIVE: "Perspective-taking and role reversal",
            DeicticFraming.DIALOGIC: "Collective 'we' decision-making",
            DeicticFraming.SPATIAL: "Physical positioning and embodied perspective",
            DeicticFraming.TEMPORAL: "Time urgency and critical moments",
            DeicticFraming.COSMOLOGICAL: "Universal, spiritual, cosmic perspective"
        }
        print(f"{i}. {framework.value.replace('_', ' ').title()}")
        print(f"   {descriptions[framework]}")
        print()
    
    print("📝 SELECT FRAMEWORKS TO USE:")
    print("Enter numbers separated by commas (e.g., 1,2,3) or 'all' for all frameworks")
    
    choice = input("Your choice: ").strip().lower()
    
    if choice == 'all':
        selected = frameworks
    else:
        try:
            numbers = [int(n.strip()) for n in choice.split(',')]
            selected = [frameworks[n-1] for n in numbers if 1 <= n <= len(frameworks)]
        except (ValueError, IndexError):
            print("❌ Invalid selection. Using first 3 frameworks as default.")
            selected = frameworks[:3]
    
    print(f"\n✅ Selected {len(selected)} frameworks:")
    for framework in selected:
        print(f"   • {framework.value.replace('_', ' ').title()}")
    
    return selected

async def generate_step_by_step_analysis(models, dilemmas, frameworks):
    """Generate analysis step by step with full logging."""
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("configured_analysis_results") / f"session_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Results will be saved to: {output_dir}")
    
    # Save configuration
    config = {
        "timestamp": timestamp,
        "models": [{"name": m["name"], "id": m["id"]} for m in models],
        "dilemmas": [{"id": d.id, "title": d.title} for d in dilemmas],
        "frameworks": [f.value for f in frameworks],
        "total_analyses": len(models) * len(dilemmas) * len(frameworks)
    }
    
    with open(output_dir / "analysis_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n🔄 STARTING STEP-BY-STEP ANALYSIS:")
    print(f"   Models: {len(models)}")
    print(f"   Dilemmas: {len(dilemmas)}")  
    print(f"   Frameworks: {len(frameworks)}")
    print(f"   Total Analyses: {config['total_analyses']}")
    print()
    
    all_results = {}
    analysis_log = []
    
    for model_idx, model in enumerate(models, 1):
        print(f"🤖 MODEL {model_idx}/{len(models)}: {model['name']}")
        print("-" * 50)
        
        # Initialize analyzer with specific model
        analyzer = DeicticEthicalAnalyzer(
            model=model["id"],
            enable_rich_logging=True,
            output_dir=str(output_dir)
        )
        
        model_results = {}
        
        for dilemma_idx, dilemma in enumerate(dilemmas, 1):
            print(f"  📋 Dilemma {dilemma_idx}/{len(dilemmas)}: {dilemma.title}")
            
            dilemma_results = {}
            
            for framework_idx, framework in enumerate(frameworks, 1):
                print(f"    🎯 Framework {framework_idx}/{len(frameworks)}: {framework.value}")
                
                try:
                    # Generate single analysis
                    result = await analyzer.analyze_single_dilemma_and_framework(
                        dilemma.id, framework
                    )
                    
                    dilemma_results[framework.value] = result.to_dict()
                    
                    # Log this analysis
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "model": model["name"],
                        "model_id": model["id"],
                        "dilemma": dilemma.title,
                        "dilemma_id": dilemma.id,
                        "framework": framework.value,
                        "success": True,
                        "response_length": len(result.llm_response),
                        "processing_time": result.processing_time,
                        "deictic_markers_count": result.total_markers
                    }
                    analysis_log.append(log_entry)
                    
                    print(f"      ✅ Success ({len(result.llm_response)} chars, {result.processing_time:.1f}s)")
                    
                    # Save individual result immediately
                    result_file = output_dir / f"result_{model['name'].replace(' ', '_')}_{dilemma.id}_{framework.value}.json"
                    with open(result_file, 'w') as f:
                        json.dump(result.to_dict(), f, indent=2, default=str)
                        
                except Exception as e:
                    print(f"      ❌ Error: {str(e)}")
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "model": model["name"],
                        "model_id": model["id"],
                        "dilemma": dilemma.title,
                        "dilemma_id": dilemma.id,
                        "framework": framework.value,
                        "success": False,
                        "error": str(e)
                    }
                    analysis_log.append(log_entry)
                
                # Save log after each analysis
                with open(output_dir / "analysis_log.json", 'w') as f:
                    json.dump(analysis_log, f, indent=2)
            
            model_results[dilemma.id] = dilemma_results
            print()
        
        all_results[model["name"]] = model_results
        
        # Save model results
        with open(output_dir / f"results_{model['name'].replace(' ', '_')}.json", 'w') as f:
            json.dump(model_results, f, indent=2, default=str)
        
        print(f"✅ Completed model: {model['name']}")
        print()
    
    # Save complete results
    with open(output_dir / "complete_results.json", 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    # Generate summary
    successful_analyses = len([log for log in analysis_log if log.get('success', False)])
    total_analyses = len(analysis_log)
    
    summary = {
        "session_info": {
            "timestamp": timestamp,
            "configuration": config,
            "total_analyses": total_analyses,
            "successful_analyses": successful_analyses,
            "success_rate": successful_analyses / total_analyses if total_analyses > 0 else 0,
            "output_directory": str(output_dir)
        },
        "model_performance": {},
        "analysis_log": analysis_log
    }
    
    # Calculate per-model performance
    for model in models:
        model_logs = [log for log in analysis_log if log.get('model') == model['name']]
        successful = len([log for log in model_logs if log.get('success', False)])
        total = len(model_logs)
        
        summary["model_performance"][model['name']] = {
            "total_analyses": total,
            "successful_analyses": successful,
            "success_rate": successful / total if total > 0 else 0,
            "avg_response_length": sum(log.get('response_length', 0) for log in model_logs if log.get('success', False)) / max(1, successful),
            "avg_processing_time": sum(log.get('processing_time', 0) for log in model_logs if log.get('success', False)) / max(1, successful)
        }
    
    with open(output_dir / "analysis_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("🎉 ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"📊 Results: {successful_analyses}/{total_analyses} successful analyses")
    print(f"📁 Saved to: {output_dir}")
    print()
    print("📄 Generated Files:")
    print("  • analysis_config.json - Your configuration settings")
    print("  • analysis_log.json - Detailed log of all analyses") 
    print("  • complete_results.json - All analysis results")
    print("  • analysis_summary.json - Performance summary")
    print("  • results_[ModelName].json - Results per model")
    print("  • result_[Model]_[Dilemma]_[Framework].json - Individual results")
    
    return output_dir, summary

def main():
    """Main configuration and analysis function."""
    print("🔬 DEICTIC RESEARCH CONFIGURATION")
    print("=" * 60)
    print("Configure your analysis step by step:")
    print("1. Choose models to use")
    print("2. Select ethical dilemmas")
    print("3. Pick deictic frameworks")
    print("4. Generate analysis with full logging")
    print()
    
    # Step 1: Select models
    models = select_models()
    
    # Step 2: Select dilemmas
    dilemmas = select_dilemmas()
    
    # Step 3: Select frameworks
    frameworks = select_frameworks()
    
    # Confirmation
    total_analyses = len(models) * len(dilemmas) * len(frameworks)
    print(f"\n📊 ANALYSIS PLAN:")
    print(f"   Models: {len(models)}")
    print(f"   Dilemmas: {len(dilemmas)}")
    print(f"   Frameworks: {len(frameworks)}")
    print(f"   Total Analyses: {total_analyses}")
    print(f"   Estimated Time: {total_analyses * 2} - {total_analyses * 4} minutes")
    print()
    
    confirm = input("🚀 Proceed with analysis? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Analysis cancelled.")
        return
    
    # Run analysis
    print("\n🔄 Starting analysis...")
    output_dir, summary = asyncio.run(generate_step_by_step_analysis(models, dilemmas, frameworks))
    
    print(f"\n✨ Analysis complete! Check {output_dir} for all results.")

if __name__ == "__main__":
    main()
