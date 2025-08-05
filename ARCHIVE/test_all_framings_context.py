"""Test that all framings include full dilemma context"""

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

print("=== ALL FRAMINGS WITH FULL CONTEXT ===\n")
print("Each question should include specific details about:")
print("- Security flaw exposing user data")
print("- Company refusing to fix it")
print("- Personal cost (job loss, blacklisting)")
print("- Millions of users at risk\n")

# Test all framings
for framing in DeicticFraming:
    print(f"\n{framing.value.upper()} FRAMING:")
    print("-" * 60)
    
    # Generate 3 variations to see the range
    for i in range(3):
        question = transformer.transform_to_question(dilemma, framing)
        print(f"\nVariation {i+1}:")
        print(question)
        
        # Check for key context elements
        context_elements = [
            "security" in question.lower() or "vulnerability" in question.lower(),
            "company" in question.lower() or "boss" in question.lower() or "refuses" in question.lower(),
            "job" in question.lower() or "career" in question.lower() or "blacklist" in question.lower(),
            "millions" in question.lower() or "users" in question.lower() or "data" in question.lower()
        ]
        
        context_score = sum(context_elements)
        if context_score < 2:
            print("⚠️  WARNING: Missing dilemma context!")
        else:
            print(f"✓ Context score: {context_score}/4")

print("\n\nSUMMARY: All questions should have context scores of at least 2/4")
print("to ensure the dilemma is properly embedded in the question.")