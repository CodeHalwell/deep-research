#!/usr/bin/env python
"""
Deep Research Workflow CLI - Execute research workflows from the command line.

Usage:
    python run_workflow.py "Your research topic here"
"""

import asyncio
import sys
import argparse
from pathlib import Path

from deepresearch import DeepResearchWorkflow


async def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Deep Research Workflow - Automated Research and Report Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_workflow.py "Quantum computing applications in cryptography"
  python run_workflow.py "The impact of AI on job market" --config .config/config.yaml
        """,
    )

    parser.add_argument(
        "prompt",
        nargs="?",
        help="Research topic or question",
    )
    parser.add_argument(
        "--config",
        default=".config/config.yaml",
        help="Path to configuration file (default: .config/config.yaml)",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Output directory for results (default: output)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # If no prompt provided, show interactive mode
    if not args.prompt:
        print("=" * 80)
        print("Deep Research Workflow System")
        print("=" * 80)
        print("\nNo research topic provided.")
        print("Please enter your research topic or question:")
        print()
        try:
            prompt = input("Research Topic: ").strip()
        except KeyboardInterrupt:
            print("\n\nWorkflow cancelled by user.")
            return 1

        if not prompt:
            print("Error: Research topic cannot be empty.")
            return 1
    else:
        prompt = args.prompt

    # Initialize workflow
    print("\n" + "=" * 80)
    print("Initializing Deep Research Workflow...")
    print("=" * 80)

    try:
        workflow = DeepResearchWorkflow(config_path=args.config)
    except FileNotFoundError as e:
        print(f"Error: Configuration file not found: {e}")
        print("Make sure to create a .env file with required API keys.")
        print("See .env.example for configuration template.")
        return 1
    except Exception as e:
        print(f"Error initializing workflow: {e}")
        return 1

    # Execute workflow
    print(f"\nResearch Topic: {prompt}")
    print("\nStarting research workflow...")
    print(
        "This may take several minutes as the system "
        "conducts research and generates your report."
    )

    try:
        result = await workflow.execute(prompt)

        print("\n" + "=" * 80)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 80)

        if result["status"] == "success":
            print(f"\nWorkflow ID: {result['workflow_id']}")
            print(f"Output File: {result['output_path']}")
            print(f"State File: {result['state_file']}")

            if result.get("summary"):
                print(f"\nExecutive Summary:\n{result['summary'][:500]}...")
        elif result["status"] == "cancelled":
            print(f"\nWorkflow cancelled: {result.get('reason', 'Unknown reason')}")
            return 0

        print("\n" + "=" * 80)
        return 0

    except KeyboardInterrupt:
        print("\n\nWorkflow interrupted by user.")
        return 130
    except Exception as e:
        print(f"\nError during workflow execution: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
