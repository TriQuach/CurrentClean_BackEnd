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
valid_id_Mimic = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',
                  '16','17','18','19','20','21','22','23','24','25','26','27','28','29','30',
                  '31','32','33','34','35','36','37','38','39','40','41','42','43','44','45',
                  '46','47','48','49','50']
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

class Patient:
    def __init__(self, time, id_patient, WT, LDL, HDL, HR,DBP,SBP,CVP,RR,SpO2,TMP,ABE,ACO2,APH,Hb,RBC,RBCF,WBC,MONO,EOS,LY,RDW,TC):
        self.time = time
        self.id_patient = id_patient
        self.WT = WT
        self.LDL = LDL
        self.HDL = HDL
        self.HR = HR
        self.DBP = DBP
        self.SBP = SBP
        self.CVP = CVP
        self.RR = RR
        self.SpO2 = SpO2
        self.TMP = TMP
        self.ABE = ABE
        self.ACO2 = ACO2
        self.APH = APH
        self.Hb = Hb
        self.RBC = RBC
        self.RBCF = RBCF
        self.WBC = WBC
        self.MONO = MONO
        self.EOS = EOS
        self.LY = LY
        self.RDW = RDW
        self.TC = TC


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
initPatient = Patient(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
dicts = {
    '1': [initSensor]
}
dictsPatient = {
    '999': [initPatient]
}

def hashTable():
    sensor0 = Sensor(0,0,0,0,0,0)
    for i in valid_id:
        dicts[i] = [sensor0]

def hashTableMimic():
    patient0 = Patient(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    for i in valid_id_Mimic:
        dictsPatient[i] = [patient0]

def removeDefaultValue():
    del dicts['1']
    del dictsPatient['999']

    for i in valid_id:
        del dicts[i][0]
    for i in valid_id_Mimic:
        del dictsPatient[i][0]

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
def readfileMimic():
    f = open("Mimic.txt", "r")
    for line in f:
        word = line.split(',')
        word[2] = word[2].split(':')[1]
        word[3] = word[3].split(':')[1]
        word[4] = word[4].split(':')[1]
        word[5] = word[5].split(':')[1]
        word[6] = word[6].split(':')[1]
        word[7] = word[7].split(':')[1]
        word[8] = word[8].split(':')[1]
        word[9] = word[9].split(':')[1]
        word[10] = word[10].split(':')[1]
        word[11] = word[11].split(':')[1]
        word[12] = word[12].split(':')[1]
        word[13] = word[13].split(':')[1]
        word[14] = word[14].split(':')[1]
        word[15] = word[15].split(':')[1]
        word[16] = word[16].split(':')[1]
        word[17] = word[17].split(':')[1]
        word[18] = word[18].split(':')[1]
        word[19] = word[19].split(':')[1]
        word[20] = word[20].split(':')[1]
        word[21] = word[21].split(':')[1]
        word[22] = word[22].split(':')[1]
        word[23] = word[23].split(':')[1].strip('\n')


        patient = Patient(word[0], word[1], word[2], word[3], word[4], word[5],word[6], word[7], word[8], word[9], word[10], word[11],word[12], word[13], word[14], word[15], word[16], word[17], word[18], word[19], word[20], word[21], word[22], word[23])
        dictsPatient[patient.id_patient].append(patient)



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
def getFreq(start,end,tableFreq,dataset):
    if (dataset == "sensor"):
        for i in valid_id:
            listSensor = dicts[i]
            for idx, sensor in enumerate(listSensor):
                if(idx < len(listSensor)-1):
                    if (int(sensor.time) >= int(start) and int(sensor.time) <= int(end)):
                        updateTableFreq(listSensor,sensor,start,end,idx,tableFreq,i)
                    elif (int(sensor.time) > int(end)):
                        break
    elif(dataset == "medical"):
        for i in valid_id_Mimic:
            listPatient = dictsPatient[i]
            for idx, patient in enumerate(listPatient):
                if(idx < len(listPatient)-1):
                    if (int(patient.time) >= int(start) and int(patient.time) <= int(end)):
                        if (patient.WT != listPatient[idx + 1].WT):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][0] += 1
                        if (patient.LDL != listPatient[idx + 1].LDL):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][1] += 1
                        if (patient.HDL != listPatient[idx + 1].HDL):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][2] += 1
                        if (patient.HR != listPatient[idx + 1].HR):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][3] += 1
                        if (patient.DBP != listPatient[idx + 1].DBP):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][4] += 1
                        if (patient.SBP != listPatient[idx + 1].SBP):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][5] += 1
                        if (patient.CVP != listPatient[idx + 1].CVP):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][6] += 1
                        if (patient.RR != listPatient[idx + 1].RR):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][7] += 1
                        if (patient.SpO2 != listPatient[idx + 1].SpO2):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][8] += 1
                        if (patient.TMP != listPatient[idx + 1].TMP):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][9] += 1
                        if (patient.ABE != listPatient[idx + 1].ABE):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][10] += 1
                        if (patient.ACO2 != listPatient[idx + 1].ACO2):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][11] += 1
                        if (patient.APH != listPatient[idx + 1].APH):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][12] += 1
                        if (patient.Hb != listPatient[idx + 1].Hb):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][13] += 1
                        if (patient.RBC != listPatient[idx + 1].RBC):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][14] += 1
                        if (patient.RBCF != listPatient[idx + 1].RBCF):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][15] += 1
                        if (patient.WBC != listPatient[idx + 1].WBC):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][16] += 1
                        if (patient.MONO != listPatient[idx + 1].MONO):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][17] += 1
                        if (patient.EOS != listPatient[idx + 1].EOS):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][18] += 1
                        if (patient.LY != listPatient[idx + 1].LY):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][19] += 1
                        if (patient.RDW != listPatient[idx + 1].RDW):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][20] += 1
                        if (patient.TC != listPatient[idx + 1].TC):
                            indexxSensor = valid_id_Mimic.index(i)
                            tableFreq[indexxSensor][21] += 1


                    elif (int(patient.time) > int(end)):
                        break
def getAge(start,end,tableAge,dataset):
    if(dataset == "sensor"):
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
    elif(dataset == "medical"):
        print("medical69")
        for idx in valid_id_Mimic:
            listPatient = dictsPatient[idx]
            for i in range(len(listPatient)-1,-1,-1):
                if (int(listPatient[i].time) <= int(end) and int(listPatient[i].time) >= int(start)):
                    indexxSensor = valid_id_Mimic.index(idx)
                    tableAge[indexxSensor][0] = float(listPatient[i].WT)
                    tableAge[indexxSensor][1] = float(listPatient[i].LDL)
                    tableAge[indexxSensor][2] = float(listPatient[i].HDL)
                    tableAge[indexxSensor][3] = float(listPatient[i].HR)
                    tableAge[indexxSensor][4] = float(listPatient[i].DBP)
                    tableAge[indexxSensor][5] = float(listPatient[i].SBP)
                    tableAge[indexxSensor][6] = float(listPatient[i].CVP)
                    tableAge[indexxSensor][7] = float(listPatient[i].RR)
                    tableAge[indexxSensor][8] = float(listPatient[i].SpO2)
                    tableAge[indexxSensor][9] = float(listPatient[i].TMP)
                    tableAge[indexxSensor][10] = float(listPatient[i].ABE)
                    tableAge[indexxSensor][11] = float(listPatient[i].ACO2)
                    tableAge[indexxSensor][12] = float(listPatient[i].APH)
                    tableAge[indexxSensor][13] = float(listPatient[i].Hb)
                    tableAge[indexxSensor][14] = float(listPatient[i].RBC)
                    tableAge[indexxSensor][15] = float(listPatient[i].RBCF)
                    tableAge[indexxSensor][16] = float(listPatient[i].WBC)
                    tableAge[indexxSensor][17] = float(listPatient[i].MONO)
                    tableAge[indexxSensor][18] = float(listPatient[i].EOS)
                    tableAge[indexxSensor][19] = float(listPatient[i].LY)
                    tableAge[indexxSensor][20] = float(listPatient[i].RDW)
                    tableAge[indexxSensor][21] = float(listPatient[i].TC)

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

def initDictDurationMimic(start, end, mimicID, prop):
    dictsDurationMimic = {
        '999': [initPatient]
    }
    del dictsDurationMimic['999']
    listPatient = dictsPatient[mimicID]
    for patient in listPatient:
        if (int(patient.time) > int(start) and int(patient.time) < int(end)):
            key = getattr(patient,prop)
            isExist = key in dictsDurationMimic.keys()
            if (isExist == False):
                dictsDurationMimic[key] = [patient]
            else:
                dictsDurationMimic[key].append(patient)

    return dictsDurationMimic

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
def initDictDurationAgeMimic(start, end, sensorID, prop):
    dictsDuration = {
        '999': [initPatient]
    }
    del dictsDuration['999']
    listPatient = dictsPatient[sensorID]
    for i in range(len(listPatient)-1):
        if (int(listPatient[i].time) >= int(start) and int(listPatient[i].time) <= int(end)):
            key = getattr(listPatient[i],prop)
            key_next = getattr(listPatient[i+1],prop)
            isExist = key in dictsDuration.keys()
            if (isExist == False):
                dictsDuration[key] = [listPatient[i]]
                if (key != key_next):
                    dictsDuration[key].append(listPatient[i + 1])
            else:
                if (key != key_next):
                    dictsDuration[key].append(listPatient[i])
                    dictsDuration[key].append(listPatient[i+1])
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
def getDurationMimic(start, dictsDurationMimic):
    tableDurationMimic = np.zeros((len(dictsDurationMimic.keys()), 2))
    for idx, key in enumerate(dictsDurationMimic.keys()):
        duration = 0

        listPatients = dictsDurationMimic[key]
        freq = len(listPatients)
        tableDurationMimic[idx][0] = (key)
        tableDurationMimic[idx][1] = (freq)
    if (len(tableDurationMimic) > 10):
        data = pd.DataFrame(tableDurationMimic)

        test = data.sort_values([1], ascending=[False])

        tableDurationMimic = test.head(10).values
        tableDurationMimic = sklearn.utils.shuffle(tableDurationMimic)

    return tableDurationMimic

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
def getDurationAgeMimic(start, dictsDurationAge):
    tableDuration = np.zeros((len(dictsDurationAge.keys()), 2))
    for idx, key in enumerate(dictsDurationAge.keys()):
        listPatients = dictsDurationAge[key]
        duration = 0
        for i in range(0,len(listPatients)-1,2):
            duration += int(listPatients[i+1].time) - int(listPatients[i].time)
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

def findValueForOneAttributeOfCellMimic(patientID,prop,start,end):
    listPatient = dictsPatient[patientID]
    array = []
    step = 0
    for idx,patient in enumerate(listPatient):
        if (int(patient.time) > int(start) and int(patient.time) < int(end)):
            time = patient.time
            value = getattr(patient, prop)
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

def findAllValueAllPatient(arrayCells,start,end):
    array = []
    for obj in arrayCells:
        patientID = list(obj.keys())[0]
        temp = findValueForOneAttributeOfCellMimic(patientID,obj[patientID],start,end)
        array.append(temp)
    return array

hashTable()
hashTableMimic()
removeDefaultValue()
readfile()
readfileMimic()
dictsDuration = initDictDurationAge("1522932390","1522987200","A434F11F1B05","temperature")
temp = dictsDuration["16.6"]


app = Flask(__name__)
CORS(app)
# http://127.0.0.1:5000/frequency?start=1&end=2
@app.route('/frequency')
def frequency():
    dataset = request.args.get('dataset', None)
    if dataset == "sensor":
        tableFreq = np.zeros((len(valid_id), numProperty))
        start = request.args.get('start', None)
        end = request.args.get('end', None)
        getFreq(start,end,tableFreq,dataset)
        print(type(tableFreq))
        tableHeatMap = createHeatMapFregColumn(tableFreq)
        print(type(tableHeatMap))
        return json.dumps(tableHeatMap.tolist(), cls=CustomEncoder)
    elif dataset == "medical":
        numcolMimic = 22
        tableFreqMimic = np.zeros((len(valid_id_Mimic), numcolMimic))
        start = request.args.get('start', None)
        end = request.args.get('end', None)
        getFreq(start, end, tableFreqMimic,dataset)
        tableHeatMap = createHeatMapFregColumn(tableFreqMimic)
        return json.dumps(tableHeatMap.tolist(), cls=CustomEncoder)
@app.route('/age')
def age():
    dataset = request.args.get('dataset', None)
    if dataset == "sensor":
        tableAge = [[0.0 for j in range(numProperty)] for i in range(len(valid_id))]
        # tableHeatMap = [[HeatMap(123, 'asd', False) for j in range(numProperty)] for i in range(len(valid_id))]
        # tableAge.astype(float)
        start = request.args.get('start', None)
        end = request.args.get('end', None)
        getAge(start,end,tableAge,dataset)
        print(type(tableAge))
        tableHeatMap = createHeatMapFregColumn(np.asarray(tableAge))
        print(tableHeatMap)
        # tableHeatMap = createHeatMapFreg(tableAge)

        return json.dumps(tableHeatMap.tolist(), cls=CustomEncoder)
    elif dataset == "medical":
        numcolMimic = 22
        tableAgeMimic = [[0.0 for j in range(numcolMimic)] for i in range(len(valid_id_Mimic))]
        start = request.args.get('start', None)
        end = request.args.get('end', None)
        getAge(start, end, tableAgeMimic,dataset)
        tableHeatMap = createHeatMapFregColumn(np.asarray(tableAgeMimic))
        print('tableHeatMap')
        print(tableHeatMap)
        return json.dumps(tableHeatMap.tolist(), cls=CustomEncoder)

@app.route('/duration')
def duration():
    dataset = request.args.get('dataset', None)
    if (dataset == "sensor"):
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
    elif (dataset == "medical"):
        start = request.args.get('start', None)
        end = request.args.get('end', None)
        sensorID = request.args.get('sensorID', None)
        prop = request.args.get('prop', None)
        dictsDurationMimic = initDictDurationMimic(start, end, sensorID, prop)
        tableDurationMimic = getDurationMimic(start, dictsDurationMimic)
        print("haha")
        print(tableDurationMimic)
        return jsonify(
            tableDurationMimic.tolist()
        )

@app.route('/comparecells', methods= ['POST'])
def comparecells():
    dataset = request.args.get('dataset', None)
    if (dataset == "sensor"):
        data = request.get_json()
        print(data["start"])

        res = findAllValueAllSensor(data["arrayCells"],data["start"],data["end"])
        return(jsonify(res))
    elif (dataset == "medical"):
        data = request.get_json()
        res = findAllValueAllPatient(data["arrayCells"], data["start"], data["end"])
        return (jsonify(res))
        print(data)

@app.route('/existedtime')
def existedtime():
    dataset = request.args.get('dataset', None)
    if (dataset == "sensor"):
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
    elif (dataset == "medical"):
        start = request.args.get('start', None)
        end = request.args.get('end', None)
        sensorID = request.args.get('sensorID', None)
        prop = request.args.get('prop', None)
        dictsDurationAge = initDictDurationAgeMimic(start, end, sensorID, prop)
        tableDurationAge = getDurationAgeMimic(start, dictsDurationAge)
        return jsonify(
            tableDurationAge.tolist()

        )
