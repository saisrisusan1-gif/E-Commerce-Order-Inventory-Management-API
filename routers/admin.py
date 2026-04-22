from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db_connection import get_db
from models.user import User, RoleEnum
from core.auth import get_current_user, require_role

router = APIRouter()

@router.get("/dashboard")
def admin_dashboard(user: User = Depends(require_role(RoleEnum.admin))):
    return {"msg": "Welcome admin"}


@router.put("/make-admin/{user_id}")
def make_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin))  # 🔥 enforce admin
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == RoleEnum.admin:
        return {"msg": "User is already admin"}

    user.role = RoleEnum.admin
    db.commit()

    return {"msg": "User promoted to admin"}