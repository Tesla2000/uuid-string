import unittest
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import ValidationError

from uuid_shaped_string import UUIDShapedString


class TestUUIDShapedStringBasic(unittest.TestCase):
    def test_creates_from_valid_uuid_string(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertEqual(result, uuid_str)
        self.assertIsInstance(result, str)
        self.assertIsInstance(result, UUIDShapedString)

    def test_creates_from_uuid_object(self) -> None:
        uuid_obj = UUID("550e8400-e29b-41d4-a716-446655440000")
        result = UUIDShapedString(uuid_obj)
        self.assertEqual(result, str(uuid_obj))
        self.assertIsInstance(result, UUIDShapedString)

    def test_creates_from_random_uuid(self) -> None:
        uuid_obj = uuid4()
        result = UUIDShapedString(uuid_obj)
        self.assertEqual(result, str(uuid_obj))

    def test_raises_on_invalid_uuid_string(self) -> None:
        with self.assertRaises(ValueError):
            UUIDShapedString("not-a-uuid")

    def test_raises_on_empty_string(self) -> None:
        with self.assertRaises(ValueError):
            UUIDShapedString("")

    def test_raises_on_no_arguments(self) -> None:
        with self.assertRaises(ValueError):
            UUIDShapedString()

    def test_raises_on_partial_uuid(self) -> None:
        with self.assertRaises(ValueError):
            UUIDShapedString("550e8400-e29b-41d4")

    def test_raises_on_malformed_uuid(self) -> None:
        with self.assertRaises(ValueError):
            UUIDShapedString("550e8400-e29b-41d4-a716-44665544000g")

    def test_accepts_uppercase_uuid(self) -> None:
        uuid_str = "550E8400-E29B-41D4-A716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertEqual(result, uuid_str)

    def test_accepts_uuid_without_hyphens(self) -> None:
        uuid_str = "550e8400e29b41d4a716446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertEqual(result, uuid_str)

    def test_string_operations_work(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertEqual(result.upper(), uuid_str.upper())
        self.assertEqual(result.replace("-", ""), uuid_str.replace("-", ""))
        self.assertTrue(result.startswith("550e"))

    def test_equality_with_string(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertEqual(result, uuid_str)

    def test_equality_with_another_uuid_shaped_string(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result1 = UUIDShapedString(uuid_str)
        result2 = UUIDShapedString(uuid_str)
        self.assertEqual(result1, result2)

    def test_hash_works(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        uuid_set = {result}
        self.assertIn(result, uuid_set)

    def test_length(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertEqual(len(result), len(uuid_str))


class TestUUIDShapedStringPydantic(unittest.TestCase):
    def test_validates_uuid_string_in_model(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = Model(id=uuid_str)
        self.assertEqual(model.id, uuid_str)
        self.assertIsInstance(model.id, UUIDShapedString)

    def test_validates_uuid_object_in_model(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString

        uuid_obj = UUID("550e8400-e29b-41d4-a716-446655440000")
        model = Model(id=uuid_obj)
        self.assertEqual(model.id, str(uuid_obj))
        self.assertIsInstance(model.id, UUIDShapedString)

    def test_rejects_invalid_uuid_in_model(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString

        with self.assertRaises(ValidationError):
            Model(id="not-a-uuid")

    def test_rejects_empty_string_in_model(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString

        with self.assertRaises(ValidationError):
            Model(id="")

    def test_serialization_returns_string(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = Model(id=uuid_str)
        serialized = model.model_dump()
        self.assertEqual(serialized["id"], uuid_str)
        self.assertIsInstance(serialized["id"], str)

    def test_json_serialization(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = Model(id=uuid_str)
        json_str = model.model_dump_json()
        self.assertIn(uuid_str, json_str)

    def test_multiple_fields_in_model(self) -> None:
        class Model(BaseModel):
            user_id: UUIDShapedString
            session_id: UUIDShapedString

        user_uuid = "550e8400-e29b-41d4-a716-446655440000"
        session_uuid = uuid4()
        model = Model(user_id=user_uuid, session_id=session_uuid)
        self.assertEqual(model.user_id, user_uuid)
        self.assertEqual(model.session_id, str(session_uuid))

    def test_optional_field(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString | None = None

        model_with_value = Model(id="550e8400-e29b-41d4-a716-446655440000")
        model_without_value = Model()
        self.assertIsInstance(model_with_value.id, UUIDShapedString)
        self.assertIsNone(model_without_value.id)

    def test_validation_error_message_on_invalid_uuid(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString

        with self.assertRaises(ValidationError) as context:
            Model(id="invalid-uuid")
        self.assertIn("id", str(context.exception))

    def test_model_round_trip(self) -> None:
        class Model(BaseModel):
            id: UUIDShapedString

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        original = Model(id=uuid_str)
        serialized = original.model_dump()
        reconstructed = Model(**serialized)
        self.assertEqual(original.id, reconstructed.id)

    def test_nested_model_validation(self) -> None:
        class InnerModel(BaseModel):
            id: UUIDShapedString

        class OuterModel(BaseModel):
            inner: InnerModel

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = OuterModel(inner={"id": uuid_str})
        self.assertEqual(model.inner.id, uuid_str)
        self.assertIsInstance(model.inner.id, UUIDShapedString)

    def test_list_of_uuids(self) -> None:
        class Model(BaseModel):
            ids: list[UUIDShapedString]

        uuid1 = "550e8400-e29b-41d4-a716-446655440000"
        uuid2 = uuid4()
        model = Model(ids=[uuid1, uuid2])
        self.assertEqual(len(model.ids), 2)
        self.assertIsInstance(model.ids[0], UUIDShapedString)
        self.assertIsInstance(model.ids[1], UUIDShapedString)

    def test_dict_with_uuid_values(self) -> None:
        class Model(BaseModel):
            mapping: dict[str, UUIDShapedString]

        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = Model(mapping={"key": uuid_str})
        self.assertIsInstance(model.mapping["key"], UUIDShapedString)


class TestUUIDShapedStringEdgeCases(unittest.TestCase):
    def test_nil_uuid(self) -> None:
        nil_uuid = "00000000-0000-0000-0000-000000000000"
        result = UUIDShapedString(nil_uuid)
        self.assertEqual(result, nil_uuid)

    def test_max_uuid(self) -> None:
        max_uuid = "ffffffff-ffff-ffff-ffff-ffffffffffff"
        result = UUIDShapedString(max_uuid)
        self.assertEqual(result, max_uuid)

    def test_different_uuid_versions(self) -> None:
        uuid_v1 = "550e8400-e29b-11d4-a716-446655440000"
        uuid_v4 = "550e8400-e29b-41d4-a716-446655440000"
        uuid_v5 = "550e8400-e29b-51d4-a716-446655440000"
        self.assertIsInstance(UUIDShapedString(uuid_v1), UUIDShapedString)
        self.assertIsInstance(UUIDShapedString(uuid_v4), UUIDShapedString)
        self.assertIsInstance(UUIDShapedString(uuid_v5), UUIDShapedString)

    def test_repr(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertIn(uuid_str, repr(result))

    def test_str(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertEqual(str(result), uuid_str)

    def test_concatenation(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        concatenated = result + "-suffix"
        self.assertEqual(concatenated, uuid_str + "-suffix")
        self.assertIsInstance(concatenated, str)

    def test_slicing(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertEqual(result[:8], "550e8400")
        self.assertEqual(result[-12:], "446655440000")

    def test_in_operator(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        self.assertIn("550e", result)
        self.assertNotIn("zzz", result)

    def test_formatting(self) -> None:
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        result = UUIDShapedString(uuid_str)
        formatted = f"UUID: {result}"
        self.assertEqual(formatted, f"UUID: {uuid_str}")


if __name__ == "__main__":
    unittest.main()
