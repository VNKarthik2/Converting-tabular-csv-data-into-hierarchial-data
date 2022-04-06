import pandas as pd
import numpy as np
import os, json

SOURCE_FILE = os.path.join(".", "hierarchy_case_20May2020.csv")
DESCINATION_FILE = os.path.join(".", "output.json")

read_file = pd.read_excel (r'hierarchy_case_20May2020.xlsx')
read_file.to_csv (r'hierarchy_case_20May2020.csv', index = None, header=True)

CEO_BOSS = "none"

class Employee:
    def __init__(self, EMPLOYEE_ID, DESIGNATION, DEPARTMENT, NAME, MANAGER_EMPLOYEE_ID):
        self.EMPLOYEE_ID = EMPLOYEE_ID
        self.DESIGNATION = DESIGNATION
        self.DEPARTMENT = DEPARTMENT
        self.NAME = NAME
        self.MANAGER_EMPLOYEE_ID = MANAGER_EMPLOYEE_ID
        self.reportees = []

    def fillReportees(self, dataList : list) -> None:
        self.reportees = []
        for item in dataList:
            if self.EMPLOYEE_ID == item.MANAGER_EMPLOYEE_ID:
                self.reportees.append(item)
        for item in self.reportees:
            item.fillReportees(dataList)

    def generateTree(self) -> dict:

        respTree = dict()
        respTree["EMPLOYEE_ID"] = self.EMPLOYEE_ID
        respTree["NAME"] = self.NAME
        respTree["DEPARTMENT"] = self.DEPARTMENT
        respTree["DESIGNATION"] = self.DESIGNATION
        respTree["reportees"] = self.reportees

        for index in range(len(respTree["reportees"])):
            respTree["reportees"][index] = respTree["reportees"][index].generateTree()

        return respTree


if __name__ == "__main__":

    readFile = pd.read_csv(SOURCE_FILE)
    readFile["MANAGER EMPLOYEE_ID"].fillna(CEO_BOSS, inplace=True)
    count = len(readFile)

    readData = list()

    for i in range(count):
        readData.append(
            Employee(
                readFile["EMPLOYEE_ID"][i],
                readFile["DESIGNATION"][i],
                readFile["DEPARTMENT"][i],
                readFile["NAME"][i],
                readFile["MANAGER EMPLOYEE_ID"][i],
            )
        )

    bossObj = None

    for item in readData:
        if item.MANAGER_EMPLOYEE_ID == CEO_BOSS:
            bossObj = item
            break
 
    if bossObj != None:
        bossObj.fillReportees(readData)
        empTree = bossObj.generateTree()
        fileObj = open(DESCINATION_FILE, "w")
        json.dump(empTree, fileObj, indent=4)
        fileObj.close()
    else:
        print("No CEO found")

        