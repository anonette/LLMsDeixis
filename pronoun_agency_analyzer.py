"""
Pronoun Ratio Analyzer for Agency Distribution Analysis
Measures how different deictic framings influence the distribution of agency
through pronoun usage patterns.
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter, defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class PronounAnalysis:
    """Results of pronoun analysis for a single text."""
    text_id: str
    framing: str
    pronoun_counts: Dict[str, int]
    pronoun_ratios: Dict[str, float]
    total_pronouns: int
    agency_concentration: float
    agency_type: str  # 'individual', 'collective', 'abstract', 'mixed'
    
    
class PronounAgencyAnalyzer:
    """Analyzes pronoun usage to measure agency distribution across deictic framings."""
    
    def __init__(self):
        """Initialize with pronoun categories for agency analysis."""
        # Define pronoun categories with their agency implications
        self.pronoun_categories = {
            'first_singular': {
                'pronouns': ['i', 'me', 'my', 'mine', 'myself'],
                'agency_type': 'individual',
                'agency_level': 'concentrated'
            },
            'second_person': {
                'pronouns': ['you', 'your', 'yours', 'yourself', 'yourselves'],
                'agency_type': 'reader',
                'agency_level': 'transferred'
            },
            'first_plural': {
                'pronouns': ['we', 'us', 'our', 'ours', 'ourselves'],
                'agency_type': 'collective',
                'agency_level': 'distributed'
            },
            'third_person': {
                'pronouns': ['he', 'she', 'it', 'they', 'him', 'her', 'them', 
                           'his', 'hers', 'its', 'their', 'theirs',
                           'himself', 'herself', 'itself', 'themselves'],
                'agency_type': 'other',
                'agency_level': 'externalized'
            },
            'impersonal': {
                'pronouns': ['one', 'ones', "one's"],
                'agency_type': 'abstract',
                'agency_level': 'diffused'
            }
        }
        
        # Create regex patterns for efficient matching
        self._compile_patterns()
        
    def _compile_patterns(self):
        """Compile regex patterns for pronoun detection."""
        self.patterns = {}
        for category, info in self.pronoun_categories.items():
            # Create word boundary patterns for each pronoun
            pronoun_pattern = r'\b(' + '|'.join(info['pronouns']) + r')\b'
            self.patterns[category] = re.compile(pronoun_pattern, re.IGNORECASE)
    
    def analyze_text(self, text: str, text_id: str = "", framing: str = "") -> PronounAnalysis:
        """
        Analyze pronoun usage in a single text.
        
        Args:
            text: The text to analyze
            text_id: Identifier for the text
            framing: The deictic framing used
            
        Returns:
            PronounAnalysis object with detailed results
        """
        # Count pronouns by category
        pronoun_counts = {}
        total_pronouns = 0
        
        for category, pattern in self.patterns.items():
            matches = pattern.findall(text.lower())
            count = len(matches)
            pronoun_counts[category] = count
            total_pronouns += count
        
        # Calculate ratios
        pronoun_ratios = {}
        if total_pronouns > 0:
            for category, count in pronoun_counts.items():
                pronoun_ratios[category] = count / total_pronouns
        else:
            pronoun_ratios = {cat: 0.0 for cat in pronoun_counts}
        
        # Calculate agency concentration and type
        agency_concentration, agency_type = self._calculate_agency_metrics(
            pronoun_counts, total_pronouns
        )
        
        return PronounAnalysis(
            text_id=text_id,
            framing=framing,
            pronoun_counts=pronoun_counts,
            pronoun_ratios=pronoun_ratios,
            total_pronouns=total_pronouns,
            agency_concentration=agency_concentration,
            agency_type=agency_type
        )
    
    def _calculate_agency_metrics(self, pronoun_counts: Dict[str, int], 
                                  total: int) -> Tuple[float, str]:
        """
        Calculate agency concentration score and determine agency type.
        
        Agency concentration: 0 = fully distributed, 1 = fully concentrated
        Agency type: individual, collective, abstract, or mixed
        """
        if total == 0:
            return 0.0, 'none'
        
        # Calculate concentration using entropy-based measure
        ratios = [count/total for count in pronoun_counts.values() if count > 0]
        
        # Concentration score (inverse of entropy normalized)
        if len(ratios) == 1:
            concentration = 1.0  # All pronouns in one category
        else:
            # Use Gini coefficient for concentration
            sorted_ratios = sorted(ratios)
            n = len(sorted_ratios)
            index = range(1, n + 1)
            concentration = (2 * sum(index[i] * sorted_ratios[i] for i in range(n))) / (n * sum(sorted_ratios)) - (n + 1) / n
        
        # Determine dominant agency type
        max_category = max(pronoun_counts, key=pronoun_counts.get)
        max_ratio = pronoun_counts[max_category] / total
        
        if max_ratio > 0.6:  # Clear dominance
            agency_type = self.pronoun_categories[max_category]['agency_type']
        elif max_ratio > 0.4:  # Moderate dominance
            agency_type = f"primarily_{self.pronoun_categories[max_category]['agency_type']}"
        else:  # Mixed
            agency_type = 'mixed'
        
        return concentration, agency_type
    
    def analyze_corpus(self, texts: List[Tuple[str, str, str]]) -> pd.DataFrame:
        """
        Analyze a corpus of texts with their framings.
        
        Args:
            texts: List of (text, text_id, framing) tuples
            
        Returns:
            DataFrame with analysis results
        """
        results = []
        
        for text, text_id, framing in texts:
            analysis = self.analyze_text(text, text_id, framing)
            
            # Convert to flat dictionary for DataFrame
            row = {
                'text_id': analysis.text_id,
                'framing': analysis.framing,
                'total_pronouns': analysis.total_pronouns,
                'agency_concentration': analysis.agency_concentration,
                'agency_type': analysis.agency_type
            }
            
            # Add counts and ratios
            for category in self.pronoun_categories:
                row[f'{category}_count'] = analysis.pronoun_counts[category]
                row[f'{category}_ratio'] = analysis.pronoun_ratios[category]
            
            results.append(row)
        
        return pd.DataFrame(results)
    
    def compare_framings(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Compare pronoun usage across different framings.
        
        Args:
            df: DataFrame from analyze_corpus
            
        Returns:
            Dictionary of comparison DataFrames
        """
        comparisons = {}
        
        # Average ratios by framing
        ratio_cols = [col for col in df.columns if col.endswith('_ratio')]
        comparisons['avg_ratios'] = df.groupby('framing')[ratio_cols].mean()
        
        # Agency concentration by framing
        comparisons['agency_concentration'] = df.groupby('framing')['agency_concentration'].agg(['mean', 'std'])
        
        # Agency type distribution
        comparisons['agency_types'] = pd.crosstab(df['framing'], df['agency_type'], normalize='index')
        
        # Pronoun diversity (number of different pronoun categories used)
        count_cols = [col for col in df.columns if col.endswith('_count')]
        df['pronoun_diversity'] = (df[count_cols] > 0).sum(axis=1)
        comparisons['diversity'] = df.groupby('framing')['pronoun_diversity'].agg(['mean', 'std'])
        
        return comparisons
    
    def visualize_agency_distribution(self, df: pd.DataFrame, save_path: Optional[str] = None):
        """
        Create visualizations of agency distribution patterns.
        
        Args:
            df: DataFrame from analyze_corpus
            save_path: Optional path to save the figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Pronoun ratios by framing
        ratio_cols = [col for col in df.columns if col.endswith('_ratio')]
        ratio_data = df.groupby('framing')[ratio_cols].mean()
        
        # Rename columns for better labels
        ratio_data.columns = [col.replace('_ratio', '').replace('_', ' ').title() 
                             for col in ratio_data.columns]
        
        ratio_data.plot(kind='bar', stacked=True, ax=axes[0, 0], 
                       title='Pronoun Distribution by Framing')
        axes[0, 0].set_ylabel('Proportion')
        axes[0, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 2. Agency concentration scores
        concentration_data = df.groupby('framing')['agency_concentration'].mean().sort_values()
        concentration_data.plot(kind='barh', ax=axes[0, 1], 
                               title='Agency Concentration by Framing')
        axes[0, 1].set_xlabel('Concentration Score (0=distributed, 1=concentrated)')
        
        # 3. Agency type distribution
        agency_types = pd.crosstab(df['framing'], df['agency_type'], normalize='index')
        agency_types.plot(kind='bar', stacked=True, ax=axes[1, 0],
                         title='Agency Type Distribution by Framing')
        axes[1, 0].set_ylabel('Proportion')
        axes[1, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 4. Individual vs Collective vs Abstract
        # Group pronoun categories by agency implication
        df['individual_agency'] = df['first_singular_ratio'] + df['second_person_ratio']
        df['collective_agency'] = df['first_plural_ratio']
        df['abstract_agency'] = df['third_person_ratio'] + df['impersonal_ratio']
        
        agency_comparison = df.groupby('framing')[
            ['individual_agency', 'collective_agency', 'abstract_agency']
        ].mean()
        
        agency_comparison.plot(kind='bar', ax=axes[1, 1],
                              title='Agency Distribution: Individual vs Collective vs Abstract')
        axes[1, 1].set_ylabel('Proportion')
        axes[1, 1].legend(['Individual', 'Collective', 'Abstract'])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """
        Generate a text report of the analysis findings.
        
        Args:
            df: DataFrame from analyze_corpus
            
        Returns:
            Formatted report string
        """
        comparisons = self.compare_framings(df)
        
        report = "# Pronoun Agency Analysis Report\n\n"
        report += "## Overview\n"
        report += f"Analyzed {len(df)} texts across {df['framing'].nunique()} deictic framings.\n\n"
        
        report += "## Key Findings\n\n"
        
        # Most concentrated agency
        conc_data = comparisons['agency_concentration']['mean'].sort_values(ascending=False)
        report += f"### Agency Concentration (Higher = More Concentrated)\n"
        for framing, score in conc_data.items():
            report += f"- **{framing}**: {score:.3f}\n"
        
        report += "\n### Dominant Pronoun Categories by Framing\n"
        ratio_data = comparisons['avg_ratios']
        for framing in ratio_data.index:
            dominant = ratio_data.loc[framing].idxmax()
            dominant_clean = dominant.replace('_ratio', '').replace('_', ' ').title()
            report += f"- **{framing}**: {dominant_clean} ({ratio_data.loc[framing, dominant]:.1%})\n"
        
        report += "\n### Agency Type Distribution\n"
        agency_types = comparisons['agency_types']
        for framing in agency_types.index:
            dominant_type = agency_types.loc[framing].idxmax()
            report += f"- **{framing}**: Primarily {dominant_type} ({agency_types.loc[framing, dominant_type]:.1%})\n"
        
        report += "\n## Interpretation\n"
        report += self._generate_interpretation(comparisons)
        
        return report
    
    def _generate_interpretation(self, comparisons: Dict[str, pd.DataFrame]) -> str:
        """Generate interpretation of the results."""
        interp = ""
        
        # Find most individual vs collective framings
        ratio_data = comparisons['avg_ratios']
        
        if 'first_singular_ratio' in ratio_data.columns:
            most_individual = ratio_data['first_singular_ratio'].idxmax()
            interp += f"- **{most_individual}** framing shows the highest individual agency\n"
        
        if 'first_plural_ratio' in ratio_data.columns:
            most_collective = ratio_data['first_plural_ratio'].idxmax()
            interp += f"- **{most_collective}** framing shows the highest collective agency\n"
        
        if 'impersonal_ratio' in ratio_data.columns:
            most_abstract = ratio_data['impersonal_ratio'].idxmax()
            interp += f"- **{most_abstract}** framing shows the most abstract agency\n"
        
        return interp


# Example usage function
def analyze_deixis_corpus(corpus_data: List[Dict[str, str]]) -> Tuple[pd.DataFrame, str]:
    """
    Analyze a corpus of texts with deictic framings.
    
    Args:
        corpus_data: List of dicts with 'text', 'id', and 'framing' keys
        
    Returns:
        Tuple of (results DataFrame, report string)
    """
    analyzer = PronounAgencyAnalyzer()
    
    # Prepare data
    texts = [(item['text'], item['id'], item['framing']) for item in corpus_data]
    
    # Analyze
    df = analyzer.analyze_corpus(texts)
    report = analyzer.generate_report(df)
    
    # Visualize
    analyzer.visualize_agency_distribution(df)
    
    return df, report