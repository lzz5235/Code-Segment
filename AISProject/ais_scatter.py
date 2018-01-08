#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import numpy as np


def Classfication_By_Weight(input_path,weight):
    print input_path
    if 0 == int(os.path.getsize(input_path)):
        return
    et = ET.parse(input_path)
    element = et.getroot()
    element_Ships = element.findall('Ship')
    ship = element_Ships[0]
    mmsi = long(ship.find("MMSI").text)
    StaticInfo = ship.find("StaticInfo")
    Draught = float(StaticInfo.find("Draught").text)

    if weight.has_key(int(Draught)):
        weight[int(Draught)] += 1
    else:
        weight[int(Draught)] = 1

def Classfication_By_WS(input_path):
    print input_path
    if 0 == int(os.path.getsize(input_path)):
        return
    et = ET.parse(input_path)
    element = et.getroot()
    element_Ships = element.findall('Ship')
    ship = element_Ships[0]
    StaticInfo = ship.find("StaticInfo")
    Length = float(StaticInfo.find("Length").text)
    Width = float(StaticInfo.find("Width").text)
    Draught = float(StaticInfo.find("Draught").text)
    slist = []
    for ship in element_Ships:
        DynamicInfo = ship.find("DynamicInfo")
        Speed = float(DynamicInfo.find("Speed").text)
        if int(Speed) != 0 :
            slist.append(Speed)
    slist = np.array(slist)
    Y = np.median(slist)
    X = int(Length*Width*Draught)
    return X,Y

def Classfication_By_WRot(input_path):
    print input_path
    if 0 == int(os.path.getsize(input_path)):
        return
    et = ET.parse(input_path)
    element = et.getroot()
    element_Ships = element.findall('Ship')
    ship = element_Ships[0]
    StaticInfo = ship.find("StaticInfo")
    Length = float(StaticInfo.find("Length").text)
    Width = float(StaticInfo.find("Width").text)
    Draught = float(StaticInfo.find("Draught").text)
    slist = []
    for ship in element_Ships:
        DynamicInfo = ship.find("DynamicInfo")
        AngularRate = float(DynamicInfo.find("AngularRate").text)
        if int(abs(AngularRate)) != 0 :
            slist.append(abs(AngularRate))

    if len(slist) == 0:
        slist.append(0)
    slist = np.array(slist)
    Y = np.mean(slist) # mean AngularRate
    X = int(Length*Width*Draught)
    return X,Y

if __name__ == "__main__":

    rot_list = []
    draught_list = []
    for file in [os.path.join('xxx', s) for s in os.listdir(
            'xxx')]:
        X,Y = Classfication_By_WRot(file)
        if Y == 0:
            continue
        draught_list.append(X)
        rot_list.append(Y)

    rot_list = np.array(rot_list)
    draught_list = np.array(draught_list)
    # print rot_list
    # print draught_list
    plt.scatter(draught_list,rot_list,25,cmap=plt.cm.jet,marker='o',edgecolors='k',zorder=10,alpha=0.7)
    # plt.xticks(np.arange(0,400000,20000))
    plt.yticks(np.arange(0,30,2))
    plt.xlabel("Ship TANKER Tonnage")
    plt.ylabel("AngularRate")
    plt.title("Global Ship TANKER Tonnage/AngularRate Scatter")
    plt.grid()
    plt.show()