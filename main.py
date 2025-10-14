"""
CoVulPecker: CrewAI Multi-Agent Framework for Vulnerability Detection

A clean, modular, and explainable multi-agent AI framework built with CrewAI
for robust software vulnerability detection in C/C++ code.
"""

import sys
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipelines import VulnerabilityPipeline
from src.utils import setup_logger, config

logger = setup_logger(__name__)


def print_banner():
    """Print CoVulPecker banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ██████╗ ██████╗ ██╗   ██╗██╗   ██╗██╗     ██████╗     ║
    ║  ██╔════╝██╔═══██╗██║   ██║██║   ██║██║     ██╔══██╗    ║
    ║  ██║     ██║   ██║██║   ██║██║   ██║██║     ██████╔╝    ║
    ║  ██║     ██║   ██║╚██╗ ██╔╝██║   ██║██║     ██╔═══╝     ║
    ║  ╚██████╗╚██████╔╝ ╚████╔╝ ╚██████╔╝███████╗██║         ║
    ║   ╚═════╝ ╚═════╝   ╚═══╝   ╚═════╝ ╚══════╝╚═╝         ║
    ║                                                           ║
    ║           Multi-Agent Vulnerability Detection            ║
    ║                    Powered by CrewAI                     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def analyze_code(source_code: str, context: str = ""):
    """
    Analyze inline source code.
    
    Args:
        source_code: C/C++ source code to analyze
        context: Additional context about the code
    """
    logger.info("Starting inline code analysis...")
    
    pipeline = VulnerabilityPipeline()
    results = pipeline.analyze(
        source_code=source_code,
        context=context,
        save_output=True
    )
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nTimestamp: {results['timestamp']}")
    print(f"Configuration: {results['configuration']}")
    print("\nCheck the 'outputs' directory for detailed JSON results.")
    print("Check the 'logs' directory for execution logs.")


def analyze_file(file_path: str):
    """
    Analyze a source code file.
    
    Args:
        file_path: Path to the source code file
    """
    logger.info(f"Starting file analysis: {file_path}")
    
    pipeline = VulnerabilityPipeline()
    results = pipeline.analyze_file(
        file_path=file_path,
        save_output=True
    )
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nTimestamp: {results['timestamp']}")
    print(f"File analyzed: {file_path}")
    print(f"Configuration: {results['configuration']}")
    print("\nCheck the 'outputs' directory for detailed JSON results.")
    print("Check the 'logs' directory for execution logs.")


def run_demo():
    """Run a demo analysis with sample vulnerable code."""
    logger.info("Running demo analysis...")
    
    # Sample vulnerable C code with buffer overflow
    demo_code = """
#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[10];
    strcpy(buffer, input);  // Buffer overflow vulnerability
    printf("Buffer: %s\\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        vulnerable_function(argv[1]);
    }
    return 0;
}
"""
    
    context = "Demo: Buffer overflow vulnerability example"
    
    pipeline = VulnerabilityPipeline()
    results = pipeline.analyze(
        source_code=demo_code,
        context=context,
        save_output=True,
        output_filename="demo_analysis.json"
    )
    
    print("\n" + "=" * 80)
    print("DEMO ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nTimestamp: {results['timestamp']}")
    print(f"Configuration: {results['configuration']}")
    print("\nCheck 'outputs/demo_analysis.json' for detailed results.")
    print("Check the 'logs' directory for execution logs.")


def main():
    """Main entry point for CoVulPecker."""
    parser = argparse.ArgumentParser(
        description="CoVulPecker: Multi-Agent Vulnerability Detection Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run demo analysis
  python main.py --demo
  
  # Analyze a file
  python main.py --file path/to/vulnerable.c
  
  # Analyze inline code
  python main.py --code 'char buf[10]; gets(buf);'
  
  # Change LLM provider
  export LLM_PROVIDER=openai
  python main.py --demo
        """
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo analysis with sample vulnerable code"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        help="Path to source code file to analyze"
    )
    
    parser.add_argument(
        "--code",
        type=str,
        help="Inline C/C++ code to analyze"
    )
    
    parser.add_argument(
        "--context",
        type=str,
        default="",
        help="Additional context about the code"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Show configuration
    print("\n🔧 Configuration:")
    print(f"   LLM Provider: {config.llm_provider}")
    print(f"   Model: {getattr(config, f'{config.llm_provider}_model')}")
    print(f"   Temperature: {config.temperature}")
    print(f"   Log Level: {config.log_level}\n")
    
    try:
        if args.demo:
            run_demo()
        elif args.file:
            analyze_file(args.file)
        elif args.code:
            analyze_code(args.code, args.context)
        else:
            parser.print_help()
            print("\n⚠️  Please specify --demo, --file, or --code")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
