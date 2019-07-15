import pymongo

myclient = pymongo.MongoClient('mongodb://139.155.103.174:27017/')
mydb = myclient['game']
mycollection = mydb['game']




count  = 0
for content in mycollection.find().batch_size(500):
    if 'youminData' not in content.keys():
        mycollection.update_one({'_id':content['_id']},{'$set':{'avgScore':0.0}})
        count += 1
        print(str(count), '103243')
        continue
    youminData = content['youminData']
    if 'score' in youminData.keys() and len(youminData['score']) > 0:
        total = 0.0
        for score in youminData['score']:
            real = (score['real_score'] / (score['full_score'] if score['full_score'] != 0 else 10)) * 10
            total += real
        v = total / len(youminData['score'])
        mycollection.update_one({'_id':content['_id']},{'$set':{'avgScore':v}})
        count += 1
        print(str(count), '103243')
        continue
    if 'userScore' in youminData.keys():
        mycollection.update_one({'_id':content['_id']},{'$set':{'avgScore':youminData['userScore']}})
        count += 1
        print(str(count), '103243')
        continue
    else:
        mycollection.update_one({'_id':content['_id']},{'$set':{'avgScore':0.0}})
        count += 1
        print(str(count), '103243')
        continue
    