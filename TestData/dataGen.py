import random
import numpy as np
import pandas as pd
from datetime import date, datetime

#definitions
startDate = date(2021,1,1)
endDate = date(2023,1,1)
endpoints = ["accounts", "balances", "beneficiaries", "direct-debits", "scheduled-payments", "statements", "transactions"]
maxUserGrowth = 20
noNewUsers = 0.5
dateRange = pd.date_range(startDate,endDate,freq='D')

#user creations
def nextUserSize(last):
    #30% chance of no change to user size, to biase towards fewer new users
    if random.random() < 0.5: return last

    newUsers = random.randint(0, maxUserGrowth)
    #next, add a random number of users
    return (last + newUsers)

def activeUsers(total):
    return (int(total * random.random()))

def generateUsers():
    #generate users
    natural = 0; corporate = 0

    naturals = []; activeNaturals = []; inactiveNaturals = []
    corporates = []; activeCorporates = []; inactiveCorporate = []
    total = []

    for currentDate in dateRange:
        #handle Naturals first
        active = activeUsers(natural)
        naturals.append(natural); activeNaturals.append(active); inactiveNaturals.append(natural - active)

        #handle Corporates next
        active = activeUsers(corporate)
        corporates.append(corporate); activeCorporates.append(active); inactiveCorporate.append(corporate - active)

        #sum totals
        total.append(natural + corporate)

        #refresh the numbers
        natural = nextUserSize(natural); corporate = nextUserSize(corporate)

    dict = {'date':dateRange, 'totalUsers':total, 'naturalUsers':naturals, 'corporateUsers':corporates, 'activeNaturalUsers':activeNaturals, 'inactiveNaturalUsers':inactiveNaturals, 'activeCorporateUsers':activeCorporates, 'inactiveCorporateUsers':inactiveCorporate}

    return(dict)

def generateCalls():
    callMax = 50000
    failMax = 0.1
    total = []; successful = []; failed = []

    for currentDate in dateRange:
        call = random.randint(0,callMax)
        fail = int(call * random.random() * failMax)
        total.append(call); successful.append(call-fail); failed.append(fail)

    dict = {'date':dateRange, 'total':total, 'successful':successful, 'failed':failed}
    return(dict)

def generateAuthentication():
    authMax = 5000
    failMax = 0.05
    total = []; successful = []; failed = []

    for currentDate in dateRange:
        auth = random.randint(0,authMax)
        fail = int(auth * random.random() * failMax)
        total.append(auth); successful.append(auth-fail); failed.append(fail)

    dict = {'date':dateRange, 'totalRequests':total, 'successfulRequests':successful, 'failedRequests':failed}
    return(dict)

def generateAuthentication():
    authMax = 5000
    failMax = 0.05
    total = []; successful = []; failed = []

    for currentDate in dateRange:
        auth = random.randint(0,authMax)
        fail = int(auth * random.random() * failMax)
        total.append(auth); successful.append(auth-fail); failed.append(fail)

    dict = {'date':dateRange, 'totalRequests':total, 'successfulRequests':successful, 'failedRequests':failed}
    return(dict)

def generateLatency():
    latencyMax = 5000
    latencyMin = 20
    latencyAverageCap = 200
    min = []; max = []; average = []

    for currentDate in dateRange:
        avgLatency = random.randint(latencyMin,latencyAverageCap)
        average.append(avgLatency)
        min.append(random.randint(latencyMin,avgLatency))
        max.append(random.randint(avgLatency, latencyMax))

    dict = {'date':dateRange, 'minimum':min, 'maximum':max, 'average':average}
    return(dict)

def generateDowntime():
    
    downtimeMin = 60
    downtimeMax = 5000
    total = []; incidents = []; average = []

    for currentDate in dateRange:

        #first roll to check if downtime has been met - assume a 99.9% uptime
        if (random.random()<0.999):
            total.append(0); incidents.append(0); average.append(0)
            print("downtime generated on "+ str(currentDate))
        else:
            #generate downtime
            downtime = random.randint(downtimeMin, downtimeMax)
            total.append(downtime)

            #next, set incidents in the day
            if (random.random()<0.8):
                incidents.append(1)
                average.append(downtime)
            elif (random.random()<0.6):
                incidents.append(2)
                average.append(downtime/2)
                print("two incidents generated on "+ str(currentDate))
            else:
                incidents.append(3)
                average.append(downtime/3)
                print("three incidents generated on "+ str(currentDate))

    dict = {'date':dateRange, 'total':total, 'numberIncidents':incidents, 'average':average}
    return(dict)

users = pd.DataFrame(generateUsers())
users.to_csv('testdata/users.csv')

for endpoint in endpoints:
    testData = pd.DataFrame(generateCalls())
    testData.to_csv('testdata/'+endpoint+'_calls.csv')

    testData = pd.DataFrame(generateAuthentication())
    testData.to_csv('testdata/'+endpoint+'_auth.csv')

    testData = pd.DataFrame(generateLatency())
    testData.to_csv('testdata/'+endpoint+'_latency.csv')

    testData = pd.DataFrame(generateDowntime())
    testData.to_csv('testdata/'+endpoint+'_downtime.csv')