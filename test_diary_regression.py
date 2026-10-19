"""Regression checks for diary matching and roommate acknowledgement."""

import unittest
import os
from datetime import date
from unittest.mock import patch

import app
from analyzer import analyze_entry


YOKAI = [
    {"id": "17", "name": "유키온나", "country": "Japan", "plutchik_dyad": "ANXIETY", "plutchik_ko": "불안", "valence": 2.51, "arousal": 4.88, "narrative_dialogue": "", "micro_action": "", "story": ""},
    {"id": "14", "name": "분노 요괴", "country": "Korea", "plutchik_dyad": "OUTRAGE", "plutchik_ko": "격분", "valence": 1.84, "arousal": 6.17, "narrative_dialogue": "", "micro_action": "", "story": ""},
    {"id": "54", "name": "기쁨 요괴", "country": "Korea", "plutchik_dyad": "DELIGHT", "plutchik_ko": "환희", "valence": 5.85, "arousal": 6.10, "narrative_dialogue": "", "micro_action": "", "story": ""},
    {"id": "55", "name": "슬픔 요괴", "country": "Korea", "plutchik_dyad": "DESPAIR", "plutchik_ko": "절망", "valence": 1.45, "arousal": 4.10, "narrative_dialogue": "", "micro_action": "", "story": ""},
]


class FakeCursor:
    def __init__(self):
        self.query = ""

    def execute(self, query, params=None):
        self.query = query

    def fetchall(self):
        return YOKAI if "FROM yokai_compendium" in self.query else []

    def close(self):
        pass


class FakeConnection:
    def cursor(self):
        return FakeCursor()

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


class DiaryRegressionTest(unittest.TestCase):
    def submit(self, entry):
        with patch.object(app, "get_db", return_value=FakeConnection()), \
                patch.object(app, "diary_roommate_acknowledgement", side_effect=ValueError("unavailable")):
            return app.submit_diary(app.DiaryInput(user_id="test-user", diary_date=date(2026, 10, 19), raw_entry=entry))

    def test_distinct_emotions_do_not_all_match_yukionna(self):
        cases = {
            "팀장이 내 기획서를 무시해서 너무 억울하고 화가 났어": "OUTRAGE",
            "친구에게 선물을 받아서 정말 기뻤어": "DELIGHT",
            "애인이랑 헤어져서 너무 슬펐어": "DESPAIR",
            "내일 시험 결과가 걱정돼": "ANXIETY",
        }
        for entry, dyad in cases.items():
            with self.subTest(entry=entry):
                result = self.submit(entry)
                self.assertEqual(result["analysis"]["plutchik_dyad"], dyad)
                self.assertEqual(result["eaten_by_yokai"]["id"], next(y["id"] for y in YOKAI if y["plutchik_dyad"] == dyad))
                self.assertTrue(result["eaten_by_yokai"]["comfort_quote"])

    def test_unspecified_emotion_is_not_forced_to_anxiety(self):
        entries = [
            "회의가 길어져서 저녁 약속에 늦었어",
            "오늘 지하철에서 우산을 놓고 내렸어",
            "점심에 새로운 가게에 다녀왔어",
            "퇴근길에 오랜 동료를 만났어",
        ]
        results = [self.submit(entry) for entry in entries]
        self.assertTrue(all(analyze_entry(entry)["plutchik_dyad"] is None for entry in entries))
        self.assertTrue(all(result["analysis"]["emotion_tag"] == "감정 탐색" for result in results))
        self.assertGreater(len({result["eaten_by_yokai"]["id"] for result in results}), 1)
        self.assertIn("회의가 길어져서", results[0]["eaten_by_yokai"]["comfort_quote"])

    def test_acknowledgement_exists_without_ai_key(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}), \
                patch.object(app, "get_db", return_value=FakeConnection()):
            result = app.submit_diary(app.DiaryInput(
                user_id="test-user", diary_date=date(2026, 10, 19),
                raw_entry="팀장이 내 기획서를 무시해서 억울했어",
            ))
        self.assertIn("기획서를 무시해서", result["eaten_by_yokai"]["comfort_quote"])


if __name__ == "__main__":
    unittest.main()
