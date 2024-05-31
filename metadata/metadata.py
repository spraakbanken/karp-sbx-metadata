from typing import Dict, List, Literal, Optional, Self

import pydantic


class BaseModel(pydantic.BaseModel):
    model_config = {
        "frozen": True,
        "extra": "forbid",
    }


class MultiLang(BaseModel):
    eng: Optional[str] = None
    swe: Optional[str] = None

    @pydantic.model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.eng is None and self.swe is None:
            raise ValueError("at least one language must be given")
        return self


class Download(BaseModel):
    url: str
    type: str = "lexicon"
    format: str = "jsonl"
    info: str | None
    licence: str = "CC BY 4.0"
    restriction: str | None = "attribution"


class Interface(BaseModel):
    access: str = "https://spraakbanken.gu.se/karp?resource="
    licence: str = "CC BY 4.0"
    restriction: str = "attribution"


class Affiliation(BaseModel):
    organisation: str = "Språkbanken"
    email: str = "sb-info@svenska.gu.se"


class ContactInfo(BaseModel):
    name: str = "Markus Forsberg"
    email: str = "sb-info@svenska.gu.se"
    affiliation: Affiliation


class Metadata(BaseModel):
    name: str | MultiLang
    short_description: str | MultiLang
    type: str = Literal["lexicon"]
    trainingdata: bool | None
    unlisted: bool | None
    successors: List[str] | None
    language_codes: List[str]
    size: int
    in_collections: List[str] = None
    downloads: List[Download] = None
    interface: List[Interface] = None
    contact_info: ContactInfo
    annotation: Optional[str | MultiLang] = None
    keywords: Optional[List[str]] = None
    caveats: Optional[str | MultiLang] = None
    references: Optional[List[str]] = None
    intended_uses: Optional[str | MultiLang] = None
    description: Optional[str | MultiLang] = None

    @pydantic.field_serializer("size")
    def serialize_size(entries: int):
        return {"entries": entries}

    @pydantic.field_validator(
        "name",
        "short_description",
        "annotation",
        "caveats",
        "intended_uses",
        "description",
    )
    def enforce_multilang(field: str | MultiLang) -> MultiLang:
        if isinstance(field, str):
            return MultiLang(swe=str, eng=str)
        return field

    @pydantic.field_validator("size", mode="before")
    @classmethod
    def unwrap_size(cls, v: Dict[str, int]) -> int:
        return v["entries"]


def create() -> Dict:
    metadata = Metadata()
    # mode="json" makes model_dump behave as model_dump_json, but without actually creating JSON (our target is YAML)
    return metadata.model_dump(mode="json")
