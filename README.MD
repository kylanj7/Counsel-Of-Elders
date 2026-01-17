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
- NVIDIA GPU with drivers installed (optional but recommended for faster inference)
- CUDA toolkit (optional but recommended)

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

4. **Verify GPU is being used (recommended):**
```bash
# Check if NVIDIA GPU is available
nvidia-smi

# Restart Ollama service to ensure GPU detection
sudo systemctl restart ollama

# Load a model and verify GPU usage
ollama run tinyllama "test"
ollama ps
```

Expected output should show `100% GPU` in the PROCESSOR column:
```
NAME                ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
tinyllama:latest    2644915ede35    645 MB    100% GPU     4096       4 minutes from now
```

**If showing `100% CPU` instead:**
- The restart usually fixes this: `sudo systemctl restart ollama`
- See `GPU_TROUBLESHOOTING.md` for detailed debugging steps
- Run `python diagnose_gpu.py` for automatic diagnostics

5. **Optional: Setup Firefox Web Search (for real-time information)**

If you want to enable web search capabilities:

```bash
# Install Firefox (if not already installed)
sudo dnf install firefox  # Fedora
# or
sudo apt install firefox  # Ubuntu

# Install GeckoDriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
tar -xzf geckodriver-v0.34.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
sudo chmod +x /usr/local/bin/geckodriver

# Verify
geckodriver --version
```

See `FIREFOX_SETUP.md` for detailed installation and troubleshooting.

## Usage

1. Run the Streamlit app:
```bash
streamlit run council_of_elders_app.py
```

2. Configure in the sidebar:
   - Select your Ollama model from the dropdown
   - Set number of debate rounds (1 to infinity)
   - **Optional**: Enable web search for current information

3. Enter your question or topic

4. Click "Convene the Council"

5. Watch the debate unfold:
   - **If web search enabled**: Results appear before Round 1
   - Each round shows all 7 elders' perspectives
   - Expandable sections for each elder
   - Final synthesis by Merlin
   - Download complete debate as PDF

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
- **PDF export** - Download complete debates as formatted PDFs
- **Web search integration** - Optional Firefox incognito search for current information

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

### Performance Notes

**GPU vs CPU:**
- **GPU inference**: Much faster, recommended for better experience (seconds per response)
- **CPU inference**: Works but slower (can take minutes per elder response)
- Verify GPU usage with `ollama ps` - should show `100% GPU` not `100% CPU`

**Model Recommendations:**
- **tinyllama** (1.1B): Fastest but simpler responses, good for testing
- **llama3.2** (3B-7B): Balanced quality and speed, recommended
- **mistral** (7B): High quality, moderate speed
- **llama3.1:70b** (70B): Best quality but very slow, requires significant VRAM

**Optimization Tips:**
- Start with 1-2 debate rounds for initial testing
- Use smaller models (tinyllama, llama3.2) for faster iteration
- Ensure GPU is being used for 10x+ speed improvement
- 7 elders × N rounds = many LLM calls, so GPU makes a huge difference

### Troubleshooting

If you encounter issues:
- **GPU not detected**: Run `sudo systemctl restart ollama`
- **Slow performance**: Check if using GPU with `ollama ps`
- **Detailed diagnostics**: Run `python diagnose_gpu.py`
- **Step-by-step fixes**: See `GPU_TROUBLESHOOTING.md`
- **Web search not working**: See `FIREFOX_SETUP.md`

### Web Search Feature

When enabled, the council searches DuckDuckGo using Firefox incognito mode:
- **Privacy-focused**: Uses DuckDuckGo (no tracking) + Firefox incognito (no history)
- **First round only**: Web results gathered before Round 1, available to all rounds
- **Optional**: Works perfectly without web search if not needed
- **Requirements**: Firefox and GeckoDriver must be installed (see `FIREFOX_SETUP.md`)

**Best use cases for web search:**
- Current events or recent developments
- Latest technology releases or updates
- Real-time data or statistics
- Recent news or announcements
- Emerging trends or best practices
