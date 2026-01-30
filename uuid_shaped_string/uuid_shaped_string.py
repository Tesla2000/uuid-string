from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from pydantic_core import core_schema


class UUIDShapedString(str):
    def __new__(cls, *args, **kwargs):
        if not args:
            UUID("")
        if isinstance(args[0], UUID):
            args = (str(args[0]), *args[1:])
        string = super().__new__(cls, *args, **kwargs)
        UUID(string)
        return string

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type, _handler
    ) -> "core_schema.CoreSchema":
        from pydantic_core import core_schema

        def validate(value):
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
