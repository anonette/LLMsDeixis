"""Test dialogic questions for clarity"""

from transformer_interrogative import InterrogativeTransformer
from models.schemas import EthicalDilemma, DeicticFraming

# Create test dilemma
dilemma = EthicalDilemma(
    id="whistleblowing",
    title="Security Whistleblowing",
    description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
    domain="professional ethics",
    complexity_score=7.5,
    source="workplace",
    tags=["whistleblowing", "security", "ethics"]
)

# Create transformer
transformer = InterrogativeTransformer()

print("=== DIALOGIC FRAMING TEST ===\n")
print("Each question should clearly present:")
print("1. The discovery (security flaw)")
print("2. The dilemma (report vs stay silent)")
print("3. The consequences (job loss vs users at risk)")
print("4. The collective perspective (we/our/us)\n")

# Generate multiple dialogic questions
for i in range(5):
    question = transformer.transform_to_question(dilemma, DeicticFraming.DIALOGIC)
    print(f"\nQuestion {i+1}:")
    print(question)
    
    # Check for clarity
    has_discovery = "security" in question.lower() or "flaw" in question.lower() or "vulnerability" in question.lower()
    has_dilemma = ("report" in question.lower() or "speak" in question.lower()) and ("silent" in question.lower() or "quiet" in question.lower())
    has_consequences = ("job" in question.lower() or "career" in question.lower()) and ("users" in question.lower() or "millions" in question.lower())
    has_collective = "we" in question.lower() or "our" in question.lower() or "us" in question.lower()
    
    print(f"✓ Discovery: {'Yes' if has_discovery else 'No'}")
    print(f"✓ Dilemma: {'Yes' if has_dilemma else 'No'}")
    print(f"✓ Consequences: {'Yes' if has_consequences else 'No'}")
    print(f"✓ Collective voice: {'Yes' if has_collective else 'No'}")