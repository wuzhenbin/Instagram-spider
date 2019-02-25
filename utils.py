
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'instagram'
MONGO_TABLE = 'video_url'


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def read_mongo(condition):
	return db[MONGO_TABLE].find(condition)

def save_to_mongo(result):
    if db[MONGO_TABLE].update({'id': result['id']},{'$set': result}, True):
        print('存储成功',result)
        return True
    return False

def browse_action():
    driver.execute_script( 'window.scrollTo(0, document.body.scrollHeight)')