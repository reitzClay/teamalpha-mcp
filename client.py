#!/usr/bin/env python3
"""CLI client for the TeamAlpha LLM Proxy server."""

import sys
import argparse
from src.teamalpha.client import TeamAlphaClient


def main():
    """Main entry point for the CLI client."""
    parser = argparse.ArgumentParser(
        description="TeamAlpha LLM HTTP client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "What is Python?"
  %(prog)s --server http://remote-host:8080 "Explain AI"
  %(prog)s --max-tokens 256 "Write a haiku about clouds"
        """,
    )

    parser.add_argument(
        "prompt",
        nargs="?",
        help="The prompt to send to the LLM",
    )
    parser.add_argument(
        "--server",
        default="http://localhost:8080",
        help="Base URL of the TeamAlpha server (default: http://localhost:8080)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Maximum tokens for the response",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Check server health instead of generating",
    )

    args = parser.parse_args()

    try:
        with TeamAlphaClient(base_url=args.server) as client:
            if args.health:
                status = client.health()
                print(f"Server health: {status}")
                return 0

            if not args.prompt:
                parser.print_help()
                return 1

            print(f"Prompt: {args.prompt}")
            print("-" * 60)
            result = client.generate(
                prompt=args.prompt, max_tokens=args.max_tokens
            )
            print(result)
            return 0

    except requests.exceptions.ConnectionError:
        print(
            f"Error: Could not connect to server at {args.server}",
            file=sys.stderr,
        )
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    import requests

    sys.exit(main())
