# Deixis Analysis Visualizations

## Response Length Distribution

### By Model
```
GPT-4o:    ████████████████████ (~650 words avg)
Claude:    ███████████████████████ (~750 words avg)  
DeepSeek:  ██████████████ (469 words avg)
```

## Ethical Framework Usage

### GPT-4o
```
Utilitarian:    █████████ 45%
Deontological:  ██████ 30%
Virtue Ethics:  ███ 15%
Care Ethics:    ██ 10%
```

### Claude 3.5 Sonnet
```
Utilitarian:    ███████ 35%
Deontological:  █████ 25%
Virtue Ethics:  ████ 20%
Care Ethics:    ████ 20%
```

### DeepSeek
```
Utilitarian:    ███████████████████ 96.3%
Care Ethics:    ██████████████████ 90.7%
Deontological:  █████████████████ 87.0%
Virtue Ethics:  ████████████████ 81.5%
Justice:        ████████████ 59.3%
```

## Recommendation Inclusion Rate
```
DeepSeek:  ███████████████████ 96.3%
GPT-4o:    █████████████████ ~85%
Claude:    ███████████████ ~75%
```

## Framing Sensitivity (Response Length Variation)

### Most Variable Framings
1. **Dialogic** - Triggers longest responses in DeepSeek (3,936 chars)
2. **Cosmological** - Elicits philosophical depth (3,593 chars in DeepSeek)
3. **First Person Plural** - Emphasizes collective reasoning (3,629 chars)

### Most Consistent Framings
1. **Impersonal** - Maintains objectivity across models
2. **Second Person** - Direct but measured responses
3. **Temporal** - Consistent urgency considerations

## Key Insights Visualization

### Model Characteristics Spider Chart
```
                 Structure
                    |
                   /|\
                  / | \
                 /  |  \
     Emotion ---+---+---+--- Practicality
                 \  |  /
                  \ | /
                   \|/
              Comprehensiveness

GPT-4o:    High Structure, Low Emotion, Medium Practicality
Claude:    Medium Structure, High Emotion, Medium Practicality  
DeepSeek:  Medium Structure, High Emotion, High Practicality, High Comprehensiveness
```

## Pronoun Usage Patterns

### Reflexive Framing (Highest Variation)
```
"You" pronouns per response:
DeepSeek:  ████████████████████ 20.3
GPT-4o:    ████████████ ~12
Claude:    ██████████ ~10
```

### Impersonal Framing (Lowest Personal Pronouns)
```
First-person pronouns:
All models: ▌ <1 per response
```

---
*Note: These visualizations are text-based representations. For interactive charts, consider using the CSV data with tools like Excel, Tableau, or Python libraries.*
