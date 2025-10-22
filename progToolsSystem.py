import os

fileName= "dataset.txt"

if not os.path.exists(fileName):
    open(fileName, 'w').close()

def getLastId(file):
    lastId = -1 #start below 0 incase file is empty
    with open(file, 'r') as f:
        for line in f:
            try:
                parts = line.strip().split('\t')
                if parts and parts[0].isdigit():
                    lastId = max(lastId, int(parts[0]))
            except(ValueError, IndexError):
                continue
    return lastId

lastId = getLastId(fileName)
identificationNumber = (lastId+1) if isinstance(lastId, int) else 0

def searchFile(file, textToSearch):
    found = False

    with open(file, 'r') as f: #open file in read more with f as its pointer
        for i, line in enumerate(f):  #enumerate to make sure it doesnt load the entire file in memory
            if textToSearch in line:
                print(line)
                found = True
                break
    if not found:
        print("Record not found")

            
def addRecord(file, callerName, phoneNumber):
    global identificationNumber

    with open(file, 'a') as f: #open file in append mode with f as its pointer
        f.write(f"{identificationNumber:04d}\t\t{callerName}\t\t\t\t{phoneNumber}\n")
        identificationNumber+=1
        print("Record added successfully")

def deleteRecord(file, idToDelete):
    found = False

    with open(file, 'r') as f:
        lines = f.readlines()

    with open(file, 'w') as f:
        for line in lines:
            parts = line.strip().split('\t')
            if parts and parts[0] == idToDelete:
                found = True
                continue
            f.write(line)
    if found:
        print("Record has been deleted successfully")
    else:
        print("Record not found")

while True:
    print("1. Add a Record")
    print("2. Delete a Record")
    print("3. Search for a Record")
    print("4. Exit")

    ch = input("Enter Choice: ")

    if ch == "1":
        callerName = input("Enter Caller Name: ")
        phoneNumber = input("Enter Caller Number: ")
        addRecord(fileName, callerName, phoneNumber)

    elif ch == "2":
        toDelete = input("Enter the ID of the record you want to delete: ")
        deleteRecord(fileName, toDelete)

    elif ch == "3":
        toSearch = input("Enter the name of the person record you want to see the record of: ")
        searchFile(fileName, toSearch)

    elif ch == "4":
        break
    else:
        print("Wrong Choice!!")

    #os.system("pause")
    #os.system("cls")

