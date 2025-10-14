# CoVulPecker - Quick Reference

## 📋 Quick Commands

### Setup
```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Configure API key in .env
# Edit GEMINI_API_KEY=your_actual_key

# 3. Run setup script (optional)
./quickstart.sh
```

### Running Analysis

```bash
# Demo with sample vulnerable code
python main.py --demo

# Analyze a specific file
python main.py --file data/vulnerable_sample.c

# Analyze inline code
python main.py --code 'char buf[10]; gets(buf);'

# With context
python main.py --code 'strcpy(dest, src);' --context "Network packet handler"

# See all options
python main.py --help
```

### Switch LLM Provider

```bash
# Google Gemini (default)
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=your_key

# OpenAI GPT
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_key

# Anthropic Claude
export LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your_key
```

## 📁 File Locations

| Type | Location | Purpose |
|------|----------|---------|
| **Source Code** | `src/` | Framework implementation |
| **Agents** | `src/agents/` | Reasoner & Critic agents |
| **Pipeline** | `src/pipelines/` | Orchestration logic |
| **Config** | `.env` | API keys & settings |
| **Logs** | `logs/` | Execution logs |
| **Results** | `outputs/` | JSON analysis reports |
| **Samples** | `data/` | Test vulnerable code |

## 🔧 Configuration (.env)

```bash
# Required: Choose one LLM provider
GEMINI_API_KEY=your_gemini_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Model Selection
LLM_PROVIDER=gemini              # gemini | openai | anthropic
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4
ANTHROPIC_MODEL=claude-3-opus-20240229

# Model Parameters
TEMPERATURE=0.7
MAX_TOKENS=4096

# Application
LOG_LEVEL=INFO                   # DEBUG | INFO | WARNING | ERROR
OUTPUT_FORMAT=json
```

## 🤖 Agent Roles

### Reasoner Agent 🧠
- **Role**: Vulnerability Analysis Expert
- **Tasks**:
  - Detect security vulnerabilities
  - Classify by CWE/CVE
  - Explain root causes
  - Identify risky lines
  - Assess impact
  - Describe exploits

### Critic Agent 🔍
- **Role**: Security Validation Expert  
- **Tasks**:
  - Validate findings
  - Detect false positives
  - Find missed issues
  - Refine severity
  - Provide confidence score
  - Final assessment

## 📊 Output Format

### JSON Report Structure
```json
{
  "timestamp": "ISO timestamp",
  "configuration": {
    "llm_provider": "gemini",
    "model": "gemini-1.5-flash",
    "temperature": 0.7
  },
  "source_code": "analyzed code",
  "context": "additional context",
  "analysis": {
    "agent": "Reasoner",
    "result": "JSON with vulnerabilities"
  },
  "review": {
    "agent": "Critic", 
    "result": "JSON with validation"
  }
}
```

### Reasoner Output
```json
{
  "vulnerabilities": [
    {
      "type": "Buffer Overflow",
      "cwe_id": "CWE-120",
      "severity": "Critical",
      "description": "...",
      "root_cause": "...",
      "risky_lines": [10, 11],
      "impact": "...",
      "exploit_scenario": "..."
    }
  ],
  "summary": "...",
  "recommendation": "..."
}
```

### Critic Output
```json
{
  "validation_status": "APPROVED",
  "confidence_score": 0.95,
  "confirmed_vulnerabilities": [...],
  "missed_vulnerabilities": [...],
  "overall_assessment": "...",
  "recommendations": "..."
}
```

## 🐛 Troubleshooting

### Issue: Import errors
```bash
# Solution: Ensure virtual environment is activated
source .venv/bin/activate
```

### Issue: API key not found
```bash
# Solution: Check .env configuration
cat .env | grep API_KEY
# Make sure you replaced the placeholder with actual key
```

### Issue: Module not found
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

### Issue: LLM provider error
```bash
# Solution: Check LLM_PROVIDER matches available API key
# Example: If using Gemini, ensure GEMINI_API_KEY is set
```

## 📝 Code Examples

### Using Pipeline Programmatically

```python
from src.pipelines import VulnerabilityPipeline

# Create pipeline
pipeline = VulnerabilityPipeline()

# Analyze code
code = """
char buffer[10];
strcpy(buffer, user_input);
"""

results = pipeline.analyze(
    source_code=code,
    context="User input handler",
    save_output=True
)

print(results)
```

### Custom Configuration

```python
from src.utils import config

# Get LLM with custom temperature
llm = config.get_llm(temperature=0.9)

# Get configuration
print(config.to_dict())
```

## 🔐 Security Best Practices

1. ✅ **Never commit .env** - Already in .gitignore
2. ✅ **Rotate API keys** - Regularly update keys
3. ✅ **Use read-only keys** - When possible
4. ✅ **Review outputs** - Validate before taking action
5. ✅ **Authorized code only** - Only analyze code you own

## 📚 Resources

- **Get Gemini API Key**: https://makersuite.google.com/app/apikey
- **CrewAI Docs**: https://docs.crewai.com/
- **CWE Database**: https://cwe.mitre.org/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/

## 🎯 Common Use Cases

### 1. Code Review
```bash
python main.py --file path/to/code.c
```

### 2. Quick Check
```bash
python main.py --code 'gets(buffer);'
```

### 3. Learning
```bash
python main.py --demo
cat outputs/demo_analysis.json
```

### 4. CI/CD Integration
```bash
# In your CI pipeline
python main.py --file $SOURCE_FILE || exit 1
```

---

**For detailed documentation, see README.md and IMPLEMENTATION.md**
