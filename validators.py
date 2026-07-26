from pydantic import BaseModel, EmailStr, field_validator, ValidationError
import re


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

    @field_validator("phone")
    @classmethod
    def valid_phone(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Phone number is required")
        # allows optional leading +, then 7-15 digits (spaces/dashes stripped before checking)
        cleaned = re.sub(r"[\s\-]", "", v)
        if not re.fullmatch(r"\+?\d{7,15}", cleaned):
            raise ValueError("Enter a valid phone number (digits only, optional +)")
        return v

    @field_validator("age")
    @classmethod
    def valid_age(cls, v: int) -> int:
        if v < 18 or v > 120:
            raise ValueError("Age must be between 18 and 120")
        return v


def format_validation_error(exc: ValidationError) -> str:
    messages = []
    for err in exc.errors():
        field = err["loc"][0]
        msg = err["msg"]
        messages.append(f"{field.replace('_', ' ').title()}: {msg}")
    return " | ".join(messages)