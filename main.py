import requests, json, csv, tzlocal 
from datetime import datetime

''' 
-site for request with example: 
api.openweathermap.org/data/2.5/weather?q=London,
uk&APPID=02c4f96bb6f0fb3fe9138341c8ff8c32

-api key: 02c4f96bb6f0fb3fe9138341c8ff8c32
'''

key = '02c4f96bb6f0fb3fe9138341c8ff8c32'
def getDayLight(zip):
    gdl = {}
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+zip+'&APPID='+ key)
    data = json.loads(response.text)
    if str(data['cod']) == '200':
        gdl['status'] = 'ok'
        riseunix = data['sys']['sunrise']
        setunix = data['sys']['sunset']
        gdl['rise'] = datetime.fromtimestamp(int(riseunix)).strftime('%H:%M:%S')
        gdl['set'] = datetime.fromtimestamp(int(setunix)).strftime('%H:%M:%S')    
        gdl['riseunix'] = int(riseunix)
        gdl['setunix'] = int(setunix)
    else:
        gdl['status'] = 'error'
    return gdl

print("First call with zip-13676 (should run ok) : ", getDayLight('13676'))
print("Second call with zip-395007 (should run ok) : ", getDayLight('395007'))
print("Third call with zip-\'oo\' (should give error ass oo is not a zipcode): ", getDayLight('oo'))
print("Fourth call with zip-123456 (logical error) : ", getDayLight('123456'))
print("Fifth call with zip-90245 (should run ok) : ", getDayLight('90245'))

f1 = open('ziplist.csv', 'r')
reader = csv.reader(f1)

f2 = open('daylight_data.csv', 'w')
f2.write("")
f2.close()
f2 = open('daylight_data.csv', 'a')
writer = csv.writer(f2, delimiter=',', lineterminator='\n')
for i, row in enumerate(reader):
    if i == 0:
        writer.writerow(row)
    else:
        zip = str(row[0])
        get_day_light = getDayLight(zip)
        if get_day_light['status'] == 'ok':
            start = get_day_light['rise']
            end = get_day_light['set']
            file_data = [zip,start,end]
        else:
            print('Error occrued for :', zip)
            start = 'Error in getting data'
            end = 'Error in getting data'
            file_data = [zip,start,end]
        writer.writerow(file_data)
    
f1.close()
f2.close()