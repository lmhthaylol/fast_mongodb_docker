from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from typing import Optional, List
from bson import ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]


class Book(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(..., description="Tiêu đề sách")
    author: str = Field(..., description="Tác giả sách")
    year: int = Field(..., description="Năm xuất bản", gt=1000, le=2100)
    is_borrowed: bool = Field(default=False, description="Trạng thái mượn sách (Mặc định: False)")


    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Tâm lý học về tiền",
                "author": "Morgan Housel",
                "year": 2020,
                "is_borrowed": False,
            }
        },
    )


class UpdateBook(BaseModel):

    title: Optional[str] = Field(None, description="Tiêu đề sách")
    author: Optional[str] = Field(None, description="Tác giả sách")
    year: Optional[int] = Field(None, description="Năm xuất bản", gt=1000, le=2100)
    is_borrowed: Optional[bool] = Field(None, description="Trạng thái mượn sách")


    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Tư duy nhanh và chậm",
                "is_borrowed": True,
            }
        },
    )
