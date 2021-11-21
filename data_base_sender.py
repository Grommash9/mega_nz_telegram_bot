import asyncio
import time
import bot
import config



async def data_base_sender():
    while True:
        await asyncio.sleep(2)
        await asyncio.create_task(data_send())


async def data_send():
    try:
        with open(r'D:\python\mega_nz_bot\data_base_sender.txt', 'r') as data_base_timings:
            for line in data_base_timings:
                last_timing = line
                if int(last_timing) + 82800 < round(time.time()):
                    await bot.bot.send_document(chat_id=config.owner_id, document=open(config.path_to_db, 'rb'))
                    with open('D:\python\mega_nz_bot\data_base_sender.txt', 'w') as data_base_timings:
                        data_base_timings.write(str(round(time.time())))
    except FileNotFoundError:
        with open('D:\python\mega_nz_bot\data_base_sender.txt', 'w') as data_base_timings:
            data_base_timings.write(str(round(time.time())))

