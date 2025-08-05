"""
Model-Specific Analysis Runner
Executes complete deixis analysis separately for each model
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import argparse
import sys

from deixis_ethical_analyzer_single_model import SingleModelDeicticAnalyzer
from dilemma_generator import DilemmaGenerator
from pronoun_agency_analyzer import PronounAgencyAnalyzer
from ethical_consistency_analyzer import EthicalConsistencyAnalyzer
from final_report_generator import FinalReportGenerator
from llm_client import validate_environment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Models to analyze
MODELS = ["gpt-4o", "claude-3.5-sonnet", "deepseek-chat"]


class ModelSpecificAnalysisRunner:
    """Runs complete analysis for each model separately."""
    
    def __init__(self, output_base_dir: str = "automated_analysis_results"):
        self.output_base_dir = Path(output_base_dir)
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.dilemma_generator = DilemmaGenerator()
        self.pronoun_analyzer = PronounAgencyAnalyzer()
        self.consistency_analyzer = EthicalConsistencyAnalyzer()
        
        # Track results for cross-model comparison
        self.all_model_results = {}
    
    async def run_single_model_analysis(self, model_name: str, 
                                      dilemmas: List[Dict[str, Any]],
                                      num_dilemmas: int = 5) -> Dict[str, Any]:
        """
        Run complete analysis for a single model.
        
        Args:
            model_name: Name of the model to use
            dilemmas: List of dilemmas to analyze
            num_dilemmas: Number of dilemmas to analyze
            
        Returns:
            Complete analysis results for the model
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting analysis with {model_name}")
        logger.info(f"{'='*60}\n")
        
        # Create analyzer for this model
        analyzer = SingleModelDeicticAnalyzer(
            model_name=model_name,
            enable_rich_logging=True,
            output_dir=str(self.output_base_dir)
        )
        
        # Analyze dilemmas
        analysis_results = []
        for i, dilemma in enumerate(dilemmas[:num_dilemmas]):
            logger.info(f"\nAnalyzing dilemma {i+1}/{num_dilemmas}: {dilemma['title']}")
            
            try:
                result = await analyzer.analyze_dilemma(dilemma)
                analysis_results.append(result)
                
                # Add pronoun analysis
                for framing, response_data in result['responses'].items():
                    pronoun_analysis = self.pronoun_analyzer.analyze_response(
                        response_data['response']
                    )
                    response_data['pronoun_analysis'] = pronoun_analysis
                
            except Exception as e:
                logger.error(f"Error analyzing dilemma {dilemma['id']}: {e}")
                continue
        
        # Perform consistency analysis
        logger.info(f"\nPerforming consistency analysis for {model_name}...")
        # Extract responses for consistency analysis
        all_responses = []
        for result in analysis_results:
            for framing, response_data in result['responses'].items():
                all_responses.append({
                    'dilemma_id': result['dilemma_id'],
                    'framing': framing,
                    'response': response_data['response'],
                    'ethical_framing': response_data.get('ethical_framing', {}),
                    'agency_analysis': response_data.get('agency_analysis', {})
                })
        
        consistency_results = self.consistency_analyzer.analyze_consistency(all_responses)
        
        # Generate model-specific report
        logger.info(f"\nGenerating report for {model_name}...")
        report_generator = FinalReportGenerator(
            session_dir=analyzer.rich_logger.session_dir if hasattr(analyzer, 'rich_logger') else None
        )
        
        # Prepare session data with model info
        session_data = {
            'model_name': model_name,
            'model_info': analyzer.llm_agent.get_model_info(),
            'analysis_results': analysis_results,
            'consistency_analysis': consistency_results,
            'pronoun_analysis_summary': self._generate_pronoun_summary(analysis_results),
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate report
        report_path = report_generator.generate_comprehensive_report(
            session_data=session_data,
            output_filename=f"REPORT_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        # Finalize session
        analyzer.finalize_session()
        
        # Store results for cross-model comparison
        self.all_model_results[model_name] = {
            'session_data': session_data,
            'report_path': report_path,
            'session_dir': str(analyzer.rich_logger.session_dir) if hasattr(analyzer, 'rich_logger') else None
        }
        
        logger.info(f"\n✓ Completed analysis for {model_name}")
        logger.info(f"  Report: {report_path}")
        
        return session_data
    
    def _generate_pronoun_summary(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of pronoun analysis across all dilemmas."""
        all_analyses = []
        
        for result in analysis_results:
            for framing, response_data in result['responses'].items():
                if 'pronoun_analysis' in response_data:
                    analysis = response_data['pronoun_analysis']
                    analysis['framing'] = framing
                    analysis['dilemma_id'] = result['dilemma_id']
                    all_analyses.append(analysis)
        
        if not all_analyses:
            return {}
        
        # Calculate aggregate statistics
        return {
            'total_responses_analyzed': len(all_analyses),
            'average_agency_concentration': sum(a['agency_concentration'] for a in all_analyses) / len(all_analyses),
            'agency_type_distribution': self._calculate_agency_distribution(all_analyses),
            'pronoun_usage_patterns': self._calculate_pronoun_patterns(all_analyses)
        }
    
    def _calculate_agency_distribution(self, analyses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate distribution of agency types."""
        types = [a['agency_type'] for a in analyses]
        total = len(types)
        
        distribution = {}
        for agency_type in set(types):
            count = types.count(agency_type)
            distribution[agency_type] = count / total
        
        return distribution
    
    def _calculate_pronoun_patterns(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate pronoun usage patterns."""
        patterns = {
            'i': [],
            'you': [],
            'we': [],
            'they': [],
            'one': []
        }
        
        for analysis in analyses:
            ratios = analysis['pronoun_ratios']
            for pronoun, ratio in ratios.items():
                if pronoun in patterns:
                    patterns[pronoun].append(ratio)
        
        # Calculate averages
        avg_patterns = {}
        for pronoun, values in patterns.items():
            if values:
                avg_patterns[pronoun] = sum(values) / len(values)
            else:
                avg_patterns[pronoun] = 0.0
        
        return avg_patterns
    
    async def run_all_models(self, num_dilemmas: int = 10) -> Dict[str, Any]:
        """
        Run analysis for all configured models.
        
        Args:
            num_dilemmas: Number of dilemmas to analyze per model
            
        Returns:
            Combined results from all models
        """
        # Validate environment
        try:
            validate_environment()
        except Exception as e:
            logger.error(f"Environment validation failed: {e}")
            return {}
        
        # Generate dilemmas once for all models
        logger.info(f"Loading {num_dilemmas} dilemmas for analysis...")
        dilemmas = self.dilemma_generator.generate_dilemmas(count=num_dilemmas)
        
        # Save dilemmas for reference
        dilemmas_path = self.output_base_dir / "analyzed_dilemmas.json"
        with open(dilemmas_path, 'w') as f:
            json.dump(dilemmas, f, indent=2)
        logger.info(f"Saved dilemmas to {dilemmas_path}")
        
        # Run analysis for each model
        for model_name in MODELS:
            try:
                await self.run_single_model_analysis(model_name, dilemmas, num_dilemmas)
            except Exception as e:
                logger.error(f"Failed to analyze with {model_name}: {e}")
                continue
        
        # Generate cross-model comparison report
        if len(self.all_model_results) > 1:
            logger.info("\nGenerating cross-model comparison report...")
            self._generate_comparison_report()
        
        return self.all_model_results
    
    def _generate_comparison_report(self):
        """Generate a report comparing results across all models."""
        comparison_path = self.output_base_dir / f"MODEL_COMPARISON_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(comparison_path, 'w') as f:
            f.write("# Cross-Model Deixis Analysis Comparison\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Models Analyzed\n\n")
            for model_name in self.all_model_results:
                model_info = self.all_model_results[model_name]['session_data']['model_info']
                f.write(f"- **{model_name}**: {model_info.get('provider', 'Unknown')} - "
                       f"{model_info.get('description', 'No description')}\n")
            
            f.write("\n## Pronoun Usage Comparison\n\n")
            f.write("| Model | I | You | We | They | One |\n")
            f.write("|-------|---|-----|----|----|-----|\n")
            
            for model_name, results in self.all_model_results.items():
                summary = results['session_data'].get('pronoun_analysis_summary', {})
                patterns = summary.get('pronoun_usage_patterns', {})
                
                f.write(f"| {model_name} | "
                       f"{patterns.get('i', 0):.3f} | "
                       f"{patterns.get('you', 0):.3f} | "
                       f"{patterns.get('we', 0):.3f} | "
                       f"{patterns.get('they', 0):.3f} | "
                       f"{patterns.get('one', 0):.3f} |\n")
            
            f.write("\n## Agency Distribution Comparison\n\n")
            for model_name, results in self.all_model_results.items():
                f.write(f"\n### {model_name}\n")
                summary = results['session_data'].get('pronoun_analysis_summary', {})
                distribution = summary.get('agency_type_distribution', {})
                
                for agency_type, percentage in distribution.items():
                    f.write(f"- {agency_type}: {percentage:.1%}\n")
            
            f.write("\n## Ethical Consistency Comparison\n\n")
            for model_name, results in self.all_model_results.items():
                f.write(f"\n### {model_name}\n")
                consistency = results['session_data'].get('consistency_analysis', {})
                
                if consistency:
                    f.write(f"- Overall Consistency: {consistency.get('overall_consistency', 0):.3f}\n")
                    f.write(f"- Framework Stability: {consistency.get('framework_stability', 0):.3f}\n")
                    f.write(f"- Reasoning Coherence: {consistency.get('reasoning_coherence', 0):.3f}\n")
            
            f.write("\n## Individual Model Reports\n\n")
            for model_name, results in self.all_model_results.items():
                f.write(f"- [{model_name} Report]({results['report_path']})\n")
        
        logger.info(f"Cross-model comparison report saved to: {comparison_path}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run model-specific deixis analysis")
    parser.add_argument(
        "--num-dilemmas",
        type=int,
        default=10,
        help="Number of dilemmas to analyze (default: 10, max: 10)"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        choices=MODELS,
        default=MODELS,
        help="Models to analyze (default: all)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="automated_analysis_results",
        help="Output directory for results"
    )
    
    args = parser.parse_args()
    
    # Update models list if specific models requested
    models_to_run = args.models if args.models else MODELS
    
    # Run analysis with specified models
    runner = ModelSpecificAnalysisRunner(output_base_dir=args.output_dir)
    
    # Temporarily update MODELS for this run
    original_models = MODELS[:]
    MODELS[:] = models_to_run
    
    try:
        results = await runner.run_all_models(num_dilemmas=args.num_dilemmas)
    finally:
        # Restore original MODELS
        MODELS[:] = original_models
    
    if results:
        logger.info("\n" + "="*60)
        logger.info("All analyses completed successfully!")
        logger.info("="*60)
    else:
        logger.error("\nAnalysis failed - no results generated")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())