from fastapi import APIRouter

from ..constants import QUADRANTS

router = APIRouter(prefix="/api", tags=["meta"])


@router.get("/quadrants")
def get_quadrants():
    """Public: the four quadrants and their fixed subject lists, for the signup form."""
    return QUADRANTS
