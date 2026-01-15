"""Configuration management for Bullhorn MCP server."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class BullhornConfig:
    """Bullhorn API configuration loaded from environment variables."""

    client_id: str
    client_secret: str
    username: str
    password: str
    auth_url: str = "https://auth.bullhornstaffing.com"
    login_url: str = "https://rest.bullhornstaffing.com"

    @classmethod
    def from_env(cls) -> "BullhornConfig":
        """Load configuration from environment variables."""
        load_dotenv()

        client_id = os.getenv("BULLHORN_CLIENT_ID")
        client_secret = os.getenv("BULLHORN_CLIENT_SECRET")
        username = os.getenv("BULLHORN_USERNAME")
        password = os.getenv("BULLHORN_PASSWORD")

        missing = []
        if not client_id:
            missing.append("BULLHORN_CLIENT_ID")
        if not client_secret:
            missing.append("BULLHORN_CLIENT_SECRET")
        if not username:
            missing.append("BULLHORN_USERNAME")
        if not password:
            missing.append("BULLHORN_PASSWORD")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            auth_url=os.getenv("BULLHORN_AUTH_URL", "https://auth.bullhornstaffing.com"),
            login_url=os.getenv("BULLHORN_LOGIN_URL", "https://rest.bullhornstaffing.com"),
        )
