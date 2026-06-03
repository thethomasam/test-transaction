from datetime import date as date_type

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Transaction

# Create tables on startup. For real migrations, use Alembic instead.
Base.metadata.create_all(bind=engine)

app = FastAPI()


class TransactionIn(BaseModel):
    amount: float
    merchant: str
    date: date_type
    card: str  # last 4 digits only — never store a full card number
    description: str = ""


class TransactionOut(TransactionIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


@app.get("/transaction", response_model=list[TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()


@app.post("/transaction", response_model=TransactionOut, status_code=201)
def add_transaction(payload: TransactionIn, db: Session = Depends(get_db)):
    transaction = Transaction(**payload.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@app.get("/transaction/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.get(Transaction, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
