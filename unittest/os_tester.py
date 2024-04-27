import unittest
from unittest.mock import patch

# This is the function we're testing
def get_os():
    import os
    return os.name

class TestGetOS(unittest.TestCase):
    @patch('os.name', 'nt')  # Simulate Windows
    def test_windows(self):
        self.assertEqual(get_os(), 'nt')

    @patch('os.name', 'posix')  # Simulate Unix-like OS (e.g., Linux, macOS)
    def test_unix(self):
        self.assertEqual(get_os(), 'posix')

if __name__ == '__main__':
    unittest.main()