import json
import os
#from bson.objectid import ObjectId

# To encode the object id of mongoDB to JSON object..!!!
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# To encode the Dae and timme objects..!!!
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       elif isinstance(obj, decimal.Decimal):
           return float(obj)
       elif isinstance(obj, ModelState):
           return None
       else:
           return json.JSONEncoder.default(self, obj)

# To write to a JSON file..!!!
def writeJSON(res, fName):
    file = open(fName, 'w+')
    file.seek(0)
    file.write(json.dumps(res, cls=DateTimeEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
    file.truncate()
    
# To write to a JSON file..!!!
def writeJSON2(res, fName):
    file = open(fName, 'w+')
    file.seek(0)
    file.write(json.dumps(res, cls=DateTimeEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
    file.truncate()
    
def readJson(request):
	with open('/var/www/safewatch_ivr/static/json/'+request.POST['To']+'_'+request.POST['CallUUID']+'.json', 'w+') as f:
		return json.load(f)
		
def writeJson(request, data, createfile):
	file = open('/var/www/safewatch_ivr/static/json/'+request.POST['To']+'_'+request.POST['CallUUID']+'.json', 'w+')
	if createfile == 1 :
		os.chmod('/var/www/safewatch_ivr/static/json/'+request.POST['To']+'_'+request.POST['CallUUID']+'.json', 0777)
		file = open('/var/www/safewatch_ivr/static/json/'+request.POST['To']+'_'+request.POST['CallUUID']+'.json', 'w+')
	file.seek(0)
	file.write(json.dumps(data, cls=DateTimeEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
	file.truncate()
	file.close()
	"""
	with open('/var/www/safewatch_ivr/static/json/'+request.POST['To']+'_'+request.POST['CallUUID']+'.json', 'w+') as f:
		if createfile == 1 :
			os.chmod('/var/www/safewatch_ivr/static/json/'+request.POST['To']+'_'+request.POST['CallUUID']+'.json', 0777)
		try:
			print data
			json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
		except Exception, e:
			print e
	"""		
