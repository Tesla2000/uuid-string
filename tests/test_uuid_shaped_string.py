import unittest
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import ValidationError
from uuid_string import UUIDString


class TestUUIDShapedStringBasic(unittest.TestCase):
    def test_creates_from_valid_uuid_string(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        self.assertEqual(result, uuid_str)
        self.assertIsInstance(result, str)
        self.assertIsInstance(result, UUIDString)

    def test_creates_from_uuid_object(self) -> None:
        uuid_obj = UUID("550e8400-e29b-41d4-a716-446655440000")
        result = UUIDString(uuid_obj)
        self.assertEqual(result, str(uuid_obj))
        self.assertIsInstance(result, UUIDString)

    def test_creates_from_random_uuid(self) -> None:
        uuid_obj = uuid4()
        result = UUIDString(uuid_obj)
        self.assertEqual(result, str(uuid_obj))

    def test_raises_on_invalid_uuid_string(self) -> None:
        with self.assertRaises(ValueError):
            UUIDString("not-a-uuid")

    def test_raises_on_empty_string(self) -> None:
        with self.assertRaises(ValueError):
            UUIDString("")

    def test_raises_on_no_arguments(self) -> None:
        with self.assertRaises(ValueError):
            UUIDString()

    def test_raises_on_partial_uuid(self) -> None:
        with self.assertRaises(ValueError):
            UUIDString("550e8400-e29b-41d4")

    def test_raises_on_malformed_uuid(self) -> None:
        with self.assertRaises(ValueError):
            UUIDString("550e8400-e29b-41d4-a716-44665544000g")

    def test_accepts_uppercase_uuid(self) -> None:
        uuid_str = "550E8400-E29B-41D4-A716-446655440000"
        result = UUIDString(uuid_str)
        self.assertEqual(result, uuid_str)

    def test_accepts_uuid_without_hyphens(self) -> None:
        uuid_str = "550e8400e29b41d4a716446655440000"
        result = UUIDString(uuid_str)
        self.assertEqual(result, uuid_str)

    def test_string_operations_work(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        self.assertEqual(result.upper(), uuid_str.upper())
        self.assertEqual(result.replace("-", ""), uuid_str.replace("-", ""))
        self.assertTrue(result.startswith("550e"))

    def test_equality_with_string(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        self.assertEqual(result, uuid_str)

    def test_equality_with_another_uuid_shaped_string(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result1 = UUIDString(uuid_str)
        result2 = UUIDString(uuid_str)
        self.assertEqual(result1, result2)

    def test_hash_works(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        uuid_set = {result}
        self.assertIn(result, uuid_set)

    def test_length(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        self.assertEqual(len(result), len(uuid_str))


class TestUUIDShapedStringPydantic(unittest.TestCase):
    def test_validates_uuid_string_in_model(self) -> None:
        class Model(BaseModel):
            id: UUIDString

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = Model(id=uuid_str)
        self.assertEqual(model.id, uuid_str)
        self.assertIsInstance(model.id, UUIDString)

    def test_validates_uuid_object_in_model(self) -> None:
        class Model(BaseModel):
            id: UUIDString

        uuid_obj = UUID("550e8400-e29b-41d4-a716-446655440000")
        model = Model(id=uuid_obj)
        self.assertEqual(model.id, str(uuid_obj))
        self.assertIsInstance(model.id, UUIDString)

    def test_rejects_invalid_uuid_in_model(self) -> None:
        class Model(BaseModel):
            id: UUIDString

        with self.assertRaises(ValidationError):
            Model(id="not-a-uuid")

    def test_rejects_empty_string_in_model(self) -> None:
        class Model(BaseModel):
            id: UUIDString

        with self.assertRaises(ValidationError):
            Model(id="")

    def test_serialization_returns_string(self) -> None:
        class Model(BaseModel):
            id: UUIDString

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = Model(id=uuid_str)
        serialized = model.model_dump()
        self.assertEqual(serialized["id"], uuid_str)
        self.assertIsInstance(serialized["id"], str)

    def test_json_serialization(self) -> None:
        class Model(BaseModel):
            id: UUIDString

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = Model(id=uuid_str)
        json_str = model.model_dump_json()
        self.assertIn(uuid_str, json_str)

    def test_multiple_fields_in_model(self) -> None:
        class Model(BaseModel):
            user_id: UUIDString
            session_id: UUIDString

        user_uuid = "550e8400-e29b-41d4-a716-446655440000"
        session_uuid = uuid4()
        model = Model(user_id=user_uuid, session_id=session_uuid)
        self.assertEqual(model.user_id, user_uuid)
        self.assertEqual(model.session_id, str(session_uuid))

    def test_optional_field(self) -> None:
        class Model(BaseModel):
            id: Optional[UUIDString] = None

        model_with_value = Model(id="550e8400-e29b-41d4-a716-446655440000")
        model_without_value = Model()
        self.assertIsInstance(model_with_value.id, UUIDString)
        self.assertIsNone(model_without_value.id)

    def test_validation_error_message_on_invalid_uuid(self) -> None:
        class Model(BaseModel):
            id: UUIDString

        with self.assertRaises(ValidationError) as context:
            Model(id="invalid-uuid")
        self.assertIn("id", str(context.exception))

    def test_model_round_trip(self) -> None:
        class Model(BaseModel):
            id: UUIDString

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        original = Model(id=uuid_str)
        serialized = original.model_dump()
        reconstructed = Model(**serialized)
        self.assertEqual(original.id, reconstructed.id)

    def test_nested_model_validation(self) -> None:
        class InnerModel(BaseModel):
            id: UUIDString

        class OuterModel(BaseModel):
            inner: InnerModel

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = OuterModel(inner={"id": uuid_str})
        self.assertEqual(model.inner.id, uuid_str)
        self.assertIsInstance(model.inner.id, UUIDString)

    def test_list_of_uuids(self) -> None:
        class Model(BaseModel):
            ids: list[UUIDString]

        uuid1 = "550e8400-e29b-41d4-a716-446655440000"
        uuid2 = uuid4()
        model = Model(ids=[uuid1, uuid2])
        self.assertEqual(len(model.ids), 2)
        self.assertIsInstance(model.ids[0], UUIDString)
        self.assertIsInstance(model.ids[1], UUIDString)

    def test_dict_with_uuid_values(self) -> None:
        class Model(BaseModel):
            mapping: dict[str, UUIDString]

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = Model(mapping={"key": uuid_str})
        self.assertIsInstance(model.mapping["key"], UUIDString)


class TestUUIDShapedStringProperties(unittest.TestCase):
    def test_bytes_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.bytes, uuid_obj.bytes)
        self.assertIsInstance(uuid_shaped.bytes, bytes)
        self.assertEqual(len(uuid_shaped.bytes), 16)

    def test_bytes_le_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.bytes_le, uuid_obj.bytes_le)
        self.assertIsInstance(uuid_shaped.bytes_le, bytes)

    def test_fields_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.fields, uuid_obj.fields)
        self.assertIsInstance(uuid_shaped.fields, tuple)
        self.assertEqual(len(uuid_shaped.fields), 6)

    def test_time_low_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.time_low, uuid_obj.time_low)
        self.assertIsInstance(uuid_shaped.time_low, int)

    def test_time_mid_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.time_mid, uuid_obj.time_mid)
        self.assertIsInstance(uuid_shaped.time_mid, int)

    def test_time_hi_version_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.time_hi_version, uuid_obj.time_hi_version)
        self.assertIsInstance(uuid_shaped.time_hi_version, int)

    def test_clock_seq_hi_variant_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(
            uuid_shaped.clock_seq_hi_variant, uuid_obj.clock_seq_hi_variant
        )
        self.assertIsInstance(uuid_shaped.clock_seq_hi_variant, int)

    def test_clock_seq_low_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.clock_seq_low, uuid_obj.clock_seq_low)
        self.assertIsInstance(uuid_shaped.clock_seq_low, int)

    def test_time_property(self) -> None:
        uuid_str = "550e8400-e29b-11d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.time, uuid_obj.time)
        self.assertIsInstance(uuid_shaped.time, int)

    def test_clock_seq_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.clock_seq, uuid_obj.clock_seq)
        self.assertIsInstance(uuid_shaped.clock_seq, int)

    def test_node_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.node, uuid_obj.node)
        self.assertIsInstance(uuid_shaped.node, int)

    def test_hex_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.hex, uuid_obj.hex)
        self.assertIsInstance(uuid_shaped.hex, str)
        self.assertNotIn("-", uuid_shaped.hex)

    def test_urn_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.urn, uuid_obj.urn)
        self.assertIsInstance(uuid_shaped.urn, str)
        self.assertTrue(uuid_shaped.urn.startswith("urn:uuid:"))

    def test_variant_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.variant, uuid_obj.variant)

    def test_version_property(self) -> None:
        uuid_v4_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_v4_str)
        uuid_obj = UUID(uuid_v4_str)
        self.assertEqual(uuid_shaped.version, uuid_obj.version)
        self.assertEqual(uuid_shaped.version, 4)

    def test_version_property_v1(self) -> None:
        uuid_v1_str = "550e8400-e29b-11d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_v1_str)
        self.assertEqual(uuid_shaped.version, 1)

    def test_is_safe_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.is_safe, uuid_obj.is_safe)

    def test_int_property(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(uuid_shaped.int, uuid_obj.int)
        self.assertIsInstance(uuid_shaped.int, int)
        self.assertGreater(uuid_shaped.int, 0)

    def test_int_dunder_method(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_shaped = UUIDString(uuid_str)
        uuid_obj = UUID(uuid_str)
        self.assertEqual(int(uuid_shaped), int(uuid_obj))
        self.assertEqual(int(uuid_shaped), uuid_shaped.int)

    def test_properties_with_random_uuid(self) -> None:
        uuid_obj = uuid4()
        uuid_shaped = UUIDString(uuid_obj)
        self.assertEqual(uuid_shaped.bytes, uuid_obj.bytes)
        self.assertEqual(uuid_shaped.hex, uuid_obj.hex)
        self.assertEqual(uuid_shaped.int, uuid_obj.int)
        self.assertEqual(uuid_shaped.version, uuid_obj.version)
        self.assertEqual(uuid_shaped.variant, uuid_obj.variant)

    def test_properties_with_nil_uuid(self) -> None:
        nil_uuid = "00000000-0000-0000-0000-000000000000"
        uuid_shaped = UUIDString(nil_uuid)
        uuid_obj = UUID(nil_uuid)
        self.assertEqual(uuid_shaped.int, 0)
        self.assertEqual(uuid_shaped.bytes, uuid_obj.bytes)
        self.assertEqual(uuid_shaped.hex, "00000000000000000000000000000000")


class TestUUIDShapedStringEdgeCases(unittest.TestCase):
    def test_nil_uuid(self) -> None:
        nil_uuid = "00000000-0000-0000-0000-000000000000"
        result = UUIDString(nil_uuid)
        self.assertEqual(result, nil_uuid)

    def test_max_uuid(self) -> None:
        max_uuid = "ffffffff-ffff-ffff-ffff-ffffffffffff"
        result = UUIDString(max_uuid)
        self.assertEqual(result, max_uuid)

    def test_different_uuid_versions(self) -> None:
        uuid_v1 = "550e8400-e29b-11d4-a716-446655440000"
        uuid_v4 = "550e8400-e29b-41d4-a716-446655440000"
        uuid_v5 = "550e8400-e29b-51d4-a716-446655440000"
        self.assertIsInstance(UUIDString(uuid_v1), UUIDString)
        self.assertIsInstance(UUIDString(uuid_v4), UUIDString)
        self.assertIsInstance(UUIDString(uuid_v5), UUIDString)

    def test_repr(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        self.assertIn(uuid_str, repr(result))

    def test_str(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        self.assertEqual(str(result), uuid_str)

    def test_concatenation(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        concatenated = result + "-suffix"
        self.assertEqual(concatenated, uuid_str + "-suffix")
        self.assertIsInstance(concatenated, str)

    def test_slicing(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        self.assertEqual(result[:8], "550e8400")
        self.assertEqual(result[-12:], "446655440000")

    def test_in_operator(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        self.assertIn("550e", result)
        self.assertNotIn("zzz", result)

    def test_formatting(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDString(uuid_str)
        formatted = f"UUID: {result}"
        self.assertEqual(formatted, f"UUID: {uuid_str}")


if __name__ == "__main__":
    unittest.main()
