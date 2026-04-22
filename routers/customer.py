from fastapi import APIRouter, Depends
from models.user import User, RoleEnum
from core.auth import require_role

router = APIRouter()

@router.get("/dashboard")
def customer_dashboard(user: User = Depends(require_role(RoleEnum.customer))):
    return {"msg": "Welcome customer"}