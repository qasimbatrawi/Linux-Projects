class MedicalTests:

    def __init__(self):
        self.dictionary = {}

    def addTestToDictionary(self , fullTestName , shortTestName , minRange , maxRange , unit , turnAroundTime):
        #copy the values from the file to the dictionary
        #dict: {testname: LIST OF DATA}
        
        self.dictionary[shortTestName] = [fullTestName , minRange , maxRange , unit , turnAroundTime]

    def addTestToFile(self , fullTestName , shortTestName , minRange , maxRange , unit , turnAroundTime):
        #add test to file => used in option one (add new test) & option 4 (update medical test)
        file = open("medicalTest.txt" , "a")

        if minRange == "": #maybe min only, max only, both
            file.write(f"{fullTestName} ({shortTestName}); < {maxRange}; {unit}, {turnAroundTime}\n")
        elif maxRange == "":
            file.write(f"{fullTestName} ({shortTestName}); > {minRange}; {unit}, {turnAroundTime}\n")
        else:
            file.write(f"{fullTestName} ({shortTestName}); > {minRange}, < {maxRange}; {unit}, {turnAroundTime}\n")

        file.close()

    def AddFromFile(self , file): #used for filling the dictionary from the test file as the file format 

        self.dictionary.clear()

        for line in file:
            
            fullTestName = line.split(" (")[0]

            shortTestName = line.split("; ")[0]
            shortTestName = shortTestName.split(" (")[1]
            shortTestName = shortTestName.split(")")[0]

            minRange=""
            if ">" in line:
                minRange = line.split(" > ")[1]
                minRange = minRange.split(",")[0]
            
            maxRange=""
            if "<" in line:
                maxRange = line.split(" < ")[1]
                maxRange = maxRange.split(";")[0]

            unit = line.split("; ")[2]
            unit = unit.split(",")[0]

            if "<" not in line or ">" not in line:
                turnAroundTime = line.split(", ")[1]
            else:
                turnAroundTime = line.split(", ")[2]
            
            turnAroundTime = turnAroundTime.replace("\n" , "")

            self.addTestToDictionary(fullTestName , shortTestName , minRange , maxRange , unit , turnAroundTime)    


    def existFullTestName(self , fullTestName): #check if test exist based on full test name

        for name,data in self.dictionary.items():

            currentFullName = data[0]

            if currentFullName == fullTestName:
                return 1
        
        return 0
    
    def existShortTestName(self , shortTestName): #check if test exist based on short test name

        return shortTestName in self.dictionary.keys()
    

    
    def UpdateMedicalTest(self , testName , option , newMinValue , newMaxValue , newTime):
        #update medical test in both file and dictionary based on test name
        #three options to update: min,max,time
        #no need to update unit

        if int(option) == 1:
            if newMinValue > float(self.dictionary[testName][2]):
                print("\nInvalid. Min value is greater than the max.")
                return

            self.dictionary[testName][1] = str(newMinValue) #store the new min value in dic

        elif int(option) == 2:
            if newMaxValue < float(self.dictionary[testName][1]):
                print("\nInvalid. Max value is less than the min.")
                return

            self.dictionary[testName][2] = str(newMaxValue) #store the new max value in dic

        elif int(option) == 3:
            self.dictionary[testName][4] = str(newTime) #store the new turn around time in dic
        else:
            print("\nInvalid option.")

        # to clear the file
        file = open("medicalTest.txt" , "w")
        file.write("")
        file.close()

        print(self.dictionary)

        for shortName,data in self.dictionary.items():

            self.addTestToFile(data[0], shortName , data[1] , data[2] , data[3] , data[4]) #update the file
        
        print("\nTest has been updated.")

    
