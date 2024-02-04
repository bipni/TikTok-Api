import asyncio
import csv
import os
from os.path import exists

from TikTokApi import TikTokApi

VIDEO_ID = '7074717081563942186'
COUNT = 30  # minimum value 30
ms_token = os.environ.get("ms_token", None)  # set your own ms_token, needs to have done a search before for this to work
FILE_NAME = f'VIDEO_{VIDEO_ID}.csv'


async def get_video_example():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(
            url=f"https://www.tiktok.com/@davidteathercodes/video/{VIDEO_ID}"
        )

        video_info = await video.info()  # is HTML request, so avoid using this too much
        # print(video_info)

        copy_dict = {}
        data = video_info.as_dict

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

        async for related_video in video.related_videos(count=10):
            print(related_video)
            print(related_video.as_dict)


if __name__ == "__main__":
    asyncio.run(get_video_example())
