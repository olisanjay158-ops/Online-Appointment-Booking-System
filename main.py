from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for e in exc.errors():
        field = ".".join(str(x) for x in e.get("loc", []) if x != "body")
        errors.append({"field": field, "message": e.get("msg")})
    return JSONResponse(status_code=400, content={"errors": errors})
class User(BaseModel):
    name: str
    email: EmailStr
    age: int

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("age")
    @classmethod
    def age_valid(cls, v: int):
        if v < 0 or v > 120:
            raise ValueError("Age must be between 0 and 120")
        return v

@app.get("/")
def read_root():
    return {"message": "Backend running successfully"}

@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "user": user
    }