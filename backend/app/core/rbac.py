from fastapi import Depends, HTTPException
from .security import get_current_user
from ..config.constants import RESEARCHER_LIKE_ROLES, ROLE_REVIEWER

class Roles:
    @staticmethod
    def researcher_like():
        return RESEARCHER_LIKE_ROLES

def require_role(allowed: set):
    def dep(user=Depends(get_current_user)):
        if user.role not in allowed:
            raise HTTPException(status_code=403, detail="Forbidden for your role")
        return user
    return dep
