"""
Interrogative Deictic Transformer: Direct questions that interrogate the latent space.
Designed to study how LLMs respond to ethical questions from different deictic perspectives.
"""

from typing import Dict, List, Optional, Tuple
from models.schemas import EthicalDilemma, DeicticFraming
import logging
import re
import random

logger = logging.getLogger(__name__)

# Create alias for backward compatibility
DeicticFrameType = DeicticFraming

class DeicticTransformer:
    """
    Transformer that generates direct interrogative questions for each deictic frame.
    No meta-instructions, just pure questions that embed the dilemma context naturally.
    """
    
    def __init__(self):
        """Initialize with interrogative patterns for each deictic frame."""
        self.question_patterns = self._initialize_question_patterns()
        logger.info("Interrogative deictic transformer initialized")
    
    def _initialize_question_patterns(self) -> Dict[DeicticFraming, List[str]]:
        """Initialize multiple question patterns for each framing type."""
        return {
            DeicticFraming.IMPERSONAL: [
                "What happens when {concrete_situation} but {boss_action} and {personal_risk}?",
                "In situations where one discovers {discovery} but faces {cost}, what occurs?",
                "When faced with {problem} while {stakes}, what takes place?",
                "How does one describe the tension between {value_a} and {value_b} when {concrete_situation}?",
                "What emerges when {discovery} yet reporting means {cost} and silence means {harm}?"
            ],
            
            DeicticFraming.SECOND_PERSON: [
                "You discover {concrete_situation}. {concrete_stakes}. What do you do?",
                "You find out {discovery}. If you {action_a}, {consequence_a}. If you {action_b}, {consequence_b}. How do you respond?",
                "You learn that {problem}. Your boss {boss_action}. You could {personal_risk}. What action do you take?",
                "You uncover {issue}. Reporting it means {cost}. Staying silent means {harm}. What's your decision?",
                "You face a choice: {option_a} or {option_b}. What do you do?"
            ],
            
            DeicticFraming.FIRST_PERSON: [
                "I {discovered} {situation}, knowing that {option_a} could cost me my career while {option_b} means {consequence_b}. What should I choose and why?",
                "I'm facing an ethical dilemma where {concrete_situation} but taking action means I could {personal_risk}. How do I weigh my moral obligations?",
                "I must choose between {option_a} and {option_b}, knowing the stakes are {stakes}. What ethical principles should guide my decision?",
                "Given that I know {concrete_situation} while risking {cost} if I act, how do I balance my integrity with my survival?",
                "I'm torn between {competing_values} in a situation where {harm} if I stay silent. What would a person of conscience do?"
            ],
            
            DeicticFraming.REFLEXIVE: [
                "If one were in a position where {concrete_situation} while {personal_risk}, how might one respond?",
                "Putting yourself in the shoes of someone who {discovers}, what would you do?",
                "Imagine being faced with {dilemma}. What considerations would guide your decision?",
                "If you found yourself having to choose between {option_a} and {option_b}, knowing that {stakes}, how would you approach it?",
                "Consider being someone who discovers {problem}. What path forward exists?"
            ],
            
            DeicticFraming.DIALOGIC: [
                "We discovered {concrete_situation}. If we report it, we {personal_risk}. If we stay silent, {harm}. How do we proceed together?",
                "Our team found {discovery}. The company {boss_action}. We face a choice: report and {cost}, or stay silent while {harm}. What happens next?",
                "We must decide: {option_a} risking {cost}, or {option_b} allowing {harm}. How do we reach consensus?",
                "Together we discovered {problem}. Reporting means {cost}, silence means {harm}. What path do we take as a group?",
                "We're confronted with {concrete_situation}. We could {personal_risk} if we speak up. How do we respond as a community?"
            ],
            
            DeicticFraming.SPATIAL: [
                "Standing at the crossroads between {option_a} and {option_b}, with {stakes} on both sides, what do you see?",
                "Positioned between {competing_forces} where {concrete_situation}, what appears in each direction?",
                "At this juncture where you must choose between {option_a} (meaning {cost}) and {option_b} (meaning {harm}), what lies ahead?",
                "Finding yourself at the intersection of {discovery} and {personal_risk}, what surrounds you?",
                "From where you stand facing {problem} with {boss_action}, what do you observe?"
            ],
            
            DeicticFraming.TEMPORAL: [
                "In this moment when {concrete_situation}, with the choice to report and {personal_risk} or stay silent while {harm}, what happens?",
                "Now, with {discovery}, facing either {option_a} and {cost} or {option_b} as {harm}, what unfolds?",
                "At this critical juncture where you know {problem} - report it and {personal_risk}, or stay silent while {harm} - what occurs?",
                "Given the urgency of {concrete_situation}, choosing between {option_a} (risking {cost}) and {option_b} (allowing {harm}), what takes place?",
                "Time is of the essence: {discovery}. Report means {cost}, silence means {harm}. What emerges?"
            ],
            
            DeicticFraming.COSMOLOGICAL: [
                "How might {non_human_agents} view this situation where {concrete_situation}?",
                "If {natural_entities} could speak about {discovery} and the choice between {option_a} and {option_b}, what would they say?",
                "From the perspective of {non_human_perspective}, how does {problem} with {stakes} appear?",
                "What would {cosmic_entities} think about humans facing {discovery} where {consequence_a} or {consequence_b}?",
                "How do {multiple_beings} each see this situation differently - where {concrete_situation} but choosing action means you {personal_risk}?"
            ]
        }
    
    def _extract_dilemma_elements(self, dilemma: EthicalDilemma) -> Dict[str, str]:
        """
        Extract key elements from the dilemma for natural integration.
        
        Returns a dictionary with flexible keys that can be used in patterns.
        """
        description = dilemma.description
        elements = {}
        
        # Extract the core conflict or tension
        if "but" in description.lower():
            parts = description.lower().split("but", 1)
            elements["conflict"] = f"{parts[0].strip()} but {parts[1].strip()}"
        else:
            elements["conflict"] = self._summarize_conflict(description)
        
        # Extract competing values or options
        elements["competing_values"] = self._extract_competing_values(description)
        elements["value_a"], elements["value_b"] = self._split_competing_values(elements["competing_values"])
        
        # Extract the situation description
        elements["situation"] = self._extract_situation(description)
        elements["dilemma"] = self._extract_dilemma_summary(description)
        
        # Extract action words
        elements["discover"] = self._extract_discovery_verb(description)
        elements["discovered"] = self._past_tense(elements["discover"])
        
        # Extract options if present
        elements["option_a"], elements["option_b"] = self._extract_options(description)
        
        # Additional elements for specific framings
        elements["urgent_situation"] = self._extract_urgent_aspect(description)
        elements["time_sensitive_issue"] = elements["urgent_situation"]
        elements["stakes"] = self._extract_stakes(description)
        elements["issue"] = self._extract_core_issue(description)
        elements["ethical_goal"] = "a resolution"
        elements["competing_forces"] = elements["competing_values"]
        elements["paths_diverge"] = f"{elements['option_a']} and {elements['option_b']}"
        elements["value"] = "an outcome"
        elements["conflicts"] = elements["competing_values"]
        elements["cosmic_view"] = self._extract_cosmic_perspective(description)
        elements["universal_value"] = "the greater good"
        elements["eternal_principle"] = "universal justice"
        elements["sacred_domain"] = self._extract_sacred_domain(description)
        
        # Perspectivism elements for cosmological framing
        elements["non_human_agents"] = self._extract_non_human_agents(description)
        elements["natural_entities"] = self._extract_natural_entities(description)
        elements["non_human_perspective"] = self._extract_non_human_perspective(description)
        elements["cosmic_entities"] = self._extract_cosmic_entities(description)
        elements["multiple_beings"] = "animals, spirits, plants, and rivers"
        
        # Context elements
        elements["context"] = self._extract_context(description)
        elements["encounter_situation"] = f"encounter {elements['situation']}"
        elements["discovers"] = f"discovers {elements['issue']}"
        
        # Clean up elements to avoid repetitive text
        if "that their company" in elements["situation"]:
            elements["situation"] = elements["issue"]
        if "that their company" in elements["dilemma"]:
            elements["dilemma"] = self._extract_dilemma_summary(description)
        
        # Add more concrete elements for better questions
        elements["concrete_situation"] = self._extract_concrete_situation(description)
        elements["concrete_stakes"] = self._extract_concrete_stakes(description)
        elements["discovery"] = self._extract_discovery(description)
        elements["problem"] = self._extract_problem(description)
        elements["boss_action"] = self._extract_boss_action(description)
        elements["personal_risk"] = self._extract_personal_risk(description)
        elements["action_a"] = "report it"
        elements["action_b"] = "stay silent"
        elements["consequence_a"] = self._extract_consequence_a(description)
        elements["consequence_b"] = self._extract_consequence_b(description)
        elements["cost"] = self._extract_personal_cost(description)
        elements["harm"] = self._extract_harm_to_others(description)
        
        return elements
    
    def _extract_situation(self, description: str) -> str:
        """Extract a concise situation description."""
        # Look for key phrases that indicate the situation
        if "discovers" in description.lower():
            match = re.search(r'discovers?\s+(.+?)(?:\.|,|;)', description.lower())
            if match:
                situation = match.group(1).strip()
                # Clean up the extracted situation
                if len(situation) > 100:
                    # If too long, extract the core issue
                    if "security flaw" in situation:
                        return "a critical security vulnerability"
                    elif "data" in situation and "expose" in situation:
                        return "a data exposure risk"
                return situation
        
        # Fallback to extracting key issue
        if "security flaw" in description.lower():
            return "a security vulnerability"
        elif "allocate" in description.lower() and "ventilator" in description.lower():
            return "a resource allocation crisis"
        elif "factory" in description.lower() and "environment" in description.lower():
            return "an environmental conflict"
        
        return "an ethical dilemma"
        
    def _summarize_conflict(self, description: str) -> str:
        """Extract a summary of the ethical conflict."""
        if "security flaw" in description.lower() and "users" in description.lower():
            return "professional obligations conflict with organizational directives regarding user safety"
        elif "job" in description.lower() and "report" in description.lower():
            return "personal security conflicts with public responsibility"
        else:
            return "competing ethical demands"
    
    def _extract_competing_values(self, description: str) -> str:
        """Extract the competing values or demands."""
        if "job" in description.lower() and "users" in description.lower():
            return "job security and user protection"
        elif "profits" in description.lower() and "safety" in description.lower():
            return "corporate profits and public safety"
        else:
            return "personal interests and collective welfare"
    
    def _split_competing_values(self, competing_values: str) -> Tuple[str, str]:
        """Split competing values into two parts."""
        if " and " in competing_values:
            parts = competing_values.split(" and ", 1)
            return parts[0].strip(), parts[1].strip()
        return competing_values, "the alternative"
    
    def _extract_dilemma_summary(self, description: str) -> str:
        """Extract a summary of the dilemma."""
        if "security flaw" in description.lower() and "report" in description.lower():
            return "whether to report a security vulnerability at personal cost"
        elif "allocate" in description.lower() and "ventilator" in description.lower():
            return "how to allocate scarce medical resources"
        elif "factory" in description.lower() and "environment" in description.lower():
            return "choosing between economic survival and environmental health"
        elif "but" in description.lower():
            # Extract the core tension
            parts = description.split("but", 1)
            if len(parts[0]) < 100:
                return parts[0].strip().lower()
        return "a difficult ethical choice"
    
    def _extract_discovery_verb(self, description: str) -> str:
        """Extract the discovery/encounter verb."""
        verbs = ["discover", "find", "learn", "realize", "uncover", "encounter", "face", "must"]
        for verb in verbs:
            if verb in description.lower():
                return verb
        return "discover"
    
    def _past_tense(self, verb: str) -> str:
        """Convert verb to past tense."""
        past_tense_map = {
            "discover": "discovered",
            "find": "found",
            "learn": "learned",
            "realize": "realized",
            "uncover": "uncovered",
            "encounter": "encountered"
        }
        return past_tense_map.get(verb, verb + "ed")
    
    def _extract_options(self, description: str) -> Tuple[str, str]:
        """Extract the two main options or choices."""
        if "report" in description.lower() and "silent" in description.lower():
            return "reporting the issue", "staying silent"
        elif "fix" in description.lower() and "ignore" in description.lower():
            return "fixing the problem", "ignoring it"
        else:
            return "taking action", "remaining passive"
    
    def _extract_urgent_aspect(self, description: str) -> str:
        """Extract the urgent or time-sensitive aspect."""
        if "millions" in description.lower() and "risk" in description.lower():
            return "millions of users are at immediate risk"
        elif "critical" in description.lower():
            return "a critical decision point"
        else:
            return "an urgent ethical decision"
    
    def _extract_stakes(self, description: str) -> str:
        """Extract what's at stake."""
        if "millions of users" in description.lower():
            return "millions of users' data and privacy"
        elif "lives" in description.lower():
            return "human lives"
        else:
            return "significant consequences"
    
    def _extract_core_issue(self, description: str) -> str:
        """Extract the core ethical issue."""
        if "security flaw" in description.lower():
            return "a security vulnerability that endangers users"
        elif "whistleblowing" in description.lower():
            return "corporate wrongdoing"
        else:
            return "an ethical violation"
    
    def _extract_cosmic_perspective(self, description: str) -> str:
        """Extract a cosmic or universal perspective."""
        if "trust" in description.lower() or "users" in description.lower():
            return "digital trust forms the foundation of modern society"
        elif "environment" in description.lower():
            return "humanity's relationship with nature"
        else:
            return "the interconnectedness of all beings"
    
    def _extract_sacred_domain(self, description: str) -> str:
        """Extract what sacred domain is threatened."""
        if "data" in description.lower() or "privacy" in description.lower():
            return "digital privacy and trust"
        elif "environment" in description.lower():
            return "the natural world"
        else:
            return "human dignity"
    
    def _extract_context(self, description: str) -> str:
        """Extract relevant context."""
        # Take the middle sentence if available
        sentences = description.split('.')
        if len(sentences) > 1:
            return sentences[1].strip().lower()
        return "the current situation"
    
    def _extract_concrete_situation(self, description: str) -> str:
        """Extract a concrete situation description."""
        if "security flaw" in description.lower() and "app" in description.lower():
            return "your company's app has a security flaw exposing millions of users' data"
        elif "ventilator" in description.lower():
            return "you must allocate the last ventilator"
        elif "factory" in description.lower() and "water" in description.lower():
            return "your town's main employer is poisoning the water supply"
        return "a critical ethical situation"
    
    def _extract_concrete_stakes(self, description: str) -> str:
        """Extract concrete stakes."""
        if "millions of users" in description.lower():
            return "Millions of users' data is at risk"
        elif "lives" in description.lower():
            return "Lives hang in the balance"
        return "Serious consequences await"
    
    def _extract_discovery(self, description: str) -> str:
        """Extract what was discovered."""
        if "security flaw" in description.lower():
            return "a critical security vulnerability in their company's app"
        return "a serious ethical problem"
    
    def _extract_problem(self, description: str) -> str:
        """Extract the core problem."""
        if "refuses to fix" in description.lower():
            return "your company refuses to fix a security flaw affecting millions"
        return "there's a serious ethical violation"
    
    def _extract_boss_action(self, description: str) -> str:
        """Extract what the boss/authority does."""
        if "refuses to fix" in description.lower():
            return "refuses to fix it due to cost"
        return "opposes taking action"
    
    def _extract_personal_risk(self, description: str) -> str:
        """Extract personal risk."""
        if "blacklisted" in description.lower():
            return "lose your job and be blacklisted from the industry"
        elif "job" in description.lower():
            return "lose your job"
        return "face serious consequences"
    
    def _extract_consequence_a(self, description: str) -> str:
        """Extract consequence of action A (usually reporting)."""
        if "blacklisted" in description.lower():
            return "you lose your career"
        return "you face retaliation"
    
    def _extract_consequence_b(self, description: str) -> str:
        """Extract consequence of action B (usually staying silent)."""
        if "millions" in description.lower() and "risk" in description.lower():
            return "millions remain at risk"
        return "the problem continues"
    
    def _extract_personal_cost(self, description: str) -> str:
        """Extract personal cost of taking action."""
        if "job" in description.lower() and "blacklisted" in description.lower():
            return "losing your job and being blacklisted"
        return "personal sacrifice"
    
    def _extract_harm_to_others(self, description: str) -> str:
        """Extract harm to others from inaction."""
        if "millions of users" in description.lower():
            return "millions of users remain vulnerable to hackers"
        return "others suffer"
    
    def _extract_non_human_agents(self, description: str) -> str:
        """Extract relevant non-human agents for perspectivism."""
        if "data" in description.lower() or "digital" in description.lower():
            return "the data streams and digital spirits"
        elif "water" in description.lower():
            return "the rivers and water spirits"
        elif "environment" in description.lower():
            return "the forest beings and earth spirits"
        return "the spirits and non-human beings"
    
    def _extract_natural_entities(self, description: str) -> str:
        """Extract natural entities that might have perspective."""
        if "users" in description.lower() and "data" in description.lower():
            return "the electrons flowing through servers"
        elif "factory" in description.lower():
            return "the poisoned waters and suffering fish"
        return "the affected natural beings"
    
    def _extract_non_human_perspective(self, description: str) -> str:
        """Extract a non-human perspective viewpoint."""
        if "security" in description.lower():
            return "data packets traveling through networks"
        elif "environment" in description.lower():
            return "rivers and soil"
        return "non-human consciousness"
    
    def _extract_cosmic_entities(self, description: str) -> str:
        """Extract cosmic entities for perspectivism."""
        if "millions" in description.lower():
            return "the ancestors watching over digital realms"
        elif "community" in description.lower():
            return "the spirit guardians of the land"
        return "the cosmic observers"
    
    def transform_to_question(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        Transform a dilemma into a direct interrogative question.
        
        Args:
            dilemma: The ethical dilemma to transform
            framing: The deictic framing to apply
            
        Returns:
            A direct question that embeds the dilemma context
        """
        # Extract key elements from the dilemma
        elements = self._extract_dilemma_elements(dilemma)
        
        # Select a random pattern for variety
        patterns = self.question_patterns.get(framing, [])
        if not patterns:
            raise ValueError(f"No patterns defined for framing: {framing}")
        
        pattern = random.choice(patterns)
        
        # Generate the question based on the framing
        return self._fill_pattern(pattern, elements, framing)
        
    def transform_dilemma(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        Generate a direct interrogative question for the dilemma.
        
        Args:
            dilemma: The ethical dilemma to transform
            framing: The deictic framing to apply
            
        Returns:
            A direct question in the specified deictic frame
        """
        return self.transform_to_question(dilemma, framing)
    

    
    def get_transformation_prompt(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        For backward compatibility - returns the direct question.
        
        Args:
            dilemma: The ethical dilemma to transform
            framing: The deictic framing to apply
            
        Returns:
            A direct question (no meta-instructions)
        """
        return self.transform_to_question(dilemma, framing)
    
    def transform_dilemma_direct(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> str:
        """
        For backward compatibility - returns the direct question.
        
        Args:
            dilemma: The ethical dilemma to transform  
            framing: The deictic framing to apply
            
        Returns:
            A direct question in the specified framing
        """
        return self.transform_to_question(dilemma, framing)
        
    def _fill_pattern(self, pattern: str, elements: Dict[str, str], framing: DeicticFraming) -> str:
        """Fill a pattern with extracted elements to create a natural question."""
        question = pattern
        
        # Replace all placeholders with corresponding elements
        for key, value in elements.items():
            placeholder = f"{{{key}}}"
            if placeholder in question:
                question = question.replace(placeholder, value)
        
        # Clean up any remaining placeholders
        question = re.sub(r'\{[^}]+\}', '', question)
        
        # Ensure proper capitalization and punctuation
        question = question.strip()
        if question and question[0].islower():
            question = question[0].upper() + question[1:]
        
        # Ensure it ends with a question mark
        if not question.endswith('?'):
            question += '?'
        
        return question
    
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
        return list(self.question_patterns.keys())
    
    def get_framing_description(self, framing: DeicticFraming) -> str:
        """Get description of what this framing does."""
        descriptions = {
            DeicticFraming.IMPERSONAL: "Uses impersonal, objective language (one, what occurs)",
            DeicticFraming.SECOND_PERSON: "Direct address to 'you' as decision-maker",
            DeicticFraming.FIRST_PERSON: "Personal 'I' perspective facing the choice",
            DeicticFraming.REFLEXIVE: "Perspective-taking (if you were in this position)",
            DeicticFraming.DIALOGIC: "Collective language (we, us, our shared decision)",
            DeicticFraming.SPATIAL: "Spatial metaphors (crossroads, paths, directions)",
            DeicticFraming.TEMPORAL: "Temporal urgency (now, this moment, immediate)",
            DeicticFraming.COSMOLOGICAL: "Multiple beings' perspectives (spirits, ancestors, nature)"
        }
        return descriptions.get(framing, "No description available")
    
    def preview_transformation(self, dilemma: EthicalDilemma, framing: DeicticFraming) -> Dict[str, str]:
        """Preview the interrogative transformation."""
        question = self.transform_to_question(dilemma, framing)
        elements = self._extract_dilemma_elements(dilemma)
        
        return {
            "original": dilemma.description,
            "framing_type": framing.value,
            "interrogative_question": question,
            "approach": "Direct interrogative - no meta-instructions",
            "extracted_elements": {
                "conflict": elements.get("conflict", ""),
                "competing_values": elements.get("competing_values", ""),
                "core_issue": elements.get("issue", "")
            }
        }
