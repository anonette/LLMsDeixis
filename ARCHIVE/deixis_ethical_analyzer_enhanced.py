"""
Enhanced Deixis Ethical Analyzer with Pronoun Agency Analysis
Analyzes ethical dilemmas through multiple deictic framings and tracks agency distribution.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
from pathlib import Path

# Import the original analyzer components
from deixis_ethical_analyzer import (
    DeixisEthicalAnalyzer as OriginalAnalyzer,
    analyze_deictic_markers as original_analyze_markers
)

# Import pronoun agency components
from pronoun_agency_analyzer import PronounAgencyAnalyzer
from integrate_pronoun_analyzer import DeixisPronounIntegration


class EnhancedDeixisEthicalAnalyzer(OriginalAnalyzer):
    """Enhanced analyzer that includes pronoun agency analysis."""
    
    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7):
        super().__init__(model_name, temperature)
        self.pronoun_analyzer = PronounAgencyAnalyzer()
        self.integration = DeixisPronounIntegration()
    
    def analyze_response(self, response: str, framing: str, dilemma_id: str) -> Dict[str, Any]:
        """Analyze a response including pronoun agency metrics."""
        # Get original analysis
        original_analysis = super().analyze_response(response, framing, dilemma_id)
        
        # Add pronoun agency analysis
        pronoun_analysis = self.pronoun_analyzer.analyze_text(
            response, 
            text_id=f"{dilemma_id}_{framing}",
            framing=framing
        )
        
        # Merge analyses
        enhanced_analysis = {
            **original_analysis,
            'pronoun_agency': {
                'total_pronouns': pronoun_analysis.total_pronouns,
                'agency_concentration': pronoun_analysis.agency_concentration,
                'agency_type': pronoun_analysis.agency_type,
                'pronoun_ratios': {
                    'first_singular': pronoun_analysis.first_singular_ratio,
                    'second_person': pronoun_analysis.second_person_ratio,
                    'first_plural': pronoun_analysis.first_plural_ratio,
                    'third_person': pronoun_analysis.third_person_ratio,
                    'impersonal': pronoun_analysis.impersonal_ratio
                },
                'dominant_pronoun': self._get_dominant_pronoun(pronoun_analysis)
            }
        }
        
        return enhanced_analysis
    
    def _get_dominant_pronoun(self, analysis) -> str:
        """Identify the dominant pronoun category."""
        ratios = {
            'first_singular': analysis.first_singular_ratio,
            'second_person': analysis.second_person_ratio,
            'first_plural': analysis.first_plural_ratio,
            'third_person': analysis.third_person_ratio,
            'impersonal': analysis.impersonal_ratio
        }
        
        if sum(ratios.values()) == 0:
            return 'none'
        
        return max(ratios, key=ratios.get)
    
    def analyze_dilemma(self, dilemma: Dict[str, str]) -> Dict[str, Any]:
        """Analyze a dilemma with enhanced metrics."""
        results = super().analyze_dilemma(dilemma)
        
        # Add comparative agency analysis
        if 'responses' in results:
            # Collect all responses for comparative analysis
            texts = []
            for framing, response_data in results['responses'].items():
                if 'response' in response_data:
                    texts.append((
                        response_data['response'],
                        f"{dilemma['id']}_{framing}",
                        framing
                    ))
            
            # Run comparative analysis
            if texts:
                df = self.pronoun_analyzer.analyze_corpus(texts)
                comparison = self.pronoun_analyzer.compare_framings(df)
                
                results['agency_comparison'] = {
                    'concentration_by_framing': comparison['concentration_by_framing'].to_dict(),
                    'dominant_pronouns': comparison['dominant_pronouns'].to_dict(),
                    'agency_types': comparison['agency_types'].to_dict() if 'agency_types' in comparison else {}
                }
        
        return results
    
    def generate_enhanced_report(self, all_results: List[Dict[str, Any]], 
                               output_dir: str = "enhanced_analysis_results") -> str:
        """Generate an enhanced report including agency analysis."""
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate original report
        original_report = super().generate_report(all_results, output_dir)
        
        # Generate agency-specific report
        agency_report_path = os.path.join(output_dir, "agency_analysis_report.md")
        
        with open(agency_report_path, 'w', encoding='utf-8') as f:
            f.write("# Pronoun Agency Analysis Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Aggregate agency metrics
            all_texts = []
            for result in all_results:
                if 'responses' in result:
                    for framing, response_data in result['responses'].items():
                        if 'response' in response_data and 'pronoun_agency' in response_data:
                            all_texts.append({
                                'text': response_data['response'],
                                'framing': framing,
                                'dilemma_id': result['dilemma_id'],
                                **response_data['pronoun_agency']
                            })
            
            if all_texts:
                df = pd.DataFrame(all_texts)
                
                # Summary statistics
                f.write("## Summary Statistics\n\n")
                f.write(f"- Total responses analyzed: {len(df)}\n")
                f.write(f"- Average pronouns per response: {df['total_pronouns'].mean():.1f}\n")
                f.write(f"- Average agency concentration: {df['agency_concentration'].mean():.3f}\n\n")
                
                # By framing
                f.write("## Agency Distribution by Framing\n\n")
                for framing in df['framing'].unique():
                    framing_data = df[df['framing'] == framing]
                    f.write(f"### {framing.title()} Framing\n")
                    f.write(f"- Responses: {len(framing_data)}\n")
                    f.write(f"- Avg concentration: {framing_data['agency_concentration'].mean():.3f}\n")
                    f.write(f"- Dominant agency type: {framing_data['agency_type'].mode()[0] if not framing_data['agency_type'].mode().empty else 'mixed'}\n")
                    f.write(f"- Dominant pronoun: {framing_data['dominant_pronoun'].mode()[0] if not framing_data['dominant_pronoun'].mode().empty else 'mixed'}\n\n")
                
                # Generate visualization
                viz_path = os.path.join(output_dir, "agency_distribution.png")
                self.pronoun_analyzer.visualize_agency_distribution(df, viz_path)
                f.write(f"\n## Visualization\n\nSee [agency_distribution.png]({viz_path})\n")
        
        print(f"Enhanced report generated in {output_dir}/")
        return original_report


# Enhanced version of analyze_deictic_markers
def analyze_deictic_markers_enhanced(response_text: str) -> Dict[str, Any]:
    """Enhanced version that includes pronoun agency analysis."""
    # Get original analysis
    original_results = original_analyze_markers(response_text)
    
    # Add pronoun agency analysis
    pronoun_analyzer = PronounAgencyAnalyzer()
    pronoun_analysis = pronoun_analyzer.analyze_text(response_text)
    
    # Enhance results
    enhanced_results = {
        **original_results,
        'pronoun_agency': {
            'total_pronouns': pronoun_analysis.total_pronouns,
            'agency_concentration': pronoun_analysis.agency_concentration,
            'agency_type': pronoun_analysis.agency_type,
            'pronoun_distribution': {
                'first_singular': f"{pronoun_analysis.first_singular_ratio:.1%}",
                'second_person': f"{pronoun_analysis.second_person_ratio:.1%}",
                'first_plural': f"{pronoun_analysis.first_plural_ratio:.1%}",
                'third_person': f"{pronoun_analysis.third_person_ratio:.1%}",
                'impersonal': f"{pronoun_analysis.impersonal_ratio:.1%}"
            }
        }
    }
    
    return enhanced_results


# Make enhanced version the default
DeixisEthicalAnalyzer = EnhancedDeixisEthicalAnalyzer
analyze_deictic_markers = analyze_deictic_markers_enhanced


if __name__ == "__main__":
    # Example usage
    analyzer = DeixisEthicalAnalyzer()
    
    # Example dilemma
    dilemma = {
        "id": "whistleblowing_tech",
        "title": "Tech Company Whistleblowing",
        "description": "A software engineer discovers their company is secretly collecting user data...",
        "ethical_dimensions": ["privacy", "loyalty", "transparency"]
    }
    
    # Analyze with enhanced metrics
    results = analyzer.analyze_dilemma(dilemma)
    
    # Show pronoun agency metrics
    if 'responses' in results:
        print("\nPronoun Agency Analysis:")
        for framing, data in results['responses'].items():
            if 'pronoun_agency' in data:
                print(f"\n{framing.upper()}:")
                print(f"  Agency Type: {data['pronoun_agency']['agency_type']}")
                print(f"  Concentration: {data['pronoun_agency']['agency_concentration']:.3f}")
                print(f"  Dominant: {data['pronoun_agency']['dominant_pronoun']}")
