import unittest
# import requests
from unittest.mock import patch
from db_utils import get_db_connection


class TestDBConnection(unittest.TestCase):
    @patch('ghpars.psycopg2.connect')
    def test_db_connection_success(self, mock_connect):
        mock_connect.return_value = True
        conn = get_db_connection()
        self.assertTrue(conn)


class TestGitHubParser(unittest.TestCase):
    @patch('ghpars.requests.get')
    def test_ghtop_parse(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "incomplete_results": False,
            "items": [
                {"full_name": "test/repo", "owner": {"login": "test_owner"},
                 "stargazers_count": 1000, "watchers_count": 1000,
                 "forks_count": 100, "open_issues_count": 10,
                 "language": "Python"}
            ]
        }
        # TODO Добавить проверки на вызовы или состояние БД


class TestUpdateTop100(unittest.TestCase):
    @patch('ghpars.get_db_connection')
    def test_update_top100_to_db(self, mock_conn):
        mock_cursor = mock_conn.return_value.cursor.return_value
        # data = [("repo_name", "owner", 1, None, 100, 100, 10, 1, "Python")]
        # update_top100_to_db(data)
        mock_cursor.executemany.assert_called_once()
