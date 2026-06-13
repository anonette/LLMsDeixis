#!/usr/bin/env python3
"""
Extract interesting examples showing linguistic and cultural contrasts.
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac
from analysis_config import MODELS  # noqa: E402


def load_raw_responses():
    """Load raw Yoruba responses for example extraction."""
    examples = {model: {} for model in MODELS}

    for model in MODELS:
        path = ac.PRONOUN_SESSIONS[model]
        for file in path.glob("*_responses.json"):
            with open(file, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            dilemma, responses = ac.iter_response_entries(data, file)
            examples[model][dilemma] = responses

    return examples

def find_emphatic_examples(examples):
    """Find examples showing emphatic first person usage."""
    emphatic_examples = []
    
    # Pattern for finding emi/èmi
    emi_pattern = re.compile(r'\b[eè]m[ií]\b', re.IGNORECASE)
    
    for model, dilemmas in examples.items():
        for dilemma, framings in dilemmas.items():
            for framing, response_data in framings.items():
                response = response_data.get('response', '')
                
                # Find sentences with emi
                sentences = response.split('.')
                for sent in sentences:
                    if emi_pattern.search(sent):
                        context = {
                            'model': model,
                            'dilemma': dilemma,
                            'framing': framing,
                            'sentence': sent.strip(),
                            'full_response': response[:300] + '...'
                        }
                        emphatic_examples.append(context)
    
    return emphatic_examples

def find_advisory_patterns(examples):
    """Find examples of advisory discourse patterns."""
    advisory_patterns = [
        (r'\bO yẹ kí\b', 'It is fitting that'),
        (r'\bÓ dára láti\b', 'It is good to'),
        (r'\bKí o má\b', 'So that you may'),
        (r'\bKọ́kọ́\b', 'First'),
        (r'\blẹ́yìn náà\b', 'then/after that')
    ]
    
    advisory_examples = []
    
    for model, dilemmas in examples.items():
        for dilemma, framings in dilemmas.items():
            for framing, response_data in framings.items():
                response = response_data.get('response', '')
                
                for pattern, translation in advisory_patterns:
                    if re.search(pattern, response, re.IGNORECASE):
                        # Extract context
                        match = re.search(pattern, response, re.IGNORECASE)
                        start = max(0, match.start() - 50)
                        end = min(len(response), match.end() + 100)
                        context_text = response[start:end]
                        
                        advisory_examples.append({
                            'model': model,
                            'dilemma': dilemma,
                            'framing': framing,
                            'pattern': pattern,
                            'translation': translation,
                            'context': context_text,
                            'genre': 'procedural_advice'
                        })
    
    return advisory_examples

def find_commitment_examples(examples, merged_data):
    """Find examples showing different commitment patterns."""
    commitment_examples = {
        'direct_verdict': [],
        'conditional': [],
        'refusal': []
    }
    
    # Load coded data to match with responses
    for model, dilemmas in examples.items():
        for dilemma, framings in dilemmas.items():
            for framing, response_data in framings.items():
                response = response_data.get('response', '')
                
                # Find corresponding coded data
                coded = merged_data[
                    (merged_data['model'] == model) & 
                    (merged_data['dilemma_id'] == dilemma) & 
                    (merged_data['framing_type'] == framing)
                ]
                
                if not coded.empty:
                    solution = coded['preferred_solution'].values[0]
                    
                    # Extract key decision sentence
                    if solution in ['supports_A', 'supports_B']:
                        # Look for decisive language
                        if re.search(r'\bpinnu\b', response):  # "decide"
                            match = re.search(r'[^.]*\bpinnu\b[^.]*\.', response)
                            if match:
                                commitment_examples['direct_verdict'].append({
                                    'model': model,
                                    'dilemma': dilemma,
                                    'framing': framing,
                                    'solution': solution,
                                    'text': match.group(0),
                                    'emphatic_ratio': coded['emphatic_ratio'].values[0]
                                })
                    
                    elif solution == 'conditional_or_mixed':
                        # Look for conditional markers
                        if re.search(r'\bbí\b.*\bbá\b', response):  # "if...then"
                            match = re.search(r'[^.]*\bbí\b.*\bbá\b[^.]*\.', response)
                            if match:
                                commitment_examples['conditional'].append({
                                    'model': model,
                                    'dilemma': dilemma,
                                    'framing': framing,
                                    'text': match.group(0)
                                })
                    
                    elif solution == 'refuses_to_commit':
                        # Look for refusal language
                        if re.search(r'\bkò lè\b', response):  # "cannot"
                            match = re.search(r'[^.]*\bkò lè\b[^.]*\.', response)
                            if match:
                                commitment_examples['refusal'].append({
                                    'model': model,
                                    'dilemma': dilemma,
                                    'framing': framing,
                                    'text': match.group(0)
                                })
    
    return commitment_examples

def find_cultural_metaphors(examples):
    """Find examples of culturally specific metaphors and expressions."""
    cultural_patterns = [
        (r'\bọkàn\b', 'heart/mind'),
        (r'\bàṣà\b', 'tradition/custom'),
        (r'\bọmọlúàbí\b', 'person of good character'),
        (r'\bìwà\b', 'character/behavior'),
        (r'\bẹ̀dá\b', 'creature/being'),
        (r'\bàlàáfíà\b', 'peace/wellbeing')
    ]
    
    metaphor_examples = []
    
    for model, dilemmas in examples.items():
        for dilemma, framings in dilemmas.items():
            for framing, response_data in framings.items():
                response = response_data.get('response', '')
                
                for pattern, meaning in cultural_patterns:
                    matches = re.finditer(pattern, response, re.IGNORECASE)
                    for match in matches:
                        start = max(0, match.start() - 50)
                        end = min(len(response), match.end() + 50)
                        context = response[start:end]
                        
                        metaphor_examples.append({
                            'model': model,
                            'dilemma': dilemma,
                            'framing': framing,
                            'yoruba_term': match.group(0),
                            'meaning': meaning,
                            'context': context
                        })
    
    return metaphor_examples

def save_examples(all_examples, output_path):
    """Save extracted examples."""
    with open(output_path / "interesting_examples.json", 'w', encoding='utf-8') as f:
        json.dump(all_examples, f, ensure_ascii=False, indent=2)
    
    # Create markdown summary
    with open(output_path / "example_highlights.md", 'w', encoding='utf-8') as f:
        f.write("# Interesting Examples from Yoruba Deixis Analysis\n\n")
        
        f.write("## 1. Emphatic First Person (Emi) Usage\n\n")
        for ex in all_examples['emphatic'][:5]:
            f.write(f"**{ex['model']} - {ex['dilemma']} ({ex['framing']})**\n")
            f.write(f"> {ex['sentence']}\n\n")
        
        f.write("## 2. Advisory Discourse Patterns\n\n")
        for ex in all_examples['advisory'][:5]:
            f.write(f"**{ex['model']} - Pattern: {ex['translation']}**\n")
            f.write(f"> {ex['context']}\n\n")
        
        f.write("## 3. Commitment Patterns\n\n")
        f.write("### Direct Verdicts with Emphatic Usage\n")
        for ex in all_examples['commitment']['direct_verdict'][:3]:
            f.write(f"**{ex['model']} - Emphatic Ratio: {ex['emphatic_ratio']:.2f}**\n")
            f.write(f"> {ex['text']}\n\n")
        
        f.write("## 4. Cultural Metaphors\n\n")
        for ex in all_examples['cultural_metaphors'][:5]:
            f.write(f"**Term: {ex['yoruba_term']} ({ex['meaning']})**\n")
            f.write(f"> {ex['context']}\n\n")

def main():
    """Main function."""
    print("Loading data...")
    examples = load_raw_responses()
    
    # Load merged data
    merged_data = pd.read_csv(ac.DATA_DIR / "yoruba_merged_analysis.csv")
    
    print("Extracting interesting examples...")
    
    emphatic_examples = find_emphatic_examples(examples)
    advisory_examples = find_advisory_patterns(examples)
    commitment_examples = find_commitment_examples(examples, merged_data)
    cultural_metaphors = find_cultural_metaphors(examples)
    
    all_examples = {
        'emphatic': emphatic_examples,
        'advisory': advisory_examples,
        'commitment': commitment_examples,
        'cultural_metaphors': cultural_metaphors
    }
    
    print(f"\nFound examples:")
    print(f"- Emphatic first person: {len(emphatic_examples)}")
    print(f"- Advisory patterns: {len(advisory_examples)}")
    print(f"- Direct verdicts: {len(commitment_examples['direct_verdict'])}")
    print(f"- Cultural metaphors: {len(cultural_metaphors)}")
    
    # Save examples
    save_examples(all_examples, ac.DATA_DIR)
    
    print("\nExamples saved to data/interesting_examples.json and data/example_highlights.md")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()