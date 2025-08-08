import aiohttp
import time
import os
import asyncio

async def fast_download(client, message, file_name, progress, progress_args):
    file = await client.get_messages(message.chat.id, message.id)
    telegram_file = await client.get_file(file.document.file_id)
    file_path = telegram_file.file_path
    file_size = telegram_file.file_size

    download_url = f"https://api.telegram.org/file/bot{client.bot_token}/{file_path}"

    start_time = time.time()
    downloaded = 0
    chunk_size = 512 * 1024  # 512KB

    async with aiohttp.ClientSession() as session:
        async with session.get(download_url) as resp:
            with open(file_name, "wb") as f:
                async for chunk in resp.content.iter_chunked(chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress:
                            asyncio.create_task(
                                progress(downloaded, file_size, *progress_args, start=start_time)
                            )
    return file_name
