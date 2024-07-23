import uvicorn
import src.main

if __name__ == "__main__":
    # If you need, you can add params for setup site (host, port)
    # More about a FastAPI deployment:
    # https://fastapi.tiangolo.com/deployment/manually/
    uvicorn.run('src.main:app')
