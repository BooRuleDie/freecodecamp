from fastapi import APIRouter

router = APIRouter(
    prefix="/easterEgg",
    tags=["Easter Egg"]
)

@router.get("/easteregg")
def easter_egg():
    return "Easter Egg, codebase changed"