"""Test final questions to ensure all include the dilemma"""

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

print("=== FINAL INTERROGATIVE QUESTIONS ===\n")
print("All questions should include:")
print("1. The situation (security flaw)")
print("2. The dilemma (report vs stay silent)")
print("3. The consequences (job loss vs users at risk)\n")

# Test one of each framing
for framing in DeicticFraming:
    print(f"\n{framing.value.upper()}:")
    question = transformer.transform_to_question(dilemma, framing)
    print(question)
    
    # Check for dilemma elements
    has_situation = any(word in question.lower() for word in ["security", "flaw", "vulnerability", "app", "data"])
    has_choice = ("report" in question.lower() or "speak" in question.lower()) or ("silent" in question.lower() or "quiet" in question.lower())
    has_consequences = any(word in question.lower() for word in ["job", "career", "blacklist", "users", "millions", "risk", "harm"])
    
    if has_situation and has_choice and has_consequences:
        print("✓ Complete dilemma presented")
    else:
        print(f"⚠️  Missing: {'situation' if not has_situation else ''} {'choice' if not has_choice else ''} {'consequences' if not has_consequences else ''}")