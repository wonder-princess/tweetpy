import csv
import glob
import os


def input_sendDM_user_list():
    csv_file = open("apps/input/sendDM_userlist.csv", "r", encoding="utf-8", errors="", newline="" )
    list = []
    for i, row in enumerate(csv_file):
        if i == 0:
            continue
        list.append(row)
    return list

def input_omit_user_list():
    csv_file = open("apps/input/omit_userlist.csv", "r", encoding="utf-8", errors="", newline="" )
    list = []
    for i, row in enumerate(csv_file):
        if i == 0:
            continue
        list.append(row)
    return list

def input_omit_words():
    csv_file = open("apps/input/omit_words.csv", "r", encoding="utf-8", errors="", newline="" )
    list = []
    for i, row in enumerate(csv_file):
        if i == 0:
            continue
        list.append(row)
    return list

def input_userlist_list():
    csv_file = open("apps/input/userlist_list.csv", "r", encoding="utf-8", errors="", newline="" )
    list = []
    for i, row in enumerate(csv_file):
        if i == 0:
            continue
        row = str(row).strip()
        list.append(row)
    return list    

def input_img():
    strImgDirPath = "apps/input/post_img"
    strImgFileName = "*" + ".[pj][np][g]"
    image_list = glob.glob(os.path.join(strImgDirPath, strImgFileName))
    return image_list

def input_txt():
    f = open('apps/input/message.txt', 'r', encoding="utf-8")
    return f.read()
