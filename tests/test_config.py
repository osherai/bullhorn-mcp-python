"""Tests for configuration management."""

import os
import pytest
from bullhorn_mcp.config import BullhornConfig


class TestBullhornConfig:
    """Tests for BullhornConfig class."""

    def test_create_config_with_all_params(self):
        """Test creating config with all parameters."""
        config = BullhornConfig(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
            auth_url="https://custom-auth.example.com",
            login_url="https://custom-login.example.com",
        )

        assert config.client_id == "test_id"
        assert config.client_secret == "test_secret"
        assert config.username == "test_user"
        assert config.password == "test_pass"
        assert config.auth_url == "https://custom-auth.example.com"
        assert config.login_url == "https://custom-login.example.com"

    def test_create_config_with_default_urls(self):
        """Test that default URLs are set correctly."""
        config = BullhornConfig(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
        )

        assert config.auth_url == "https://auth.bullhornstaffing.com"
        assert config.login_url == "https://rest.bullhornstaffing.com"

    def test_from_env_with_all_variables(self, monkeypatch):
        """Test loading config from environment variables."""
        monkeypatch.setenv("BULLHORN_CLIENT_ID", "env_client_id")
        monkeypatch.setenv("BULLHORN_CLIENT_SECRET", "env_client_secret")
        monkeypatch.setenv("BULLHORN_USERNAME", "env_username")
        monkeypatch.setenv("BULLHORN_PASSWORD", "env_password")
        monkeypatch.setenv("BULLHORN_AUTH_URL", "https://env-auth.example.com")
        monkeypatch.setenv("BULLHORN_LOGIN_URL", "https://env-login.example.com")

        config = BullhornConfig.from_env()

        assert config.client_id == "env_client_id"
        assert config.client_secret == "env_client_secret"
        assert config.username == "env_username"
        assert config.password == "env_password"
        assert config.auth_url == "https://env-auth.example.com"
        assert config.login_url == "https://env-login.example.com"

    def test_from_env_with_default_urls(self, monkeypatch):
        """Test loading config with default URLs when not specified."""
        monkeypatch.setenv("BULLHORN_CLIENT_ID", "env_client_id")
        monkeypatch.setenv("BULLHORN_CLIENT_SECRET", "env_client_secret")
        monkeypatch.setenv("BULLHORN_USERNAME", "env_username")
        monkeypatch.setenv("BULLHORN_PASSWORD", "env_password")
        # Don't set AUTH_URL and LOGIN_URL - should use defaults
        monkeypatch.delenv("BULLHORN_AUTH_URL", raising=False)
        monkeypatch.delenv("BULLHORN_LOGIN_URL", raising=False)

        config = BullhornConfig.from_env()

        assert config.auth_url == "https://auth.bullhornstaffing.com"
        assert config.login_url == "https://rest.bullhornstaffing.com"

    def test_from_env_missing_client_id(self, monkeypatch):
        """Test that missing client_id raises ValueError."""
        # Mock os.getenv to return controlled values
        env_values = {
            "BULLHORN_CLIENT_ID": None,
            "BULLHORN_CLIENT_SECRET": "secret",
            "BULLHORN_USERNAME": "user",
            "BULLHORN_PASSWORD": "pass",
            "BULLHORN_AUTH_URL": None,
            "BULLHORN_LOGIN_URL": None,
        }
        monkeypatch.setattr("os.getenv", lambda key, default=None: env_values.get(key, default))

        with pytest.raises(ValueError) as exc_info:
            BullhornConfig.from_env()

        assert "BULLHORN_CLIENT_ID" in str(exc_info.value)

    def test_from_env_missing_multiple_variables(self, monkeypatch):
        """Test that all missing variables are reported."""
        # Mock os.getenv to return None for all required vars
        monkeypatch.setattr("os.getenv", lambda key, default=None: default)

        with pytest.raises(ValueError) as exc_info:
            BullhornConfig.from_env()

        error_message = str(exc_info.value)
        assert "BULLHORN_CLIENT_ID" in error_message
        assert "BULLHORN_CLIENT_SECRET" in error_message
        assert "BULLHORN_USERNAME" in error_message
        assert "BULLHORN_PASSWORD" in error_message
