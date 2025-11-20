#!/usr/bin/env python3
"""HTTP client for the TeamAlpha LLM Proxy server."""

import requests
from typing import Optional
import json


class TeamAlphaClient:
    """Client for interacting with the TeamAlpha LLM HTTP endpoint."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        Initialize the TeamAlpha client.

        Args:
            base_url: The base URL of the TeamAlpha server (default: http://localhost:8080)
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def health(self) -> dict:
        """
        Check the health of the server.

        Returns:
            dict: Health status response.

        Raises:
            requests.RequestException: If the request fails.
        """
        url = f"{self.base_url}/health"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def generate(
        self, prompt: str, max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text from the LLM.

        Args:
            prompt: The input prompt for the LLM.
            max_tokens: Optional maximum token limit for the response.

        Returns:
            str: The generated text.

        Raises:
            requests.RequestException: If the request fails.
            ValueError: If the response is invalid.
        """
        url = f"{self.base_url}/generate"
        payload = {"prompt": prompt}
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        response = self.session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if "text" not in data:
            raise ValueError(f"Invalid response: {data}")

        return data["text"]

    def close(self):
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
