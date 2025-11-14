"""
Tests for verify-log command.
"""

import pytest
from pathlib import Path
import tempfile
import json
from cli.commands.verify_log import validate_log_entry, load_log_file


class TestVerifyLog:
    """Test verify-log command functionality."""

    def test_valid_log_entry(self):
        """Test that valid log entry passes validation."""
        entry = {
            "timestamp": "2025-11-14T10:00:00Z",
            "event_type": "test_event",
            "message": "Test message"
        }

        errors = validate_log_entry(entry, 0)
        assert len(errors) == 0, "Valid entry should have no errors"

    def test_missing_required_field(self):
        """Test that missing required field is detected."""
        entry = {
            "timestamp": "2025-11-14T10:00:00Z",
            "event_type": "test_event"
            # Missing 'message'
        }

        errors = validate_log_entry(entry, 0)
        assert len(errors) > 0, "Missing field should produce error"
        assert any("message" in err.lower() for err in errors)

    def test_empty_required_field(self):
        """Test that empty required field is detected."""
        entry = {
            "timestamp": "2025-11-14T10:00:00Z",
            "event_type": "",
            "message": "Test"
        }

        errors = validate_log_entry(entry, 0)
        assert len(errors) > 0, "Empty field should produce error"

    def test_invalid_timestamp_format(self):
        """Test that invalid timestamp format is detected."""
        entry = {
            "timestamp": "not-a-timestamp",
            "event_type": "test",
            "message": "Test"
        }

        errors = validate_log_entry(entry, 0)
        assert len(errors) > 0, "Invalid timestamp should produce error"
        assert any("timestamp" in err.lower() for err in errors)

    def test_valid_timestamp_formats(self):
        """Test that various valid timestamp formats are accepted."""
        valid_timestamps = [
            "2025-11-14T10:00:00Z",
            "2025-11-14T10:00:00+00:00",
            "2025-11-14T10:00:00.123456Z",
        ]

        for ts in valid_timestamps:
            entry = {
                "timestamp": ts,
                "event_type": "test",
                "message": "Test"
            }
            errors = validate_log_entry(entry, 0)
            assert len(errors) == 0, f"Timestamp {ts} should be valid"

    def test_load_json_log_file(self):
        """Test loading a JSON log file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            log_data = [
                {
                    "timestamp": "2025-11-14T10:00:00Z",
                    "event_type": "test",
                    "message": "Test 1"
                },
                {
                    "timestamp": "2025-11-14T10:01:00Z",
                    "event_type": "test",
                    "message": "Test 2"
                }
            ]
            json.dump(log_data, f)
            f.flush()

            try:
                entries = load_log_file(Path(f.name))
                assert len(entries) == 2
                assert entries[0]["message"] == "Test 1"
            finally:
                Path(f.name).unlink()

    def test_load_invalid_json(self):
        """Test that invalid JSON raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            f.flush()

            try:
                with pytest.raises(ValueError, match="Invalid JSON/YAML"):
                    load_log_file(Path(f.name))
            finally:
                Path(f.name).unlink()

    def test_load_non_list_json(self):
        """Test that non-list JSON raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"not": "a list"}, f)
            f.flush()

            try:
                with pytest.raises(ValueError, match="must contain a list"):
                    load_log_file(Path(f.name))
            finally:
                Path(f.name).unlink()

    def test_all_required_fields_present(self):
        """Test that entry with all required fields is valid."""
        entry = {
            "event_id": "evt_001",
            "timestamp": "2025-11-14T10:00:00Z",
            "event_type": "session_start",
            "actor": "user",
            "message": "Session started",
            "metadata": {"platform": "test"}
        }

        errors = validate_log_entry(entry, 0)
        assert len(errors) == 0, "Entry with all fields should be valid"
