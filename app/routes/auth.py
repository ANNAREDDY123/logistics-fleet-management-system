from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from jose import jwt

from passlib.context import CryptContext

from sqlalchemy.orm import Session

from database import get_db

from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from models import User

from schemas import UserCreate


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



# PASSWORD HASHING


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# JWT TOKEN


def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# REGISTER


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    new_user = User(

        full_name=user.full_name,

        email=user.email,

        password=hash_password(
            user.password
        ),

        phone=user.phone,

        role=user.role

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {

        "message": "User registered successfully.",

        "user_id": new_user.id

    }



# LOGIN


@router.post("/login")
def login_user(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(

        User.email == form_data.username

    ).first()

    if not user:

        raise HTTPException(

            status_code=401,

            detail="Invalid email."

        )

    if not verify_password(

        form_data.password,

        user.password

    ):

        raise HTTPException(

            status_code=401,

            detail="Invalid password."

        )

    access_token = create_access_token(

        data={

            "sub": user.email,

            "role": user.role

        }

    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }


# CURRENT USER


def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )

        email = payload.get("sub")

        if email is None:

            raise HTTPException(

                status_code=401,

                detail="Invalid token."

            )

    except Exception:

        raise HTTPException(

            status_code=401,

            detail="Invalid or expired token."

        )

    user = db.query(User).filter(

        User.email == email

    ).first()

    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found."

        )

    return user



# ROLE AUTHORIZATION


def role_required(
    allowed_roles: list
):

    def verify_role(

        current_user: User = Depends(
            get_current_user
        )

    ):

        if current_user.role not in allowed_roles:

            raise HTTPException(

                status_code=403,

                detail="Access denied."

            )

        return current_user

    return verify_role



# GET CURRENT USER


@router.get("/me")
def get_logged_in_user(

    current_user: User = Depends(
        get_current_user
    )

):

    return {

        "id": current_user.id,

        "full_name": current_user.full_name,

        "email": current_user.email,

        "phone": current_user.phone,

        "role": current_user.role,

        "is_verified": current_user.is_verified

    }
