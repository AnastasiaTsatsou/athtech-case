import datetime
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from datetime import date
from enum import Enum
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Database connection
DATABASE_URL = "mysql+pymysql://root:root@db:3306/expensesdb"
engine = create_engine(DATABASE_URL, echo=True)


class CategoryEnum(str, Enum):
    FOOD = "food"
    ENTERTAINMENT = "entertainment"
    TRANSPORT = "transport"
    HEALTH = "health"
    OTHER = "other"


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, max_length=225)
    description: str | None = Field(default=None, max_length=400)
    amount: float = Field(gt=0)
    expense_date: date | None = Field(default=datetime.date.today())
    category: CategoryEnum = Field(default=CategoryEnum.OTHER)


app = FastAPI()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}
