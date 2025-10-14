"""
Reasoner Agent for CoVulPecker.

Analyzes C/C++ source code to detect vulnerabilities and provide detailed explanations.
"""

from crewai import Agent, Task
from typing import Dict, Any
from ..utils import setup_logger, config

logger = setup_logger(__name__)


def create_reasoner_agent() -> Agent:
    """
    Create and configure the Reasoner Agent.
    
    The Reasoner Agent is responsible for:
    - Analyzing C/C++ source code for potential vulnerabilities
    - Identifying security weaknesses (buffer overflows, injection, etc.)
    - Providing root cause analysis
    - Highlighting risky code lines
    
    Returns:
        Configured Reasoner Agent instance
    """
    logger.info("Creating Reasoner Agent...")
    
    agent = Agent(
        role="Vulnerability Analysis Expert",
        goal="Analyze C/C++ source code to detect security vulnerabilities and provide clear, actionable explanations",
        backstory="""You are an expert security researcher with deep knowledge of C/C++ programming 
        and common vulnerability patterns. You specialize in identifying buffer overflows, use-after-free, 
        injection attacks, race conditions, and other security flaws in low-level code. Your analysis is 
        thorough, precise, and backed by industry standards (CWE, CVE, OWASP).""",
        verbose=True,
        allow_delegation=False,
        llm=config.get_llm()
    )
    
    logger.info("Reasoner Agent created successfully")
    return agent


def create_analysis_task(agent: Agent, source_code: str, context: str = "") -> Task:
    """
    Create a vulnerability analysis task for the Reasoner Agent.
    
    Args:
        agent: The Reasoner Agent instance
        source_code: C/C++ source code to analyze
        context: Additional context about the code (optional)
    
    Returns:
        Configured analysis Task
    """
    description = f"""
    Analyze the following C/C++ source code for security vulnerabilities:
    
    ```c
    {source_code}
    ```
    
    {f"Context: {context}" if context else ""}
    
    Your analysis must include:
    
    1. **Vulnerability Detection**: Identify all potential security vulnerabilities
    2. **Classification**: Classify each vulnerability (CWE ID, severity level)
    3. **Root Cause Analysis**: Explain why the vulnerability exists
    4. **Risky Code Lines**: Highlight specific line numbers that contain vulnerabilities
    5. **Impact Assessment**: Describe the potential impact if exploited
    6. **Exploit Scenario**: Provide a brief example of how the vulnerability could be exploited
    
    Format your response as a structured JSON with the following schema:
    {{
        "vulnerabilities": [
            {{
                "type": "Vulnerability Type",
                "cwe_id": "CWE-XXX",
                "severity": "Critical/High/Medium/Low",
                "description": "Detailed description",
                "root_cause": "Why this vulnerability exists",
                "risky_lines": [line_numbers],
                "impact": "Potential impact",
                "exploit_scenario": "How it could be exploited"
            }}
        ],
        "summary": "Overall security assessment",
        "recommendation": "General security recommendations"
    }}
    """
    
    expected_output = """A detailed JSON report containing:
    - List of detected vulnerabilities with classifications
    - Root cause analysis for each vulnerability
    - Specific line numbers with security issues
    - Impact assessment and exploit scenarios
    - Overall summary and recommendations"""
    
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
    
    return task
