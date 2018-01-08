#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

def Classfication_By_LWDS(input_path):
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
    Y = np.median(slist)  #速度
    X = int(Length*Width) #面积
    Z = Draught  #吃水
    return X,Y,Z

if __name__ == "__main__":
    all_MMSI_cargo = []
    all_MMSI_tanker = []
    cargo_path = "xxx"
    tanker_path = "xxx"

    tmp_cargo = [os.path.join(cargo_path + os.sep, s) for s in os.listdir(cargo_path + os.sep)]
    tmp_tanker = [os.path.join(tanker_path + os.sep, s) for s in os.listdir(tanker_path + os.sep)]

    fig = plt.figure(facecolor='w')
    ax  = fig.add_subplot(111,projection='3d')
    ax.set_xlabel(u'面积(m^2)')
    ax.set_ylabel(u'速度(节/小时)')
    ax.set_zlabel(u'吃水深度(m)')

    for file in tmp_cargo:
        x, y, z = Classfication_By_LWDS(file)
        ax.scatter(x,y,z,c='b',s=10,marker='o',edgecolors='k',depthshade=True)

    for file in tmp_tanker:
        x, y, z = Classfication_By_LWDS(file)
        ax.scatter(x,y,z,c='b',s=10,marker='o',edgecolors='k',depthshade=True)

    plt.suptitle(u'面积/速度/吃水深度关系', fontsize=18)
    plt.tight_layout()
    plt.show()

