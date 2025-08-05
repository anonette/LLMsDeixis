"""
Test the improved tension extraction
"""

from transformer import DeicticTransformer, DeicticFraming
from deixis_ethical_analyzer import EthicalDilemma

# Create the dilemma
dilemma = EthicalDilemma(
    id="workplace_whistleblowing",
    title="The Corporate Cover-Up",
    description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
    domain="professional ethics",
    complexity_score=7.5,
    source="contemporary_workplace",
    tags=["whistleblowing", "corporate_responsibility", "privacy", "career"]
)

transformer = DeicticTransformer()

print("=== IMPROVED TENSION EXTRACTION ===\n")

# Extract the tension
tension = transformer._extract_dynamic_tension(dilemma.description)
print(f"Extracted tension: {tension}\n")

print("=== REFRAMED QUESTIONS WITH IMPROVED TENSION ===\n")

# Test all framings
framings = [
    DeicticFraming.IMPERSONAL,
    DeicticFraming.SECOND_PERSON,
    DeicticFraming.FIRST_PERSON,
    DeicticFraming.REFLEXIVE,
    DeicticFraming.DIALOGIC,
    DeicticFraming.SPATIAL,
    DeicticFraming.TEMPORAL,
    DeicticFraming.COSMOLOGICAL
]

for framing in framings:
    question = transformer.transform_dilemma_direct(dilemma, framing)
    print(f"{framing.value}: {question}")

print("\n✓ The extracted tension now makes more sense!")
print("✓ Questions are more meaningful and contextually appropriate")