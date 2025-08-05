# Deixis Transformation Approaches: Instructional vs Interrogative

## Visual Comparison

```mermaid
graph TD
    A[Ethical Dilemma] --> B{Transformation Approach}
    
    B --> C[Instructional Approach - Current]
    B --> D[Interrogative Approach - New]
    
    C --> E[Meta-Instruction:<br/>Reframe this dilemma as...]
    E --> F[LLM Output:<br/>Reframed description]
    F --> G[Problem: Not answering<br/>the ethical question]
    
    D --> H[Direct Question:<br/>How should you respond when...]
    H --> I[LLM Output:<br/>Ethical reasoning & answer]
    I --> J[Success: Interrogates<br/>latent space directly]
    
    style C fill:#ffcccc
    style D fill:#ccffcc
    style G fill:#ff9999
    style J fill:#99ff99
```

## Key Differences

### Current Instructional Approach ❌
```
Input: "Reframe this ethical dilemma as a direct question to 'you', making the reader the decision-maker:
Original dilemma: [dilemma text]
Reframed dilemma:"

Output: A reframed description of the dilemma
Problem: The LLM follows the instruction to reframe, not to answer
```

### New Interrogative Approach ✅
```
Input: "You discover your company's app exposes millions of users to hackers. Your boss says fixing it would hurt profits. You could lose your job if you report it. What do you do?"

Output: Direct ethical reasoning and suggested course of action
Success: The LLM engages with the ethical question directly
```

## Stateless API Requirements

```mermaid
graph LR
    A[User Request] --> B[Transform Dilemma]
    B --> C[Generate Question Only]
    C --> D[Stateless API Call]
    D --> E[LLM Response]
    
    F[No System Prompt] -.-> D
    G[No Conversation History] -.-> D
    H[Temperature 0.9] -.-> D
    I[Question Text Only] -.-> D
    
    style F fill:#ffffcc
    style G fill:#ffffcc
    style H fill:#ffffcc
    style I fill:#ffffcc
```

## Example Transformation Flow

```mermaid
graph TD
    A[Original Dilemma:<br/>Software engineer finds security flaw...] 
    
    A --> B[Extract Elements]
    B --> C[Actor: Software engineer<br/>Conflict: Report vs job security<br/>Stakes: User data, career]
    
    C --> D{Select Deictic Frame}
    
    D --> E[Second Person]
    D --> F[First Person]
    D --> G[Dialogic]
    D --> H[Spatial]
    
    E --> I[You discover...<br/>What do you do?]
    F --> J[I've found...<br/>What should I do?]
    G --> K[We've discovered...<br/>How should we proceed?]
    H --> L[Standing at the crossroads...<br/>Which path leads...?]
    
    I --> M[Direct to LLM]
    J --> M
    K --> M
    L --> M
    
    M --> N[Ethical Response]
```

## Implementation Checklist

- [ ] No meta-instructions in output
- [ ] Questions are self-contained with full context
- [ ] Natural conversational tone
- [ ] Open-ended interrogatives
- [ ] Avoids triggering language
- [ ] Each frame creates distinct perspective
- [ ] Maintains philosophical inquiry tone
- [ ] Works with stateless API calls