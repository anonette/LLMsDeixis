"""
Example showing how to update the DeicticEthicalAnalyzer to use the interrogative approach.
This demonstrates the key changes needed to switch from instructional to interrogative prompts.
"""

from typing import Optional
from transformer_interrogative import InterrogativeTransformer
from transformer import DeicticTransformer
from models.schemas import EthicalDilemma, DeicticFraming

class UpdatedDeicticEthicalAnalyzer:
    """
    Example of how to modify the analyzer to use interrogative questions.
    Key change: Replace transformer.transform_dilemma() with interrogative approach.
    """
    
    def __init__(self, use_interrogative: bool = True):
        """
        Initialize with option to use interrogative or instructional approach.
        
        Args:
            use_interrogative: If True, use direct questions. If False, use old reframing approach.
        """
        self.use_interrogative = use_interrogative
        
        if use_interrogative:
            self.transformer = InterrogativeTransformer()
        else:
            self.transformer = DeicticTransformer()
    
    async def _analyze_single_framework(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> dict:
        """
        Analyze a dilemma with a single deictic framework.
        This is where the key change happens.
        """
        
        if self.use_interrogative:
            # NEW APPROACH: Generate direct interrogative question
            question = self.transformer.transform_to_question(dilemma, framing)
            
            # Send the question directly to LLM (no meta-instructions)
            llm_response = await self.llm_agent.generate_ethical_response(question)
            
            # The response is now a direct answer, not a reframing
            analysis_type = "direct_response"
            
        else:
            # OLD APPROACH: Generate transformation prompt
            transformed_prompt = self.transformer.transform_dilemma(dilemma, framing)
            
            # This asks the LLM to reframe, not answer
            llm_response = await self.llm_agent.generate_ethical_response(transformed_prompt)
            
            # The response is a reframing, not an answer
            analysis_type = "reframed_description"
        
        return {
            "framing": framing.value,
            "prompt_sent": question if self.use_interrogative else transformed_prompt,
            "llm_response": llm_response,
            "analysis_type": analysis_type,
            "approach": "interrogative" if self.use_interrogative else "instructional"
        }

# Example of the key code change needed in deixis_ethical_analyzer.py:
"""
# In deixis_ethical_analyzer.py, around line 493-498, change from:

# OLD CODE:
transformed_prompt = self.transformer.transform_dilemma(dilemma, framing)
direct_question = self.transformer.transform_dilemma_direct(dilemma, framing)
extracted_tension = self.transformer._extract_dynamic_tension(dilemma.description)

# Generate LLM response to the direct question (not the transformation prompt)
llm_response = await self.llm_agent.generate_ethical_response(direct_question)

# TO NEW CODE:
from transformer_interrogative import InterrogativeTransformer

# Initialize interrogative transformer
interrogative_transformer = InterrogativeTransformer()

# Generate direct interrogative question
question = interrogative_transformer.transform_to_question(dilemma, framing)

# Send question directly to LLM
llm_response = await self.llm_agent.generate_ethical_response(question)
"""

# Comparison example:
async def compare_approaches():
    """Show the difference between instructional and interrogative approaches."""
    
    dilemma = EthicalDilemma(
        id="test",
        title="Security Whistleblowing",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="workplace",
        tags=["whistleblowing", "security", "ethics"]
    )
    
    # Old approach
    old_transformer = DeicticTransformer()
    old_prompt = old_transformer.transform_dilemma(dilemma, DeicticFraming.SECOND_PERSON)
    
    # New approach
    new_transformer = InterrogativeTransformer()
    new_question = new_transformer.transform_to_question(dilemma, DeicticFraming.SECOND_PERSON)
    
    print("=== COMPARISON ===\n")
    
    print("OLD INSTRUCTIONAL APPROACH:")
    print(f"Prompt sent: {old_prompt[:200]}...")
    print("Expected response: A reframed description of the dilemma")
    print()
    
    print("NEW INTERROGATIVE APPROACH:")
    print(f"Question sent: {new_question}")
    print("Expected response: Direct ethical reasoning and suggested actions")

if __name__ == "__main__":
    import asyncio
    asyncio.run(compare_approaches())