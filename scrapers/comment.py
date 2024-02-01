import asyncio
import csv
import os
from os.path import exists

from TikTokApi import TikTokApi

video_ids = ['7248300636498890011']
COUNT = 30  # minimum value 20
ms_token = os.environ.get("ms_token", None)  # set your own ms_token
FILE_NAME = 'comments.csv'


async def get_comments():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)

        for video_id in video_ids:
            video = api.video(id=video_id)

            async for comment in video.comments(count=COUNT):
                copy_dict = {}
                data = comment.as_dict

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
    asyncio.run(get_comments())
