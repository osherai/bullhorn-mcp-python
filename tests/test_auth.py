"""Tests for Bullhorn authentication."""

import time
import pytest
import httpx
import respx
from bullhorn_mcp.auth import BullhornAuth, BullhornSession, AuthenticationError


class TestBullhornSession:
    """Tests for BullhornSession class."""

    def test_session_creation(self):
        """Test creating a session."""
        session = BullhornSession(
            bh_rest_token="token123",
            rest_url="https://rest99.bullhornstaffing.com/rest-services/abc/",
            expires_at=time.time() + 600,
        )

        assert session.bh_rest_token == "token123"
        assert session.rest_url == "https://rest99.bullhornstaffing.com/rest-services/abc/"

    def test_session_expiry(self):
        """Test session expiry tracking."""
        # Session that expires in the future
        future_session = BullhornSession(
            bh_rest_token="token",
            rest_url="https://rest.example.com/",
            expires_at=time.time() + 600,
        )
        assert future_session.expires_at > time.time()

        # Session that has expired
        expired_session = BullhornSession(
            bh_rest_token="token",
            rest_url="https://rest.example.com/",
            expires_at=time.time() - 100,
        )
        assert expired_session.expires_at < time.time()


class TestBullhornAuth:
    """Tests for BullhornAuth class."""

    @respx.mock
    def test_full_auth_flow(self, sample_config):
        """Test complete authentication flow."""
        # Mock authorization endpoint - returns redirect with code
        respx.get(f"{sample_config.auth_url}/oauth/authorize").mock(
            return_value=httpx.Response(
                302,
                headers={"location": "https://callback.example.com?code=auth_code_123"},
            )
        )

        # Mock token endpoint
        respx.post(f"{sample_config.auth_url}/oauth/token").mock(
            return_value=httpx.Response(
                200,
                json={
                    "access_token": "access_token_123",
                    "refresh_token": "refresh_token_123",
                    "expires_in": 600,
                },
            )
        )

        # Mock REST login endpoint
        respx.get(f"{sample_config.login_url}/rest-services/login").mock(
            return_value=httpx.Response(
                200,
                json={
                    "BhRestToken": "bh_rest_token_123",
                    "restUrl": "https://rest99.bullhornstaffing.com/rest-services/abc/",
                },
            )
        )

        auth = BullhornAuth(sample_config)
        session = auth.session

        assert session.bh_rest_token == "bh_rest_token_123"
        assert session.rest_url == "https://rest99.bullhornstaffing.com/rest-services/abc/"
        assert session.expires_at > time.time()

    @respx.mock
    def test_auth_code_error(self, sample_config):
        """Test handling of OAuth error response."""
        respx.get(f"{sample_config.auth_url}/oauth/authorize").mock(
            return_value=httpx.Response(
                302,
                headers={"location": "https://callback.example.com?error=invalid_client&error_description=Invalid%20client"},
            )
        )

        auth = BullhornAuth(sample_config)

        with pytest.raises(AuthenticationError) as exc_info:
            _ = auth.session

        assert "invalid_client" in str(exc_info.value)

    @respx.mock
    def test_token_exchange_failure(self, sample_config):
        """Test handling of token exchange failure."""
        # Mock successful auth code
        respx.get(f"{sample_config.auth_url}/oauth/authorize").mock(
            return_value=httpx.Response(
                302,
                headers={"location": "https://callback.example.com?code=auth_code_123"},
            )
        )

        # Mock failed token exchange
        respx.post(f"{sample_config.auth_url}/oauth/token").mock(
            return_value=httpx.Response(
                400,
                json={"error": "invalid_grant"},
            )
        )

        auth = BullhornAuth(sample_config)

        with pytest.raises(AuthenticationError) as exc_info:
            _ = auth.session

        assert "Token exchange failed" in str(exc_info.value)

    @respx.mock
    def test_rest_login_failure(self, sample_config):
        """Test handling of REST login failure."""
        # Mock successful auth code and token
        respx.get(f"{sample_config.auth_url}/oauth/authorize").mock(
            return_value=httpx.Response(
                302,
                headers={"location": "https://callback.example.com?code=auth_code_123"},
            )
        )
        respx.post(f"{sample_config.auth_url}/oauth/token").mock(
            return_value=httpx.Response(
                200,
                json={"access_token": "token", "expires_in": 600},
            )
        )

        # Mock failed REST login
        respx.get(f"{sample_config.login_url}/rest-services/login").mock(
            return_value=httpx.Response(401, text="Unauthorized")
        )

        auth = BullhornAuth(sample_config)

        with pytest.raises(AuthenticationError) as exc_info:
            _ = auth.session

        assert "REST login failed" in str(exc_info.value)

    @respx.mock
    def test_session_caching(self, sample_config):
        """Test that session is cached and reused."""
        # Set up mocks
        auth_route = respx.get(f"{sample_config.auth_url}/oauth/authorize").mock(
            return_value=httpx.Response(
                302,
                headers={"location": "https://callback.example.com?code=code123"},
            )
        )
        respx.post(f"{sample_config.auth_url}/oauth/token").mock(
            return_value=httpx.Response(
                200,
                json={"access_token": "token", "expires_in": 600},
            )
        )
        respx.get(f"{sample_config.login_url}/rest-services/login").mock(
            return_value=httpx.Response(
                200,
                json={
                    "BhRestToken": "cached_token",
                    "restUrl": "https://rest.example.com/",
                },
            )
        )

        auth = BullhornAuth(sample_config)

        # First access - should trigger auth
        session1 = auth.session
        assert auth_route.call_count == 1

        # Second access - should use cached session
        session2 = auth.session
        assert auth_route.call_count == 1  # Still 1, no new auth

        assert session1.bh_rest_token == session2.bh_rest_token
