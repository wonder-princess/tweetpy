from apps.config import Keys, SearchFilter, connect_twetter
from apps.input_file import input_img, input_txt

api = connect_twetter()

def post_tweet():
    if not input_img():
        api.update_status(status=input_txt())
    else:
        media_ids = []
        i = 0
        for image in input_img():
            i += 1
            if i >= 5:
                break
            img = api.media_upload(image)
            media_ids.append(img.media_id)
        api.update_status(status=input_txt(), media_ids=media_ids) 

def is_empty():
    if not input_img():
        print("empty")
    else:
        print("not empty")

