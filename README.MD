# Council of Elders - Tech Wisdom Debate

A Streamlit app that orchestrates a council of 7 tech experts to debate any topic using local Ollama models, with Merlin the Wizard synthesizing their collective wisdom.

## The Council

1. **AI/ML Expert** - Deep learning, neural networks, transformers
2. **Cybersecurity Specialist** - Threat modeling, security architecture
3. **Cloud & Infrastructure Architect** - AWS, Azure, GCP, containerization
4. **Data Engineer** - Data pipelines, ETL, big data
5. **DevOps/SRE Engineer** - CI/CD, monitoring, reliability
6. **Software Architecture Expert** - Design patterns, system design
7. **Quantum Physics PhD** - Quantum mechanics, quantum computing

## How It Works

1. **Parallel Broadcast**: User submits a question, all 7 elders analyze it simultaneously
2. **Aggregation**: Their opinions are collected and summarized
3. **Round 2+**: Elders debate based on aggregated context from previous rounds
4. **Merlin's Synthesis**: After all rounds, Merlin weaves together all perspectives into final wisdom

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- At least one Ollama model pulled (e.g., `ollama pull llama3.2`)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Verify Ollama is installed:
```bash
ollama list
```

3. If no models are available, pull one:
```bash
ollama pull llama3.2
# or
ollama pull mistral
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run council_of_elders_app.py
```

2. Configure in the sidebar:
   - Select your Ollama model from the dropdown
   - Set number of debate rounds (1 to infinity)

3. Enter your question or topic

4. Click "Convene the Council"

5. Watch the debate unfold:
   - Each round shows all 7 elders' perspectives
   - Expandable sections for each elder
   - Final synthesis by Merlin

## Example Questions

- "What are the key considerations for building a real-time ML inference system?"
- "How should we design a secure multi-tenant SaaS architecture?"
- "What's the best approach for implementing event-driven microservices?"
- "How does quantum computing impact cryptographic security?"

## Features

- Dynamic model selection from locally available Ollama models
- Configurable debate rounds (1 to 100)
- Parallel expert analysis
- Context-aware multi-round debates
- Mystical synthesis by Merlin
- Clean, expandable UI

## Architecture

The app uses:
- **langchain-ollama**: For local LLM inference
- **Streamlit**: For interactive UI
- **Subprocess**: To dynamically fetch Ollama models

Each elder has a unique system prompt defining their expertise and perspective.

## Notes

- Longer debates (5+ rounds) provide deeper analysis but take more time
- Model selection affects response quality and speed
- All processing is done locally via Ollama
