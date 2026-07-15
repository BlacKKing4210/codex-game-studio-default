from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from feishu_gateway.app import GatewayAlreadyRunning, GatewayInstanceLock


class GatewayInstanceLockTests(unittest.TestCase):
    def test_rejects_second_instance_and_releases_cleanly(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "gateway.lock"
            first = GatewayInstanceLock(path)
            second = GatewayInstanceLock(path)

            first.acquire()
            try:
                with self.assertRaises(GatewayAlreadyRunning):
                    second.acquire()
            finally:
                first.close()

            second.acquire()
            second.close()


if __name__ == "__main__":
    unittest.main()
