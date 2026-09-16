from pydantic import BaseModel, Field, field_validator


class WebsiteRuleCreate(BaseModel):
    domain: str = Field(min_length=3, max_length=255)
    action: str

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, value: str) -> str:
        value = value.strip().lower()

        if not value:
            raise ValueError("Domain cannot be empty")

        return value

    @field_validator("action")
    @classmethod
    def validate_action(cls, value: str) -> str:
        value = value.strip().upper()

        if value not in {"ALLOW", "BLOCK"}:
            raise ValueError("Action must be ALLOW or BLOCK")

        return value


class UserWebsiteRuleCreate(BaseModel):
    user_id: int
    website_rule_id: int
    action: str

    @field_validator("action")
    @classmethod
    def validate_action(cls, value: str) -> str:
        value = value.strip().upper()

        if value not in {"ALLOW", "BLOCK"}:
            raise ValueError("Action must be ALLOW or BLOCK")

        return value

class WebsiteRuleUpdate(BaseModel):
    action:str
    
    @field_validator("action")
    @classmethod
    def validate_action(cls, value):
        value = value.strip().upper()

        if value not in {"ALLOW", "BLOCK"}:
            raise ValueError("Action must be ALLOW or BLOCK")

        return value