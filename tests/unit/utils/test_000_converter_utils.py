"""Tests for from_TYPE helper functions in converter_utils."""

from __future__ import annotations

import logging
import unittest
from datetime import datetime, time
from enum import Enum
from uuid import UUID

from ffbb_api_client_v2.utils.converter_utils import (
    from_bool,
    from_datetime,
    from_enum,
    from_float,
    from_int,
    from_list,
    from_obj,
    from_str,
    from_time,
    from_timestamp,
    from_uuid,
)

# --- Fixtures / helpers ---

LOGGER_NAME = "ffbb_api_client_v2.utils.converter_utils"


class Color(Enum):
    RED = "red"
    BLUE = "blue"


class SimpleModel:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def from_dict(obj: dict) -> SimpleModel:
        return SimpleModel(obj["name"])


# ==========================================================================
# from_str
# ==========================================================================


class TestFromStr(unittest.TestCase):
    def test_000_str_returns_str(self) -> None:
        self.assertEqual(from_str({"k": "hello"}, "k"), "hello")

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_str({"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_str({}, "k"))

    def test_003_int_coerced_to_str(self) -> None:
        self.assertEqual(from_str({"k": 42}, "k"), "42")

    def test_004_float_coerced_to_str(self) -> None:
        self.assertEqual(from_str({"k": 3.14}, "k"), "3.14")

    def test_005_bool_coerced_to_str(self) -> None:
        self.assertEqual(from_str({"k": True}, "k"), "True")


# ==========================================================================
# from_int
# ==========================================================================


class TestFromInt(unittest.TestCase):
    def test_006_int_returns_int(self) -> None:
        self.assertEqual(from_int({"k": 42}, "k"), 42)

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_int({"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_int({}, "k"))

    def test_009_str_coerced_to_int(self) -> None:
        self.assertEqual(from_int({"k": "0"}, "k"), 0)

    def test_010_str_negative_coerced(self) -> None:
        self.assertEqual(from_int({"k": "-7"}, "k"), -7)

    def test_061_empty_str_returns_none(self) -> None:
        self.assertIsNone(from_int({"k": ""}, "k"))

    def test_012_whitespace_str_returns_none(self) -> None:
        self.assertIsNone(from_int({"k": "  "}, "k"))

    def test_013_str_non_numeric_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_int({"k": "abc"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("cannot parse" in msg for msg in cm.output))

    def test_014_float_coerced_to_int(self) -> None:
        self.assertEqual(from_int({"k": 3.0}, "k"), 3)

    def test_022_bool_not_coerced(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_int({"k": True}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("unexpected type" in msg for msg in cm.output))


# ==========================================================================
# from_float
# ==========================================================================


class TestFromFloat(unittest.TestCase):
    def test_016_float_returns_float(self) -> None:
        self.assertEqual(from_float({"k": 3.14}, "k"), 3.14)

    def test_017_int_returns_float(self) -> None:
        result = from_float({"k": 3}, "k")
        self.assertEqual(result, 3.0)
        self.assertIsInstance(result, float)

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_float({"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_float({}, "k"))

    def test_020_str_coerced_to_float(self) -> None:
        self.assertEqual(from_float({"k": "3.14"}, "k"), 3.14)

    def test_029_str_invalid_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_float({"k": "abc"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("cannot parse" in msg for msg in cm.output))

    def test_022_bool_not_coerced(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_float({"k": True}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("unexpected type" in msg for msg in cm.output))


# ==========================================================================
# from_bool
# ==========================================================================


class TestFromBool(unittest.TestCase):
    def test_023_bool_returns_bool(self) -> None:
        self.assertIs(from_bool({"k": True}, "k"), True)
        self.assertIs(from_bool({"k": False}, "k"), False)

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_bool({"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_bool({}, "k"))

    def test_026_str_true_coerced(self) -> None:
        self.assertIs(from_bool({"k": "true"}, "k"), True)

    def test_027_str_false_coerced(self) -> None:
        self.assertIs(from_bool({"k": "false"}, "k"), False)

    def test_028_str_TRUE_case_insensitive(self) -> None:
        self.assertIs(from_bool({"k": "TRUE"}, "k"), True)
        self.assertIs(from_bool({"k": "False"}, "k"), False)

    def test_029_str_invalid_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_bool({"k": "maybe"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("cannot parse" in msg for msg in cm.output))

    def test_030_int_not_coerced(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_bool({"k": 1}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("unexpected type" in msg for msg in cm.output))


# ==========================================================================
# from_datetime
# ==========================================================================


class TestFromDatetime(unittest.TestCase):
    def test_031_iso_string_returns_datetime(self) -> None:
        result = from_datetime({"k": "2024-01-01T00:00:00"}, "k")
        self.assertIsInstance(result, datetime)
        self.assertEqual(result.year, 2024)

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_datetime({"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_datetime({}, "k"))

    def test_054_empty_string_returns_none(self) -> None:
        self.assertIsNone(from_datetime({"k": ""}, "k"))

    def test_035_invalid_string_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_datetime({"k": "not-a-date"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("cannot parse" in msg for msg in cm.output))

    def test_036_non_string_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_datetime({"k": 12345}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("unexpected type" in msg for msg in cm.output))


# ==========================================================================
# from_enum
# ==========================================================================


class TestFromEnum(unittest.TestCase):
    def test_037_known_value_returns_member(self) -> None:
        self.assertEqual(from_enum(Color, {"k": "red"}, "k"), Color.RED)

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_enum(Color, {"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_enum(Color, {}, "k"))

    def test_040_unknown_value_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_enum(Color, {"k": "unknown"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("unknown value" in msg for msg in cm.output))
        self.assertTrue(any("Color" in msg for msg in cm.output))


# ==========================================================================
# from_obj
# ==========================================================================


class TestFromObj(unittest.TestCase):
    def test_041_dict_calls_from_dict(self) -> None:
        result = from_obj(SimpleModel.from_dict, {"k": {"name": "test"}}, "k")
        self.assertIsInstance(result, SimpleModel)
        self.assertEqual(result.name, "test")

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_obj(SimpleModel.from_dict, {"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_obj(SimpleModel.from_dict, {}, "k"))

    def test_044_non_dict_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_obj(SimpleModel.from_dict, {"k": "string"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("expected dict" in msg for msg in cm.output))


# ==========================================================================
# from_list
# ==========================================================================


class TestFromList(unittest.TestCase):
    def test_045_list_maps_items(self) -> None:
        result = from_list(
            SimpleModel.from_dict,
            {"k": [{"name": "a"}, {"name": "b"}]},
            "k",
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "a")
        self.assertEqual(result[1].name, "b")

    def test_046_list_of_primitives(self) -> None:
        result = from_list(int, {"k": ["1", "2", "3"]}, "k")
        self.assertEqual(result, [1, 2, 3])

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_list(str, {"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_list(str, {}, "k"))

    def test_049_empty_list_returns_empty(self) -> None:
        self.assertEqual(from_list(str, {"k": []}, "k"), [])

    def test_050_non_list_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_list(str, {"k": "string"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("expected list" in msg for msg in cm.output))


# ==========================================================================
# from_uuid
# ==========================================================================


class TestFromUuid(unittest.TestCase):
    def test_051_valid_uuid_string(self) -> None:
        result = from_uuid({"k": "550e8400-e29b-41d4-a716-446655440000"}, "k")
        self.assertIsInstance(result, UUID)
        self.assertEqual(str(result), "550e8400-e29b-41d4-a716-446655440000")

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_uuid({"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_uuid({}, "k"))

    def test_054_empty_string_returns_none(self) -> None:
        self.assertIsNone(from_uuid({"k": ""}, "k"))

    def test_055_invalid_uuid_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_uuid({"k": "not-a-uuid"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("invalid UUID" in msg for msg in cm.output))


# ==========================================================================
# from_time
# ==========================================================================


class TestFromTime(unittest.TestCase):
    def test_056_iso_format(self) -> None:
        self.assertEqual(from_time({"k": "20:30:00"}, "k"), time(20, 30, 0))

    def test_057_hhmm_format(self) -> None:
        self.assertEqual(from_time({"k": "2030"}, "k"), time(20, 30, 0))

    def test_058_hh_mm(self) -> None:
        self.assertEqual(from_time({"k": "20:30"}, "k"), time(20, 30, 0))

    def test_059_none_returns_none(self) -> None:
        self.assertIsNone(from_time({"k": None}, "k"))

    def test_060_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_time({}, "k"))

    def test_061_empty_str_returns_none(self) -> None:
        self.assertIsNone(from_time({"k": ""}, "k"))

    def test_062_invalid_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_time({"k": "abc"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("cannot parse" in msg for msg in cm.output))

    def test_063_time_passthrough(self) -> None:
        self.assertEqual(from_time({"k": time(20, 30)}, "k"), time(20, 30))


# ==========================================================================
# from_timestamp
# ==========================================================================


class TestFromTimestamp(unittest.TestCase):
    def test_064_int_value(self) -> None:
        result = from_timestamp({"k": 1757534767}, "k")
        self.assertIsInstance(result, datetime)
        assert result is not None
        self.assertEqual(result.year, 2025)

    def test_065_numeric_string(self) -> None:
        result = from_timestamp({"k": "1757534767"}, "k")
        self.assertIsInstance(result, datetime)

    def test_066_none_returns_none(self) -> None:
        self.assertIsNone(from_timestamp({"k": None}, "k"))

    def test_067_missing_key_returns_none(self) -> None:
        self.assertIsNone(from_timestamp({}, "k"))

    def test_068_empty_str_returns_none(self) -> None:
        self.assertIsNone(from_timestamp({"k": ""}, "k"))

    def test_069_non_numeric_str_warns(self) -> None:
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_timestamp({"k": "not-a-number"}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("cannot parse" in msg for msg in cm.output))

    def test_070_float_value(self) -> None:
        result = from_timestamp({"k": 1757534767.5}, "k")
        self.assertIsInstance(result, datetime)

    def test_071_bool_ignored(self) -> None:
        """Booleans are not treated as ints."""
        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            result = from_timestamp({"k": True}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("unexpected type" in msg for msg in cm.output))

    def test_072_whitespace_string(self) -> None:
        self.assertIsNone(from_timestamp({"k": "   "}, "k"))


if __name__ == "__main__":
    unittest.main()
