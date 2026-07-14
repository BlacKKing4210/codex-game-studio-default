from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from feishu_gateway.conversations import ConversationStore


class ConversationStoreTests(unittest.TestCase):
    def test_persists_thread_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "conversations.json"
            store = ConversationStore(path)
            binding = store.get_or_create("chat-1", "user-1", "studio")
            self.assertIsNone(binding.thread_id)
            self.assertTrue(store.attach_thread(binding.key, binding.generation, "thread-1"))

            restored = ConversationStore(path).get(binding.key)
            self.assertIsNotNone(restored)
            self.assertEqual(restored.thread_id, "thread-1")
            self.assertEqual(restored.project_alias, "studio")

    def test_reset_prevents_old_job_from_overwriting_new_thread_slot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = ConversationStore(Path(directory) / "conversations.json")
            first = store.get_or_create("chat-1", "user-1", "studio")
            second = store.reset("chat-1", "user-1", "fisher")

            self.assertGreater(second.generation, first.generation)
            self.assertFalse(store.attach_thread(first.key, first.generation, "old-thread"))
            self.assertTrue(store.attach_thread(second.key, second.generation, "new-thread"))
            self.assertEqual(store.get(second.key).thread_id, "new-thread")


if __name__ == "__main__":
    unittest.main()
