import time
from mega import Mega
from mega.errors import RequestError
import config
import db_api
import os
import bot
import requests


def send_results(owner_id, results):
    requests.get(f"https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id={owner_id}&text={results}")


def file_upload(file_local_name, file_name, owner_id):
    mega = Mega()
    try:
        m = mega.login(email=config.mega_account_details['login'], password=config.mega_account_details['password'])
    except RequestError as e:
        send_results(owner_id, e)
        return e
    else:
        try:
            if file_name != file_local_name:
                os.rename(src=f"{config.files_path}/{file_local_name}", dst=f"{config.files_path}/{file_name}")
        except FileExistsError as e:
            send_results(owner_id, e)
            return e
        except FileNotFoundError as e:
            send_results(owner_id, e)
            return e

        folder = m.find(str(owner_id))
        if folder == None:
            m.create_folder(str(owner_id))
            folder = m.find(str(owner_id))
        is_here = m.find(exclude_deleted=True, filename=file_name)
        if is_here != None:
            if is_here[1]['p'] == folder[0]:
                send_results(owner_id, 'file name already exists on mega, please choose another')
                return 'file name already exists on mega, please choose another'
        new_file = m.upload(f"{config.files_path}/{file_name}", folder[0], upstatusmsg='d')
        url = m.get_upload_link(new_file)
        db_api.add_files_data(file_name=file_name, file_url=url, upload_date=str(time.time()), owner=owner_id)
        try:
            os.remove(f"{config.files_path}/{file_name}")
        except:
            pass
        send_results(owner_id, 'File uploaded successfully\n\n')
        return 'file_uploaded'

