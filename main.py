import numpy as np
from flask import Flask, request
from flask import jsonify
from collections import defaultdict
import json

valid_id = ['A434F11F1B05', 'A434F11EEE06', 'A434F11F1684', 'A434F11F1E86', 'A434F11EF48B', 'A434F11F2003',
				'A434F11EEF0E', 'A434F11EA281', 'A434F11F1D06', 'A434F11F1000', 'A434F11F1606', 'A434F11FF78E',
				'A434F11F3681', 'A434F11F0C80', 'A434F11F1B88', 'A434F11EF609', 'A434F11FFE0D', 'A434F11F1B8A',
				'A434F1201380', 'A434F11F1B07', 'A434F11F0E06', 'A434F11F2F84', 'A434F11F1001', 'A434F11A3408',
				'A434F1204007', 'A434F11EA080', 'A434F1201282', 'A434F11EF80D', 'A434F11F1404', 'A434F11F1486',
				'A434F11F1683', 'A434F11F1A0A', 'A434F11F1783', 'A434F11F118D', 'A434F11EEB80', 'A434F11F0E83',
				'A434F11F1083', 'A434F11F1B84', 'A434F11F1D04', 'A434F11F1482', 'A434F11F1187', 'A434F11F1C85',
				'A434F1204005', 'A434F11F1F03', 'A434F11F3902', 'A434F11EF68F', 'A434F11F1106', 'A434F11F1782',
				'A434F11F1607', 'A434F11F4287', 'A434F11F1F02', 'A434F11F1406', 'A434F11F0E85', 'A434F11EEF8C',
				'A434F11F1E09', 'A434F11F0E03', 'A434F11F1483', 'A434F11F1F85']
numProperty = 4 #Temperature;Humidity;AirPressure;Voltage


k = np.zeros((5, 5))

class Sensor:
    def __init__(self, time, id_sensor, temperature, humidity, airPressure, voltage):
        self.time = time
        self.id_sensor = id_sensor
        self.temperature = temperature
        self.humidity = humidity
        self.airPressure = airPressure
        self.voltage = voltage

initSensor = Sensor(0,0,0,0,0,0)
dicts = {
    '1': [initSensor]
}

def hashTable():
    sensor0 = Sensor(0,0,0,0,0,0)
    for i in valid_id:
        dicts[i] = [sensor0]


def removeDefaultValue():
    del dicts['1']
    for i in valid_id:
        del dicts[i][0]
# string = [{'id' : 'id1','f': 2},{'id' : 'id2','f': 32}]

def readfile():
    f = open("data_example.txt", "r")
    for line in f:
        word = line.split(',')
        word[2] = word[2].split(':')[1]
        word[3] = word[3].split(':')[1]
        word[4] = word[4].split(':')[1]
        word[5] = word[5].split(':')[1].strip('\n')
        sensor = Sensor(word[0],word[1],word[2],word[3],word[4],word[5])
        dicts[sensor.id_sensor].append(sensor)

def getFreq(start,end,tableFreq):
    for i in valid_id:
        listSensor = dicts[i]
        print(i)
        for idx, sensor in enumerate(listSensor):
            if(idx < len(listSensor)-1):
                if (int(sensor.time) >= int(start) and int(sensor.time) <= int(end)):
                    if (sensor.temperature != listSensor[idx+1].temperature):
                        indexxSensor = valid_id.index(i)
                        tableFreq[indexxSensor][0] += 1
                    if (sensor.humidity != listSensor[idx+1].humidity):
                        indexxSensor = valid_id.index(i)
                        tableFreq[indexxSensor][1] += 1
                    if (sensor.airPressure != listSensor[idx+1].airPressure):
                        indexxSensor = valid_id.index(i)
                        tableFreq[indexxSensor][2] += 1
                    if (sensor.voltage != listSensor[idx+1].voltage):
                        indexxSensor = valid_id.index(i)
                        tableFreq[indexxSensor][3] += 1
                elif (int(sensor.time) > int(end)):
                    break


def testDict():
    count = 0
    sen = dicts['A434F11EEE06']
    for idx,i in enumerate(sen):
        if (idx < len(sen)-3):
            if (i.voltage != sen[idx+1].voltage):
                count += 1
    print(count)

hashTable()
removeDefaultValue()
readfile()
# print(tableFreq)
app = Flask(__name__)
# http://127.0.0.1:5000/frequency?start=1&end=2
@app.route('/frequency')
def frequency():
    tableFreq = np.zeros((len(valid_id), numProperty))
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    getFreq(start,end,tableFreq)
    return jsonify (
        tableFreq.tolist()
    )



