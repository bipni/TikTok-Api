import asyncio
import csv
import os
from os.path import exists

from TikTokApi import TikTokApi

SEARCH_TEXT = 'david teather'
COUNT = 30  # minimum value 30
ms_token = os.environ.get("ms_token", None)  # set your own ms_token, needs to have done a search before for this to work
FILE_NAME = f'{SEARCH_TEXT}_hashtag.csv'


async def search_users():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)

        async for user in api.search.users(SEARCH_TEXT, count=COUNT):
            copy_dict = {}
            data = user.as_dict

            for key, value in data.items():
                copy_dict[key] = str(value)

            if exists(f'files/{FILE_NAME}'):
                with open(f'files/{FILE_NAME}', 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=copy_dict.keys())
                    writer.writerow(copy_dict)
            else:
                with open(f'files/{FILE_NAME}', 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=copy_dict.keys())
                    writer.writeheader()
                    writer.writerow(copy_dict)


if __name__ == "__main__":
    asyncio.run(search_users())
