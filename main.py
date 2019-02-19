import numpy as np
import pandas as pd
from flask import Flask, request
from flask import jsonify
from flask import Response
import QuickSort
from collections import defaultdict
import sklearn.utils
import json
import matplotlib
from flask_cors import CORS

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

class HeatMap:
    def __init__(self, value, hex, isSelected):
        self.value = value
        self.hex = hex
        self.isSelected = isSelected

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HeatMap):
            return {
                "value": obj.value,
                "hex": obj.hex,
                "isSelected": obj.isSelected
            }
        #Let the base class handle the problem.
        return json.JSONEncoder.default(self, obj)

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
            if (int(listSensor[i].time) <= int(end) and int(listSensor[i].time) >= int(start)):
                indexxSensor = valid_id.index(idx)
                tableAge[indexxSensor][0] = float(listSensor[i].temperature)
                tableAge[indexxSensor][1] = float(listSensor[i].humidity)
                tableAge[indexxSensor][2] = float(listSensor[i].airPressure)
                tableAge[indexxSensor][3] = float(listSensor[i].voltage)
                break


def initDictDuration(start, end, sensorID, prop):
    dictsDuration = {
        '1': [initSensor]
    }
    del dictsDuration['1']
    listSensor = dicts[sensorID]
    for sensor in listSensor:
        if (int(sensor.time) > int(start) and int(sensor.time) < int(end)):
            key = getattr(sensor,prop)
            isExist = key in dictsDuration.keys()
            if (isExist == False):
                dictsDuration[key] = [sensor]
            else:
                dictsDuration[key].append(sensor)

    return  dictsDuration

def initDictDurationAge(start, end, sensorID, prop):
    dictsDuration = {
        '1': [initSensor]
    }
    del dictsDuration['1']
    listSensor = dicts[sensorID]
    for i in range(len(listSensor)-1):
        if (int(listSensor[i].time) >= int(start) and int(listSensor[i].time) <= int(end)):
            key = getattr(listSensor[i],prop)
            key_next = getattr(listSensor[i+1],prop)
            isExist = key in dictsDuration.keys()
            if (isExist == False):
                dictsDuration[key] = [listSensor[i]]
                if (key != key_next):
                    dictsDuration[key].append(listSensor[i + 1])
            else:
                if (key != key_next):
                    dictsDuration[key].append(listSensor[i])
                    dictsDuration[key].append(listSensor[i+1])
    return  dictsDuration
def getDuration(start, dictsDuration):
    tableDuration = np.zeros((len(dictsDuration.keys()), 2))
    for idx, key in enumerate(dictsDuration.keys()):
        duration = 0

        listSensors = dictsDuration[key]
        freq = len(listSensors)
        tableDuration[idx][0] = (key)
        tableDuration[idx][1] = (freq)
    if (len(tableDuration) > 10):
        data = pd.DataFrame(tableDuration)

        test = data.sort_values([1], ascending=[False])

        tableDuration = test.head(10).values
        tableDuration = sklearn.utils.shuffle(tableDuration)

    return tableDuration

def getDurationAge(start, dictsDurationAge):
    tableDuration = np.zeros((len(dictsDurationAge.keys()), 2))
    for idx, key in enumerate(dictsDurationAge.keys()):
        listSensors = dictsDurationAge[key]
        duration = 0
        for i in range(0,len(listSensors)-1,2):
            duration += int(listSensors[i+1].time) - int(listSensors[i].time)
        tableDuration[idx][0] = (key)
        tableDuration[idx][1] = (duration)
    # for idx, key in enumerate(dictsDurationAge.keys()):
    #     duration = 0
    #
    #     listSensors = dictsDuration[key]
    #     freq = len(listSensors)
    #     tableDuration[idx][0] = (key)
    #     tableDuration[idx][1] = (freq)
    # if (len(tableDuration) > 10):
    #     data = pd.DataFrame(tableDuration)
    #
    #     test = data.sort_values([1], ascending=[False])
    #
    #     tableDuration = test.head(10).values
    #     tableDuration = sklearn.utils.shuffle(tableDuration)

    return tableDuration

def testPandas():
    d = {'col1': [initSensor], 'col2':[1]}
    df = pd.DataFrame(data=d)
    df = df.append({'col1': initSensor}, ignore_index=True)


def moveTo1dArray(table):
    temp = []
    for i in range(len(table)):
        for j in range(len(table[i])):
            temp.append(table[i][j])
    return temp
def createHeatMapFreg(tableFreq):
    # 0.9 i 0.4
    # [0.9, i, 0.2]
    # ([0.3, i, 0.4])
    temp = moveTo1dArray(tableFreq)

    temp_norm = [float(i) / max(temp) for i in temp]

    lower, upper = 0.45, 1.0
    norm = [lower + (upper - lower) * x for x in temp_norm]
    arrayHex = []
    for i in norm:
        hex = matplotlib.colors.to_hex([ i,i, 0.2])
        arrayHex.append(hex)

    index = 0
    tableHeatMap = [[HeatMap(123,'asd',False) for j in range(numProperty)] for i in range(len(valid_id))]
    for i in range(len(tableFreq)):
        for j in range(len(tableFreq[i])):
            temp = HeatMap(tableFreq[i][j],arrayHex[index],False)
            tableHeatMap[i][j] = temp
            index += 1
    return tableHeatMap

def createHeatMapFregColumn(tableFreq):
    # 0.9 i 0.4
    # [0.9, i, 0.2]
    # ([0.3, i, 0.4])
    tableHeatMap = [[HeatMap(123, 'asd',False) for j in range(numProperty)] for i in range(len(valid_id))]
    dataFrame = pd.DataFrame()
    for i in range(len(tableFreq[0])):
        col = tableFreq[:,i]
        temp_norm = [1 - float(j) / max(col) for j in col]

        lower, upper = 0.45, 1.0
        norm = [lower + (upper - lower) * x for x in temp_norm]
        arrayHeat = []

        for idx, normValue in enumerate(norm):

            hex = matplotlib.colors.to_hex([normValue, normValue, 0.2])
            tempHeat = HeatMap(tableFreq[idx][i],hex, False)

            arrayHeat.append(tempHeat)


        data1 = pd.DataFrame(arrayHeat)
        # print(arrayHeat)
    #
        # print('-----------')
        # print(data1)
        # print('-----------')
        dataFrame = pd.concat([dataFrame,data1],axis=1)
        # print (dataFrame.size)
        #

    return dataFrame.values
    #
    # print(dataFrame.values)
    # return dataFrame.values

def createHeatMapAge(tableAge):
    # 0.9 i 0.4
    # [0.9, i, 0.2]
    temp = moveTo1dArray(tableAge)
    norm = [float(i) / max(temp) for i in temp]
    arrayHex = []
    for i in norm:
        hex = matplotlib.colors.to_hex([ 0.9,i, i])
        arrayHex.append(hex)

    index = 0
    tableHeatMap = [[HeatMap(123,'asd',False) for j in range(numProperty)] for i in range(len(valid_id))]
    for i in range(len(tableAge)):
        for j in range(len(tableAge[i])):
            temp = HeatMap(tableAge[i][j],arrayHex[index],False)
            tableHeatMap[i][j] = temp
            index += 1
    return tableHeatMap

def findValueForOneAttributeOfCell(sensorID,prop,start,end):
    listSensor = dicts[sensorID]
    array = []
    step = 0
    for idx,sensor in enumerate(listSensor):
        if (int(sensor.time) > int(start) and int(sensor.time) < int(end)):
            time = sensor.time
            value = getattr(sensor, prop)
            temp={'x':step,'y':value}
            array.append(temp)
            step += 2
    for sub in array:
        for key in sub:
            sub[key] = float(sub[key])
    return  array

def findAllValueAllSensor(arrayCells,start,end):
    array = []
    for obj in arrayCells:
        sensorID = list(obj.keys())[0]
        temp = findValueForOneAttributeOfCell(sensorID,obj[sensorID],start,end)
        array.append(temp)
    return array

hashTable()
removeDefaultValue()
readfile()
dictsDuration = initDictDurationAge("1522932390","1522987200","A434F11F1B05","temperature")
temp = dictsDuration["16.6"]


app = Flask(__name__)
CORS(app)
# http://127.0.0.1:5000/frequency?start=1&end=2
@app.route('/frequency')
def frequency():
    tableFreq = np.zeros((len(valid_id), numProperty))
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    getFreq(start,end,tableFreq)
    print(type(tableFreq))
    tableHeatMap = createHeatMapFregColumn(tableFreq)
    print(type(tableHeatMap))
    return json.dumps(tableHeatMap.tolist(), cls=CustomEncoder)
@app.route('/age')
def age():
    tableAge = [[0.0 for j in range(numProperty)] for i in range(len(valid_id))]
    # tableHeatMap = [[HeatMap(123, 'asd', False) for j in range(numProperty)] for i in range(len(valid_id))]
    # tableAge.astype(float)
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    getAge(start,end,tableAge)
    print(type(tableAge))
    tableHeatMap = createHeatMapFregColumn(np.asarray(tableAge))
    print(tableHeatMap)
    # tableHeatMap = createHeatMapFreg(tableAge)

    return json.dumps(tableHeatMap.tolist(), cls=CustomEncoder)

@app.route('/duration')
def duration():

    start = request.args.get('start', None)
    end = request.args.get('end', None)
    sensorID = request.args.get('sensorID', None)
    prop = request.args.get('prop', None)
    dictsDuration = initDictDuration(start,end,sensorID,prop)

    tableDuration = getDuration(start,dictsDuration)
    print("haha")
    print(tableDuration)
    return jsonify (
        tableDuration.tolist()
    )

@app.route('/comparecells', methods= ['POST'])
def comparecells():
    data = request.get_json()
    print(data["start"])

    res = findAllValueAllSensor(data["arrayCells"],data["start"],data["end"])
    return(jsonify(res))

@app.route('/existedtime')
def existedtime():

    start = request.args.get('start', None)
    end = request.args.get('end', None)
    sensorID = request.args.get('sensorID', None)
    prop = request.args.get('prop', None)
    dictsDurationAge = initDictDurationAge(start,end,sensorID,prop)
    print(dictsDurationAge)
    tableDurationAge = getDurationAge(start,dictsDurationAge)
    print(tableDurationAge)
    return jsonify (
        tableDurationAge.tolist()
    )
