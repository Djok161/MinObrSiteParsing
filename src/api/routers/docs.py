import os

import pandas as pd
from fastapi import APIRouter

from core.database.site import SiteDB
from core.services.redis_client import get_redis

router = APIRouter(
    tags=['Docs'],
    prefix="/doc",
)

r = get_redis(0)
site_db = SiteDB()


@router.get("/all")
async def get_all():
    res = {}

    try:
        all_files = os.listdir("site_data")

        for file in all_files:
            key = file.split("_rule")[0]
            df = pd.read_csv(os.path.join("site_data", file))
            df.fillna("", inplace=True)

            # Преобразование DataFrame в JSON-совместимую структуру
            data_as_dict = df.to_dict(orient="records")
            valid_counts = {key: val for key, val in df["valid"].value_counts().to_dict().items()}

            res[key] = {
                "valid": valid_counts,
                "data": data_as_dict,
            }

        return res

    except Exception as e:
        return {"error": str(e)}


@router.get("/")
async def get_by_key(key: str):
    try:
        # Найти файл, соответствующий ключу
        file = next(
            (val for val in os.listdir("site_data") if val.split("_rule")[0] == key),
            None
        )
        if not file:
            return {"error": f"File with key '{key}' not found"}

        # Загрузить данные из файла
        df = pd.read_csv(os.path.join("site_data", file))
        df.fillna("", inplace=True)

        # Сериализуем данные
        data_as_dict = df.to_dict(orient="records")  # Преобразование DataFrame в список словарей
        valid_counts = {key: val for key, val in df["valid"].value_counts().to_dict().items()}

        return {
            key: {
                "valid": valid_counts,
                "data": data_as_dict
            }
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/valid")
async def get_valid_by_key(key: str):
    try:
        # Найти файл, соответствующий ключу
        file = next(
            (val for val in os.listdir("site_data") if val.split("_rule")[0] == key),
            None
        )
        if not file:
            return {"error": f"File with key '{key}' not found"}

        # Загрузить данные из файла
        df = pd.read_csv(os.path.join("site_data", file))
        df.fillna("", inplace=True)
        valid_counts = {key: val for key, val in df["valid"].value_counts().to_dict().items()}

        return {
            key: {
                "valid": valid_counts,
            }
        }
    except Exception as e:
        return {"error": str(e)}
