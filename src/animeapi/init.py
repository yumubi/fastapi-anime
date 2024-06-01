import asyncio
import asyncpg
import os
import yaml

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "../config.yaml")
config = yaml.safe_load(open(config_path))


async def create_tables():
    conn = await asyncpg.connect(
        host=config["database"]["host"],
        port=config["database"]["port"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        database=config["database"]["database"],
    )

    # # 创建动漫数据表
    # await conn.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS anime (
    #         id SERIAL PRIMARY KEY,
    #         type VARCHAR(255),
    #         description TEXT,
    #         status VARCHAR(255),
    #         playback_link VARCHAR(255)
    #     )
    #     """
    # )
    #
    # # 创建用户数据表
    # await conn.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS users (
    #         id SERIAL PRIMARY KEY,
    #         username VARCHAR(255),
    #         password VARCHAR(255)
    #     )
    #     """
    # )

    # 创建动漫评论postgres数据表
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            user_id INT,
            anime_id INT,
            comment TEXT
        )
        """
    )

    # 创建动漫评分postgres数据表
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            id SERIAL PRIMARY KEY,
            user_id INT,
            anime_id INT,
            rating FLOAT
        )
        """
    )

    # 创建用户收藏postgres数据表
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS favorites (
            id SERIAL PRIMARY KEY,
            user_id INT,
            anime_id INT
        )
        """
    )

    # 创建用户播放历史postgres数据表
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS play_history (
            id SERIAL PRIMARY KEY,
            user_id INT,
            anime_id INT
        )
        """
    )

    await conn.close()


asyncio.run(create_tables())
print("finish")
