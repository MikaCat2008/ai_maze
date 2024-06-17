from __future__ import annotations

from typing import Any, Type, Union, TypeVar, Optional, GenericAlias

T = TypeVar("T")


class Field:
    name: Optional[str]
    alias: Optional[GenericAlias]
    hidden: bool

    def __init__(self, hidden=False) -> None:
        self.name = None
        self.alias = None
        self.hidden = hidden

    def __repr__(self) -> str:
        return f"Field({self.name} : {self.alias})"


class Model:
    fields: list[Field]
    models: dict[str, type[Model]] = {}

    def __init_subclass__(cls) -> None:
        cls.fields = []
        cls.models[cls.__name__] = cls

        for key, value in list(cls.__dict__.items()):
            if isinstance(value, Field):
                value.name = key
                value.alias = cls.__annotations__[key]
                cls.fields.append(value)
                delattr(cls, key)

    def __init__(self, **kwds: Any) -> None:
        for field in self.fields:
            value = kwds.get(field.name)

            setattr(self, field.name, self.validate_alias(value, field.alias))

    def to_json(self) -> dict:
        data = {}
        
        for field in self.fields:
            value = getattr(self, field.name)

            if isinstance(value, Model):
                data[field.name] = value.to_json()
            elif isinstance(value, list):
                data[field.name] = [item.to_json() for item in value]
            elif value is not None:
                data[field.name] = value

        return data

    def validate_alias(self, data: Any, alias: GenericAlias | str) -> Any:
        if data is None or isinstance(data, Model):
            return data

        if isinstance(alias, str):
            alias = eval(alias, Model.models)

        args = getattr(alias, "__args__", None)
        origin = getattr(alias, "__origin__", None)

        if origin is Union and isinstance(None, args[1]):
            return self.validate_alias(data, args[0])
        elif Model in alias.__mro__:
            model = alias.__mro__[0]

            return model(**data)
        elif origin in (None, dict):
            return data
        elif origin is list:
            return [self.validate_alias(item, args[0]) for item in data]


    def validate_model(self, data: Any, model: Type[Model]) -> Model:
        method_returning = model.__orig_bases__[0].__args__[0]

        return self.validate_alias(data, method_returning)

    def __repr__(self) -> str:
        fields = {}

        for field in self.fields:
            if field.hidden:
                continue

            value = getattr(self, field.name, None)

            if value is not None:
                fields[field.name] = value

        return f"{self.__class__.__name__}({' '.join(f'{k}={v}' for k, v in fields.items())})"

    @classmethod
    def set_api(cls, api) -> None:
        cls.api = api
