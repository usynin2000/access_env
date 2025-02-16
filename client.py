import aiohttp
import logging
import asyncio

from config import YANDEX_ORG_API

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_access_envs(url, api_key, place):
    params = f"?apikey={api_key}&lang=ru_RU&type=biz&text={place}"
    final_url = url + params

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(final_url) as response:
                print(response)
                if response.status == 200:
                    data = await response.json()
                    features = data["features"][0]["properties"]["CompanyMetaData"]["Features"]
                    access_envs = []
                    for env in features:
                        if env["id"] == "wheelchair_access":
                            wheelchair_access = f"{env["name"]}: {env["value"][0]["name"]}"
                            access_envs.append(wheelchair_access)
                            continue
                        if env["value"]:
                            access_envs.append(env["name"])
                    print(access_envs)
                    return access_envs
                elif response.status == 403:
                    return "Токен Протух"

                else:
                    logger.warning(f"Ошибка при получении данных: статус {response.status}")
        except Exception as e:
            logger.error(f"Ошибка при получении данных: {e}")


if __name__ == "__main__":
    url = "https://search-maps.yandex.ru/v1"
    place = "ТЦ Вегас Мякинено"
    api_key = YANDEX_ORG_API

    asyncio.run(get_access_envs(url=url, api_key=api_key, place=place))

