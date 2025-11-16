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
    
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""

        # Mock payload returned by get_json (repos_payload)
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_payload

        # Mocked URL for _public_repos_url
        mock_url = "https://api.github.com/orgs/testorg/repos"

        with patch("client.GithubOrgClient._public_repos_url", new_callable=property, return_value=mock_url):
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Expected repo names from the mock payload
            expected = ["repo1", "repo2", "repo3"]

            self.assertEqual(result, expected)

            # Assert _public_repos_url was accessed exactly once
            # (By calling repos_payload -> get_json)
            # get_json must have been called once with mock_url
            mock_get_json.assert_called_once_with(mock_url)



if __name__ == "__main__":
    unittest.main()
