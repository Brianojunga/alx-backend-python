#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Arrange
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"payload": True}

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"payload": True})

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url"""
        # Mocked payload
        mock_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch("client.GithubOrgClient.org", return_value=mock_payload):
            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, mock_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
