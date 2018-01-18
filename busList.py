import sys
import transitfeed
import optparse
from google.transit import gtfs_realtime_pb2
import urllib
import requests
import numpy as np
import os.path

def avgDelay(arr):
     avg = 0
     div = 0
     for x in arr:
        avg = avg + x.delay
        div = div + 1

     avg = avg / div
     return avg



def busCounter(arr,fNOne,fNTwo,fNThree):
    busLine = []
    busCount = []
    tripID = []
    busLine = alreadyCounter(fNOne,'str')
    busCount = alreadyCounter(fNTwo,'int')
    tripID = alreadyCounter(fNThree,'str')
    for x in arr:
        index = 0
        isIn = False
        alreadyCounted = False
        for y in tripID:
            if x.trip.trip_id == y:
                alreadyCounted = True
        if alreadyCounted == False:
            for a in busLine :
                if x.trip.route_id == a:
                    isIn = True
                    busCount[index] = busCount[index] + 1
                    tripID.append(x.trip.trip_id)
                index = index + 1
            if isIn == False:
                busLine.append(x.trip.route_id)
                tripID.append(x.trip.trip_id)
                busCount.append(1)
    pickler(busLine,fNOne)    
    pickler(busCount,fNTwo)
    pickler(tripID,fNThree)
   # alreadyCounter(fN)
   # check(fN,fN2)

def alreadyCounter(fN,type):
    arrNew = []
    if os.path.exists(fN):
        arrNew = np.loadtxt(fN,dtype = type,delimiter = ',')
        return arrNew.tolist()
    return arrNew

def check(fN, fN2):
    obj1 = []
    obj2 = []

    obj1 = readFrom(fN)
    obj2 = readFrom(fN2)

    for x in obj1:
        print x
    for y in obj2:
        print y

def pickler(arr,fileName):
    x = np.array(arr)
    np.savetxt(fileName,x,fmt = '%s',delimiter = ',')

def readFrom(fileName):
    objects = []
    with (open(fileName,'rb')) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects




def main():
  
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://gtfsrt.prod.obanyc.com/tripUpdates?key=<5f02572f-8d3a-40eb-9684-1d21fbf5265c>')
    feed.ParseFromString(response.content)
    arrayOfTrip = []
    for entity in feed.entity:
          if entity.HasField('trip_update'):
                  arrayOfTrip.append(entity.trip_update)
                  print entity

    avg = avgDelay(arrayOfTrip)
    print avg
    busCounter(arrayOfTrip,'busLines.txt','busCounts.txt','tripIDs.txt')
    


if __name__ == '__main__':
      main()

