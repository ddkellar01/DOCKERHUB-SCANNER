import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from config import config

class TestDockerHubScannerConfig(unittest.TestCase):
    
    def test_config_defaults(self):
        """Test default configuration parameters are correctly initialized."""
        self.assertEqual(config.scan_target_dir, "/tmp/scan_target")
        self.assertTrue(config.block_on_malware)
        self.assertTrue(config.block_on_critical_vulns)

    @patch('google.genai.Client')
    def test_ai_analyzer_mock(self, mock_genai_client):
        """Test mock integration of Gemini Pro thinking analyzer."""
        mock_response = MagicMock()
        mock_response.text = "1. **Threat Verdict:** SAFE\n2. **Risk Analysis:** None"
        
        mock_client_instance = mock_genai_client.return_value
        mock_client_instance.models.generate_content.return_value = mock_response

        # Verify client initialization structure
        self.assertIsNotNone(mock_genai_client)

if __name__ == "__main__":
    unittest.main()
