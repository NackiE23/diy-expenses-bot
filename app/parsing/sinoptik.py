import asyncio
import platform
from typing import List, Tuple

import aiohttp
from bs4 import BeautifulSoup


async def get_weather(region: str) -> Tuple[str, List[dict], List[dict]]:
    url = f"https://ua.sinoptik.ua/погода-{region}"
    week_res = []
    today_res = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print("Sinoptik does not respond!")
                return url, week_res, today_res
            html = await response.text()

    soup = BeautifulSoup(html, "lxml")

    mains = soup.select(".tabs .main")
    for main in mains:
        p_tags = main.find_all("p")
        divs = main.find_all("div")

        week_res.append({
            "day": f"{p_tags[0].text}",
            "date": f"{p_tags[1].text} {p_tags[2].text}",
            "description": f"{divs[0]['title']}",
            "temperature": f"{divs[1].text}"
        })

    return url, week_res, today_res

if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(asyncio.run(get_weather("тернопіль")))
