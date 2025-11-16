#!/usr/bin/env python3
"""Test cases for utils module functions:
- access_nested_map
- get_json
- memoize
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from utils import access_nested_map, get_json, memoize
import client
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import requests


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct value for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(expected_key))


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns expected payload."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch(
            "utils.requests.get", return_value=mock_response
        ) as mock_get:
            result = get_json(test_url)
            # Test that requests.get was called once with test_url
            mock_get.assert_called_once_with(test_url)
            # Test that the output of get_json is equal to test_payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""
    def test_memoize(self):
        """Test that memoize caches the method result."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_obj = TestClass()

        # Patch 'a_method' of test_obj to monitor calls
        with patch.object(
            TestClass,
            "a_method",
            wraps=test_obj.a_method
        ) as mock_method:
            # Call a_property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Assert the result is correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method was called only once
            mock_method.assert_called_once()

@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(org_payload, repos_payload, expected_repos, apache2_repos)]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get for integration tests"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url.endswith("/repos"):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = cls.org_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns the expected repos list"""
        gh_client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(gh_client.public_repos(), self.expected_repos)

    # def test_public_repos_with_license(self):
    #     """Test public_repos filtering by license"""
    #     gh_client = GithubOrgClient(self.org_payload["login"])
    #     self.assertEqual(
    #         gh_client.public_repos(license="apache-2.0"),
    #         self.apache2_repos
    #     )
if __name__ == "__main__":
    unittest.main()
