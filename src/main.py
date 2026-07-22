
from fastapi import FastAPI

from routers.user import router as user_router
from routers.transaction import router as trans_router
from routers.analytics import router as anal_router
from schemas.user import *
from schemas.enums import *
from schemas.transaction import *


app = FastAPI()
app.include_router(user_router)
app.include_router(trans_router)
app.include_router(anal_router)



# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=7999, reload=True)
