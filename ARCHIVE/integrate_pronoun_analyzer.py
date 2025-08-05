"""
Integration module to connect the pronoun agency analyzer with the deixis ethical analyzer.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
import pandas as pd
from pronoun_agency_analyzer import PronounAgencyAnalyzer
from models.schemas import DeicticAnalysisResult


class DeixisPronounIntegration:
    """Integrates pronoun agency analysis with existing deixis analysis results."""
    
    def __init__(self):
        self.pronoun_analyzer = PronounAgencyAnalyzer()
        
    def analyze_existing_results(self, results_path: str) -> pd.DataFrame:
        """
        Analyze pronoun usage in existing deixis analysis results.
        
        Args:
            results_path: Path to JSON file with deixis analysis results
            
        Returns:
            DataFrame with pronoun analysis results
        """
        # Load existing results
        with open(results_path, 'r') as f:
            data = json.load(f)
        
        # Extract texts with their framings
        corpus_data = []
        
        if isinstance(data, list):
            # List of results
            for item in data:
                if 'llm_response' in item and 'framing' in item:
                    corpus_data.append({
                        'text': item['llm_response'],
                        'id': f"{item.get('dilemma_id', 'unknown')}_{item['framing']}",
                        'framing': item['framing']
                    })
        elif isinstance(data, dict) and 'results' in data:
            # Results in a 'results' key
            for item in data['results']:
                if 'llm_response' in item and 'framing' in item:
                    corpus_data.append({
                        'text': item['llm_response'],
                        'id': f"{item.get('dilemma_id', 'unknown')}_{item['framing']}",
                        'framing': item['framing']
                    })
        
        # Analyze the corpus
        texts = [(item['text'], item['id'], item['framing']) for item in corpus_data]
        df = self.pronoun_analyzer.analyze_corpus(texts)
        
        return df
    
    def enhance_deixis_analyzer(self):
        """
        Create an enhanced version of analyze_deictic_markers that includes
        pronoun agency analysis.
        """
        def analyze_deictic_markers_enhanced(response_text: str) -> Dict[str, any]:
            """Enhanced deictic marker analysis including pronoun agency metrics."""
            
            # Get basic pronoun analysis
            analysis = self.pronoun_analyzer.analyze_text(response_text)
            
            # Format for compatibility with existing system
            enhanced_markers = {
                # Original deictic marker categories
                "first_person_singular": analysis.pronoun_counts['first_singular'],
                "first_person_plural": analysis.pronoun_counts['first_plural'],
                "second_person": analysis.pronoun_counts['second_person'],
                "third_person": analysis.pronoun_counts['third_person'],
                
                # New agency-focused metrics
                "agency_concentration": analysis.agency_concentration,
                "agency_type": analysis.agency_type,
                "total_pronouns": analysis.total_pronouns,
                
                # Pronoun ratios for detailed analysis
                "pronoun_ratios": analysis.pronoun_ratios,
                
                # Agency distribution
                "individual_agency_ratio": (
                    analysis.pronoun_ratios['first_singular'] + 
                    analysis.pronoun_ratios['second_person']
                ),
                "collective_agency_ratio": analysis.pronoun_ratios['first_plural'],
                "abstract_agency_ratio": (
                    analysis.pronoun_ratios['third_person'] + 
                    analysis.pronoun_ratios['impersonal']
                ),
                
                # Keep total for compatibility
                "total_markers": analysis.total_pronouns
            }
            
            return enhanced_markers
        
        return analyze_deictic_markers_enhanced
    
    def generate_agency_report(self, df: pd.DataFrame, output_path: Optional[str] = None) -> str:
        """
        Generate a comprehensive agency analysis report.
        
        Args:
            df: DataFrame with pronoun analysis results
            output_path: Optional path to save the report
            
        Returns:
            Report text
        """
        report = self.pronoun_analyzer.generate_report(df)
        
        # Add research-specific insights
        report += "\n## Research Implications\n\n"
        report += "### RQ: How do deixis-based prompting techniques influence agency distribution?\n\n"
        
        # Analyze agency shifts
        comparisons = self.pronoun_analyzer.compare_framings(df)
        
        # Find framings with most dramatic shifts
        ratio_data = comparisons['avg_ratios']
        
        # Calculate variance across framings for each pronoun type
        variances = ratio_data.var()
        most_variable = variances.idxmax()
        
        report += f"- **Most variable pronoun category**: {most_variable.replace('_ratio', '').replace('_', ' ').title()}\n"
        report += f"  - This suggests {most_variable} usage is most sensitive to deictic framing\n\n"
        
        # Agency concentration insights
        conc_data = comparisons['agency_concentration']
        most_concentrated = conc_data['mean'].idxmax()
        most_distributed = conc_data['mean'].idxmin()
        
        report += f"- **Most concentrated agency**: {most_concentrated} framing\n"
        report += f"- **Most distributed agency**: {most_distributed} framing\n"
        report += f"- **Range**: {conc_data['mean'].max() - conc_data['mean'].min():.3f}\n\n"
        
        # Save if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
        
        return report


# Monkey patch function to add to existing transformer
def add_pronoun_analysis_to_transformer(transformer_instance):
    """
    Add pronoun agency analysis capabilities to an existing transformer instance.
    
    Args:
        transformer_instance: Instance of DeicticTransformer
    """
    integration = DeixisPronounIntegration()
    
    # Store original method
    original_analyze = transformer_instance.analyze_deictic_markers
    
    # Create enhanced method
    def analyze_deictic_markers_with_agency(response_text: str) -> Dict[str, any]:
        # Get original analysis
        original_results = original_analyze(response_text)
        
        # Get pronoun agency analysis
        pronoun_analysis = integration.pronoun_analyzer.analyze_text(response_text)
        
        # Merge results
        original_results.update({
            "agency_concentration": pronoun_analysis.agency_concentration,
            "agency_type": pronoun_analysis.agency_type,
            "pronoun_ratios": pronoun_analysis.pronoun_ratios,
            "individual_agency_ratio": (
                pronoun_analysis.pronoun_ratios['first_singular'] + 
                pronoun_analysis.pronoun_ratios['second_person']
            ),
            "collective_agency_ratio": pronoun_analysis.pronoun_ratios['first_plural'],
            "abstract_agency_ratio": (
                pronoun_analysis.pronoun_ratios['third_person'] + 
                pronoun_analysis.pronoun_ratios['impersonal']
            )
        })
        
        return original_results
    
    # Replace method
    transformer_instance.analyze_deictic_markers = analyze_deictic_markers_with_agency
    
    return transformer_instance


# Example usage
if __name__ == "__main__":
    # Example of analyzing existing results
    integration = DeixisPronounIntegration()
    
    # Path to your existing results
    results_path = "automated_analysis_results/latest_session/all_results.json"
    
    if Path(results_path).exists():
        df = integration.analyze_existing_results(results_path)
        report = integration.generate_agency_report(df, "pronoun_agency_report.md")
        print("Analysis complete! Report saved to pronoun_agency_report.md")
        
        # Generate visualizations
        integration.pronoun_analyzer.visualize_agency_distribution(
            df, "agency_distribution_plots.png"
        )
    else:
        print(f"Results file not found at {results_path}")
        print("Creating example analysis...")
        
        # Example data
        example_data = [
            {
                'text': "I must report this issue to protect the users.",
                'id': "example_1_first_person",
                'framing': "first_person"
            },
            {
                'text': "You should consider the consequences before deciding.",
                'id': "example_1_second_person", 
                'framing': "second_person"
            },
            {
                'text': "We need to work together to find a solution.",
                'id': "example_1_dialogic",
                'framing': "dialogic"
            },
            {
                'text': "One must weigh the options carefully in such situations.",
                'id': "example_1_impersonal",
                'framing': "impersonal"
            }
        ]
        
        texts = [(item['text'], item['id'], item['framing']) for item in example_data]
        df = integration.pronoun_analyzer.analyze_corpus(texts)
        
        print("\nExample Analysis Results:")
        print(df[['framing', 'agency_type', 'agency_concentration']].to_string())