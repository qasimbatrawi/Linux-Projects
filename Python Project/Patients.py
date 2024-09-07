from datetime import *
import csv

class Patients:

    def __init__(self):
        self.dictionary = {}   
    
    def addRecordToDictionary(self , id , testName , BeginDateTime , result , unit , status , EndDateTime): #copy the data from the file to the dictionary
        ####### its used after AddFromFile to take the whole record and split it to seperate data ######
        if id in self.dictionary: #if the id already exist: add to its list of list
            self.dictionary[id].append([testName , BeginDateTime , result , unit , status , EndDateTime])
        else:
            self.dictionary.update({id:[]}) #else: create new key and list of list
            self.dictionary[id].append([testName , BeginDateTime , result , unit , status , EndDateTime])

    def addToFile(self , id , testname , BeginDateTime , result , unit , status , EndDateTime):
        #used to copy the dictionary to the file at the end of the program
        file = open("medicalRecord.txt" , "a")

        if EndDateTime == "": #as file format
            file.write(f"{id}: {testname}, {BeginDateTime}, {result}, {unit}, {status}\n")
        else:
            file.write(f"{id}: {testname}, {BeginDateTime}, {result}, {unit}, {status}, {EndDateTime}\n")

        file.close()


    def AddFromFile(self , file):
        #take the whole record and split it to seperate data

        self.dictionary.clear()

        for i in file:

            if i == '\n':
                continue

            id = i.split(":")[0]

            testName = i.split(": ")[1].split(",")[0]

            BeginDateTime = i.split(", ")[1]

            result = i.split(", ")[2]

            unit = i.split(", ")[3]

            status = i.split(", ")[4]

            EndDateTime = ""

            if status == "completed":
                EndDateTime = i.split(", ")[5]
                EndDateTime = EndDateTime.replace("\n" , "")
            else:
                status = status.replace("\n" , "")
            
            self.addRecordToDictionary(id , testName , BeginDateTime , result , unit , status , EndDateTime)

    def addDictionaryToFile(self):
        #used at the end of the program to copy all the edits to the file

        file = open("medicalRecord.txt" , "w")
        file.write("")
        file.close()

        for id,ListOfList in self.dictionary.items():

            for List in ListOfList:

                self.addToFile(id , List[0] , List[1] , List[2] , List[3] , List[4] , List[5])


    def FilterTestName(self , testName): #get tests based on testname

        Set = set()

        for id,ListOfList in self.dictionary.items():
            
            for data in ListOfList:
                currentTestName = data[0]

                if currentTestName == testName:

                    if data[4] == "completed":
                        newLine = f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}"
                    else:
                        newLine = f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}"
                    
                    Set.add(newLine) #return set for intersection (combination filter)

        return Set
    
    def FilterAbnormalTest(self , test): #get all abnormal tests
        #it takes test object to access the test dictionary to get min & max ranges
        Set = set()

        for id,ListOfList in self.dictionary.items():

            for data in ListOfList:

                currentResult = data[2]
                currentTestName = data[0]

                minRange = test.dictionary[currentTestName][1]
                maxRange = test.dictionary[currentTestName][2]

                if minRange == "":
                    minRange = -10000000000000
                elif maxRange == "":
                    maxRange = 10000000000000

                minRange = float(minRange)
                maxRange = float(maxRange)

                currentResult = float(currentResult)

                if currentResult < minRange or currentResult > maxRange:
                    
                    if data[4] == "completed":
                        newLine = f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}"
                    else:
                        newLine = f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}"
                    
                    Set.add(newLine)
                
        return Set #return set for intersection (combination filter)
    
    def FilterStatus(self , status):

        Set = set()

        for id,ListOfList in self.dictionary.items():

            for data in ListOfList:
                
                currentStatus = data[4]

                if currentStatus == status:
                    if data[4] == "completed":
                        newLine = f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}"
                    else:
                        newLine = f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}"
                    
                    Set.add(newLine)

        return Set #return set for intersection (combination filter)
    
    def TurnAroundTimeStatics(self , List , test): #statistics of turn around time

        status = "pending"

        for data in List: # loop to check if there is a single completed test
            
            currnetStatus = status = data.split(", ")[4]

            if currnetStatus == "completed": 
                status = "completed"
                break

        if status == "pending":
            print("\nAll test records are pending. Currently, there are no turn around time for the above tests.")

        else:
            # we will convert all units to minute, so it will be more simple to calc the average, min and max
            minMinutes=1000000000000000 # to store the minimum time needed
            maxMinutes=0 # to store the maximum time needed
            totalSumMinutes=0 # this is for the averge
            counter=0 # counter for the average

            minTest="" # store the min test
            maxTest="" # store the max test

            for data in List:

                id = data.split(":")[0]

                testName = data.split(": ")[1].split(",")[0]

                currnetStatus = data.split(", ")[4]

                if currnetStatus == "completed":
                    counter+=1

                    # we will take the turnaround time from the medical test, insted of subtracting EndDate-startDate
                    time = test.dictionary[testName][4] 

                    day = int(time.split("-")[0])
                    hour = int(time.split("-")[1])
                    minute = int(time.split("-")[2])

                    currentMinutesSum = day*24*60 + hour*60 + minute # convert to minutes

                    if currentMinutesSum < minMinutes:
                        minMinutes = currentMinutesSum
                        minTest = data
                    
                    if currentMinutesSum > maxMinutes:
                        maxMinutes = currentMinutesSum
                        maxTest = data

                    totalSumMinutes+=currentMinutesSum


            # calc the average
            totalSumMinutes = totalSumMinutes//counter

            days = totalSumMinutes//(24*60) # number of days needed
            totalSumMinutes = totalSumMinutes%(24*60) # بنخزن الباقي تبع العملية الي فوق

            hours = totalSumMinutes//60 # number of hours needed
            totalSumMinutes = totalSumMinutes%60

            minutes = totalSumMinutes

            print(f"\nMinimum turnaround time test: {minTest}\nMaximum turnaroundTime test: {maxTest}\nAverage turnaround time: {days}-{hours}-{minutes}")


    def periodFilter(self , mindate , maxdate): #get all tests in this period of time
        
        myset = set()
        #splitting the start date
        minyear=int(mindate.split("-")[0]) 
        minmonth=int(mindate.split("-")[1])
        minday=int(mindate.split("-")[2])

        #splitting the end date
        maxyear=int(maxdate.split("-")[0])
        maxmonth=int(maxdate.split("-")[1])
        maxday=int(maxdate.split("-")[2])

        #creating date objects for comparing
        mindate = date(minyear , minmonth , minday)
        maxdate = date(maxyear , maxmonth , maxday) 

        for id,ListOfList in self.dictionary.items():

            for data in ListOfList:

                testdate = data[1].split()[0] #gat the date of test without time

                #splitting the test date
                year=int(testdate.split("-")[0])
                month=int(testdate.split("-")[1])
                day=int(testdate.split("-")[2])

                currentDate = date(year , month , day) #test date

                if currentDate >= mindate and currentDate <= maxdate:

                    newLine=""
                    
                    if data[4] == "completed":
                        newLine = f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}"
                    else:
                        newLine = f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}"
                    
                    myset.add(newLine)

        return myset #return set for intersection (combination filter)


    def idFilter(self , id):

        myset=set()

        for ID,ListOfList in self.dictionary.items():
               
               for data in ListOfList:

                    if int(ID) == int(id):

                        if data[4]=="completed":
                            text=f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}"
                        else:
                             text=f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}"

                        myset.add(text)

        return myset #return set for intersection (combination filter)
    
    
    def TurnAroundFilter(self , minvalue,maxvalue,test): 
        #get all tests has excution time between two values
        #test object is used to access turnaround time in its dictionary
        
        #splitting start and end values, then creating date objects for comparing
        min_days=int(minvalue.split("-")[0]) #plus 1 for using the date object (cant be zero)
        min_hours=int(minvalue.split("-")[1])
        min_minutes=int(minvalue.split("-")[2])
        
        max_days=int(maxvalue.split("-")[0])
        max_hours=int(maxvalue.split("-")[1])
        max_minutes=int(maxvalue.split("-")[2])

        minSumMinutes = min_days*60*24 + min_hours*60 + min_minutes

        maxSumMinutes = max_days*60*24 + max_hours*60 + max_minutes

        myset=set()

        for id,listOflist in self.dictionary.items():

            for data in listOflist:

                testname = data[0]
                status = data[4]

                if status == "completed": #must be completed for turn around time

                    turnaroundtime=test.dictionary[testname][4]

                    days=int(turnaroundtime.split("-")[0])
                    hours=int(turnaroundtime.split("-")[1])
                    minutes=int(turnaroundtime.split("-")[2])

                    currentSumMinutes = days*24*60 + hours*60 + minutes

                    if minSumMinutes <= currentSumMinutes and currentSumMinutes <= maxSumMinutes:
                        text=f"{id}: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}"
                        myset.add(text)

        return myset
    

    def MinMaxAverage(self, l1 , test): #statistics

        tempDic = {} #temp dictionary too store the number of specific test and its total result

        for line in l1:

            testname = line.split(",")[0].split(": ")[1] #get test name
            result = float(line.split(", ")[2]) #get test result

            if testname in tempDic: #if already exist

                tempDic[testname][0]+=1 #counter of tests
                tempDic[testname][1]+=result #calculating the total test results (sum)
                tempDic[testname][2] = min(tempDic[testname][2] , result) #store the min value between past and mew results 
                tempDic[testname][3] = max(tempDic[testname][3] , result) # same for max

            else:

                tempDic.update({testname:[]}) #create new key and list of values
                tempDic[testname].append(1) #number of this test initially 1
                tempDic[testname].append(result) #result in index 1
                tempDic[testname].append(result) # min in index 2
                tempDic[testname].append(result) # max in index 3


        for testName,List in tempDic.items():

            print(f"The minimum value of {testName}: {List[2]}") #min
            print(f"The maximum value of {testName}: {List[3]}") #max
            print(f"The avearge value of {testName}: {List[1]/List[0]}\n") #calculate average   

        del tempDic    
        
    def FindIdTestNameResult(self , id , shortTestName , result): #used for updaing record based on id and result and test name (option 3 in menu)

        for List in self.dictionary[id]:

            if List[0] == shortTestName and List[2] == result:
               return 1
                
        return 0
    
    def updateRecord(self , id , oldShortTestName , oldResult , newShortTestName , newBeginDate , newResult , unit , newStatus , newEndDateTime):
        #Updaing record based on id and result and test name (option 3 in menu)
        for List in self.dictionary[id]:

            if List[0] == oldShortTestName and List[2] == oldResult:
                
                List[0] = newShortTestName
                List[1] = newBeginDate
                List[2] = newResult
                List[3] = unit
                List[4] = newStatus
                List[5] = newEndDateTime

                return
    

    def ExportCSV(self):
        Exportfile = "RECORDS.csv"

        Matrix = [] #the matrix to be exported
        for id,ListOfList in self.dictionary.items():

            for records in ListOfList:
                tempList = []
                #add all the record fields to the templist
                tempList.append(id)
                tempList.append(records[0])
                tempList.append(records[1])
                tempList.append(records[2])
                tempList.append(records[3])
                tempList.append(records[4])
                tempList.append(records[5])

                Matrix.append(tempList) #add templist to matrix

            with open(Exportfile, 'w') as csvfile: 
             csvwriter = csv.writer(csvfile) #object writer
             csvwriter.writerow(Matrix)  
            

            csvfile.close()
   

    def ImportCSV(self):

        with open('RECORDS.csv', 'r') as csvfile:
          csvreader = csv.reader(csvfile) #object reader

          for row in csvreader:
                print(row)

        csvfile.close()





                

    

    
          
