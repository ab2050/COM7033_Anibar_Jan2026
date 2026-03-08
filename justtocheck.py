from mongoconnect import patdata
results = list(patdata.find({"_id": "usertry"}))
print(len(results))
print(results)
#delete cause of duplicate data with different field names
#patdata.delete_many({"_id": "usertry"})