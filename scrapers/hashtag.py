import asyncio
import csv
import os
from os.path import exists

from TikTokApi import TikTokApi

HASHTAG = 'cocacola'
COUNT = 30  # minimum value 30
ms_token = os.environ.get("ms_token", None)  # set your own ms_token
FILE_NAME = f'{HASHTAG}_hashtag.csv'


async def get_hashtag_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)

        tag = api.hashtag(name=HASHTAG)

        async for video in tag.videos(count=30):
            copy_dict = {}
            data = video.as_dict

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
    asyncio.run(get_hashtag_videos())
