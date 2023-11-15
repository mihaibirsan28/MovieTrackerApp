from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    first_name: str
    last_name: str
