from pydantic import BaseModel, ConfigDict, Field, field_validator # Field ve field_validator import edildi


class UserCreate(BaseModel):
    email: str
    # Maximum length set due to bcrypt's 72-byte limitation.
    # Some characters in UTF-8 can take multiple bytes.
    # Therefore, we check the byte limit alongside the character limit.
    password: str = Field(
        min_length=8, max_length=60, description="Password must be between 8 and 60 characters."
    )

    @field_validator("password")
    @classmethod
    def password_byte_length(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password is too long (byte limit exceeded).")
        return v


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str