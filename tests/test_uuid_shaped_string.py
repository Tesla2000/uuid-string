from typing import Optional
from uuid import UUID
from uuid import uuid4

import pytest
from pydantic import BaseModel
from pydantic import ValidationError
from uuid_string import UUIDString

UUID_STR = "550e8400-e29b-41d4-a716-446655440000"
UUID_OBJ = UUID(UUID_STR)


def test_creates_from_valid_uuid_string() -> None:
    result = UUIDString(UUID_STR)
    assert result == UUID_STR
    assert isinstance(result, str)
    assert isinstance(result, UUIDString)


def test_creates_from_uuid_object() -> None:
    result = UUIDString(UUID_OBJ)
    assert result == str(UUID_OBJ)
    assert isinstance(result, UUIDString)


def test_creates_from_random_uuid() -> None:
    uuid_obj = uuid4()
    result = UUIDString(uuid_obj)
    assert result == str(uuid_obj)


def test_raises_on_invalid_uuid_string() -> None:
    with pytest.raises(ValueError):
        UUIDString("not-a-uuid")


def test_raises_on_empty_string() -> None:
    with pytest.raises(ValueError):
        UUIDString("")


def test_raises_on_no_arguments() -> None:
    with pytest.raises(ValueError):
        UUIDString()


def test_raises_on_partial_uuid() -> None:
    with pytest.raises(ValueError):
        UUIDString("550e8400-e29b-41d4")


def test_raises_on_malformed_uuid() -> None:
    with pytest.raises(ValueError):
        UUIDString("550e8400-e29b-41d4-a716-44665544000g")


def test_accepts_uppercase_uuid() -> None:
    uuid_str = "550E8400-E29B-41D4-A716-446655440000"
    result = UUIDString(uuid_str)
    assert result == uuid_str


def test_accepts_uuid_without_hyphens() -> None:
    uuid_str = "550e8400e29b41d4a716446655440000"
    result = UUIDString(uuid_str)
    assert result == uuid_str


def test_string_operations_work() -> None:
    result = UUIDString(UUID_STR)
    assert result.upper() == UUID_STR.upper()
    assert result.replace("-", "") == UUID_STR.replace("-", "")
    assert result.startswith("550e")


def test_equality_with_string() -> None:
    result = UUIDString(UUID_STR)
    assert result == UUID_STR


def test_equality_with_another_uuid_shaped_string() -> None:
    assert UUIDString(UUID_STR) == UUIDString(UUID_STR)


def test_hash_works() -> None:
    result = UUIDString(UUID_STR)
    assert result in {result}


def test_length() -> None:
    result = UUIDString(UUID_STR)
    assert len(result) == len(UUID_STR)


def test_validates_uuid_string_in_model() -> None:
    class Model(BaseModel):
        id: UUIDString

    model = Model(id=UUID_STR)
    assert model.id == UUID_STR
    assert isinstance(model.id, UUIDString)


def test_validates_uuid_object_in_model() -> None:
    class Model(BaseModel):
        id: UUIDString

    model = Model(id=UUID_OBJ)
    assert model.id == str(UUID_OBJ)
    assert isinstance(model.id, UUIDString)


def test_rejects_invalid_uuid_in_model() -> None:
    class Model(BaseModel):
        id: UUIDString

    with pytest.raises(ValidationError):
        Model(id="not-a-uuid")


def test_rejects_empty_string_in_model() -> None:
    class Model(BaseModel):
        id: UUIDString

    with pytest.raises(ValidationError):
        Model(id="")


def test_serialization_returns_string() -> None:
    class Model(BaseModel):
        id: UUIDString

    model = Model(id=UUID_STR)
    serialized = model.model_dump()
    assert serialized["id"] == UUID_STR
    assert isinstance(serialized["id"], str)


def test_json_serialization() -> None:
    class Model(BaseModel):
        id: UUIDString

    model = Model(id=UUID_STR)
    assert UUID_STR in model.model_dump_json()


def test_multiple_fields_in_model() -> None:
    class Model(BaseModel):
        user_id: UUIDString
        session_id: UUIDString

    session_uuid = uuid4()
    model = Model(user_id=UUID_STR, session_id=session_uuid)
    assert model.user_id == UUID_STR
    assert model.session_id == str(session_uuid)


def test_optional_field() -> None:
    class Model(BaseModel):
        id: Optional[UUIDString] = None

    assert isinstance(Model(id=UUID_STR).id, UUIDString)
    assert Model().id is None


def test_validation_error_message_on_invalid_uuid() -> None:
    class Model(BaseModel):
        id: UUIDString

    with pytest.raises(ValidationError) as exc_info:
        Model(id="invalid-uuid")
    assert "id" in str(exc_info.value)


def test_model_round_trip() -> None:
    class Model(BaseModel):
        id: UUIDString

    original = Model(id=UUID_STR)
    assert original.id == Model(**original.model_dump()).id


def test_nested_model_validation() -> None:
    class InnerModel(BaseModel):
        id: UUIDString

    class OuterModel(BaseModel):
        inner: InnerModel

    model = OuterModel(inner={"id": UUID_STR})
    assert model.inner.id == UUID_STR
    assert isinstance(model.inner.id, UUIDString)


def test_list_of_uuids() -> None:
    class Model(BaseModel):
        ids: list[UUIDString]

    uuid2 = uuid4()
    model = Model(ids=[UUID_STR, uuid2])
    assert len(model.ids) == 2
    assert isinstance(model.ids[0], UUIDString)
    assert isinstance(model.ids[1], UUIDString)


def test_dict_with_uuid_values() -> None:
    class Model(BaseModel):
        mapping: dict[str, UUIDString]

    model = Model(mapping={"key": UUID_STR})
    assert isinstance(model.mapping["key"], UUIDString)


def test_bytes_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.bytes == UUID_OBJ.bytes
    assert isinstance(uuid_shaped.bytes, bytes)
    assert len(uuid_shaped.bytes) == 16


def test_bytes_le_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.bytes_le == UUID_OBJ.bytes_le
    assert isinstance(uuid_shaped.bytes_le, bytes)


def test_fields_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.fields == UUID_OBJ.fields
    assert isinstance(uuid_shaped.fields, tuple)
    assert len(uuid_shaped.fields) == 6


def test_time_low_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.time_low == UUID_OBJ.time_low
    assert isinstance(uuid_shaped.time_low, int)


def test_time_mid_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.time_mid == UUID_OBJ.time_mid
    assert isinstance(uuid_shaped.time_mid, int)


def test_time_hi_version_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.time_hi_version == UUID_OBJ.time_hi_version
    assert isinstance(uuid_shaped.time_hi_version, int)


def test_clock_seq_hi_variant_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.clock_seq_hi_variant == UUID_OBJ.clock_seq_hi_variant
    assert isinstance(uuid_shaped.clock_seq_hi_variant, int)


def test_clock_seq_low_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.clock_seq_low == UUID_OBJ.clock_seq_low
    assert isinstance(uuid_shaped.clock_seq_low, int)


def test_time_property() -> None:
    uuid_v1_str = "550e8400-e29b-11d4-a716-446655440000"
    uuid_shaped = UUIDString(uuid_v1_str)
    assert uuid_shaped.time == UUID(uuid_v1_str).time
    assert isinstance(uuid_shaped.time, int)


def test_clock_seq_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.clock_seq == UUID_OBJ.clock_seq
    assert isinstance(uuid_shaped.clock_seq, int)


def test_node_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.node == UUID_OBJ.node
    assert isinstance(uuid_shaped.node, int)


def test_hex_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.hex == UUID_OBJ.hex
    assert isinstance(uuid_shaped.hex, str)
    assert "-" not in uuid_shaped.hex


def test_urn_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.urn == UUID_OBJ.urn
    assert isinstance(uuid_shaped.urn, str)
    assert uuid_shaped.urn.startswith("urn:uuid:")


def test_variant_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.variant == UUID_OBJ.variant


def test_version_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.version == UUID_OBJ.version
    assert uuid_shaped.version == 4


def test_version_property_v1() -> None:
    uuid_shaped = UUIDString("550e8400-e29b-11d4-a716-446655440000")
    assert uuid_shaped.version == 1


def test_is_safe_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.is_safe == UUID_OBJ.is_safe


def test_int_property() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert uuid_shaped.int == UUID_OBJ.int
    assert isinstance(uuid_shaped.int, int)
    assert uuid_shaped.int > 0


def test_int_dunder_method() -> None:
    uuid_shaped = UUIDString(UUID_STR)
    assert int(uuid_shaped) == int(UUID_OBJ)
    assert int(uuid_shaped) == uuid_shaped.int


def test_properties_with_random_uuid() -> None:
    uuid_obj = uuid4()
    uuid_shaped = UUIDString(uuid_obj)
    assert uuid_shaped.bytes == uuid_obj.bytes
    assert uuid_shaped.hex == uuid_obj.hex
    assert uuid_shaped.int == uuid_obj.int
    assert uuid_shaped.version == uuid_obj.version
    assert uuid_shaped.variant == uuid_obj.variant


def test_properties_with_nil_uuid() -> None:
    nil_uuid = "00000000-0000-0000-0000-000000000000"
    uuid_shaped = UUIDString(nil_uuid)
    uuid_obj = UUID(nil_uuid)
    assert uuid_shaped.int == 0
    assert uuid_shaped.bytes == uuid_obj.bytes
    assert uuid_shaped.hex == "00000000000000000000000000000000"


def test_nil_uuid() -> None:
    nil_uuid = "00000000-0000-0000-0000-000000000000"
    assert UUIDString(nil_uuid) == nil_uuid


def test_max_uuid() -> None:
    max_uuid = "ffffffff-ffff-ffff-ffff-ffffffffffff"
    assert UUIDString(max_uuid) == max_uuid


def test_different_uuid_versions() -> None:
    assert isinstance(
        UUIDString("550e8400-e29b-11d4-a716-446655440000"), UUIDString
    )
    assert isinstance(
        UUIDString("550e8400-e29b-41d4-a716-446655440000"), UUIDString
    )
    assert isinstance(
        UUIDString("550e8400-e29b-51d4-a716-446655440000"), UUIDString
    )


def test_repr() -> None:
    result = UUIDString(UUID_STR)
    assert UUID_STR in repr(result)


def test_str() -> None:
    result = UUIDString(UUID_STR)
    assert str(result) == UUID_STR


def test_concatenation() -> None:
    result = UUIDString(UUID_STR)
    concatenated = result + "-suffix"
    assert concatenated == UUID_STR + "-suffix"
    assert isinstance(concatenated, str)


def test_slicing() -> None:
    result = UUIDString(UUID_STR)
    assert result[:8] == "550e8400"
    assert result[-12:] == "446655440000"


def test_in_operator() -> None:
    result = UUIDString(UUID_STR)
    assert "550e" in result
    assert "zzz" not in result


def test_formatting() -> None:
    result = UUIDString(UUID_STR)
    assert f"UUID: {result}" == f"UUID: {UUID_STR}"
