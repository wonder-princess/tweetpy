import glob
import os


def input_user_list():
    csv_file = open("apps/input/userlist.csv", "r", encoding="utf-8", errors="", newline="" )
    list = []
    for i, row in enumerate(csv_file):
        if i == 0:
            continue
        #rowはList
        #row[0]で必要な項目を取得することができる
        list.append(row)
    return list

def input_img():
    strImgDirPath = "apps/input"
    strImgFileName = "*" + ".[pj][np][g]"
    image_list = glob.glob(os.path.join(strImgDirPath, strImgFileName))
    return image_list

def input_txt():
    f = open('apps/input/message.txt', 'r', encoding="utf-8")
    return f.read()
