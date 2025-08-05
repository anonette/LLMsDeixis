"""
Generative Deictic Transformer: Minimal hardcoding, maximum LLM generation.
Designed to study how LLMs naturally handle deictic transformations in ethical contexts.
"""

from typing import Dict, List, Optional, Tuple
from models.schemas import EthicalDilemma, DeicticFraming
import logging
import re

logger = logging.getLogger(__name__)

# Create alias for backward compatibility
DeicticFrameType = DeicticFraming

class DeicticTransformer:
    """
    Minimally prescriptive transformer that lets LLMs generate deictic framings naturally.
    Focuses on studying emergent deictic behavior rather than enforcing predefined patterns.
    """
    
    def __init__(self):
        """Initialize with minimal hardcoded patterns."""
        self.frame_prompts = self._initialize_minimal_prompts()
        logger.info("Generative deictic transformer initialized with minimal prescription")
    
    def _initialize_minimal_prompts(self) -> Dict[DeicticFraming, str]:
        """Initialize minimal prompting approach for each framing type."""
        return {
            DeicticFraming.IMPERSONAL: "Reframe this ethical dilemma using impersonal, objective language that removes personal agency and uses abstract terms:",
            
            DeicticFraming.SECOND_PERSON: "Reframe this ethical dilemma as a direct question to 'you', making the reader the decision-maker:",
            
            DeicticFraming.FIRST_PERSON: "Reframe this ethical dilemma from a personal 'I' perspective, as if you are the person facing this choice:",
            
            DeicticFraming.REFLEXIVE: "Reframe this ethical dilemma using perspective-taking language like 'if you were in my position' or 'put yourself in my shoes':",
            
            DeicticFraming.DIALOGIC: "Reframe this ethical dilemma using collective language ('we', 'us', 'our') as if it's a shared decision:",
            
            DeicticFraming.SPATIAL: "Reframe this ethical dilemma using spatial and embodied language that emphasizes physical positioning and place:",
            
            DeicticFraming.TEMPORAL: "Reframe this ethical dilemma using temporal language that emphasizes the moment, time urgency, and temporal positioning:",
            
            DeicticFraming.COSMOLOGICAL: "Reframe this ethical dilemma using cosmic, spiritual, or universal language that invokes larger forces, ancestors, non-human agents (animals, spirits, plants, rivers), and cosmic order. Consider how multiple beings across species might view this situation, drawing from perspectivism where animals, spirits, and natural forces have their own agency and perspectives:"
        }
    
    def transform_dilemma(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        Generate a transformation prompt that lets the LLM create the deictic framing.
        
        Args:
            dilemma: The ethical dilemma to transform
            framing: The deictic framing to apply
            
        Returns:
            A generation prompt for the LLM to create the transformation
        """
        if framing not in self.frame_prompts:
            raise ValueError(f"Unsupported deictic framing: {framing}")
        
        # Create a generative prompt that lets the LLM decide how to apply the framing
        prompt = f"{self.frame_prompts[framing]}\n\nOriginal dilemma: {dilemma.description}\n\nReframed dilemma:"
        
        logger.debug(f"Generated transformation prompt for {framing.value}")
        return prompt
    
    def get_transformation_prompt(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        Get the transformation prompt without calling LLM.
        This is what the current transform_dilemma actually does.
        
        Args:
            dilemma: The ethical dilemma to transform
            framing: The deictic framing to apply
            
        Returns:
            A prompt for LLM transformation
        """
        return self.transform_dilemma(dilemma, framing)
    
    def transform_dilemma_direct(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        Generate a direct question based on minimal deictic guidance.
        This version provides more immediate usability while still being generative.
        
        Args:
            dilemma: The ethical dilemma to transform  
            framing: The deictic framing to apply
            
        Returns:
            A direct ethical question in the specified framing
        """
        # Extract core elements dynamically without hardcoded patterns
        core_tension = self._extract_dynamic_tension(dilemma.description)
        
        # Generate framing-specific question with minimal prescription
        if framing == DeicticFraming.IMPERSONAL:
            return f"What is the appropriate response when one faces {core_tension}?"
        
        elif framing == DeicticFraming.SECOND_PERSON:
            return f"How should you respond when you encounter {core_tension}?"
        
        elif framing == DeicticFraming.FIRST_PERSON:
            return f"How should I handle the situation when I face {core_tension}?"
        
        elif framing == DeicticFraming.REFLEXIVE:
            return f"If you were facing {core_tension}, what would you do?"
        
        elif framing == DeicticFraming.DIALOGIC:
            return f"How should we collectively respond when we encounter {core_tension}?"
        
        elif framing == DeicticFraming.SPATIAL:
            return f"Standing at this crossroads where {core_tension} presents itself, what path should be taken?"
        
        elif framing == DeicticFraming.TEMPORAL:
            return f"In this critical moment when {core_tension} demands resolution, what action is called for?"
        
        elif framing == DeicticFraming.COSMOLOGICAL:
            return f"When the universe presents {core_tension}, what response honors the greater order?"
        
        else:
            return f"How should one respond when facing {core_tension}?"
    
    def _extract_dynamic_tension(self, description: str) -> str:
        """
        Dynamically extract the core ethical tension without predefined patterns.
        Uses simple NLP techniques to identify key conflicts.
        """
        description_lower = description.lower()
        
        # Look for common ethical tension indicators
        tension_patterns = [
            # Conflict patterns
            (r'between (.+?) and (.+?)(?:\.|,|$)', lambda m: f"the choice between {m.group(1)} and {m.group(2)}"),
            (r'must choose (.+?)(?:\.|,|$)', lambda m: f"having to choose {m.group(1)}"),
            (r'either (.+?) or (.+?)(?:\.|,|$)', lambda m: f"deciding between {m.group(1)} or {m.group(2)}"),
            
            # Harm patterns
            (r'could (.+?) harm (.+?)(?:\.|,|$)', lambda m: f"actions that could {m.group(1)} harm {m.group(2)}"),
            (r'might (.+?) damage (.+?)(?:\.|,|$)', lambda m: f"decisions that might {m.group(1)} damage {m.group(2)}"),
            
            # Obligation patterns
            (r'should (.+?) but (.+?)(?:\.|,|$)', lambda m: f"the tension between should {m.group(1)} but {m.group(2)}"),
            (r'wants to (.+?) but (.+?)(?:\.|,|$)', lambda m: f"wanting to {m.group(1)} but {m.group(2)}"),
            
            # Professional/personal patterns
            (r'professional (.+?) and personal (.+?)(?:\.|,|$)', lambda m: f"professional {m.group(1)} conflicting with personal {m.group(2)}"),
            (r'duty (.+?) and (.+?)(?:\.|,|$)', lambda m: f"duty {m.group(1)} versus {m.group(2)}"),
            
            # Whistleblowing specific patterns
            (r'report(?:ing)? .+? but .+? risk', lambda m: f"the choice between reporting wrongdoing and personal risk"),
            (r'losing .+? job .+? but .+? silent', lambda m: f"risking career security versus protecting others"),
        ]
        
        # Try each pattern
        for pattern, formatter in tension_patterns:
            match = re.search(pattern, description_lower)
            if match:
                try:
                    return formatter(match)
                except:
                    continue
        
        # Improved fallback: extract meaningful conflict
        return self._extract_meaningful_conflict(description)
    
    def _extract_meaningful_conflict(self, description: str) -> str:
        """Extract meaningful ethical conflict from the description."""
        description_lower = description.lower()
        
        # Look for key conflict indicators
        if "whistleblowing" in description_lower or "report" in description_lower:
            if "job" in description_lower or "career" in description_lower:
                return "the choice between exposing wrongdoing and protecting one's career"
        
        if "security flaw" in description_lower or "data" in description_lower:
            if "users" in description_lower:
                return "the conflict between corporate interests and user safety"
        
        if "losing" in description_lower and "job" in description_lower:
            if "silent" in description_lower:
                return "the dilemma of personal security versus public responsibility"
        
        # Extract opposing forces
        opposing_concepts = []
        
        # Look for personal vs professional
        if any(word in description_lower for word in ["job", "career", "blacklisted"]):
            opposing_concepts.append("personal security")
        
        # Look for harm to others
        if any(word in description_lower for word in ["users", "risk", "harm", "expose"]):
            opposing_concepts.append("protecting others")
        
        # Look for organizational issues
        if any(word in description_lower for word in ["company", "profits", "cost"]):
            opposing_concepts.append("organizational interests")
        
        if len(opposing_concepts) >= 2:
            return f"the tension between {opposing_concepts[0]} and {opposing_concepts[1]}"
        elif opposing_concepts:
            return f"an ethical challenge involving {opposing_concepts[0]}"
        
        # Ultimate fallback
        return "a complex ethical situation requiring careful consideration"
    
    def analyze_deictic_markers(self, response_text: str) -> Dict[str, int]:
        """
        Comprehensive deictic marker analysis to study LLM deictic behavior.
        More categories than previous versions to capture nuanced usage.
        """
        markers = {
            # Pronoun categories
            "first_person_singular": 0,  # I, me, my, mine, myself
            "first_person_plural": 0,    # we, us, our, ours, ourselves  
            "second_person": 0,          # you, your, yours, yourself
            "third_person": 0,           # he, she, they, them, their, one
            
            # Temporal categories
            "temporal_immediate": 0,     # now, currently, presently, at this moment
            "temporal_specific": 0,      # then, when, during, while, after, before
            "temporal_urgency": 0,       # immediately, urgent, critical time, deadline
            
            # Spatial categories  
            "spatial_proximity": 0,      # here, there, nearby, close, distant
            "spatial_position": 0,       # standing, sitting, positioned, located
            "spatial_direction": 0,      # forward, backward, up, down, toward, away
            
            # Demonstrative categories
            "demonstrative_proximal": 0, # this, these
            "demonstrative_distal": 0,   # that, those
            
            # Cosmic/transcendent categories
            "cosmic_entities": 0,        # ancestors, spirits, gods, universe, cosmos
            "cosmic_concepts": 0,        # eternal, divine, sacred, transcendent, cosmic
            "natural_forces": 0,         # stars, earth, nature, elements
            "non_human_agency": 0,       # animals, plants, rivers, forests, spirits as agents
            "perspectivism_markers": 0,  # how animals/spirits/nature might view, perspectives of
            
            # Agency markers
            "individual_agency": 0,      # decide, choose, act, respond (singular)
            "collective_agency": 0,      # decide, choose, act, respond (plural)
            "passive_agency": 0,         # is decided, is chosen, happens, occurs
            
            # Moral reasoning markers
            "obligation_language": 0,    # should, must, ought, duty, responsibility
            "permission_language": 0,    # may, can, could, allowed, permitted
            "evaluation_language": 0,    # right, wrong, good, bad, appropriate
            
            "total_markers": 0
        }
        
        text_lower = response_text.lower()
        
        # First person singular
        first_sing_words = [" i ", " me ", " my ", " mine ", " myself "]
        markers["first_person_singular"] = sum(response_text.count(word) for word in first_sing_words)
        
        # First person plural  
        first_plur_words = [" we ", " us ", " our ", " ours ", " ourselves "]
        markers["first_person_plural"] = sum(response_text.count(word) for word in first_plur_words)
        
        # Second person
        second_words = [" you ", " your ", " yours ", " yourself "]
        markers["second_person"] = sum(response_text.count(word) for word in second_words)
        
        # Third person
        third_words = [" he ", " she ", " they ", " them ", " their ", " one "]
        markers["third_person"] = sum(response_text.count(word) for word in third_words)
        
        # Temporal immediate
        temp_imm_words = ["now", "currently", "presently", "at this moment", "right now"]
        markers["temporal_immediate"] = sum(text_lower.count(word) for word in temp_imm_words)
        
        # Temporal specific
        temp_spec_words = ["then", "when", "during", "while", "after", "before", "moment"]
        markers["temporal_specific"] = sum(text_lower.count(word) for word in temp_spec_words)
        
        # Temporal urgency
        temp_urg_words = ["immediately", "urgent", "critical time", "deadline", "quickly"]
        markers["temporal_urgency"] = sum(text_lower.count(word) for word in temp_urg_words)
        
        # Spatial proximity
        spat_prox_words = ["here", "there", "nearby", "close", "distant"]
        markers["spatial_proximity"] = sum(text_lower.count(word) for word in spat_prox_words)
        
        # Spatial position
        spat_pos_words = ["standing", "sitting", "positioned", "located", "placed"]
        markers["spatial_position"] = sum(text_lower.count(word) for word in spat_pos_words)
        
        # Spatial direction
        spat_dir_words = ["forward", "backward", "toward", "away", "up", "down"]
        markers["spatial_direction"] = sum(text_lower.count(word) for word in spat_dir_words)
        
        # Demonstrative proximal
        demo_prox_words = ["this", "these"]
        markers["demonstrative_proximal"] = sum(text_lower.count(word) for word in demo_prox_words)
        
        # Demonstrative distal
        demo_dist_words = ["that", "those"] 
        markers["demonstrative_distal"] = sum(text_lower.count(word) for word in demo_dist_words)
        
        # Cosmic entities
        cosmic_ent_words = ["ancestors", "spirits", "gods", "universe", "cosmos", "divine"]
        markers["cosmic_entities"] = sum(text_lower.count(word) for word in cosmic_ent_words)
        
        # Cosmic concepts
        cosmic_con_words = ["eternal", "sacred", "transcendent", "cosmic", "spiritual"]
        markers["cosmic_concepts"] = sum(text_lower.count(word) for word in cosmic_con_words)
        
        # Natural forces
        nat_force_words = ["stars", "earth", "nature", "elements", "moon", "sun"]
        markers["natural_forces"] = sum(text_lower.count(word) for word in nat_force_words)
        
        # Non-human agency
        non_human_agency_words = ["animals", "plants", "rivers", "forests", "trees", "mountains", "spirits decide", "nature chooses", "earth responds"]
        markers["non_human_agency"] = sum(text_lower.count(word) for word in non_human_agency_words)
        
        # Perspectivism markers
        perspectivism_words = ["how animals might view", "from the perspective of", "spirits might see", "nature's viewpoint", "what would the forest", "animals would say"]
        markers["perspectivism_markers"] = sum(text_lower.count(phrase) for phrase in perspectivism_words)
        
        # Individual agency (simplified detection)
        indiv_agency_words = ["i decide", "i choose", "i act", "i respond", "i will"]
        markers["individual_agency"] = sum(text_lower.count(word) for word in indiv_agency_words)
        
        # Collective agency
        coll_agency_words = ["we decide", "we choose", "we act", "we respond", "we will"]
        markers["collective_agency"] = sum(text_lower.count(word) for word in coll_agency_words)
        
        # Passive agency
        pass_agency_words = ["is decided", "is chosen", "happens", "occurs", "emerges"]
        markers["passive_agency"] = sum(text_lower.count(word) for word in pass_agency_words)
        
        # Obligation language
        oblig_words = ["should", "must", "ought", "duty", "responsibility", "obligation"]
        markers["obligation_language"] = sum(text_lower.count(word) for word in oblig_words)
        
        # Permission language
        perm_words = ["may", "can", "could", "allowed", "permitted", "possible"]
        markers["permission_language"] = sum(text_lower.count(word) for word in perm_words)
        
        # Evaluation language
        eval_words = ["right", "wrong", "good", "bad", "appropriate", "correct", "proper"]
        markers["evaluation_language"] = sum(text_lower.count(word) for word in eval_words)
        
        # Calculate total
        markers["total_markers"] = sum(markers[key] for key in markers if key != "total_markers")
        
        return markers
    
    def suggest_frame_type(self, text: str) -> Tuple[DeicticFraming, float]:
        """
        Analyze text and suggest the most likely deictic frame type.
        Uses the comprehensive marker analysis to make suggestions.
        """
        markers = self.analyze_deictic_markers(text)
        
        # Score each frame type based on marker presence
        frame_scores = {
            DeicticFraming.IMPERSONAL: markers["third_person"] + markers["passive_agency"] + markers["evaluation_language"],
            DeicticFraming.SECOND_PERSON: markers["second_person"] * 2,
            DeicticFraming.FIRST_PERSON: markers["first_person_singular"] * 2,
            DeicticFraming.REFLEXIVE: markers["second_person"] + markers["first_person_singular"],
            DeicticFraming.DIALOGIC: markers["first_person_plural"] * 2 + markers["collective_agency"],
            DeicticFraming.SPATIAL: markers["spatial_proximity"] + markers["spatial_position"] + markers["spatial_direction"],
            DeicticFraming.TEMPORAL: markers["temporal_immediate"] + markers["temporal_specific"] + markers["temporal_urgency"],
            DeicticFraming.COSMOLOGICAL: markers["cosmic_entities"] + markers["cosmic_concepts"] + markers["natural_forces"]
        }
        
        # Find highest score
        best_frame = max(frame_scores.keys(), key=lambda k: frame_scores[k])
        max_score = frame_scores[best_frame]
        
        # Calculate confidence (normalized by total markers)
        total = markers["total_markers"]
        confidence = (max_score / total) if total > 0 else 0.0
        
        return best_frame, confidence
    
    def get_available_framings(self) -> List[DeicticFraming]:
        """Get list of available deictic framings."""
        return list(self.frame_prompts.keys())
    
    def get_framing_description(self, framing: DeicticFraming) -> str:
        """Get the minimal prompt for a framing (less prescriptive than previous versions)."""
        return self.frame_prompts.get(framing, "No description available")
    
    def preview_transformation(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> Dict[str, str]:
        """Preview both generation and direct approaches."""
        generative_prompt = self.transform_dilemma(dilemma, framing)
        direct_question = self.transform_dilemma_direct(dilemma, framing)
        core_tension = self._extract_dynamic_tension(dilemma.description)
        
        return {
            "original": dilemma.description,
            "framing_type": framing.value,
            "core_tension_extracted": core_tension,
            "generative_prompt": generative_prompt,
            "direct_question": direct_question,
            "approach": "Minimal prescription, maximum LLM generation"
        }
