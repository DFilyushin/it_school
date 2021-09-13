import uvicorn
from sapp.main_application import app


if __name__ == '__main__':
    uvicorn.run(app, port=80)
