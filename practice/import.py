import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.icd2
# for i in db.codes.find():
#     print(i)
# for j in db.codes.find({"codeSet": "icd9"}):
#     print(j)
# for k in db.codes.find({"desc": "Other genetic screening"}):
#     print(k)
#
# for i in db.section_info.find():
#     print(i)

for k in db.chapter_info.find():
    print(k)

