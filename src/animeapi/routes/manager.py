from fastapi import APIRouter, Depends
from animeapi.database import get_connection


router = APIRouter()

##async def add_anime(anime_url: str, conn=Depends(get_connection)):
#添加至数据库

#@router.delete("/apis/delete/{anime_id}")
#def delete(anime_id: int, conn=Depends(get_connection)):
#去数据库删除链接
