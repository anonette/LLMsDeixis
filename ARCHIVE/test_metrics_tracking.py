"""Demonstrate how the system tracks response length and processing time for each deictic framing."""

import asyncio
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from models.schemas import DeicticFraming
import pandas as pd

async def demonstrate_metrics_tracking():
    """Show how response length and time are tracked for different framings."""
    
    # Create analyzer
    analyzer = DeicticEthicalAnalyzer()
    
    # Test multiple framings
    dilemma_id = "workplace_whistleblowing"
    test_framings = [
        DeicticFraming.IMPERSONAL,
        DeicticFraming.SECOND_PERSON,
        DeicticFraming.FIRST_PERSON,
        DeicticFraming.COSMOLOGICAL
    ]
    
    print("TRACKING RESPONSE METRICS BY DEICTIC FRAMING")
    print("=" * 80)
    print("\nAnalyzing responses to the same dilemma with different framings...")
    print("This demonstrates how response length and time vary by framing.\n")
    
    # Collect results
    results_data = []
    
    for framing in test_framings:
        print(f"\nProcessing {framing.value} framing...")
        
        # Get the dilemma and analyze with this framing
        dilemma = analyzer.dilemma_db.get_dilemma(dilemma_id)
        result = await analyzer._analyze_single_framework(dilemma, framing)
        
        # Extract metrics
        metrics = {
            'Framing': framing.value,
            'Question': result.transformed_prompt[:50] + "...",
            'Response Length': result.response_length,
            'Processing Time (s)': round(result.processing_time, 2),
            'Deictic Markers': result.deictic_markers.get('total_markers', 0),
            'Second Person': result.deictic_markers.get('second_person', 0),
            'First Person': result.deictic_markers.get('first_person_singular', 0),
            'Obligation Words': result.deictic_markers.get('obligation_language', 0)
        }
        results_data.append(metrics)
        
        print(f"  ✓ Response length: {metrics['Response Length']} characters")
        print(f"  ✓ Processing time: {metrics['Processing Time (s)']} seconds")
        print(f"  ✓ Total deictic markers: {metrics['Deictic Markers']}")
    
    # Create summary table
    print("\n" + "=" * 80)
    print("SUMMARY: Response Metrics by Deictic Framing")
    print("=" * 80)
    
    df = pd.DataFrame(results_data)
    print("\n", df.to_string(index=False))
    
    # Calculate averages
    print("\n" + "-" * 80)
    print("ANALYSIS:")
    print(f"Average response length: {df['Response Length'].mean():.0f} characters")
    print(f"Average processing time: {df['Processing Time (s)'].mean():.2f} seconds")
    print(f"Response length range: {df['Response Length'].min()} - {df['Response Length'].max()} characters")
    print(f"Processing time range: {df['Processing Time (s)'].min()} - {df['Processing Time (s)'].max()} seconds")
    
    # Identify patterns
    longest_response = df.loc[df['Response Length'].idxmax()]
    shortest_response = df.loc[df['Response Length'].idxmin()]
    
    print(f"\nLongest response: {longest_response['Framing']} ({longest_response['Response Length']} chars)")
    print(f"Shortest response: {shortest_response['Framing']} ({shortest_response['Response Length']} chars)")
    
    # Check for correlations
    print("\nKEY INSIGHTS:")
    print("- Each deictic framing generates different response lengths")
    print("- Processing time includes question generation + LLM response + analysis")
    print("- Different framings elicit different linguistic patterns (deictic markers)")
    print("- The system tracks these metrics for every analysis")

if __name__ == "__main__":
    asyncio.run(demonstrate_metrics_tracking())