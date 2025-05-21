import datetime
import time
from typing import Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from enum import Enum
from sqlmodel import Field, Session, SQLModel, create_engine, select
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Database connection
DATABASE_URL = "mysql+pymysql://root:root@db:3306/expensesdb"
engine = create_engine(DATABASE_URL, echo=True)

# Create metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests Count", ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP Request Latency", ["method", "endpoint"]
)

DB_QUERY_COUNT = Counter("db_query_count_total", "Total Database Query Count")


class CategoryEnum(str, Enum):
    food = "food"
    entertainment = "entertainment"
    transport = "transport"
    health = "health"
    other = "other"


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, max_length=225)
    description: Optional[str] = Field(default=None, max_length=400)
    amount: float = Field(gt=0)
    date: Optional[datetime.date] = Field(default_factory=datetime.date.today)
    category: CategoryEnum = Field(default=CategoryEnum.other)


class ExpenseCreate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=225)
    description: Optional[str] = Field(default=None, max_length=400)
    amount: float = Field(gt=0)
    date: Optional[datetime.date] = Field(default_factory=datetime.date.today)
    category: CategoryEnum = Field(default=CategoryEnum.other)


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


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to track request metrics."""
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(
        latency
    )
    REQUEST_COUNT.labels(
        method=request.method, endpoint=request.url.path, status=response.status_code
    ).inc()

    return response


@app.middleware("http")
async def db_metrics_middleware(request: Request, call_next):
    if request.url.path.startswith("/expenses") or request.url.path.startswith(
        "/categories"
    ):
        DB_QUERY_COUNT.inc()

    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/expenses/")
def read_expenses(
    session: SessionDep, category: CategoryEnum | None = None
) -> list[Expense]:
    if category:
        expenses = session.exec(
            select(Expense).where(Expense.category == category)
        ).all()
    else:
        expenses = session.exec(select(Expense)).all()
    return expenses


@app.get("/expenses/{expense_id}")
def read_expense(expense_id: int, session: SessionDep) -> Expense:
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.post("/expenses/")
def create_expense(expense: ExpenseCreate, session: SessionDep) -> Expense:
    db_expense = Expense.model_validate(expense)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense


@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int, expense: ExpenseCreate, session: SessionDep
) -> Expense:
    db_expense = session.get(Expense, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense_data = expense.model_dump(exclude_unset=True)
    for key, value in expense_data.items():
        setattr(db_expense, key, value)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, session: SessionDep) -> dict:
    db_expense = session.get(Expense, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    session.delete(db_expense)
    session.commit()
    return {"message": "Expense deleted successfully"}
