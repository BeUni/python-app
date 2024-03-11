import typing as t
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated

import utils
from mydatabase import MyDatabase
from pydantic import BaseModel
from sections import loginUser, categories, store, products
from starlette import status

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

import secrets

app = FastAPI()
# oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='token', tokenUrl='token')
# Placeholder for a database containing valid token values
known_tokens = {"scmsdn csdncnsdc"}
# We will handle a missing token ourselves
get_bearer_token = HTTPBearer(auto_error=False)

security = HTTPBasic()


class UnauthorizedMessage(BaseModel):
    detail: str = "Bearer token missing or unknown"


async def get_token(
        auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    # Simulate a database query to find a known token
    print(auth.credentials)
    authorization = utils.verify_token_access(auth.credentials)
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )
    return authorization


@app.on_event("startup")
def startup_db_client():
    app.mydb = MyDatabase.instance()
    app.mongodb_client = app.mydb.client
    app.database = app.mydb.db
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    MyDatabase.instance().close_db()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "sharma@619Shivam")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# @app.get("/docs")
# async def get_documentation(username: str = Depends(get_current_username)):
#     return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.post('/api/v1/store/create_user')
async def create_user_store(store_user_request: loginUser.StoreUserRequest):
    return loginUser.create_store_user(store_user_request)


@app.post('/api/v1/store/create_password')
async def create_user_store_password(create_password: loginUser.CreatePasswordStoreUser,
                                     token: dict = Depends(get_token)):
    return loginUser.create_password_store_user(create_password, email=token.get('email'))


@app.post('/api/v1/store/login')
async def login(login_request: loginUser.LoginRequest, ):
    return loginUser.verify_user(login_request)


@app.post('/api/v1/store/add_store')
async def create_store(store_request: store.StoreRequest, token: dict = Depends(get_token)):
    return store.add_store(store_request, email=token.get('email'))


@app.post('/api/v1/categories/create')
async def create_category(items: categories.CategoriesRequest, token: dict = Depends(get_token)):
    return categories.add_categories(category_request=items)


@app.post('/api/v1/product/add_item')
async def add_product(items: products.ProductRequest, token: dict = Depends(get_token), ):
    return products.add_product(product_request=items)


@app.get('/api/v1/get_product_category')
async def get_product_category_info(token: dict = Depends(get_token)):
    return products.get_product_category_info()
