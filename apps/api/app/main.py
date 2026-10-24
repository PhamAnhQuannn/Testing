from fastapi import FastAPI

app = FastAPI(title="Prep App API")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
