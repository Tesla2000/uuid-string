from typing import Optional
from typing import TYPE_CHECKING
from uuid import SafeUUID
from uuid import UUID

from typing_extensions import Self

if TYPE_CHECKING:
    from pydantic_core import core_schema


class UUIDString(str):
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        if not args:
            UUID("")
        if isinstance(args[0], UUID):
            args = (str(args[0]), *args[1:])
        string = super().__new__(cls, *args, **kwargs)
        UUID(string)
        return string

    @property
    def _uuid(self) -> UUID:
        return UUID(self)

    @property
    def bytes_le(self) -> bytes:
        return self._uuid.bytes_le

    @property
    def bytes(self) -> bytes:
        return self._uuid.bytes

    @property
    def fields(self) -> tuple[int, int, int, int, int, int]:
        return self._uuid.fields

    @property
    def time_low(self) -> int:
        return self._uuid.time_low

    @property
    def time_mid(self) -> int:
        return self._uuid.time_mid

    @property
    def time_hi_version(self) -> int:
        return self._uuid.time_hi_version

    @property
    def clock_seq_hi_variant(self) -> int:
        return self._uuid.clock_seq_hi_variant

    @property
    def clock_seq_low(self) -> int:
        return self._uuid.clock_seq_low

    @property
    def time(self) -> int:
        return self._uuid.time

    @property
    def clock_seq(self) -> int:
        return self._uuid.clock_seq

    @property
    def node(self) -> int:
        return self._uuid.node

    @property
    def hex(self) -> str:
        return self._uuid.hex

    @property
    def urn(self) -> str:
        return self._uuid.urn

    @property
    def variant(self) -> str:
        return self._uuid.variant

    @property
    def version(self) -> Optional[int]:
        return self._uuid.version

    @property
    def is_safe(self) -> SafeUUID:
        return self._uuid.is_safe

    def __int__(self) -> int:
        return self._uuid.int

    @property
    def int(self) -> int:
        return self._uuid.int

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: object, _handler: object
    ) -> "core_schema.CoreSchema":
        from pydantic_core import core_schema

        def validate(value: object) -> UUIDString:
            if isinstance(value, UUID):
                value = str(value)
            return cls(value)

        return core_schema.no_info_after_validator_function(
            validate,
            core_schema.union_schema(
                [
                    core_schema.str_schema(),
                    core_schema.uuid_schema(),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance),
                return_schema=core_schema.str_schema(),
            ),
        )


__all__ = [
    "UUIDString",
]
