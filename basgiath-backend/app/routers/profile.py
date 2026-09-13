from fastapi import APIRouter, Depends

from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/api", tags=["profile"])


@router.get("/me", response_model=schemas.UserOut)
def read_profile(current_user: models.User = Depends(get_current_user)):
    return current_user
