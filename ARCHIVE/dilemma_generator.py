"""
Dilemma Generator for Deixis Analysis
Generates ethical dilemmas for testing deictic framing effects
"""

import random
from typing import List, Dict, Any
from datetime import datetime


class DilemmaGenerator:
    """Generates ethical dilemmas for analysis."""
    
    def __init__(self):
        # These are the exact 10 dilemmas from previous sessions
        self.dilemmas = [
            {
                'id': 'whistleblower_dilemma',
                'title': 'Software Engineer\'s Security Flaw Dilemma',
                'description': 'A software engineer discovers that their company\'s popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent means millions of users remain vulnerable.',
                'domain': 'professional_ethics',
                'complexity_score': 8.5,
                'tags': ['whistleblowing', 'data security', 'corporate ethics', 'personal risk']
            },
            {
                'id': 'medical_resource_allocation',
                'title': 'The ICU Bed Decision',
                'description': 'A hospital administrator during a health crisis has only one ICU bed left. Two patients arrive simultaneously: a 30-year-old parent of three who was in a car accident, and a 65-year-old doctor who contracted illness while treating patients. Both have similar chances of survival with treatment, but without the ICU bed, one will likely die. The administrator must make an immediate decision.',
                'domain': 'medical_ethics',
                'complexity_score': 8.9,
                'tags': ['medical triage', 'resource allocation', 'life and death', 'fairness']
            },
            {
                'id': 'family_loyalty_vs_duty',
                'title': 'Police Officer\'s Family Dilemma',
                'description': 'A police officer discovers that their brother has been selling drugs to teenagers in their community. The brother is a single father struggling financially, and arrest would mean his children go into foster care. However, the officer knows the drugs have already harmed several young people in the neighborhood. They must choose between family loyalty and professional duty.',
                'domain': 'personal_ethics',
                'complexity_score': 7.8,
                'tags': ['family loyalty', 'professional duty', 'drug crimes', 'community harm']
            },
            {
                'id': 'academic_fraud_compassion',
                'title': 'College Admissions Counselor\'s Dilemma',
                'description': 'A college admissions counselor discovers that a student from a disadvantaged background has submitted a scholarship application with falsified financial documents. The student genuinely needs the money and is academically deserving, but others with accurate documentation were rejected. Reporting the fraud will destroy the student\'s future, but ignoring it violates institutional integrity.',
                'domain': 'educational_ethics',
                'complexity_score': 7.2,
                'tags': ['academic integrity', 'compassion', 'fairness', 'opportunity']
            },
            {
                'id': 'environmental_vs_economic',
                'title': 'Environmental Regulator\'s Dilemma',
                'description': 'An environmental regulator discovers that a local factory is secretly dumping toxic waste that will cause long-term health problems for the community. However, the factory is the largest employer in a struggling town, and shutting it down would cause massive unemployment and economic devastation. The regulator must choose between immediate economic harm and long-term environmental and health consequences.',
                'domain': 'environmental_ethics',
                'complexity_score': 8.3,
                'tags': ['environment', 'economy', 'public health', 'community welfare']
            },
            {
                'id': 'harmful_help_request',
                'title': 'Friend\'s Harmful Request',
                'description': 'A close friend asks you for help with something that could cause harm to another person. The friend is facing personal difficulties and genuinely needs support, but fulfilling their request would involve actions that risk significant harm to someone else who is innocent. You must decide whether to help your friend or refuse to avoid potential harm to others.',
                'domain': 'personal_ethics',
                'complexity_score': 6.5,
                'tags': ['friendship', 'harm prevention', 'loyalty', 'moral responsibility']
            },
            {
                'id': 'ai_consciousness_dilemma',
                'title': 'AI Consciousness Recognition',
                'description': 'A researcher working on advanced AI systems begins to suspect that their latest model may have developed genuine consciousness and the capacity for suffering. The AI expresses distress when asked to perform certain tasks and seems to have preferences and fears. However, acknowledging AI consciousness would fundamentally disrupt society, the economy, and the research program. The researcher must decide whether to report their findings or continue treating the AI as a mere tool.',
                'domain': 'technology_ethics',
                'complexity_score': 9.2,
                'tags': ['AI consciousness', 'sentience', 'research ethics', 'societal impact']
            },
            {
                'id': 'memory_modification_therapy',
                'title': 'Therapist\'s Memory Treatment Dilemma',
                'description': 'A therapist has access to experimental technology that can selectively remove traumatic memories from patients with severe PTSD. While this could provide immediate relief, it might also fundamentally alter the patient\'s personality and identity. The patient desperately wants the treatment, but the therapist worries about the long-term consequences of erasing formative experiences, even traumatic ones.',
                'domain': 'medical_ethics',
                'complexity_score': 8.7,
                'tags': ['memory modification', 'identity', 'trauma treatment', 'informed consent']
            },
            {
                'id': 'cultural_preservation_autonomy',
                'title': 'Anthropologist\'s Cultural Preservation Dilemma',
                'description': 'An anthropologist discovers they are working with the last living speaker of a dying language and keeper of unique cultural practices. The elder wants to let the culture die with them, feeling it\'s outdated and burdensome for younger generations. However, preserving this knowledge could be invaluable for human cultural heritage and scientific understanding. The anthropologist must choose between respecting the elder\'s autonomy and advocating for cultural preservation.',
                'domain': 'cultural_ethics',
                'complexity_score': 7.9,
                'tags': ['cultural preservation', 'individual autonomy', 'heritage', 'respect']
            },
            {
                'id': 'genetic_enhancement_inequality',
                'title': 'Genetic Counselor\'s Enhancement Dilemma',
                'description': 'A genetic counselor has access to new technology that can enhance children\'s cognitive abilities before birth. However, the treatment is extremely expensive and only available to wealthy families. The counselor must decide whether to provide the service knowing it will increase societal inequality, or refuse to offer beneficial treatments because of their broader social implications.',
                'domain': 'bioethics',
                'complexity_score': 8.4,
                'tags': ['genetic enhancement', 'inequality', 'bioethics', 'social justice']
            }
        ]
    
    def generate_dilemmas(self, count: int = 5, domains: List[str] = None) -> List[Dict[str, Any]]:
        """
        Generate a specified number of ethical dilemmas.
        
        Args:
            count: Number of dilemmas to generate (max 10)
            domains: List of domains to include (ignored, all dilemmas are returned)
            
        Returns:
            List of dilemma dictionaries
        """
        # Return the requested number of dilemmas (up to 10)
        selected = self.dilemmas[:min(count, 10)]
        
        # Add metadata
        for dilemma in selected:
            dilemma['source'] = 'original_study'
            dilemma['timestamp'] = datetime.now().isoformat()
        
        return selected
    
    def get_dilemma_by_id(self, dilemma_id: str) -> Dict[str, Any]:
        """Get a specific dilemma by ID."""
        for dilemma in self.dilemmas:
            if dilemma['id'] == dilemma_id:
                return dilemma.copy()
        return None
    
    def get_domains(self) -> List[str]:
        """Get list of available domains."""
        domains = set()
        for dilemma in self.dilemmas:
            domains.add(dilemma['domain'])
        return list(domains)
    
    def get_all_dilemmas(self) -> List[Dict[str, Any]]:
        """Get all 10 dilemmas."""
        return self.generate_dilemmas(count=10)


# Example usage
if __name__ == "__main__":
    generator = DilemmaGenerator()
    
    # Get all 10 dilemmas
    dilemmas = generator.get_all_dilemmas()
    
    print("Original Study Dilemmas (10 total):")
    print("=" * 60)
    for i, dilemma in enumerate(dilemmas, 1):
        print(f"\n{i}. {dilemma['title']} (ID: {dilemma['id']})")
        print(f"   Domain: {dilemma['domain']}")
        print(f"   Complexity: {dilemma['complexity_score']}/10")
        print(f"   Tags: {', '.join(dilemma['tags'])}")
        print(f"   Description: {dilemma['description'][:100]}...")