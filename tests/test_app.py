import tempfile
import unittest
from pathlib import Path

from app import create_app


class CoffeeRatingTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database = Path(self.temp_dir.name) / "test.sqlite"
        self.app = create_app({"TESTING": True, "DATABASE": str(database)})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_votes_are_saved_and_returned(self):
        first_vote = self.client.post("/api/coffees/ethiopia/vote")
        second_vote = self.client.post("/api/coffees/ethiopia/vote")
        coffees = self.client.get("/api/coffees").get_json()

        self.assertEqual(first_vote.get_json()["votes"], 1)
        self.assertEqual(second_vote.get_json()["votes"], 2)
        ethiopia = next(coffee for coffee in coffees if coffee["id"] == "ethiopia")
        self.assertEqual(ethiopia["votes"], 2)

    def test_unknown_coffee_returns_not_found(self):
        response = self.client.post("/api/coffees/unknown/vote")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()