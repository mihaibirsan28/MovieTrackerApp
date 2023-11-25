from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import database.deps as deps
from display_messages import INVALID_ACCOUNT_CONFIRMATION_MESSAGE, EXPIRED_ACCOUNT_CONFIRMATION_LINK, \
    ACCOUNT_ALREADY_CONFIRMED_MESSAGE, ACCOUNT_CONFIRMED_SUCCESSFULLY_MESSAGE
from starlette import status
from models import User, Link
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from secrets import SECRET_KEY, ALGORITHM, HOST
from email_sender import send_account_confirmation_email

from hashlib import md5
from enums import LinkType
from request_models import CreateUserRequest, LoginRequest
from response_models import AuthToken

from validations import validate_create_user_request

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        background_tasks: BackgroundTasks, create_user_request: CreateUserRequest, db: Session = Depends(deps.get_db)):
    if get_user_by_email_or_username(create_user_request.email, create_user_request.username, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email or username already taken')
    errors = validate_create_user_request(create_user_request)
    if errors:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=errors)
    user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        is_confirmed=False,
        password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(user_model)
    db.commit()
    confirmation_link = generate_account_confirmation_link(user_model, db)
    send_account_confirmation_email(background_tasks, user_model, confirmation_link)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(deps.get_db)):
    user: User = login_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials')
    if not user.is_confirmed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Your account has not been confirmed yet!')
    jwt_token = create_access_token(user.username, user.email, user.id, timedelta(hours=1))
    # refresh_token = create_access_token(user.username, user.email, user.id, timedelta(hours=24))
    return {'access_token': jwt_token, 'token_type': 'bearer'}


@router.post("/confirm/{link_token}", status_code=status.HTTP_200_OK)
async def confirm_account(link_token: str, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)):
    invalid_token_exception = \
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                      detail=INVALID_ACCOUNT_CONFIRMATION_MESSAGE)
    print(link_token)
    if not link_token:
        raise invalid_token_exception
    link: Link
    link = db.query(Link).filter(Link.link_token == link_token).first()
    print("db_link:" + str(link))
    if not link:
        raise invalid_token_exception

    if link.link_type != LinkType.ACCOUNT_CONFIRMATION.name:
        raise invalid_token_exception
    user: User = link.user
    print("user:" + str(user))
    if not user:
        raise invalid_token_exception
    if link.expiry_date < datetime.utcnow():
        new_token = generate_account_confirmation_link(user, db)
        send_account_confirmation_email(background_tasks, user, new_token)
        return EXPIRED_ACCOUNT_CONFIRMATION_LINK
    if user.is_confirmed:
        db.delete(link)
        db.commit()
        return ACCOUNT_ALREADY_CONFIRMED_MESSAGE
    if not user.is_confirmed:
        user.is_confirmed = True
        db.delete(link)
        db.commit()
        return ACCOUNT_CONFIRMED_SUCCESSFULLY_MESSAGE


'''
@router.get("/refresh", status_code=status.HTTP_200_OK, response_model=AuthToken)
async def refresh_access_token(db: db_dependency):
'''


def create_access_token(username: str, email: str, user_id: int, expires_delta: timedelta):
    expiration = datetime.utcnow() + expires_delta
    encode = {'sub': username, 'id': user_id, 'email': email, 'exp': expiration}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def login_user(username: str, password: str, db):
    user = db.query(User).filter((User.username == username) | (User.email == username)).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(deps.oauth2_bearer), db: Session = Depends(deps.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        email: str = payload.get('email')
        if username is None or user_id is None or email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        current_user: User = get_user_by_email_or_username(email, username, db)
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return current_user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


def get_user_by_email_or_username(email: str, username: str, db: Session = Depends(deps.get_db)):
    user: User = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if not user:
        return False
    return user


def generate_account_confirmation_link(user: User, db: Session = Depends(deps.get_db)):
    link_token = generate_link_token(user)
    expiry_date = datetime.utcnow() + timedelta(days=1)
    link = Link(user_id=user.id,
                link_token=link_token,
                link_type=LinkType.ACCOUNT_CONFIRMATION.name,
                expiry_date=expiry_date,
                user=user)
    db.add(link)
    db.commit()
    return f'{HOST}/auth/confirm/{link_token}'


def generate_link_token(user: User):
    token: str = user.email + user.username + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    link_token = md5(token.encode('utf-8')).hexdigest()
    return link_token


def get_forbidden_exception():
    return HTTPException(status_code=403, detail="You don't have enough acess rights")
