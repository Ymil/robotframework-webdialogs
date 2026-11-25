import unittest

from WebDialogs.server.app import app
from WebDialogs.server.services import dialog_manager


class DialogCompatibilityTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        dialog_manager.reset()

    def tearDown(self):
        dialog_manager.reset()

    def test_builtin_dialog_round_trips(self):
        cases = [
            ("get_value_from_user", {}, {"response": "Alice"}, "Alice"),
            ("get_selection_from_user", {"options": ["A", "B"]}, {"response": "A"}, "A"),
            ("get_selections_from_user", {"options": ["A", "B"]}, {"response": ["A", "B"]}, ["A", "B"]),
            ("execute_manual_step", {}, {"response": "PASS"}, "PASS"),
            ("pause_execution", {}, {"response": "continue"}, "continue"),
        ]
        for dialog_type, options, form, expected in cases:
            with self.subTest(dialog_type=dialog_type):
                response = self.client.post(
                    f"/api/create/{dialog_type}", json={"message": "Compatibility check", **options}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(self.client.get("/dialog/").status_code, 200)
                self.assertIsNone(self.client.get("/api/get_response").json["response"])
                self.assertEqual(self.client.post("/dialog/submit", data=form).status_code, 302)
                self.assertEqual(self.client.get("/api/get_response").json["response"], expected)
                self.assertIsNone(self.client.get("/api/get_response").json["response"])

    def test_custom_dialog_returns_form_data(self):
        response = self.client.post(
            "/api/create/execute_custom_step",
            json={"message": "Custom check", "step": "custom_form", "data": {"name": "Alice"}},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dialog_manager.get().data, {"name": "Alice"})
        response = self.client.post("/dialog/submit", data={"name": "Alice", "choices": ["A", "B"]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.get("/api/get_response").json["response"], {"name": "Alice", "choices": ["A", "B"]}
        )


if __name__ == "__main__":
    unittest.main()
