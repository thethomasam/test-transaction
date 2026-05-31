from fastapi import FastAPI

app = FastAPI()


@app.get("/transaction")
def get_transaction():
    return {"message": "Transaction endpoint", "status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
