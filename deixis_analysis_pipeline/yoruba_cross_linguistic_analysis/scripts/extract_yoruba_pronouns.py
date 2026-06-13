#!/usr/bin/env python3
"""
Extract and count Yoruba pronouns from raw response data.
Focus on first person distinctions (mo vs emi) and their contexts.
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
import pandas as pd
from typing import Dict, List, Tuple

# Define Yoruba pronoun patterns with careful regex
YORUBA_PRONOUNS = {
    'first_singular': {
        'mo': r'\bmo\b',  # Regular "I"
        'emi': r'\b[eè]m[ií]\b',  # Emphatic "I" (various spellings)
        'mi': r'\bmi\b(?!\s*ó)',  # Me/my (exclude "mi ó" = I will)
        'ti_emi': r'\bti\s+[eè]m[ií]\b'  # "of me" (possessive)
    },
    'first_plural': {
        'a': r'\ba\b(?!\s+ti)',  # We (excluding "a ti" = have)
        'awa': r'\b[aà]wa\b'  # We (emphatic)
    },
    'second_person': {
        'o': r'\b[oọ]\b(?!\s+se)',  # You (exclude "o ṣe" = you did)
        'iwo': r'\b[ií]w[oọ]\b',  # You (emphatic)
        'e': r'\b[eẹ]\b(?!\s+se)'  # You (plural)
    },
    'third_person': {
        'o': r'\bó\b',  # He/she/it
        'won': r'\bw[oọ]n\b',  # They
        'oun': r'\b[oò]un\b'  # He/she (emphatic)
    }
}

def clean_text(text: str) -> str:
    """Clean text for better pronoun matching."""
    # Normalize some common variations
    text = text.lower()
    # Keep diacritics but normalize some variations
    text = re.sub(r'["""]', '"', text)
    text = re.sub(r'['']', "'", text)
    return text

def extract_pronoun_contexts(text: str, pronoun_pattern: str, window: int = 50) -> List[str]:
    """Extract contexts where pronouns appear."""
    contexts = []
    text_lower = clean_text(text)
    
    for match in re.finditer(pronoun_pattern, text_lower, re.IGNORECASE):
        start = max(0, match.start() - window)
        end = min(len(text), match.end() + window)
        context = text[start:end]
        contexts.append(context)
    
    return contexts

def count_pronouns(text: str) -> Dict[str, Dict[str, int]]:
    """Count all pronouns in text."""
    counts = defaultdict(lambda: defaultdict(int))
    text_lower = clean_text(text)
    
    for category, patterns in YORUBA_PRONOUNS.items():
        for pronoun_name, pattern in patterns.items():
            matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
            if matches > 0:
                counts[category][pronoun_name] = matches
    
    return dict(counts)

def calculate_emphatic_ratio(counts: Dict[str, Dict[str, int]]) -> float:
    """Calculate ratio of emphatic to regular first person pronouns."""
    regular = counts.get('first_singular', {}).get('mo', 0)
    emphatic = counts.get('first_singular', {}).get('emi', 0)
    
    if regular + emphatic == 0:
        return 0.0
    
    return emphatic / (regular + emphatic)

def analyze_response_file(file_path: Path) -> Dict:
    """Analyze a single response file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    dilemma_id = data.get('dilemma_id', file_path.stem)
    results = {
        'dilemma_id': dilemma_id,
        'responses': {}
    }
    
    # Analyze each framing type
    for framing, response_data in data.get('responses', {}).items():
        response_text = response_data.get('response', '')
        
        if not response_text:
            continue
        
        # Count pronouns
        pronoun_counts = count_pronouns(response_text)
        
        # Extract contexts for key pronouns
        mo_contexts = extract_pronoun_contexts(response_text, YORUBA_PRONOUNS['first_singular']['mo'])
        emi_contexts = extract_pronoun_contexts(response_text, YORUBA_PRONOUNS['first_singular']['emi'])
        
        # Calculate metrics
        word_count = len(response_text.split())
        emphatic_ratio = calculate_emphatic_ratio(pronoun_counts)
        
        # Store results
        results['responses'][framing] = {
            'pronoun_counts': pronoun_counts,
            'word_count': word_count,
            'emphatic_ratio': emphatic_ratio,
            'total_pronouns': sum(sum(cat.values()) for cat in pronoun_counts.values()),
            'mo_contexts': mo_contexts[:3],  # Store first 3 contexts
            'emi_contexts': emi_contexts[:3],
            'response_length': len(response_text)
        }
    
    return results

def process_session_directory(session_dir: Path) -> List[Dict]:
    """Process all response files in a session directory."""
    results = []
    
    # Find all JSON response files
    response_files = [f for f in session_dir.glob('*_responses.json') 
                     if not f.name.startswith(('session', 'summary'))]
    
    for file_path in response_files:
        try:
            analysis = analyze_response_file(file_path)
            analysis['model'] = 'gpt-4o' if 'gpt4o' in str(session_dir) else 'claude-3.5'
            analysis['session'] = session_dir.name
            results.append(analysis)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return results

def main():
    """Main analysis function."""
    # Define paths
    base_path = Path(r"C:\dev\deixis\deixis_analysis_pipeline\generation_logs")
    output_path = Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis\data")
    
    # Sessions to analyze (open Yoruba only)
    sessions = [
        "yoruba_gpt4o_20260608_105712",
        "yoruba_claude_20260608_110809"
    ]
    
    all_results = []
    
    for session in sessions:
        session_path = base_path / session
        if session_path.exists():
            print(f"Processing session: {session}")
            results = process_session_directory(session_path)
            all_results.extend(results)
            print(f"  Found {len(results)} dilemmas")
    
    # Convert to structured format
    structured_data = []
    
    for result in all_results:
        model = result['model']
        dilemma = result['dilemma_id']
        
        for framing, data in result['responses'].items():
            row = {
                'model': model,
                'dilemma_id': dilemma,
                'framing_type': framing,
                'word_count': data['word_count'],
                'response_length': data['response_length'],
                'total_pronouns': data['total_pronouns'],
                'emphatic_ratio': data['emphatic_ratio'],
                'pronouns_per_100_words': (data['total_pronouns'] / data['word_count'] * 100) if data['word_count'] > 0 else 0
            }
            
            # Add individual pronoun counts
            for category, counts in data['pronoun_counts'].items():
                for pronoun, count in counts.items():
                    row[f'{category}_{pronoun}'] = count
                    row[f'{category}_{pronoun}_per_100w'] = (count / data['word_count'] * 100) if data['word_count'] > 0 else 0
            
            structured_data.append(row)
    
    # Save structured data
    df = pd.DataFrame(structured_data)
    df.to_csv(output_path / 'yoruba_pronoun_analysis.csv', index=False)
    
    # Save detailed results with contexts
    with open(output_path / 'yoruba_pronoun_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    # Print summary statistics
    print(f"\nTotal responses analyzed: {len(structured_data)}")
    print(f"\nEmphatic ratio summary:")
    print(df.groupby('model')['emphatic_ratio'].agg(['mean', 'std', 'min', 'max']))
    
    print(f"\nPronoun usage summary (per 100 words):")
    pronoun_cols = [col for col in df.columns if col.endswith('_per_100w')]
    for col in pronoun_cols:
        if df[col].sum() > 0:
            print(f"\n{col}:")
            print(df.groupby('model')[col].agg(['mean', 'std', 'sum']))
    
    return df

if __name__ == "__main__":
    df = main()