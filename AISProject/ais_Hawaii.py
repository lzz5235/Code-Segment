#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import shutil

def get_data_DY(input_path,*location):
    theta = 3.00
    lon1 = float(str(location[0][0]))-theta
    lon2 = float(str(location[0][0]))+theta
    lat1 = float(str(location[0][1]))+theta
    lat2 = float(str(location[0][1]))-theta

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

        if (Longitude > lon1 and Longitude < lon2) and (Latitude < lat1 and Latitude > lat2):
            return True

    return False

if __name__ == "__main__":
    Hawaii_longtitude = -157.00
    Hawaii_latitude = 21.00
    file_path = "xxx"
    for file in [os.path.join(file_path, s) for s in os.listdir(file_path)]:
        ret = get_data_DY(file,[float(Hawaii_longtitude),float(Hawaii_latitude)])
        if ret:
            print file
            shutil.copyfile(file, './Hawaii/tanker/' + os.path.split(file)[1])