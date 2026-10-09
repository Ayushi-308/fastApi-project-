from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import get_db

from auth.models import (
    User,
    Role
)

from auth.schemas import (
    UserCreate,
    LoginRequest,
    UserResponse,
    Token
)

from auth.auth import (
    hash_password,
    verify_password,
    create_access_token
)

from auth.dependencies import (
    get_current_user,
    require_permission
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# REGISTER
# =========================================================

@router.post(
    "/register",
    response_model=UserResponse
)
def register(

    user_data: UserCreate,

    db: Session = Depends(get_db)
):

    # Check username

    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check email

    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Get student role

    student_role = db.query(Role).filter(
        Role.name == "student"
    ).first()

    if student_role is None:

        raise HTTPException(
            status_code=500,
            detail="Student role not found"
        )

    # Hash password

    hashed_password = hash_password(
        user_data.password
    )

    # Create user

    new_user = User(

        username=user_data.username,

        email=user_data.email,

        password=hashed_password,

        role_id=student_role.id
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=Token
)
def login(

    login_data: LoginRequest,

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == login_data.username
    ).first()

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_correct = verify_password(

        login_data.password,

        user.password
    )

    if not password_correct:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        user.id
    )

    return {

        "access_token": token,

        "token_type": "bearer"
    }


# =========================================================
# GET CURRENT USER
# =========================================================

@router.get(
    "/me"
)
def get_me(

    current_user: User = Depends(
        get_current_user
    )
):

    return {

        "id": current_user.id,

        "username": current_user.username,

        "email": current_user.email,

        "role": current_user.role.name
    }


# =========================================================
# MAKE USER ADMIN
# =========================================================

@router.put(
    "/users/{user_id}/make-admin"
)
def make_user_admin(

    user_id: int,

    current_user: User = Depends(
        require_permission("manage_admin")
    ),

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    admin_role = db.query(Role).filter(
        Role.name == "admin"
    ).first()

    if admin_role is None:

        raise HTTPException(
            status_code=500,
            detail="Admin role not found"
        )

    user.role_id = admin_role.id

    db.commit()

    db.refresh(user)

    return {

        "message": "User is now an admin",

        "user_id": user.id,

        "username": user.username,

        "role": user.role.name
    }


# =========================================================
# REMOVE ADMIN
# =========================================================

@router.put(
    "/users/{user_id}/remove-admin"
)
def remove_admin(

    user_id: int,

    current_user: User = Depends(
        require_permission("manage_admin")
    ),

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.id == current_user.id:

        raise HTTPException(
            status_code=400,
            detail="You cannot remove your own access"
        )

    student_role = db.query(Role).filter(
        Role.name == "student"
    ).first()

    if student_role is None:

        raise HTTPException(
            status_code=500,
            detail="Student role not found"
        )

    user.role_id = student_role.id

    db.commit()

    db.refresh(user)

    return {

        "message": "Admin access removed",

        "user_id": user.id,

        "username": user.username,

        "role": user.role.name
    }