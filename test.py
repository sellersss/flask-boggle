from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        """Make sure board is in session"""

        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)

    def test_check_guess(self):
        """Make sure sending guess works"""

        with self.client:
            self.client.get('/')
            response = self.client.get('/check-guess?guess=to')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.is_json)

    def test_stats(self):
        """Make sure times_played and highscore is in session"""

        with self.client:
            self.client.get('/')
            response = self.client.post(
                '/stats', json={'score': '25'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('times_played', session)
            self.assertIn('highscore', session)
