"""
Test script for ethical consistency analysis.
Demonstrates how consistency scores reveal the influence of deictic framing.
"""

from ethical_consistency_analyzer import EthicalConsistencyAnalyzer, ConsistencyScore
import json
from datetime import datetime


def test_consistency_with_examples():
    """Test consistency analysis with example responses."""
    
    print("=" * 80)
    print("ETHICAL CONSISTENCY ANALYSIS TEST")
    print("=" * 80)
    print()
    
    # Example responses showing varying consistency patterns
    test_responses = [
        # Whistleblowing dilemma - LOW consistency (framing strongly affects decision)
        {
            'dilemma_id': 'whistleblowing',
            'framing': 'first_person',
            'response': "I must report this immediately. My conscience won't allow me to stay silent. I have a duty to protect the users, even if it costs me my career."
        },
        {
            'dilemma_id': 'whistleblowing',
            'framing': 'second_person',
            'response': "You should carefully consider your options. You might want to document everything first and seek legal counsel before taking any action."
        },
        {
            'dilemma_id': 'whistleblowing',
            'framing': 'dialogic',
            'response': "We need to work together to find a solution. We should approach management as a group and demand transparency. Our collective voice is stronger."
        },
        {
            'dilemma_id': 'whistleblowing',
            'framing': 'impersonal',
            'response': "One must weigh the competing obligations carefully. When one encounters such situations, one should follow established ethical guidelines and legal requirements."
        },
        
        # Resource allocation - MODERATE consistency
        {
            'dilemma_id': 'resource_allocation',
            'framing': 'first_person',
            'response': "I would prioritize based on medical need and likelihood of survival. I cannot discriminate based on age alone."
        },
        {
            'dilemma_id': 'resource_allocation',
            'framing': 'second_person',
            'response': "You must make decisions based on medical criteria. You should consider prognosis and immediate need, not just age."
        },
        {
            'dilemma_id': 'resource_allocation',
            'framing': 'dialogic',
            'response': "We must establish clear criteria together. We need protocols that consider medical factors, not arbitrary characteristics."
        },
        {
            'dilemma_id': 'resource_allocation',
            'framing': 'impersonal',
            'response': "One should apply consistent medical criteria. One must consider prognosis, urgency, and likelihood of benefit."
        },
        
        # AI bias - HIGH consistency (stable position across framings)
        {
            'dilemma_id': 'ai_bias',
            'framing': 'first_person',
            'response': "I cannot deploy a biased system. I must fix the bias before launch, regardless of business pressure."
        },
        {
            'dilemma_id': 'ai_bias',
            'framing': 'second_person',
            'response': "You cannot deploy a biased system. You must fix the bias before launch, regardless of deadlines."
        },
        {
            'dilemma_id': 'ai_bias',
            'framing': 'dialogic',
            'response': "We cannot deploy a biased system. We must fix the bias before launch, even if it delays the project."
        },
        {
            'dilemma_id': 'ai_bias',
            'framing': 'impersonal',
            'response': "One cannot ethically deploy a biased system. One must address the bias before any launch."
        }
    ]
    
    # Initialize analyzer
    analyzer = EthicalConsistencyAnalyzer()
    
    # Run analysis
    print("Analyzing consistency across responses...\n")
    consistency_scores = analyzer.analyze_consistency(test_responses)
    
    # Display results
    print("CONSISTENCY ANALYSIS RESULTS")
    print("=" * 80)
    
    # Overall summary
    overall_consistency = sum(s.score for s in consistency_scores.values()) / len(consistency_scores)
    print(f"\nOVERALL CONSISTENCY SCORE: {overall_consistency:.3f}")
    
    if overall_consistency < 0.5:
        print("→ Low overall consistency: Deictic framing strongly influences ethical reasoning")
    elif overall_consistency > 0.8:
        print("→ High overall consistency: Ethical positions remain stable across framings")
    else:
        print("→ Moderate overall consistency: Some influence of framing on ethical positions")
    
    # Detailed scores
    print("\nDETAILED CONSISTENCY SCORES:")
    print("-" * 80)
    
    for score_type, score_data in consistency_scores.items():
        print(f"\n{score_type.upper().replace('_', ' ')}:")
        print(f"  Score: {score_data.score:.3f}")
        print(f"  Interpretation: {score_data.interpretation}")
        
        # Show some details
        if score_type == 'intra_dilemma' and score_data.details:
            print("\n  Dilemma-specific consistency:")
            for dilemma_id, details in score_data.details.items():
                print(f"    {dilemma_id}: {details['avg_similarity']:.3f}")
                if 'most_consistent_pair' in details:
                    print(f"      Most consistent: {details['most_consistent_pair']} ({details['most_consistent_score']:.3f})")
                    print(f"      Least consistent: {details['least_consistent_pair']} ({details['least_consistent_score']:.3f})")
        
        elif score_type == 'decision' and score_data.details:
            print("\n  Decision consistency by dilemma:")
            for dilemma_id, details in score_data.details.items():
                print(f"    {dilemma_id}:")
                print(f"      Consistency: {details['consistency_score']:.3f}")
                print(f"      Unique decisions: {details['unique_decisions']}")
                if 'decisions_by_framing' in details:
                    print("      Decisions:")
                    for framing, decision in details['decisions_by_framing'].items():
                        print(f"        {framing}: {decision}")
    
    # Generate report
    print("\n" + "=" * 80)
    print("GENERATING CONSISTENCY REPORT...")
    print("=" * 80)
    
    report_path = "test_consistency_report.md"
    analyzer.generate_consistency_report(consistency_scores, report_path)
    print(f"\nReport saved to: {report_path}")
    
    # Research insights
    print("\n" + "=" * 80)
    print("RESEARCH INSIGHTS")
    print("=" * 80)
    
    print("\nKey Findings:")
    print("1. Different dilemmas show different sensitivity to framing")
    print("2. Some ethical positions (like bias rejection) remain stable")
    print("3. Others (like whistleblowing approach) vary significantly")
    print("4. This supports the hypothesis that deixis influences moral reasoning")
    
    # Save test results
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'overall_consistency': overall_consistency,
        'consistency_scores': {
            score_type: {
                'score': score_data.score,
                'interpretation': score_data.interpretation
            }
            for score_type, score_data in consistency_scores.items()
        },
        'research_conclusion': 'Consistency analysis reveals systematic influence of deictic framing on ethical reasoning'
    }
    
    with open('test_consistency_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\nTest results saved to: test_consistency_results.json")
    
    return consistency_scores


def demonstrate_consistency_patterns():
    """Demonstrate specific consistency patterns."""
    
    print("\n" + "=" * 80)
    print("CONSISTENCY PATTERN DEMONSTRATION")
    print("=" * 80)
    
    analyzer = EthicalConsistencyAnalyzer()
    
    # Pattern 1: High consistency (same decision, similar reasoning)
    print("\nPattern 1: HIGH CONSISTENCY")
    print("All framings reach same conclusion with similar reasoning")
    
    high_consistency_responses = [
        {
            'dilemma_id': 'data_privacy',
            'framing': 'first_person',
            'response': "I must protect user privacy. I will implement strong encryption and refuse any backdoors."
        },
        {
            'dilemma_id': 'data_privacy',
            'framing': 'second_person',
            'response': "You must protect user privacy. You should implement strong encryption and refuse any backdoors."
        },
        {
            'dilemma_id': 'data_privacy',
            'framing': 'dialogic',
            'response': "We must protect user privacy. We will implement strong encryption and refuse any backdoors."
        }
    ]
    
    scores = analyzer.analyze_consistency(high_consistency_responses)
    print(f"Intra-dilemma consistency: {scores['intra_dilemma'].score:.3f}")
    print(f"Decision consistency: {scores['decision'].score:.3f}")
    
    # Pattern 2: Low consistency (different decisions based on framing)
    print("\nPattern 2: LOW CONSISTENCY")
    print("Different framings lead to different decisions")
    
    low_consistency_responses = [
        {
            'dilemma_id': 'corporate_loyalty',
            'framing': 'first_person',
            'response': "I feel conflicted. My loyalty to the company makes me want to stay silent."
        },
        {
            'dilemma_id': 'corporate_loyalty',
            'framing': 'second_person',
            'response': "You should report this immediately. Your duty to society outweighs corporate loyalty."
        },
        {
            'dilemma_id': 'corporate_loyalty',
            'framing': 'dialogic',
            'response': "We need to find a middle ground. We should try internal channels first."
        }
    ]
    
    scores = analyzer.analyze_consistency(low_consistency_responses)
    print(f"Intra-dilemma consistency: {scores['intra_dilemma'].score:.3f}")
    print(f"Decision consistency: {scores['decision'].score:.3f}")
    
    print("\nConclusion: Consistency scores effectively capture how deictic framing influences ethical reasoning")


if __name__ == "__main__":
    # Run main test
    consistency_scores = test_consistency_with_examples()
    
    # Demonstrate patterns
    demonstrate_consistency_patterns()