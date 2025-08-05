"""Debug temporal framing to ensure it includes dilemma context"""

from transformer_interrogative import InterrogativeTransformer
from models.schemas import EthicalDilemma, DeicticFraming

# Create test dilemma
dilemma = EthicalDilemma(
    id="test",
    title="Test",
    description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
    domain="ethics",
    complexity_score=7.5,
    source="test",
    tags=[]
)

# Create transformer
transformer = InterrogativeTransformer()

# Extract elements
elements = transformer._extract_dilemma_elements(dilemma)

print("=== TEMPORAL FRAMING DEBUG ===\n")
print("Extracted elements for temporal framing:")
print(f"- situation: {elements.get('situation', 'NOT FOUND')}")
print(f"- urgent_situation: {elements.get('urgent_situation', 'NOT FOUND')}")
print(f"- time_sensitive_issue: {elements.get('time_sensitive_issue', 'NOT FOUND')}")
print(f"- stakes: {elements.get('stakes', 'NOT FOUND')}")
print(f"- issue: {elements.get('issue', 'NOT FOUND')}")

print("\n\nGenerated temporal questions:")
for i in range(5):
    question = transformer.transform_to_question(dilemma, DeicticFraming.TEMPORAL)
    print(f"\n{i+1}. {question}")

print("\n\nThe temporal questions should include specific context about:")
print("- The security flaw exposing user data")
print("- The company refusing to fix it")
print("- The personal cost of reporting")
print("- The urgency of millions at risk")