from fastapi import HTTPException, status, Response, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db_connection as get_db
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas, models
from app.config import setting
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = f"{setting.secret_key}"
ALGORITHM = f"{setting.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


def create_access_token(details: dict):
    to_encode = details.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # print(datetime.utcnow().timestamp(), expire)
    generated_jwt_token = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM, )
    # print(generated_jwt_token)
    return generated_jwt_token


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print("Token is still valid and active")
        uid: int = payload.get("user_id")
        # expire = payload.get("exp")
        if uid is None:
            raise credential_exception
        # elif expire is None:
        #     raise credential_exception
        # elif datetime.now() > datetime.fromtimestamp(expire):
        #     raise credential_exception
        token_data = schemas.TokenData(id=uid)
    except jwt.ExpiredSignatureError:
        print("Token expired. Get new one")
        raise credential_exception
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not validate credential",
                                         headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credential_exception)
    result = db.query(models.User).filter(models.User.id == token_data.id).first()
    return result
