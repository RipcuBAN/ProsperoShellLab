import hashlib
from pathlib import Path
import tempfile
import unittest
from shell_lab import classify, extract, inspect


class EvidenceTests(unittest.TestCase):
    def test_unknown_is_not_accepted_as_executable(self):
        self.assertEqual(classify(b'ordinary text'), 'unknown')

    def test_streamed_hash_includes_data_after_first_chunk(self):
        data = b'\x7fELF' + b'x' * (1024 * 1024 + 100)
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'sample'
            path.write_bytes(data)
            result = inspect(path)
        self.assertEqual(result['sha256'], hashlib.sha256(data).hexdigest())
        self.assertEqual(result['bytes'], len(data))
        self.assertFalse(result['executed'])

    def test_reference_extraction_deduplicates_without_claiming_implementation(self):
        result = extract('mono_class_from_name(); mono_class_from_name(); "Sce.PlayStation.PUI.UI2"; LaunchApp_orig();')
        self.assertEqual(result['mono_api_references'], ['mono_class_from_name'])
        self.assertEqual(result['managed_namespaces'], ['Sce.PlayStation.PUI.UI2'])


if __name__ == '__main__':
    unittest.main()
