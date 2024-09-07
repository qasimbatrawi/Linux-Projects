from MedicalTests import *
from Patients import *
from datetime import * 


def displayMenu():

    print("""\n1- Add new medical Test.
2- Add new medical Record.
3- Update patient records including all fields.
4- Update medicalt test in the medical test file.
5- Filter medical tests.
6- Generate textual summary report.
7- Export medical records to a comma separated file. 
8- Import medical records from a comma separated file.
9- Exit.\n""")
    
def displayFliterMenu():

    print("""\n1- Patient id.
2- Test name.
3- Abnormal tests.
4- Test added to the system within a spesific period.
5- Test status.
6- Test turnaround time within a period.
7- Exit\n""")
    
def displayRangeMenu():

    print("""\n1- Only minimum value.
2- Only maximum vlaue.
3- Both minimum and maximum.\n""")
    
def checkFloat(num):

    try:
        temp = float(num)
    except:
        return 0
    
    return 1

def checkInt(num):

    try:
        temp = int(num)
    except:
        return 0
    
    return 1

patient = Patients()
test = MedicalTests()

#check file names input
while 1:
    filename = input("Please enter the medical record file name: ")
    f=""
    try:
        f=open(filename,"r+")
    except:
        print("File does not exist...")
        continue
    
    if filename=="medicalRecord.txt":
        f.close()
        break    

print("")
while 1:
    filename = input("Please enter the medical test file name: ")
    f=""
    try:
        f=open(filename,"r+")
    except:
        print("File does not exist...")
        continue
    
    if filename=="medicalTest.txt":
        f.close()
        break        


recordFile = open("medicalRecord.txt" , "r+")
testFile = open("medicalTest.txt" , "r+")

#initially clearing the dictionaries
patient.dictionary.clear()
test.dictionary.clear()

#filling the dictionaries from the files
patient.AddFromFile(recordFile)
test.AddFromFile(testFile)

testFile.close()
recordFile.close()

print("\nWelcome to our Program.")

option=0 #menu

EXPORTED=0 #to checkk if exported before import (option 7/8)
while 1:
    
    displayMenu()
    option = input("Please choose one of the options above from 1-9: ")
    if checkInt(option) == 0:
        print("\nInvalid option.")
        continue

    option = int(option)
    
    if option == 1: #add medical test to dic & file
        
        #check valid inputs
        fullTestName = input("\nEnter the full test name: ")
        if test.existFullTestName(fullTestName) == 1:
            print("\nTest is already in the medical test.")
            continue
        
        shortTestName = input("Enter the short test name: ")
        if test.existShortTestName(shortTestName) == 1:
            print("\nTest is already in the medical test.")
            continue

        minRange=""
        maxRange=""
        
        displayRangeMenu() #some tests has only min, only max, or both
        newOption = input("Choose the type of range you want: ")
        if checkInt(newOption) == 0:
            print("\nInvalid type.")
            continue
        
        newOption = int(newOption)
        if newOption == 1:
            minRange = input("\nEnter the minimum range: ")
            if checkFloat(minRange) == 0 and checkInt(minRange) == 0:
                print("\nInvalid minimum range.")
                continue

        elif newOption == 2:
            maxRange = input("\nEnter the maximum range: ")
            if checkFloat(maxRange) == 0 and checkInt(maxRange) == 0:
                print("\nInvalid maximum range.")
                continue

        elif newOption == 3:
            minRange = input("\nEnter the minimum range: ")
            if checkFloat(minRange) == 0 and checkInt(minRange) == 0:
                print("\nInvalid minimum range.")
                continue

            maxRange = input("Enter the maximum range: ")
            if checkFloat(maxRange) == 0 and checkInt(maxRange) == 0:
                print("\nInvalid maximum range.")
                continue

            if float(minRange) > float(maxRange):
                print("\nInvalid range. Minimum is greater than the maximum")
                continue

        else:
            print("\nInvalid type.")
            continue

        unit = input("Enter the unit of the test: ")

        time = input("Enter the turnaround time of the test (DD-HH-MM): ")
            
        List = time.split("-")
        if len(List) != 3: #DD:HH:MM
            print("\nInvalid turnaround time.")
            continue
        elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0 or checkInt(List[2]) == 0:
            print("\nInvalid turnaround time.")
            continue
        elif int(List[0]) > 99 or int(List[1]) > 24 or int(List[2]) > 60:
            print("\nInvalid turnaround time.")
            continue

        test.addTestToDictionary(fullTestName , shortTestName , minRange , maxRange , unit , time)
        test.addTestToFile(fullTestName , shortTestName , minRange , maxRange , unit , time)

        print("\nTest has been added.")

    elif option == 2: #add new test record
        
        id = input("Enter the id from 7 digits: ")
        if checkInt(id) == 0 or len(id) != 7: #check if 7
            print("\nInvalid id.")
            continue

        shortTestName = input("Enter the test name: ")
        if test.existShortTestName(shortTestName) == 0:
            print("\nTest does not exist in the medical test.")
            continue

        unit = test.dictionary[shortTestName][3] #take the unit from the test file

        result = input("Enter the result of the test: ")
        if checkInt(result) == 0 and checkFloat(result) == 0:
            print("\nInvalid test result.")
            continue

        status = input("Enter the status of the test: ")
        if status != "completed" and status != "pending":
            print("\nInvalid status.")
            continue
        
        BeginDate = input("Enter the begin date: ")

        #check valid

        try:
            date = BeginDate.split()[0]
            time = BeginDate.split()[1]
        except:
            print("\nInvalid date and time.")
            continue
        
        List = date.split("-")

        if len(List) != 3:
            print("\nInvalid date.")
            continue
        elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0 or checkInt(List[2]) == 0:
            print("\nInvalid date.")
            continue
        elif int(List[1]) > 12 or int(List[1]) < 1 or int(List[2]) > 31 or int(List[2]) < 1:
            print("\nInvalid date.")
            continue
        elif int(List[1]) == 2 and int(List[2]) > 29:
            print("\nInvalid date.")
            continue

        List = time.split(":")
        if len(List) != 2:
            print("\nInvalid time.")
            continue
        elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0:
            print("\nInvalid time.")
            continue
        elif int(List[0]) > 23 or int(List[1]) > 59:
            print("\nInvalid time.")
            continue

        currentDateTime = datetime.now() #get the current date

        tempBeginDate = datetime.strptime(BeginDate , "%Y-%m-%d %H:%M") #make it as this format for comparing

        if tempBeginDate > currentDateTime:
            print("\nInput begin date and time is greater than current date and time.")
            continue

        EndDateTime=""
        if status == "completed": #turn around time only for completed
            turnAroundTime = test.dictionary[shortTestName][4] #take the turn around time from the test file

            day = int(turnAroundTime.split("-")[0])
            hour = int(turnAroundTime.split("-")[1])
            minute = int(turnAroundTime.split("-")[2])

            EndDateTime = tempBeginDate + timedelta(days=day , hours=hour , minutes=minute) #add the turn around time to the begin date

            EndDateTime = EndDateTime.strftime("%Y-%m-%d %H:%M") #casting with format

            tempEndDate = datetime.strptime(EndDateTime , "%Y-%m-%d %H:%M") #used for comparing with the current time to check invalid inputs

            if tempEndDate > currentDateTime:
                print("\nInput end date and time is greater than current date and time.")
                continue

        # it will insert to dictionary not the file, at the end of the program => insert to file
        patient.addRecordToDictionary(id , shortTestName , BeginDate , result , unit , status , EndDateTime)

        print("\nRecord has been added")

    elif option == 3: #update record including all fields based on id and test name and result :) (we will not change the id)
        
        id = input("\nEnter the id of the patient you want to update: ")
        if checkInt(id) == 0 or len(id) != 7:
            print("\nInvalid id.")
            continue
        if id not in patient.dictionary:
            print("\nId does not exist in the record.")
            continue

        oldShortTestName = input("Enter the test name: ")
        if test.existShortTestName(oldShortTestName) == 0:
            print("\nTest does not exist in the medical test.")
            continue

        oldResult = input("Enter the result of the test: ")
        if checkInt(oldResult) == 0 and checkFloat(oldResult) == 0:
            print("\nInvalid test result.")
            continue
    
        exist = patient.FindIdTestNameResult(id , oldShortTestName , oldResult)

        if exist == 0:
            print("This test does not exist in the record.")
            continue

        #ENTER THE NEW VALUESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSs :)

        newShortTestName = input("\nEnter the new test name: ")
        if test.existShortTestName(newShortTestName) == 0:
            print("\nTest does not exist in the medical test.")
            continue

        unit = test.dictionary[newShortTestName][3]  #take unit from test file

        newResult = input("Enter the new result of the test: ")
        if checkInt(newResult) == 0 and checkFloat(newResult) == 0:
            print("\nInvalid test result.")
            continue

        newStatus = input("Enter the new status of the test: ")
        if newStatus != "completed" and newStatus != "pending":
            print("\nInvalid status.")
            continue
        
        newBeginDate = input("Enter the new begin date: ")

        #check valid

        try:
            date = newBeginDate.split()[0]
            time = newBeginDate.split()[1]
        except:
            print("\nInvalid date.")
            continue
        
        List = date.split("-")

        if len(List) != 3:
            print("\nInvalid date.")
            continue
        elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0 or checkInt(List[2]) == 0:
            print("\nInvalid date.")
            continue
        elif int(List[1]) > 12 or int(List[1]) < 1 or int(List[2]) > 31 or int(List[2]) < 1:
            print("\nInvalid date.")
            continue
        elif int(List[1]) == 2 and int(List[2]) > 29:
            print("\nInvalid date.")
            continue
        
        List = time.split(":")
        if len(List) != 2:
            print("\nInvalid time.")
            continue
        elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0:
            print("\nInvalid time.")
            continue
        elif int(List[0]) > 23 or int(List[1]) > 59:
            print("\nInvalid time.")
            continue

        currentDateTime = datetime.now()

        tempBeginDate = datetime.strptime(newBeginDate , "%Y-%m-%d %H:%M")

        if tempBeginDate > currentDateTime:
            print("\nInput begin date and time is greater than current date and time.")
            continue

        newEndDateTime=""
        if newStatus == "completed":
            turnAroundTime = test.dictionary[newShortTestName][4]

            day = int(turnAroundTime.split("-")[0])
            hour = int(turnAroundTime.split("-")[1])
            minute = int(turnAroundTime.split("-")[2])

            newEndDateTime = tempBeginDate + timedelta(days=day , hours=hour , minutes=minute)

            newEndDateTime = newEndDateTime.strftime("%Y-%m-%d %H:%M")

            tempEndDate = datetime.strptime(newEndDateTime , "%Y-%m-%d %H:%M")

            if tempEndDate > currentDateTime:
                print("\nInput end date and time is greater than current date and time.")
                continue

        patient.updateRecord(id , oldShortTestName , oldResult , newShortTestName , newBeginDate , newResult , unit , newStatus , newEndDateTime)

        print("\Record has been updated.")

    elif option == 4: #Update medical test in test file based on test name

        testName = input("\nPlease enter the short test name you want to update: ")
        if test.existShortTestName(testName) == 0:
            print("\nTest does not exist in the medical test.")
            continue

        print("\n1-Minimum range")
        print("2-Maximum range")
        print("3-Turn around time\n")

        newOption = input("Please enter which property you want to change: ")
        if checkInt(newOption) == 0:
            print("\nInvalid type.")
            continue
        
        newOption = int(newOption)

        newMinValue=""
        newMaxValue=""
        newTime=""

        if newOption == 1:
            newMinValue=input("Please enter the new min value: ")
            if checkFloat(newMinValue) == 0 and checkInt(newMinValue) == 0:
                print("\nInvalid minimum range.")
                continue
            newMinValue = float(newMinValue)

        elif newOption == 2:
            newMaxValue=input("Please enter the new max value: ")
            if checkFloat(newMaxValue) == 0 and checkInt(newMaxValue) == 0:
                print("\nInvalid minimum range.")
                continue
            newMaxValue = float(newMaxValue)

        elif newOption == 3:

            newTime=input("Please enter the new turnaroundtime: ")

            List = newTime.split("-")
            if len(List) != 3:
                print("\nInvalid turnaround time.")
                continue
            elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0 or checkInt(List[2]) == 0:
                print("\nInvalid turnaround time.")
                continue
            elif int(List[0]) > 99 or int(List[1]) > 24 or int(List[2]) > 60:
                print("\nInvalid turnaround time.")
                continue

        else:
            print("\nInvalid option.")
            continue

        test.UpdateMedicalTest(testName , newOption , newMinValue , newMaxValue , newTime)


    elif option == 5 or option == 6: #filter & statistics 
        
        LIST = [] # to store sets in it

        while 1:

            displayFliterMenu()

            newOption = input("Please choose a combination of the options from 1-7: ")
            if checkInt(newOption) == 0:
                print("\nInvalid option.")
                continue

            newOption = int(newOption)

            if newOption == 1: #id
                
                id = input("\nEnter the id of the patient: ")
                if checkInt(id) == 0 or len(id) != 7:
                    print("\nInvalid id.")
                    continue
                if id not in patient.dictionary:
                    print("\nId does not exist in the record.")
                    continue

                LIST.append(patient.idFilter(id)) #add this id tests to the list (this method returns a set)

            elif newOption == 2: #testname

                testName = input("\nPlease enter the test name: ")

                if test.existShortTestName(testName) == 0:
                    print("\nTest is not in the medical test")
                    continue
                
                LIST.append(patient.FilterTestName(testName)) # this methods return a set, we will insert it to the LIST to make intersection at the end

            elif newOption == 3: #abnormal

                LIST.append(patient.FilterAbnormalTest(test))

            elif newOption == 4: #period of time

                StartDate = input("\nEnter the start date: ") # without time (given in project description)
                
                List = StartDate.split("-")

                if len(List) != 3:
                    print("\nInvalid date.")
                    continue
                elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0 or checkInt(List[2]) == 0:
                    print("\nInvalid date.")
                    continue
                elif int(List[1]) > 12 or int(List[1]) < 1 or int(List[2]) > 31 or int(List[2]) < 1:
                    print("\nInvalid date.")
                    continue
                elif int(List[1]) == 2 and int(List[2]) > 29:
                    print("\nInvalid date.")
                    continue
                
                EndDate = input("Enter the end date: ") # without time
                
                List = EndDate.split("-")

                if len(List) != 3:
                    print("\nInvalid date.")
                    continue
                elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0 or checkInt(List[2]) == 0:
                    print("\nInvalid date.")
                    continue
                elif int(List[1]) > 12 or int(List[1]) < 1 or int(List[2]) > 31 or int(List[2]) < 1:
                    print("\nInvalid date.")
                    continue
                elif int(List[1]) == 2 and int(List[2]) > 29:
                    print("\nInvalid date.")
                    continue

                LIST.append(patient.periodFilter(StartDate , EndDate)) #add all tests in this period of time

            elif newOption == 5: #status

                status = input("\nEnter the status you want: ")

                if status != "completed" and status != "pending":
                    print("\nInvalid status.")

                else:
                    LIST.append(patient.FilterStatus(status))
                
            elif newOption == 6: # the test status must be completed
                
                StartTime = input("\nEnter the min turnaround time of the test (DD-HH-MM): ")
            
                List = StartTime.split("-")

                if len(List) != 3:
                    print("\nInvalid turnaround time.")
                    continue
                elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0 or checkInt(List[2]) == 0:
                    print("\nInvalid turnaround time.")
                    continue
                elif int(List[0]) > 99 or int(List[1]) > 24 or int(List[2]) > 60:
                    print("\nInvalid turnaround time.")
                    continue

                EndTime = input("Enter the max turnaround time of the test (DD-HH-MM): ")
            
                List = StartTime.split("-")

                if len(List) != 3:
                    print("\nInvalid turnaround time.")
                    continue
                elif checkInt(List[0]) == 0 or checkInt(List[1]) == 0 or checkInt(List[2]) == 0:
                    print("\nInvalid turnaround time.")
                    continue
                elif int(List[0]) > 99 or int(List[1]) > 24 or int(List[2]) > 60:
                    print("\nInvalid turnaround time.")
                    continue

                LIST.append(patient.TurnAroundFilter(StartTime , EndTime , test))

            elif newOption == 7: #exit and check intersection
                
                if len(LIST) == 0:
                    print("\nNo data chose.") #if exit without any other options
                else:
                    FinalSet = LIST[0]

                    i=1
                    while i < len(LIST): #trace the list and store the intersection between tests
                        FinalSet = FinalSet.intersection(LIST[i])
                        i=i+1

                    if len(FinalSet) == 0: #if no intersection
                        print("\nThere are no data for the entered combination.")
                    else:

                        print("")

                        for i in FinalSet: #print them
                            print(i)

                        if option == 6: #statistics
                            print("")
                            patient.MinMaxAverage(list(FinalSet) , test)
                            patient.TurnAroundTimeStatics(list(FinalSet) , test)
                break
            
                
            else:
                print("\nInvalid option.")

    elif option == 7: #export to csv file

        patient.ExportCSV()
        EXPORTED=1
        print("\nRecords has been exported successfully.")


    elif option == 8: #import only if exported

        if EXPORTED == 1:
            print("")
            patient.ImportCSV()
        else:
            print("\nCan't import... Export records first.")    
            


    elif option == 9:
        break 

    else:
        print("\nInvalid option.")


print("\nThank you for using our program. Goodbye\n.")

patient.addDictionaryToFile() #store the dictionary to the file after all edits