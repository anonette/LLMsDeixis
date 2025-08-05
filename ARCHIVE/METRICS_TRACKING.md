# Metrics Tracking in Deixis Analysis

## Overview
The system tracks comprehensive metrics for each deictic framing to understand how different interrogative approaches affect LLM responses.

## Tracked Metrics

### 1. Response Characteristics
- **Response Length** (`response_length`): Character count of LLM response
- **Processing Time** (`processing_time`): Total seconds from question to analysis completion
- **Timestamp**: Exact time of analysis

### 2. Deictic Markers (Linguistic Patterns)
Counts of specific language features in the response:
- **Pronouns**: first_person_singular, first_person_plural, second_person, third_person
- **Temporal**: temporal_immediate, temporal_specific, temporal_urgency
- **Spatial**: spatial_proximity, spatial_position, spatial_direction
- **Demonstrative**: demonstrative_proximal, demonstrative_distal
- **Cosmic**: cosmic_entities, cosmic_concepts, natural_forces, non_human_agency
- **Agency**: individual_agency, collective_agency, passive_agency
- **Moral Language**: obligation_language, permission_language, evaluation_language
- **Total Markers**: Sum of all deictic markers

### 3. Analysis Metadata
- **Dilemma ID**: Which ethical scenario was analyzed
- **Framing Type**: Which deictic frame was used (impersonal, second_person, etc.)
- **Model Used**: Which LLM generated the response
- **Suggested Frame**: What frame the response naturally fits
- **Frame Confidence**: How well the response matches its intended frame

## Data Storage

### DeicticAnalysisResult Schema
```python
@dataclass
class DeicticAnalysisResult:
    dilemma_id: str
    framing: DeicticFraming
    transformed_prompt: str
    llm_response: str
    agency_analysis: AgencyAnalysis
    ethical_framing_analysis: EthicalFramingAnalysis
    deictic_markers: dict
    response_length: int          # Tracked here
    processing_time: float        # Tracked here
    timestamp: datetime
```

### Analysis Logger
The `RichAnalysisLogger` records all metrics for each analysis:
- Session-based tracking
- JSON export capability
- Aggregated statistics

## Use Cases

1. **Compare Response Patterns**: How do different framings affect response length?
2. **Performance Analysis**: Which framings take longer to process?
3. **Linguistic Analysis**: Which framings elicit more first-person vs third-person language?
4. **Temporal Patterns**: Do certain framings trigger more urgency language?
5. **Agency Distribution**: How does framing affect who is seen as the decision-maker?

## Example Insights
- Second-person framings ("You discover...") may generate longer, more detailed responses
- Cosmological framings may have higher processing times due to complex perspective-taking
- Impersonal framings may show more passive agency markers
- First-person framings likely have highest first_person_singular counts

## Access Methods
1. Real-time: Each `DeicticAnalysisResult` contains metrics
2. Session logs: `analysis_logger.py` saves all metrics
3. Batch analysis: Can aggregate metrics across multiple analyses
4. Export: JSON format for external analysis