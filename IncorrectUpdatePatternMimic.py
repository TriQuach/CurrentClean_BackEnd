from main import *

class InccorectUpdatePatternMimic:
    def __init__(self, id_patient, count):

        self.id_patient = id_patient
        self.count = count

def incorrectUpdatePatternMimic():
    for id in valid_id_Mimic:
        arr = dictsPatient[id]
        for i in range(len(arr)-1):
            if (arr[i].HR != arr[i+1].HR and arr[i].SBP == arr[i+1].SBP and arr[i].DBP == arr[i+1].DBP):
                arrObj = dictsUncorrectUpdatePatternMimic[id]
                arrObj.append(arr[i+1])
                dictsUncorrectUpdatePatternMimic[id] = arrObj


def lengthIncorrect():
    arrObj = []
    for id in valid_id_Mimic:
        arr = dictsUncorrectUpdatePatternMimic[id]
        obj = InccorectUpdatePatternMimic(id,len(arr))
        arrObj.append(obj)
    return arrObj

def printResult(arr):
    for i in arr:
        print("number of incorrect update pattern of HR for patient_" + str(i.id_patient) + ": " + str(i.count))
        # print(i.freq)

incorrectUpdatePatternMimic()
res = lengthIncorrect()
res.sort(key=lambda x: x.count, reverse=True)
printResult(res)