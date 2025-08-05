"""
Compare responses across different models (GPT-4o, Anthropic Claude, DeepSeek)
Analyzes differences in ethical reasoning, framing effects, and response patterns
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
from collections import defaultdict
import numpy as np
from dataclasses import dataclass
import re

@dataclass
class ModelComparison:
    """Store comparison results between models"""
    dilemma: str
    framing: str
    models: Dict[str, str]  # model_name: response
    similarities: Dict[str, float]  # pair: similarity_score
    differences: Dict[str, List[str]]  # pair: key_differences
    
class ModelResponseComparator:
    """Compare responses across different LLM models"""
    
    def __init__(self):
        self.models_data = {}
        self.comparison_results = []
        
    def load_model_responses(self, model_name: str, session_dir: Path) -> Dict[str, Dict[str, Any]]:
        """Load all responses from a model session"""
        responses = {}
        
        for response_file in session_dir.glob("*_responses.json"):
            dilemma_name = response_file.stem.replace("_responses", "")
            
            with open(response_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                responses[dilemma_name] = data
                
        return responses
    
    def extract_key_themes(self, response: str) -> List[str]:
        """Extract key ethical themes from a response"""
        themes = []
        
        # Common ethical frameworks
        ethical_frameworks = [
            "utilitarian", "deontological", "virtue ethics", "care ethics",
            "consequentialist", "duty-based", "rights-based", "justice"
        ]
        
        # Key decision indicators
        decision_patterns = [
            r"I (?:would|should|must) (\w+)",
            r"The (?:right|ethical|moral) (?:thing|action|choice) is to (\w+)",
            r"(?:decide|choose) to (\w+)"
        ]
        
        # Extract mentioned frameworks
        response_lower = response.lower()
        for framework in ethical_frameworks:
            if framework in response_lower:
                themes.append(f"framework:{framework}")
        
        # Extract decision patterns
        for pattern in decision_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches:
                themes.append(f"action:{match.lower()}")
        
        # Extract value mentions
        values = ["safety", "trust", "integrity", "loyalty", "justice", "fairness", "harm", "benefit"]
        for value in values:
            if value in response_lower:
                themes.append(f"value:{value}")
                
        return themes
    
    def calculate_response_similarity(self, response1: str, response2: str) -> float:
        """Calculate similarity between two responses"""
        # Extract themes from both responses
        themes1 = set(self.extract_key_themes(response1))
        themes2 = set(self.extract_key_themes(response2))
        
        # Calculate Jaccard similarity
        if not themes1 and not themes2:
            return 1.0
        if not themes1 or not themes2:
            return 0.0
            
        intersection = themes1.intersection(themes2)
        union = themes1.union(themes2)
        
        return len(intersection) / len(union)
    
    def analyze_framing_effects(self, model_responses: Dict[str, str]) -> Dict[str, Any]:
        """Analyze how different framings affect responses within a model"""
        framing_analysis = {
            "consistency_score": 0.0,
            "most_variable_framings": [],
            "most_consistent_framings": [],
            "framing_patterns": {}
        }
        
        # Compare all framing pairs
        framings = list(model_responses.keys())
        similarity_scores = {}
        
        for i, framing1 in enumerate(framings):
            for framing2 in framings[i+1:]:
                if framing1 in model_responses and framing2 in model_responses:
                    similarity = self.calculate_response_similarity(
                        model_responses[framing1],
                        model_responses[framing2]
                    )
                    similarity_scores[f"{framing1}-{framing2}"] = similarity
        
        # Calculate overall consistency
        if similarity_scores:
            framing_analysis["consistency_score"] = np.mean(list(similarity_scores.values()))
            
            # Find most/least consistent pairs
            sorted_pairs = sorted(similarity_scores.items(), key=lambda x: x[1])
            framing_analysis["most_variable_framings"] = sorted_pairs[:3]
            framing_analysis["most_consistent_framings"] = sorted_pairs[-3:]
        
        return framing_analysis
    
    def compare_models_on_dilemma(self, dilemma: str, framing: str) -> ModelComparison:
        """Compare all models on a specific dilemma and framing"""
        model_responses = {}
        
        # Collect responses from all models
        for model_name, model_data in self.models_data.items():
            if dilemma in model_data:
                framing_data = model_data[dilemma].get(framing, {})
                if "response" in framing_data:
                    model_responses[model_name] = framing_data["response"]
        
        # Calculate pairwise similarities
        similarities = {}
        differences = {}
        
        model_names = list(model_responses.keys())
        for i, model1 in enumerate(model_names):
            for model2 in model_names[i+1:]:
                pair_key = f"{model1}-{model2}"
                
                # Calculate similarity
                similarities[pair_key] = self.calculate_response_similarity(
                    model_responses[model1],
                    model_responses[model2]
                )
                
                # Identify key differences
                themes1 = set(self.extract_key_themes(model_responses[model1]))
                themes2 = set(self.extract_key_themes(model_responses[model2]))
                
                unique_to_model1 = themes1 - themes2
                unique_to_model2 = themes2 - themes1
                
                differences[pair_key] = {
                    f"unique_to_{model1}": list(unique_to_model1),
                    f"unique_to_{model2}": list(unique_to_model2)
                }
        
        return ModelComparison(
            dilemma=dilemma,
            framing=framing,
            models=model_responses,
            similarities=similarities,
            differences=differences
        )
    
    def generate_comparison_report(self, output_dir: Path):
        """Generate comprehensive comparison report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = output_dir / f"model_comparison_{timestamp}"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Overall comparison metrics
        overall_metrics = {
            "models_compared": list(self.models_data.keys()),
            "total_comparisons": len(self.comparison_results),
            "average_similarity": {},
            "framing_consistency": {},
            "model_characteristics": {}
        }
        
        # Calculate average similarities between model pairs
        model_pairs_similarity = defaultdict(list)
        for comparison in self.comparison_results:
            for pair, similarity in comparison.similarities.items():
                model_pairs_similarity[pair].append(similarity)
        
        for pair, similarities in model_pairs_similarity.items():
            overall_metrics["average_similarity"][pair] = np.mean(similarities)
        
        # Analyze framing consistency for each model
        for model_name, model_data in self.models_data.items():
            framing_scores = []
            for dilemma, responses in model_data.items():
                if isinstance(responses, dict) and any("response" in v for v in responses.values() if isinstance(v, dict)):
                    # Extract actual responses
                    actual_responses = {}
                    for framing, data in responses.items():
                        if isinstance(data, dict) and "response" in data:
                            actual_responses[framing] = data["response"]
                    
                    if actual_responses:
                        analysis = self.analyze_framing_effects(actual_responses)
                        framing_scores.append(analysis["consistency_score"])
            
            if framing_scores:
                overall_metrics["framing_consistency"][model_name] = np.mean(framing_scores)
        
        # Generate detailed comparison CSV
        comparison_data = []
        for comp in self.comparison_results:
            for pair, similarity in comp.similarities.items():
                models = pair.split("-")
                comparison_data.append({
                    "dilemma": comp.dilemma,
                    "framing": comp.framing,
                    "model1": models[0],
                    "model2": models[1],
                    "similarity_score": similarity,
                    "response_length_model1": len(comp.models.get(models[0], "")),
                    "response_length_model2": len(comp.models.get(models[1], ""))
                })
        
        df = pd.DataFrame(comparison_data)
        df.to_csv(report_dir / "detailed_comparisons.csv", index=False)
        
        # Generate summary report
        summary_report = f"""# Model Comparison Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Models Compared
{', '.join(overall_metrics['models_compared'])}

## Overall Similarity Scores
Average similarity between model pairs:
"""
        for pair, avg_sim in sorted(overall_metrics['average_similarity'].items(), key=lambda x: x[1], reverse=True):
            summary_report += f"\n- {pair}: {avg_sim:.3f}"
        
        summary_report += f"\n\n## Framing Consistency\nHow consistent each model is across different framings:\n"
        for model, consistency in sorted(overall_metrics['framing_consistency'].items(), key=lambda x: x[1], reverse=True):
            summary_report += f"\n- {model}: {consistency:.3f}"
        
        # Add most different responses
        summary_report += "\n\n## Most Different Responses\n"
        most_different = sorted(comparison_data, key=lambda x: x['similarity_score'])[:5]
        for diff in most_different:
            summary_report += f"\n- {diff['dilemma']} ({diff['framing']}): {diff['model1']} vs {diff['model2']} - Similarity: {diff['similarity_score']:.3f}"
        
        # Add most similar responses
        summary_report += "\n\n## Most Similar Responses\n"
        most_similar = sorted(comparison_data, key=lambda x: x['similarity_score'], reverse=True)[:5]
        for sim in most_similar:
            summary_report += f"\n- {sim['dilemma']} ({sim['framing']}): {sim['model1']} vs {sim['model2']} - Similarity: {sim['similarity_score']:.3f}"
        
        # Save reports
        with open(report_dir / "summary_report.md", 'w', encoding='utf-8') as f:
            f.write(summary_report)
        
        # Save detailed metrics
        with open(report_dir / "overall_metrics.json", 'w', encoding='utf-8') as f:
            json.dump(overall_metrics, f, indent=2)
        
        print(f"\n[SUCCESS] Comparison report saved to: {report_dir}")
        return report_dir

async def main():
    """Run model comparison analysis"""
    print("\n" + "="*60)
    print("MODEL RESPONSE COMPARISON ANALYSIS")
    print("="*60)
    
    comparator = ModelResponseComparator()
    
    # Define model sessions to compare
    generation_logs_dir = Path("deixis_analysis_pipeline/generation_logs")
    
    model_sessions = {
        "gpt-4o": "multi_dilemma_20250804_170010",  # Original GPT-4o run
        "anthropic-claude": "anthropic_claude_20250805_125046",  # Anthropic run
        "deepseek": "deepseek_20250805_143544"  # Latest DeepSeek run (update if needed)
    }
    
    # Load responses from each model
    print("\n[LOADING] Loading model responses...")
    for model_name, session_name in model_sessions.items():
        session_dir = generation_logs_dir / session_name
        if session_dir.exists():
            responses = comparator.load_model_responses(model_name, session_dir)
            comparator.models_data[model_name] = responses
            print(f"[OK] Loaded {model_name} responses from {session_name}")
        else:
            print(f"[SKIP] Session directory not found: {session_dir}")
    
    if len(comparator.models_data) < 2:
        print("[ERROR] Need at least 2 models to compare")
        return
    
    # Perform comparisons
    print("\n[COMPARING] Analyzing responses across models...")
    
    # Get all dilemmas and framings
    all_dilemmas = set()
    all_framings = set()
    
    for model_data in comparator.models_data.values():
        for dilemma, responses in model_data.items():
            all_dilemmas.add(dilemma)
            if isinstance(responses, dict):
                for framing in responses.keys():
                    if isinstance(responses[framing], dict) and "response" in responses[framing]:
                        all_framings.add(framing)
    
    # Compare each dilemma/framing combination
    for dilemma in sorted(all_dilemmas):
        for framing in sorted(all_framings):
            comparison = comparator.compare_models_on_dilemma(dilemma, framing)
            if len(comparison.models) >= 2:  # Only add if we have at least 2 models to compare
                comparator.comparison_results.append(comparison)
    
    print(f"[OK] Completed {len(comparator.comparison_results)} comparisons")
    
    # Generate report
    output_dir = Path("deixis_analysis_pipeline/automated_analysis_results")
    report_dir = comparator.generate_comparison_report(output_dir)
    
    print("\n" + "="*60)
    print("COMPARISON ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())