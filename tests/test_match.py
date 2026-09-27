import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lostfound.__main__ import validate, match


def report(id, direction, category="umbrella", place="library", date="2026-09-25", **extra):
    return dict(id=id, direction=direction, category=category, place=place, date=date, **extra)


class MatchingTests(unittest.TestCase):
    def test_match_does_not_verify_owner(self):
        result = match(validate({"reports": [report("l", "lost"), report("f", "found")]}))
        self.assertEqual(result[0]["status"], "candidate_staff_review")
        self.assertEqual((result[0]["lost_id"], result[0]["found_id"]), ("l", "f"))

    def test_disagreeing_place_category_or_date_never_matches(self):
        rows = [report("l", "lost"), report("f1", "found", place="north gate"), report("f2", "found", category="laptop"), report("f3", "found", date="2026-09-29")]
        self.assertEqual(match(validate({"reports": rows})), [])

    def test_sensitive_never_matches(self):
        rows = [report("l", "lost", sensitive=True), report("f", "found")]
        self.assertEqual(match(validate({"reports": rows})), [])

    def test_private_fields_rejected(self):
        for key in ("email", "name", "serial_number", "verification_answer", "body"):
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    validate({"reports": [report("l", "lost", **{key: "do not leak"})]})

    def test_duplicates_and_bad_dates_rejected(self):
        with self.assertRaises(ValueError):
            validate({"reports": [report("x", "lost"), report("x", "found")]})
        with self.assertRaises(ValueError):
            validate({"reports": [report("x", "lost", date="2026-02-30")]})


if __name__ == "__main__":
    unittest.main()
