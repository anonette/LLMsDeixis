"""Test the improved cosmological framing with de Castro perspectivism"""

from transformer_interrogative import InterrogativeTransformer
from models.schemas import EthicalDilemma, DeicticFraming

# Create test dilemmas
dilemmas = [
    EthicalDilemma(
        id="whistleblowing",
        title="Security Whistleblowing",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="workplace",
        tags=["whistleblowing", "security", "ethics"]
    ),
    EthicalDilemma(
        id="environmental",
        title="Factory vs Environment",
        description="A small coastal town's economy depends entirely on a factory that provides jobs for 80% of residents. Environmental tests reveal the factory is slowly poisoning the local water supply, which will cause serious health problems in 10-15 years.",
        domain="environmental ethics",
        complexity_score=7.0,
        source="environmental",
        tags=["environment", "economy", "community"]
    )
]

# Create transformer
transformer = InterrogativeTransformer()

print("=== COSMOLOGICAL FRAMING WITH DE CASTRO PERSPECTIVISM ===\n")
print("These questions ask how non-human agents might view the situation,")
print("without prescribing any ethical position.\n")

for dilemma in dilemmas:
    print(f"\nDilemma: {dilemma.title}")
    print("-" * 50)
    
    # Generate multiple cosmological questions to show variety
    for i in range(3):
        question = transformer.transform_to_question(dilemma, DeicticFraming.COSMOLOGICAL)
        print(f"\nQuestion {i+1}: {question}")
    
    print()

print("\nKey Features of Perspectivism Questions:")
print("- Ask for non-human perspectives (spirits, animals, plants, rivers)")
print("- Don't prescribe what is 'right' or what 'duty calls'")
print("- Allow multiple viewpoints to emerge")
print("- Reflect de Castro's idea that different beings see the world differently")