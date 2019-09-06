from main import *


def uncorrectUpdatePattern(dicts):
    res = []
    for id in valid_id:
        arr = dicts[id]
        for i in range(len(arr)-1):
            if (arr[i].temperature != arr[i+1].temperature and arr[i].humidity == arr[i+1].humidity and arr[i].airPressure == arr[i+1].airPressure):
                arrObj = dictsUncorrectUpdatePattern[id]
                arrObj.append(arr[i+1])
                dictsUncorrectUpdatePattern[id] = arrObj

def lengthEachUccorctSensor():
    for id in  valid_id:
        arr = dictsUncorrectUpdatePattern[id]
        print("number of incorrect update pattern of sensor_" + id + ":    " + str(len(arr)))

uncorrectUpdatePattern(dicts)

lengthEachUccorctSensor()
