from main import *


class HRFreq:
    def __init__(self, id_patient, freq):

        self.id_patient = id_patient
        self.freq = freq


def lengthFreqHR():
    arrObj = []
    for id in valid_id_Mimic:
        arr = dictsPatientHRFreg[id]
        obj = HRFreq(id,len(arr))
        arrObj.append(obj)
    return arrObj

def printResult(arr):
    for i in arr:
        print("Update Frequency of HR for patient_" + str(i.id_patient) + ": " + str(i.freq))
        # print(i.freq)

def freqOfHR():
    for id in valid_id_Mimic:
        arr = dictsPatient[id]
        for i in range(len(arr)-1):
            if (arr[i].HR != arr[i+1].HR):
                arrObj = dictsPatientHRFreg[id]
                arrObj.append(arr[i+1])
                dictsPatientHRFreg[id] = arrObj


freqOfHR()
res = lengthFreqHR()
res.sort(key=lambda x: x.freq, reverse=True)
printResult(res)