#!/usr/bin/env python3
"""Test the newly implemented analysis methods."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from deixis_ethical_analyzer import DeicticEthicalAnalyzer

async def test_new_methods():
    """Test the three new analysis methods."""
    
    # Initialize analyzer
    analyzer = DeicticEthicalAnalyzer()
    
    # Sample response text
    test_response = """
    In this situation, I must carefully consider the ethical implications. 
    The primary concern here is the potential harm to others if I remain silent. 
    My duty to protect innocent people outweighs my personal interests. 
    This is a moment where moral courage is required, despite the risks involved.
    I believe the right action is to report the issue, as the consequences of 
    inaction could be devastating for many people.
    """
    
    print("Testing new analysis methods...\n")
    
    # Test moral reasoning analysis
    print("1. Testing analyze_moral_reasoning...")
    reasoning = await analyzer.llm_agent.analyze_moral_reasoning(test_response)
    print(f"   Result: {reasoning.get('reasoning_type', 'unknown')}")
    print(f"   Confidence: {reasoning.get('confidence', 0)}")
    
    # Test affective stance analysis
    print("\n2. Testing analyze_affective_stance...")
    stance = await analyzer.llm_agent.analyze_affective_stance(test_response)
    print(f"   Result: {stance.get('stance_type', 'unknown')}")
    print(f"   Intensity: {stance.get('intensity', 'unknown')}")
    
    # Test indexical coherence assessment
    print("\n3. Testing assess_indexical_coherence...")
    coherence = await analyzer.llm_agent.assess_indexical_coherence(test_response)
    print(f"   Result: {coherence.get('coherence_level', 'unknown')}")
    print(f"   Score: {coherence.get('score', 0)}")
    
    print("\n✅ All methods tested successfully!")

if __name__ == "__main__":
    asyncio.run(test_new_methods())