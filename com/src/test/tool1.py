from pymongo import MongoClient


stb_data = {"host":"192.168.3.29","port":27017,"username":"prd_ivs","password":"prd_ivs@123","database":"platform_crd","table":"HOR_DATA","key":"uuid"}

uuid = "D3500D13EE684A99BF6C70B6111E0310"


def checkMongo(data,uuid):
    conn = MongoClient(data['host'],data['port'])
    db = conn[data['database']]
    if db.authenticate(data['username'],data['password']):
        table = db[data['table']]
        result = table.find_one({data['key']:uuid})
        if result:
            conn.close()
            return result
        else:
            conn.close()
            return False
    else:
        conn.close()
        return False



data = stb_data

print(checkMongo(data,uuid))


