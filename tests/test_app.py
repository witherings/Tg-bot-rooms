import unittest

from code_generator import generate_sequential_codes
from main import app


class WebsiteApiTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_homepage_and_health_check(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"Team Code Lab", page.data)
        self.assertIn(b"generator-form", page.data)

        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.get_json(), {"status": "ok"})

    def test_generates_ten_results_from_a_code(self):
        response = self.client.post(
            "/api/generate",
            json={"teamCodeOrLink": "XWADUQNY", "offset": 50, "language": "en"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        expected_codes = generate_sequential_codes("XWADUQNY", 50, 10)
        self.assertEqual(len(payload["results"]), 10)
        self.assertEqual(
            [result["teamCode"] for result in payload["results"]],
            [result["team_code"] for result in expected_codes],
        )
        self.assertEqual(
            payload["results"][0]["inviteUrl"],
            "https://link.brawlstars.com/invite/gameroom/en/"
            f"?tag={expected_codes[0]['team_code']}",
        )

    def test_accepts_an_invite_url_and_custom_offset(self):
        response = self.client.post(
            "/api/generate",
            json={
                "teamCodeOrLink": (
                    "https://link.brawlstars.com/invite/gameroom/en/"
                    "?tag=XWADUQNY"
                ),
                "offset": 123,
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["baseCode"], "XWADUQNY")
        self.assertEqual(payload["offset"], 123)
        self.assertEqual(len(payload["results"]), 10)

    def test_rejects_bad_codes_and_offsets(self):
        bad_code = self.client.post(
            "/api/generate", json={"teamCodeOrLink": "not-a-code"}
        )
        self.assertEqual(bad_code.status_code, 400)
        self.assertIn("error", bad_code.get_json())

        bad_offset = self.client.post(
            "/api/generate",
            json={"teamCodeOrLink": "XWADUQNY", "offset": 1.5},
        )
        self.assertEqual(bad_offset.status_code, 400)

        too_large = self.client.post(
            "/api/generate",
            json={"teamCodeOrLink": "XWADUQNY", "offset": 10001},
        )
        self.assertEqual(too_large.status_code, 400)

    def test_handles_non_string_language_values(self):
        response = self.client.post(
            "/api/generate",
            json={
                "teamCodeOrLink": "XWADUQNY",
                "offset": 50,
                "language": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.get_json()["results"][0]["inviteUrl"].startswith(
                "https://link.brawlstars.com/invite/gameroom/ru/"
            )
        )

    def test_rejects_non_json_requests(self):
        response = self.client.post("/api/generate", data="team=XWADUQNY")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
