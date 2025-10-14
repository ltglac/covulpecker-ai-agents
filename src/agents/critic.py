"""
Critic Agent for CoVulPecker.

Validates and refines the Reasoner's vulnerability analysis using expert knowledge.
"""

from crewai import Agent, Task
from typing import Dict, Any
from ..utils import setup_logger, config

logger = setup_logger(__name__)


def create_critic_agent() -> Agent:
    """
    Create and configure the Critic Agent.
    
    The Critic Agent is responsible for:
    - Validating the Reasoner's vulnerability findings
    - Identifying false positives or missed vulnerabilities
    - Refining the analysis with additional insights
    - Ensuring accuracy and completeness of the report
    
    Returns:
        Configured Critic Agent instance
    """
    logger.info("Creating Critic Agent...")
    
    agent = Agent(
        role="Security Validation Expert",
        goal="Critically review and validate vulnerability analysis reports, ensuring accuracy and completeness",
        backstory="""You are a senior security auditor with decades of experience in code review 
        and vulnerability assessment. You have an exceptional eye for detail and can spot both false 
        positives and overlooked issues. Your expertise includes C/C++ memory safety, secure coding 
        practices, and attack surface analysis. You validate findings against industry standards 
        (CWE, OWASP, CERT) and provide constructive feedback to improve security assessments.""",
        verbose=True,
        allow_delegation=False,
        llm=config.get_llm()
    )
    
    logger.info("Critic Agent created successfully")
    return agent


def create_review_task(agent: Agent, analysis_report: str, source_code: str) -> Task:
    """
    Create a review task for the Critic Agent.
    
    Args:
        agent: The Critic Agent instance
        analysis_report: The Reasoner's vulnerability analysis report
        source_code: Original C/C++ source code that was analyzed
    
    Returns:
        Configured review Task
    """
    description = f"""
    Review and validate the following vulnerability analysis report:
    
    **Original Source Code:**
    ```c
    {source_code}
    ```
    
    **Reasoner's Analysis Report:**
    ```
    {analysis_report}
    ```
    
    Your critical review must assess:
    
    1. **Accuracy Verification**: Are the identified vulnerabilities legitimate?
    2. **False Positive Detection**: Are there any false alarms that need to be removed?
    3. **Completeness Check**: Are there any missed vulnerabilities?
    4. **Severity Assessment**: Are the severity ratings appropriate?
    5. **Technical Precision**: Are the technical explanations accurate and clear?
    6. **CWE/CVE Validation**: Are the classifications correct?
    7. **Exploit Feasibility**: Are the exploit scenarios realistic?
    
    Provide your feedback as a structured JSON with the following schema:
    {{
        "validation_status": "APPROVED/NEEDS_REVISION/REJECTED",
        "confidence_score": 0.0-1.0,
        "confirmed_vulnerabilities": [
            {{
                "original_finding": "Reference to original vulnerability",
                "validation": "CONFIRMED/FALSE_POSITIVE",
                "reasoning": "Why this finding is valid or invalid",
                "refinement": "Any corrections or additional details"
            }}
        ],
        "missed_vulnerabilities": [
            {{
                "type": "Vulnerability type",
                "description": "What was missed",
                "risky_lines": [line_numbers],
                "severity": "Critical/High/Medium/Low"
            }}
        ],
        "overall_assessment": "Summary of the review",
        "recommendations": "Suggestions for improving the analysis"
    }}
    """
    
    expected_output = """A comprehensive validation report containing:
    - Validation status and confidence score
    - Verification of each identified vulnerability
    - False positive identification
    - Any missed vulnerabilities
    - Technical accuracy assessment
    - Overall assessment and recommendations"""
    
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
    
    return task
