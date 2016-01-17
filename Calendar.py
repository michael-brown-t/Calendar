#This program will allow a user to create, read, and delete calendar entries
#This version does not have input validation or results formatting implemented. So a user can input end dates before start dates
#and there is nothing to guide a user to correct any incorrect inputs

import os
import sqlite3
import datetime
from datetime import timedelta

DBPATH = 'calendar.db'
conn = sqlite3.connect(DBPATH)
cursor = conn.cursor()

CreateTable = "CREATE TABLE IF NOT EXISTS tbl_events (id INTEGER PRIMARY KEY AUTOINCREMENT, fldEventName TEXT, fldStartDate TEXT, fldEndDate TEXT, fldDuration TEXT)"
#varID=""
conn.execute(CreateTable)

#Create menu to determine what user would like to do
def CollectUserInput ():
    print ("-----")
    print ("Select an Option:")
    print ("1 - Add new calendar entry")
    print ("2 - View agenda for a date range")
    print ("3 - View today's agenda")
    print ("4 - Delete an entry")
    print ("5 - Exit the program")
    print ("-----")
    print ("")
    OptionSelect = raw_input("Enter your selection:  ")
    return OptionSelect

#Add new calendar entry into database
def AddNew ():
    varEventName = raw_input("Enter Event Name:  ")
    
    StartDate = raw_input("Enter event start date mm/dd/yyyy:  ")
    varStartDate = datetime.datetime.strptime(StartDate, "%m/%d/%Y")
    
    StartTime = raw_input("Enter Start time HH:MM:AM  ")
    varStartTime = datetime.datetime.strptime(StartTime, "%I:%M:%p")

    CombinedStart = StartDate + "-" + StartTime
    varCombinedStart = datetime.datetime.strptime(CombinedStart, "%m/%d/%Y-%I:%M:%p")

    EndDate = raw_input("Enter event end date mm/dd/yyyy:  ")
    varEndDate = datetime.datetime.strptime(EndDate, "%m/%d/%Y")

    EndTime = raw_input("Enter End time HH:MM:AM  ")
    varEndTime = datetime.datetime.strptime(EndTime, "%I:%M:%p")
    
    CombinedEnd = EndDate + "-" + EndTime
    varCombinedEnd = datetime.datetime.strptime(CombinedEnd, "%m/%d/%Y-%I:%M:%p")
    
    varDuration = str(varCombinedEnd - varCombinedStart)
    
    sql = "INSERT INTO tbl_events (fldEventName, fldStartDate, fldEndDate, fldDuration) VALUES (?, ?, ?, ?)"
    conn.execute(sql, (varEventName, varCombinedStart, varCombinedEnd, varDuration))
    conn.commit()

    print ("")
    print ("You have successfully entered a calendar entry for date....")
    
# Look at calendar entries for a given date range
def ViewAgenda():
    print("-----")
    StartRange = raw_input("Enter the START of your date range (mm/dd/yyyy):  ")
    varStartRange = datetime.datetime.strptime(StartRange, "%m/%d/%Y")
    EndRange = raw_input("Enter the END of your date range (mm/dd/yyyy):  ")
    varEndRange = datetime.datetime.strptime(EndRange, "%m/%d/%Y")
    print("-----")
    
    for row in cursor.execute("SELECT id, fldEventName, fldStartDate, fldEndDate, fldDuration FROM tbl_events WHERE fldStartDate between ? and ? ORDER BY fldStartDate", (varStartRange,varEndRange)):
        print row

# Prints all calendar entries that are taking place on the current day
def ViewToday():
    print("-----")
    print("")
    
    TodayDate = (datetime.date.today())
    print "Your agenda for " + str(TodayDate) +":"
    
    print("")
    
    for row in cursor.execute("SELECT id, fldEventName, fldStartDate, fldEndDate, fldDuration FROM tbl_events WHERE fldStartDate<=? AND fldEndDate>=?", (TodayDate, TodayDate, )):
        print row

# Removes a calendar entry from the database based on the id selected
def DeleteEntry():
    print("")
    print("-----")
    print("Let's first find the entry you would like to delete...")
    ViewAgenda()    
    RowToDelete = raw_input("Enter the ID for the calendar entry that you would like to delete:  ")
    conn.execute("DELETE FROM tbl_events WHERE id=?", (RowToDelete, ));
    conn.commit()
    print("row deleted")
    print("")

# Exits the program and closes database connection
def ExitProgram():
    print ("-----")
    print "Thank you for using the calendar program, good-bye!"
    print ("")
    conn.close()
    exit()
#---------------------------------------------------------------
#*****Program flow: Obtain user input and select the appropriate function
#---------------------------------------------------------------
varSelectedChoice = int(CollectUserInput())

while varSelectedChoice <= 5:
    if varSelectedChoice == 1:
        AddNew()
    elif varSelectedChoice == 2:
        ViewAgenda()
    elif varSelectedChoice == 3:
        ViewToday()
    elif varSelectedChoice == 4:
        DeleteEntry()
    elif varSelectedChoice == 5:
        ExitProgram()
    
    print ("")
    print ("-----")
    varContinue = raw_input("Would you like another transaction? Y-to continue, or any key to exit:  ")
    if varContinue == "Y":
        varSelectedChoice = int(CollectUserInput())
    else:
        ExitProgram()