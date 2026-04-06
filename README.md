# llm-pharma-research
LLM in Pharmaceutical Research - Practical Applications

## Projects

### 1. Drug Interaction Chatbot
A chatbot that can answer questions about drug-drug interactions, side effects, and contraindications.

### 2. Literature Review Assistant
Automated summarization of pharmaceutical research papers.

### 3. Clinical Trial Matcher
Match patients to relevant clinical trials based on eligibility criteria.

---

## Quick Start

### Installation

```bash
cd llm-pharma-research
pip install -r requirements.txt
```

### Configuration

Copy `config.example.py` to `config.py` and add your API keys:

```python
# OpenAI API (for GPT models)
OPENAI_API_KEY = "your-api-key"

# Or use local models
USE_LOCAL = True
MODEL_NAME = "llama2"
```

### Usage

```python
from pharma.chatbot import DrugInteractionChatbot

# Initialize chatbot
chatbot = DrugInteractionChatbot()

# Ask questions
response = chatbot.ask("What are the interactions between aspirin and warfarin?")
print(response)
```

## Project Structure

```
llm-pharma-research/
├── chatbot/              # Drug interaction chatbot
│   ├── __init__.py
│   ├── chatbot.py      # Main chatbot class
│   ├── knowledge_base.py  # Drug knowledge base
│   └── prompts.py      # Chat prompts
├── literature/          # Literature review tools
│   ├── __init__.py
│   ├── summarizer.py  # Paper summarizer
│   └── extractor.py    # Information extractor
├── trials/             # Clinical trial matching
│   ├── __init__.py
│   ├── matcher.py     # Trial matching
│   └── eligibility.py # Criteria parsing
├── data/               # Data files
├── config.example.py   # Configuration template
├── requirements.txt    # Dependencies
└── README.md
```

## Features

### Drug Interaction Chatbot
- [x] Drug-drug interaction queries
- [x] Side effect information
- [x] Contraindication warnings
- [ ] Integration with drug databases
- [ ] Prescription safety checks

### Literature Review Assistant
- [x] Paper summarization
- [x] Key finding extraction
- [ ] Citation management
- [ ] Trend analysis

### Clinical Trial Matcher
- [ ] Patient eligibility matching
- [ ] Trial search
- [ ] Outcome prediction

## Tech Stack

- **Python 3.10+**
- **LangChain** - LLM orchestration
- **OpenAI** - GPT models (or local alternatives)
- **Streamlit** - Web UI
- **Chroma** - Vector database

## Disclaimer

⚠️ This project is for educational/research purposes only.
Always consult healthcare professionals for medical advice.

## License

MIT License
