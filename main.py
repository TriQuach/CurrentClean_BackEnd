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


def updateTableFreq(listSensor,sensor,start,end,idx,table,indexValidID):

        if (sensor.temperature != listSensor[idx + 1].temperature):
            indexxSensor = valid_id.index(indexValidID)
            table[indexxSensor][0] += 1
        if (sensor.humidity != listSensor[idx + 1].humidity):
            indexxSensor = valid_id.index(indexValidID)
            table[indexxSensor][1] += 1
        if (sensor.airPressure != listSensor[idx + 1].airPressure):
            indexxSensor = valid_id.index(indexValidID)
            table[indexxSensor][2] += 1
        if (sensor.voltage != listSensor[idx + 1].voltage):
            indexxSensor = valid_id.index(indexValidID)
            table[indexxSensor][3] += 1


def updateTableAge(listSensor, sensor, start, end, idx, table, indexValidID):
    if (sensor.temperature != listSensor[idx + 1].temperature):
        indexxSensor = valid_id.index(indexValidID)
        table[indexxSensor][0] += 1
    if (sensor.humidity != listSensor[idx + 1].humidity):
        indexxSensor = valid_id.index(indexValidID)
        table[indexxSensor][1] += 1
    if (sensor.airPressure != listSensor[idx + 1].airPressure):
        indexxSensor = valid_id.index(indexValidID)
        table[indexxSensor][2] += 1
    if (sensor.voltage != listSensor[idx + 1].voltage):
        indexxSensor = valid_id.index(indexValidID)
        table[indexxSensor][3] += 1
def getFreq(start,end,tableFreq):
    for i in valid_id:
        listSensor = dicts[i]
        for idx, sensor in enumerate(listSensor):
            if(idx < len(listSensor)-1):
                if (int(sensor.time) >= int(start) and int(sensor.time) <= int(end)):
                    updateTableFreq(listSensor,sensor,start,end,idx,tableFreq,i)
                elif (int(sensor.time) > int(end)):
                    break
def getAge(start,end,tableAge):
    for idx in valid_id:
        listSensor = dicts[idx]
        count = 0
        flag = 0
        tempSensor = initSensor
        for i in range(len(listSensor)-1,-1,-1):
            if (i>0):
                if (int(listSensor[i].time) <= int(end) and int(listSensor[i].time) >= int(start)):
                    if (flag == 0):
                        tempSensor = listSensor[i]
                        flag = 1
                    indexxSensor = valid_id.index(idx)
                    if(listSensor[i].temperature != listSensor[i-1].temperature and tableAge[indexxSensor][0]== 0):
                        tableAge[indexxSensor][0] =int(listSensor[i].time) - int(listSensor[i-1].time)
                        count += 1
                    if (listSensor[i].humidity != listSensor[i - 1].humidity and tableAge[indexxSensor][1] == 0):
                        tableAge[indexxSensor][1] = int(listSensor[i].time) - int(listSensor[i - 1].time)
                        count += 1
                    if (listSensor[i].airPressure != listSensor[i - 1].airPressure and tableAge[indexxSensor][2] == 0):
                        tableAge[indexxSensor][2] = int(listSensor[i].time) - int(listSensor[i - 1].time)
                        count += 1
                    if (listSensor[i].voltage != listSensor[i - 1].voltage and tableAge[indexxSensor][3] == 0):
                        tableAge[indexxSensor][3] = int(listSensor[i].time) - int(listSensor[i - 1].time)
                        count += 1
                    if (count == 4):
                        break
                elif (int(listSensor[i].time) <= int(start)):
                    indexxSensor = valid_id.index(idx)
                    for i in range(numProperty):
                        if (tableAge[indexxSensor][i] == 0):
                            tableAge[indexxSensor][i] = int(tempSensor.time) - int(start)



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
@app.route('/age')
def age():
    tableAge = np.zeros((len(valid_id), numProperty))
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    getAge(start,end,tableAge)
    return jsonify (
        tableAge.tolist()
    )



