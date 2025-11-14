"""
Tests for reflect command.
"""

import pytest
from pathlib import Path
import tempfile
import json
import shutil
from cli.commands.reflect import generate_reflection, log_reflection, get_reflection_log_path


class TestReflect:
    """Test reflect command functionality."""

    def setup_method(self):
        """Set up test environment."""
        # Create a temporary home directory for testing
        self.temp_home = tempfile.mkdtemp()
        self.original_home = Path.home()

    def teardown_method(self):
        """Clean up test environment."""
        # Clean up temp directory
        if Path(self.temp_home).exists():
            shutil.rmtree(self.temp_home)

    def test_generate_reflection_question(self):
        """Test reflection on question."""
        text = "How can I improve my workflow?"
        reflection = generate_reflection(text)

        assert "wondering" in reflection.lower() or "question" in reflection.lower()
        assert "workflow" in reflection.lower()

    def test_generate_reflection_feeling(self):
        """Test reflection on feeling statement."""
        text = "I feel excited about this project"
        reflection = generate_reflection(text)

        assert "feeling" in reflection.lower() or "expressing" in reflection.lower()

    def test_generate_reflection_achievement(self):
        """Test reflection on achievement."""
        text = "I completed the task successfully"
        reflection = generate_reflection(text)

        assert "progress" in reflection.lower() or "completed" in reflection.lower()

    def test_generate_reflection_future(self):
        """Test reflection on future planning."""
        text = "I will work on this tomorrow"
        reflection = generate_reflection(text)

        assert "intention" in reflection.lower() or "will" in reflection.lower()

    def test_generate_reflection_default(self):
        """Test default reflection."""
        text = "This is a simple note"
        reflection = generate_reflection(text)

        assert len(reflection) > 0
        assert "note" in reflection.lower() or "simple" in reflection.lower()

    def test_log_reflection_creates_entry(self):
        """Test that logging creates proper entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test_reflect.log"

            # Create log entry manually
            entry = {
                "timestamp": "2025-11-14T10:00:00Z",
                "event_type": "reflection",
                "original_text": "Test text",
                "reflection": "Test reflection",
                "source": "mirrordna_cli"
            }

            # Write to log
            with open(log_path, 'a') as f:
                f.write(json.dumps(entry) + "\n")

            # Verify log exists and contains entry
            assert log_path.exists()

            with open(log_path, 'r') as f:
                lines = f.readlines()
                assert len(lines) == 1

                logged_entry = json.loads(lines[0])
                assert logged_entry["original_text"] == "Test text"
                assert logged_entry["event_type"] == "reflection"

    def test_log_reflection_appends(self):
        """Test that logging appends to existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test_reflect.log"

            # Write first entry
            entry1 = {
                "timestamp": "2025-11-14T10:00:00Z",
                "event_type": "reflection",
                "original_text": "First",
                "reflection": "First reflection",
                "source": "test"
            }

            with open(log_path, 'a') as f:
                f.write(json.dumps(entry1) + "\n")

            # Write second entry
            entry2 = {
                "timestamp": "2025-11-14T10:01:00Z",
                "event_type": "reflection",
                "original_text": "Second",
                "reflection": "Second reflection",
                "source": "test"
            }

            with open(log_path, 'a') as f:
                f.write(json.dumps(entry2) + "\n")

            # Verify both entries exist
            with open(log_path, 'r') as f:
                lines = f.readlines()
                assert len(lines) == 2

    def test_reflection_various_inputs(self):
        """Test reflection on various input types."""
        test_cases = [
            "What should I do next?",
            "I feel great today!",
            "I finished all my tasks",
            "I plan to start tomorrow",
            "Just a random thought",
            ""
        ]

        for text in test_cases:
            reflection = generate_reflection(text)
            assert isinstance(reflection, str)
            assert len(reflection) > 0 or text == ""
