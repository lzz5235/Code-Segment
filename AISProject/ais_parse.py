#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import numpy as np
import pandas as pd

def get_data_DY(input_path, all_MMSI):
    print input_path
    if 0 == int(os.path.getsize(input_path)):
        return
    et = ET.parse(input_path)
    element = et.getroot()
    element_Ships = element.findall('Ship')
    for ship in element_Ships:
        mmsi = long(ship.find("MMSI").text)
        DynamicInfo = ship.find("DynamicInfo")
        LastTime = DynamicInfo.find("LastTime").text
        Latitude = float(DynamicInfo.find("Latitude").text)
        Longitude = float(DynamicInfo.find("Longitude").text)
        Speed = float(DynamicInfo.find("Speed").text)
        course = float(DynamicInfo.find("course").text)
        HeadCourse = float(DynamicInfo.find("HeadCourse").text)
        AngularRate = float(DynamicInfo.find("AngularRate").text)
        NaviStatus = float(DynamicInfo.find("NaviStatus").text)
        ShipData = {'MMSI':mmsi, 'DynamicInfo':[]}
        ShipData['DynamicInfo'].append({'LastTime':str(LastTime),'Latitude':Latitude,'Longitude':Longitude,
                                        'Speed':Speed,
                                        'course':course,'HeadCourse':HeadCourse,'AngularRate':AngularRate,
                                        'NaviStatus':NaviStatus})
        if mmsi < 100000000:
            continue

        all_MMSI.append(ShipData)

def dump_data_DY_TXT(input_path,all_MMSI):
    with open(input_path,'r') as f:
        string = f.readlines()
        for line in string:
            str_part = line.split(',')
            Longitude = float(str_part[10][1:])
            Latitude = float(str_part[11][:-2])
            mmsi = long(str_part[0])
            LastTime = str_part[12][:-4]
            Speed = float(str_part[17])
            course = float(str_part[2])
            HeadCourse = float(str_part[2])
            AngularRate = float(0.0)
            NaviStatus = float(str_part[20])
            ShipData = {'MMSI': mmsi, 'DynamicInfo': []}
            ShipData['DynamicInfo'].append({'LastTime': LastTime, 'Latitude': Latitude, 'Longitude': Longitude,
                                            'Speed': Speed,
                                            'course': course, 'HeadCourse': HeadCourse, 'AngularRate': AngularRate,
                                            'NaviStatus': NaviStatus})

            if mmsi < 100000000:
                continue

            all_MMSI.append(ShipData)
            info = ShipData['DynamicInfo'][0]['LastTime'] + ',' + str(
                ShipData['DynamicInfo'][0]['Latitude']) \
                     + ',' + str(ShipData['DynamicInfo'][0]['Longitude']) + ',' + str(
                ShipData['DynamicInfo'][0]['Speed']) + \
                     ',' + str(ShipData['DynamicInfo'][0]['course']) + ',' + str(
                ShipData['DynamicInfo'][0]['NaviStatus'])

            with open('./Japan/'+ str(mmsi), 'a') as f:
                f.write(info + '\n')

def read_data_DY_TXT(input_path):
    colums = np.array([u'LastTime', u'Latitude',u'Longtitude, 'u'Speed', u'course', u'NaviStatus'])
    table = pd.read_csv(input_path, sep=',', header=None)
    table.set_index(0,drop=True,append=False,inplace=True,verify_integrity=False)
    table = table.sort_index()
    # print table
    # print table[1].values,table[2].values
    # data = np.vstack((table[1].values,table[2].values))
    # print data.T,data.T.shape
    return table


def get_data_ST(input_path,all_MMSI):
    print input_path
    if 0 == int(os.path.getsize(input_path)):
        return
    et = ET.parse(input_path)
    element = et.getroot()
    element_Ships = element.findall('Ship')
    for ship in element_Ships:
        mmsi = long(ship.find("MMSI").text)
        StaticInfo = ship.find("StaticInfo")
        LastTime = StaticInfo.find("LastTime").text
        ShipType = int(StaticInfo.find("ShipType").text)
        Length = float(StaticInfo.find("Length").text)
        Width = float(StaticInfo.find("Width").text)
        Left = float(StaticInfo.find("Left").text)
        Trail = float(StaticInfo.find("Trail").text)
        Draught = float(StaticInfo.find("Draught").text)
        IMO = long(StaticInfo.find("IMO").text)
        CallSign = StaticInfo.find("CallSign").text
        ETA = StaticInfo.find("ETA").text
        Name = StaticInfo.find("Name").text
        Dest = StaticInfo.find("Dest").text

        ShipData = {'MMSI': mmsi, 'StaticInfo': []}
        ShipData['StaticInfo'].append({'LastTime': str(LastTime), 'ShipType': ShipType, 'Length': Length,
                                        'Width': Width,
                                        'Left': Left, 'Trail': Trail, 'Draught': Draught,
                                        'IMO': IMO,
                                        'CallSign': str(CallSign),'ETA':str(ETA),'Name':str(Name),'Dest':str(Dest)})
        if mmsi < 100000000:
            continue

        all_MMSI.append(ShipData)

def dump_data(all_MMSI_DY,all_MMSI_ST,fileName):
    AIS  = ET.Element('AIS')
    Flag = False
    isNavy = False
    isGARGO = False # HUO CHUAN
    isTANKER = False # YOU LUN
    DataST = []
    for shipdata in all_MMSI_DY:
        Ship = ET.SubElement(AIS,'Ship')
        MMSI = ET.SubElement(Ship,'MMSI')
        MMSI.text = str(shipdata['MMSI'])
        for shipST in all_MMSI_ST:
            if Flag ==True:
                break
            if shipST['MMSI'] == shipdata['MMSI']:
                Flag = True
                DataST = shipST
        DynamicInfo = ET.SubElement(Ship,'DynamicInfo')
        LastTime = ET.SubElement(DynamicInfo,'LastTime')
        LastTime.text = str(shipdata['DynamicInfo'][0]['LastTime'])
        Latitude = ET.SubElement(DynamicInfo, 'Latitude')
        Latitude.text = str(shipdata['DynamicInfo'][0]['Latitude'])
        Longitude = ET.SubElement(DynamicInfo, 'Longitude')
        Longitude.text = str(shipdata['DynamicInfo'][0]['Longitude'])
        Speed = ET.SubElement(DynamicInfo, 'Speed')
        Speed.text = str(shipdata['DynamicInfo'][0]['Speed'])
        course = ET.SubElement(DynamicInfo, 'course')
        course.text = str(shipdata['DynamicInfo'][0]['course'])
        HeadCourse = ET.SubElement(DynamicInfo, 'HeadCourse')
        HeadCourse.text = str(shipdata['DynamicInfo'][0]['HeadCourse'])
        AngularRate = ET.SubElement(DynamicInfo, 'AngularRate')
        AngularRate.text = str(shipdata['DynamicInfo'][0]['AngularRate'])
        NaviStatus = ET.SubElement(DynamicInfo, 'NaviStatus')
        NaviStatus.text = str(shipdata['DynamicInfo'][0]['NaviStatus'])
        if len(DataST) > 0:
            print shipdata['MMSI']
            StaticInfo = ET.SubElement(Ship, 'StaticInfo')
            LastTime = ET.SubElement(StaticInfo, 'LastTime')
            LastTime.text = str(DataST['StaticInfo'][0]['LastTime'])
            ShipType = ET.SubElement(StaticInfo, 'ShipType')
            ShipType.text = str(DataST['StaticInfo'][0]['ShipType'])
            type = DataST['StaticInfo'][0]['ShipType']

            if type >= 50 and type < 60:
                isNavy = True
            elif type >=70 and type < 80:
                isGARGO = True
            elif type >=80 and type < 90:
                isTANKER = True

            Length = ET.SubElement(StaticInfo, 'Length')
            Length.text = str(DataST['StaticInfo'][0]['Length'])
            Width = ET.SubElement(StaticInfo, 'Width')
            Width.text = str(DataST['StaticInfo'][0]['Width'])
            Left = ET.SubElement(StaticInfo, 'Left')
            Left.text = str(DataST['StaticInfo'][0]['Left'])
            Trail = ET.SubElement(StaticInfo, 'Trail')
            Trail.text = str(DataST['StaticInfo'][0]['Trail'])
            Draught = ET.SubElement(StaticInfo, 'Draught')
            Draught.text = str(DataST['StaticInfo'][0]['Draught'])
            IMO = ET.SubElement(StaticInfo, 'IMO')
            IMO.text = str(DataST['StaticInfo'][0]['IMO'])
            CallSign = ET.SubElement(StaticInfo, 'CallSign')
            CallSign.text = str(DataST['StaticInfo'][0]['CallSign'])
            ETA = ET.SubElement(StaticInfo, 'ETA')
            ETA.text = str(DataST['StaticInfo'][0]['ETA'])
            Name = ET.SubElement(StaticInfo, 'Name')
            Name.text = str(DataST['StaticInfo'][0]['Name'])
            Dest = ET.SubElement(StaticInfo, 'Dest')
            Dest.text = str(DataST['StaticInfo'][0]['Dest'])


    tree = ET.tostring(AIS,'utf-8')
    tree = minidom.parseString(tree)

    result = os.path.split(fileName)

    if isNavy == True: # Jun Chuan
        newfilepath = os.path.join('./ShipNavy', result[1])
        with open(newfilepath,'w+') as f:
            tree.writexml(f, addindent="    ", newl="\n", encoding='utf-8')

    if isGARGO == True: # Huo Lun
        newfilepath = os.path.join('./ShipGARGO', result[1])
        with open(newfilepath, 'w+') as f:
            tree.writexml(f, addindent="    ", newl="\n", encoding='utf-8')

    if isTANKER == True: # You Lun
        newfilepath = os.path.join('./ShipTANKER', result[1])
        with open(newfilepath, 'w+') as f:
            tree.writexml(f, addindent="    ", newl="\n", encoding='utf-8')

    if Flag == True:# DY + ST
        newfilepath = os.path.join('./ShipDYST', result[1])
        with open(newfilepath,'w+') as f:
            tree.writexml(f, addindent="    ", newl="\n", encoding='utf-8')

    with open(fileName,'w+') as f: # DY
       tree.writexml(f,addindent="    ",newl="\n",encoding='utf-8')




if __name__ == "__main__":
    all_MMSI_DY=[]
    all_MMSI_ST=[]
    data_paths_dy = []
    data_paths_st = []

    read_data_DY_TXT('XXX')
