from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from feishu_gateway.receipts import MessageReceiptStore, ReceiptStateError


class MessageReceiptStoreTests(unittest.TestCase):
    def test_claim_is_persisted_across_store_restart(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipts.json"
            first = MessageReceiptStore(path)

            self.assertTrue(first.claim("message-1"))
            self.assertFalse(first.claim("message-1"))

            restored = MessageReceiptStore(path)
            self.assertFalse(restored.claim("message-1"))
            self.assertTrue(restored.claim("message-2"))

    def test_capacity_prunes_oldest_receipts_and_keeps_recent_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipts.json"
            store = MessageReceiptStore(path)
            timestamps = [
                "2026-07-14T00:00:01+00:00",
                "2026-07-14T00:00:02+00:00",
                "2026-07-14T00:00:03+00:00",
                "2026-07-14T00:00:04+00:00",
            ]

            with (
                patch("feishu_gateway.receipts._MAX_RECEIPTS", 3),
                patch.object(MessageReceiptStore, "_now", side_effect=timestamps),
            ):
                self.assertTrue(store.claim("message-1"))
                self.assertTrue(store.claim("message-2"))
                self.assertTrue(store.claim("message-3"))
                self.assertTrue(store.claim("message-4"))
                self.assertFalse(store.claim("message-4"))

            state = json.loads(path.read_text(encoding="utf-8"))["receipts"]
            self.assertEqual(set(state), {"message-2", "message-3", "message-4"})

    def test_corrupt_state_raises_without_overwriting_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipts.json"
            corrupt = "{not-json"
            path.write_text(corrupt, encoding="utf-8")

            with self.assertRaises(ReceiptStateError):
                MessageReceiptStore(path).claim("message-1")

            self.assertEqual(path.read_text(encoding="utf-8"), corrupt)


if __name__ == "__main__":
    unittest.main()
