from pydantic import BaseModel, EmailStr, field_validator, ValidationError


class SignupData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str = ""
    age: int
    country: str = ""

    @field_validator("first_name", "last_name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("This field cannot be empty")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("age")
    @classmethod
    def valid_age(cls, v: int) -> int:
        if v < 1 or v > 120:
            raise ValueError("Age must be between 1 and 120")
        return v


def format_validation_error(exc: ValidationError) -> str:
    """Turn Pydantic's error list into one readable line per field."""
    messages = []
    for err in exc.errors():
        field = err["loc"][0]
        msg = err["msg"]
        messages.append(f"{field.replace('_', ' ').title()}: {msg}")
    return " | ".join(messages)