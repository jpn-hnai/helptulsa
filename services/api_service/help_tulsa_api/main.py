from fastapi import FastAPI
from .routes import router

app = FastAPI(title="HelpTulsa API")
app.include_router(router)

def main():
    import uvicorn
    uvicorn.run("help_tulsa_api.main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
