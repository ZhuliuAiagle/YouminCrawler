import pymongo

myclient = pymongo.MongoClient('mongodb://139.155.103.174:27017/')
mydb = myclient['game']
testdb = myclient['game_backup']
from_collection = mydb['game']
to_collection = mydb['youminScoreNew']

count = 0
all_count = 0
print("hahaha")
for element in to_collection.find().batch_size(500):
    cnFullName = "NAAAAAAAAAAA"
    enFullName = "NAAAAAAAAAAA"
    shortName = "NAAAAAAAAAAA"
    try:
        cnFullName = element['cnFullName']
    except:
        pass
    try:
        enFullName = element['enFullName']
    except:
        pass
    try:
        shortName = element['name']
    except:
        pass
    if(from_collection.find({'name':cnFullName}).count() > 0):
        for item in from_collection.find({'name':cnFullName}):
            _id = item['_id']
            from_collection.update({'_id':_id},{'$set': {'youminData': element}})
        count += 1
    elif (from_collection.find({'name':shortName}).count() > 0):
        for item in from_collection.find({'name':shortName}):
            _id = item['_id']
            from_collection.update({'_id':_id},{'$set': {'youminData': element}})
        count += 1
    elif (from_collection.find({'name':enFullName}).count() > 0):
        for item in from_collection.find({'name':enFullName}):
            _id = item['_id']
            from_collection.update({'_id':_id},{'$set': {'youminData': element}})
        count += 1
    elif (from_collection.find({'subname':enFullName}).count() > 0):
        for item in from_collection.find({'subname':enFullName}):
            _id = item['_id']
            from_collection.update({'_id':_id},{'$set': {'youminData': element}})
        count += 1
    all_count += 1
    print(count, all_count)
        
