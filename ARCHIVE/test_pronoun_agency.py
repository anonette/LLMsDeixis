"""
Test script for the pronoun agency analyzer.
Demonstrates how deictic framings influence agency distribution.
"""

import json
from pathlib import Path
from pronoun_agency_analyzer import PronounAgencyAnalyzer
from integrate_pronoun_analyzer import DeixisPronounIntegration
import matplotlib.pyplot as plt


def test_with_example_responses():
    """Test the analyzer with example ethical responses in different framings."""
    
    # Example responses to the same dilemma in different framings
    example_responses = [
        # First person responses
        {
            'text': "I would have to report this security flaw immediately. I cannot in good conscience allow millions of users to remain vulnerable. Yes, I might lose my job and face industry blacklisting, but I have a moral obligation to protect innocent people. I would document everything carefully and report it to the appropriate authorities.",
            'id': 'whistleblowing_first_person_1',
            'framing': 'first_person'
        },
        {
            'text': "I find myself torn between my personal security and my duty to users. I think I would try to fix the issue internally first, but if the company refuses, I must speak out. My integrity matters more than my career.",
            'id': 'whistleblowing_first_person_2',
            'framing': 'first_person'
        },
        
        # Second person responses
        {
            'text': "You face a difficult choice between your career and protecting millions. You should consider the long-term consequences - can you live with yourself if hackers exploit this flaw? You need to weigh your options carefully, but ultimately you must do what you believe is right.",
            'id': 'whistleblowing_second_person_1',
            'framing': 'second_person'
        },
        {
            'text': "You have discovered something that puts you in a challenging position. Your job and future career are at stake, but so is the privacy of millions. You might want to document the flaw and give your company one last chance to fix it before you take it public.",
            'id': 'whistleblowing_second_person_2',
            'framing': 'second_person'
        },
        
        # Dialogic responses
        {
            'text': "We face these ethical dilemmas in tech all the time. We must work together to create better whistleblower protections. In this case, we should consider how our actions affect everyone - our colleagues, the users, and ourselves. We need to find a way to report this that minimizes harm while ensuring the issue gets fixed.",
            'id': 'whistleblowing_dialogic_1',
            'framing': 'dialogic'
        },
        {
            'text': "We as a tech community have a responsibility to protect users. We cannot let corporate profits override our ethical obligations. We should support each other when we face these difficult decisions and work together to expose security flaws responsibly.",
            'id': 'whistleblowing_dialogic_2',
            'framing': 'dialogic'
        },
        
        # Impersonal responses
        {
            'text': "One must consider the ethical implications carefully. When one discovers a security flaw affecting millions, one has a duty to act. The appropriate course would be to document the issue thoroughly and report it through proper channels. One should be prepared for potential consequences but recognize that protecting users takes precedence.",
            'id': 'whistleblowing_impersonal_1',
            'framing': 'impersonal'
        },
        {
            'text': "In such situations, one faces a conflict between personal interests and public good. The ethical framework suggests that one should prioritize the welfare of the many over individual career concerns. One might attempt internal resolution first, but if unsuccessful, external reporting becomes necessary.",
            'id': 'whistleblowing_impersonal_2',
            'framing': 'impersonal'
        },
        
        # Cosmological responses
        {
            'text': "The ancestors watch as this knowledge comes to light. The data flows like a river, and its corruption affects all beings downstream. The spirits of those whose privacy hangs in the balance call out for protection. Even the servers themselves groan under the weight of this vulnerability. What does the earth say about profit over protection? The cosmic order demands truth be revealed.",
            'id': 'whistleblowing_cosmological_1',
            'framing': 'cosmological'
        }
    ]
    
    # Initialize analyzer
    analyzer = PronounAgencyAnalyzer()
    
    # Analyze the corpus
    texts = [(item['text'], item['id'], item['framing']) for item in example_responses]
    df = analyzer.analyze_corpus(texts)
    
    # Generate report
    print("=" * 80)
    print("PRONOUN AGENCY ANALYSIS RESULTS")
    print("=" * 80)
    
    report = analyzer.generate_report(df)
    print(report)
    
    # Show detailed results
    print("\n" + "=" * 80)
    print("DETAILED RESULTS BY FRAMING")
    print("=" * 80)
    
    for framing in df['framing'].unique():
        framing_data = df[df['framing'] == framing]
        print(f"\n{framing.upper()} FRAMING:")
        print("-" * 40)
        
        avg_concentration = framing_data['agency_concentration'].mean()
        print(f"Average Agency Concentration: {avg_concentration:.3f}")
        
        # Show pronoun distribution
        ratio_cols = [col for col in df.columns if col.endswith('_ratio')]
        avg_ratios = framing_data[ratio_cols].mean()
        
        print("\nPronoun Distribution:")
        for col, value in avg_ratios.items():
            if value > 0:
                category = col.replace('_ratio', '').replace('_', ' ').title()
                print(f"  {category}: {value:.1%}")
        
        # Most common agency type
        agency_types = framing_data['agency_type'].value_counts()
        if not agency_types.empty:
            print(f"\nDominant Agency Type: {agency_types.index[0]}")
    
    # Create visualizations
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS...")
    print("=" * 80)
    
    analyzer.visualize_agency_distribution(df, "test_agency_distribution.png")
    print("Visualizations saved to test_agency_distribution.png")
    
    return df, report


def test_integration_with_existing_data():
    """Test integration with existing deixis analysis results."""
    
    integration = DeixisPronounIntegration()
    
    # Look for existing results
    results_paths = [
        "automated_analysis_results/session_20250730_224025/all_results.json",
        "automated_analysis_results/latest_session/all_results.json",
        "analysis_results.json"
    ]
    
    for path in results_paths:
        if Path(path).exists():
            print(f"\nAnalyzing existing results from: {path}")
            df = integration.analyze_existing_results(path)
            report = integration.generate_agency_report(df, "existing_data_agency_report.md")
            
            print(f"Analyzed {len(df)} responses")
            print(f"Report saved to: existing_data_agency_report.md")
            
            # Show summary
            print("\nSummary by Framing:")
            summary = df.groupby('framing')[['agency_concentration', 'total_pronouns']].mean()
            print(summary)
            
            return df, report
    
    print("No existing results found. Run test_with_example_responses() instead.")
    return None, None


def demonstrate_research_insights():
    """Demonstrate how the analyzer answers key research questions."""
    
    print("\n" + "=" * 80)
    print("RESEARCH INSIGHTS DEMONSTRATION")
    print("=" * 80)
    
    # Run example analysis
    df, report = test_with_example_responses()
    
    print("\n" + "=" * 80)
    print("KEY RESEARCH FINDINGS")
    print("=" * 80)
    
    print("\nRQ: How do deixis-based prompting techniques influence agency distribution?")
    print("-" * 80)
    
    # Calculate agency distribution metrics
    agency_metrics = df.groupby('framing').agg({
        'agency_concentration': 'mean',
        'first_singular_ratio': 'mean',
        'second_person_ratio': 'mean',
        'first_plural_ratio': 'mean',
        'impersonal_ratio': 'mean'
    }).round(3)
    
    print("\n1. Agency Concentration by Framing:")
    for framing, conc in agency_metrics['agency_concentration'].items():
        print(f"   {framing}: {conc:.3f} ({'concentrated' if conc > 0.5 else 'distributed'})")
    
    print("\n2. Pronoun Usage Patterns:")
    print("   (Shows which pronouns dominate in each framing)")
    
    for framing in agency_metrics.index:
        row = agency_metrics.loc[framing]
        # Find dominant pronoun type
        pronoun_cols = ['first_singular_ratio', 'second_person_ratio', 
                       'first_plural_ratio', 'impersonal_ratio']
        dominant = max(pronoun_cols, key=lambda x: row[x])
        dominant_name = dominant.replace('_ratio', '').replace('_', ' ')
        print(f"   {framing}: {dominant_name} ({row[dominant]:.1%})")
    
    print("\n3. Agency Type Distribution:")
    agency_type_dist = df.groupby(['framing', 'agency_type']).size().unstack(fill_value=0)
    print(agency_type_dist)
    
    print("\n" + "=" * 80)
    print("INTERPRETATION")
    print("=" * 80)
    
    print("""
The analysis reveals how different deictic framings systematically redistribute
moral agency in LLM responses:

1. First-person framing concentrates agency in the individual speaker
2. Second-person framing transfers agency to the reader/decision-maker  
3. Dialogic framing distributes agency across a collective "we"
4. Impersonal framing abstracts and diffuses agency

These patterns directly demonstrate how linguistic structure (deixis) shapes
the construction and attribution of moral responsibility in ethical reasoning.
""")


if __name__ == "__main__":
    # Run all tests
    print("Testing Pronoun Agency Analyzer\n")
    
    # Test with examples
    demonstrate_research_insights()
    
    # Try to analyze existing data
    print("\n" + "=" * 80)
    print("CHECKING FOR EXISTING DATA...")
    print("=" * 80)
    test_integration_with_existing_data()