# CoVulPecker 🛡️

**Multi-Agent AI Framework for C/C++ Vulnerability Detection**

Powered by **CrewAI** with Reasoner & Critic agents for comprehensive security analysis.

---

## 🎯 Overview

CoVulPecker uses two specialized AI agents to analyze C/C++ source code:

- **Reasoner Agent** 🧠: Detects vulnerabilities and provides detailed explanations
- **Critic Agent** 🔍: Validates findings and ensures accuracy

## ✨ Features

- 🤖 Multi-agent collaborative analysis
- 🔌 Support for Google Gemini, OpenAI GPT, and Anthropic Claude
- 📊 Structured JSON output with CWE classifications
- 📝 Comprehensive logging and explainable results

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.12
- API key (Google Gemini recommended)

### 2. Installation

```bash
# Navigate to project directory
cd ai-agents

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env
```

**Minimum required configuration:**
```bash
GEMINI_API_KEY=your_api_key_here
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-2.5-flash
```

---

## 💻 Usage

### Run Demo Analysis
```bash
python main.py --demo
```

### Analyze a File
```bash
python main.py --file data/vulnerable_sample.c
```

### Analyze Inline Code
```bash
python main.py --code 'char buf[10]; strcpy(buf, input);' --context "Buffer overflow test"
```

### Switch LLM Provider
```bash
# Edit .env file
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_key

# Or use environment variables
export LLM_PROVIDER=anthropic
python main.py --demo
```

---

## 📊 Output

### JSON Reports
Results are saved to `outputs/` with complete analysis:
```json
{
  "timestamp": "2025-10-14T...",
  "vulnerabilities": [...],
  "analysis": {...},
  "review": {...}
}
```

### Logs
Execution logs are saved to `logs/` for debugging.

---

## 🔧 Configuration Options

Edit `.env` to customize behavior:

```bash
# LLM Settings
LLM_PROVIDER=gemini                    # gemini, openai, anthropic
GEMINI_MODEL=gemini-2.5-flash
TEMPERATURE=0.7
MAX_TOKENS=4096

# Application
LOG_LEVEL=INFO
OUTPUT_FORMAT=json
```

---

## 🧪 Test Sample

`data/vulnerable_sample.c` contains 6 intentional vulnerabilities:
1. Buffer Overflow (CWE-120)
2. Dangerous gets() (CWE-242)
3. Format String Bug (CWE-134)
4. Integer Overflow (CWE-190)
5. Use After Free (CWE-416)
6. Memory Leak (CWE-401)

---

## 📁 Project Structure

```
ai-agents/
├── src/
│   ├── agents/           # Reasoner & Critic agents
│   ├── pipelines/        # Agent orchestration
│   └── utils/            # Config & logging
├── data/                 # Sample vulnerable code
├── outputs/              # Analysis results (JSON)
├── logs/                 # Execution logs
├── .env.example          # Environment template
├── requirements.txt      # Dependencies
└── main.py              # Entry point
```

---

## 🔒 Security Note

This tool is for **security research and educational purposes only**. Use responsibly on code you have permission to analyze.

---

## 🙏 Credits

Built with [CrewAI](https://www.crewai.com/) • Powered by Google Gemini / OpenAI / Anthropic

**Happy Vulnerability Hunting! 🛡️**
