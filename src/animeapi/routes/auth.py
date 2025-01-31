from fastapi import APIRouter, Request, Depends
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from starlette import status
from animeapi.logger import logger

from animeapi.models import (
    User,
    UserCreate,
    UserLogin,
    Favorite,
    FavoriteCreate,
    PlayHistory,
    PlayHistoryCreate,
)
from animeapi.database import get_connection
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/apis/login")
async def login_user(
        request: Request, user_data: UserLogin, conn=Depends(get_connection)
):
    # 用户登录逻辑
    query = "SELECT username, password FROM users WHERE username = $1"

    result = await conn.fetchrow(query, user_data.username)
    if result is None:
        return {"message": "Invalid username or password"}

    username, hashed_password = result["username"], result["password"]
    logger.info(f'db exist user, username: {username}, hashed_password: {hashed_password}')
    if not pwd_context.verify(user_data.password, hashed_password):
        return {"message": "Invalid username or password"}

    # 设置登录会话
    request.session["username"] = username
    logger.info("set session", extra={"username": username})

    # 重定向到主页
    return RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)


@router.post("/apis/register")
async def register_user(user_data: UserCreate, conn=Depends(get_connection)):
    # 用户注册逻辑
    hashed_password = pwd_context.hash(user_data.password)
    query = "INSERT INTO users (username, password) VALUES ($1, $2)"
    await conn.execute(query, user_data.username, hashed_password)
    return {"message": "User registered successfully"}


@router.get("/home")
async def home_page(request: Request):
    # 主页逻辑
    username = request.session.get("username")
    if username is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("home.html", {"request": request, "username": username})


@router.post("/apis/users/{user_id}/favorites")
async def create_favorite(
        user_id: int, favorite_data: FavoriteCreate, conn=Depends(get_connection)
):
    # 创建收藏的逻辑
    query = "INSERT INTO favorites (user_id, anime_id) VALUES ($1, $2)"
    await conn.execute(query, user_id, favorite_data.anime_id)
    return {"message": "Favorite created successfully"}


@router.get("/apis/users/{user_id}/favorites")
async def get_favorites(user_id: int, conn=Depends(get_connection)):
    # 获取用户收藏的逻辑
    query = "SELECT * FROM favorites WHERE user_id = $1"
    results = await conn.fetch(query, user_id)
    favorites = [Favorite(**result).dict() for result in results]
    return favorites


@router.post("/apis/users/{user_id}/play_history")
async def create_play_history(
        user_id: int, play_history_data: PlayHistoryCreate, conn=Depends(get_connection)
):
    # 创建播放记录的逻辑
    query = "INSERT INTO play_history (user_id, anime_id) VALUES ($1, $2)"
    await conn.execute(query, user_id, play_history_data.anime_id)
    return {"message": "Play history created successfully"}


@router.get("/apis/users/{user_id}/play_history")
async def get_play_history(user_id: int, conn=Depends(get_connection)):
    # 获取用户播放记录的逻辑
    query = "SELECT * FROM play_history WHERE user_id = $1"
    results = await conn.fetch(query, user_id)
    play_history = [PlayHistory(**result).dict() for result in results]
    return play_history


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
