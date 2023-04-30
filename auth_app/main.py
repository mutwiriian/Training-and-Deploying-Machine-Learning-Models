import codecs
import json
import logging
from datetime import datetime
from random import randint, random
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", scheme_name="Bearer")


class User(BaseModel):
    full_name: str
    visit_time: datetime


class AuthToken(BaseModel):
    token: str


class ModelPrediction(BaseModel):
    rsquare: float
    accuracy: float
    confidence: float
    value: int


@app.get(
    "/generate-token/",
    summary="Generate user authentication token given their full name.",
    response_model=AuthToken,
)
async def generate_user_token(full_name: str):
    """
    Use this endpoint to create authentication tokens for users.

    Params:
    - full_name: string type path parameter specifiying user's full name.

    How it works:
    - The endpoint takes user's full name as a path parameter
    - Using python's codec library, input full name is encoded to equivalent hex-code
    - Resulting hex-code is saved on a json file (out temp data-store) and returned as request response
    """
    hex_code = codecs.encode(full_name.encode(encoding="ascii"), encoding="hex").decode(
        encoding="utf-8"
    )
    with open("auth-tokens.json", "w+") as tf:
        try:
            tokens = json.loads(tf.read())
        except Exception:
            tf.write(json.dumps([hex_code]))
        else:
            tokens = tokens + [hex_code]
            tf.write(json.dumps(tokens))
    return AuthToken(token=hex_code)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Helper function for checking existence of user token in our data store (json file)."""
    with open("auth-tokens.json", "r") as tf:
        try:
            tokens = json.loads(tf.read())
        except Exception as err:
            logging.error(err)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user authentication system is under maintenance, Try again later.",
            )
        else:
            # check if token provided matches any of the tokens in our data-store
            user_found = [hex_code for hex_code in tokens if hex_code == token]
            # if length of tokens that match is zero, the user does not exist.
            # otherwise, if we have matching hex-code, decode the token and return user's full name and visit time
            if len(user_found):
                full_name = codecs.decode(token, encoding="hex").decode(
                    encoding="utf-8"
                )
                return User(full_name=full_name, visit_time=datetime.now())
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found."
    )


@app.get("/users/me/", summary="Get details of logged-in user", response_model=User)
async def authenticate_user(user: Annotated[User, Depends(get_current_user)]):
    """Retrive details of currently logged-in user.

    This endpoint require authentication code provided through Bearer header content.
    """
    return user


@app.get(
    "/model/predict/",
    summary="Get simulation model prediction results",
    response_model=ModelPrediction,
)
async def get_model_prediction(user: Annotated[User, Depends(get_current_user)]):
    """Simulates execution of model and returns sample model outputs"""
    return ModelPrediction(
        rsquare=random(), accuracy=random(), confidence=random(), value=randint(10, 20)
    )
