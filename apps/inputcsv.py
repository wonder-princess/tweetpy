# import csv

csv_file = open("apps/inputcsv/userlist.csv", "r", encoding="utf-8", errors="", newline="" )
#リスト形式

# f = csv.reader(csv_file , delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
# header = next(f)
# print(header)

def printdata():
    list = []
    for i, row in enumerate(csv_file):
        if i == 0:
            continue
        #rowはList
        #row[0]で必要な項目を取得することができる
        list.append(row)
    return list
