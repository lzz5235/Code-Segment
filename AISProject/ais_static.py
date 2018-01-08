import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from mpl_toolkits.basemap import Basemap
import ais_parse as parse
import pandas as pd
from pandas import datetime
from sklearn.cluster import DBSCAN,MeanShift,AffinityPropagation
from sklearn.metrics import euclidean_distances
import json
from collections import OrderedDict

def formatShipLine(one_MMSI):
    x_list = []
    y_list = []
    date_list = []
    speed_list = []

    for shipdata in one_MMSI:
        shipMMSI = shipdata['MMSI']
        x = shipdata['DynamicInfo'][0]['Longitude']  # jingdu
        y = shipdata['DynamicInfo'][0]['Latitude']  # weidu
        datetime = shipdata['DynamicInfo'][0]['LastTime']
        speed = shipdata['DynamicInfo'][0]['Speed'] #Speed
        x_list.append(x)
        y_list.append(y)
        date_list.append(datetime)
        speed_list.append(speed)

    date = np.array(date_list)
    x = np.array(x_list)
    rows = x.shape
    for i in range(rows[0]):
        if x[i] <=0:
            x[i] = 360 + x[i]

    y = np.array(y_list)
    table = pd.DataFrame(columns=['Date','X','Y','Speed'])
    table['Date'] = date
    table['X'] = x
    table['Y'] = y
    table['Speed'] = np.array(speed_list)

    table.set_index('Date',drop=False,append=False,inplace=True,verify_integrity=False)
    table = table.sort_index()
    # table.to_csv('look.csv')

    return shipMMSI,table

def compare(lat0,lon0,lat1,lon1):
    delta0 = abs(abs(float(lat0)) - abs(float(lat1)))
    delta1 = abs(abs(float(lon0)) - abs(float(lon1)))
    if delta0 > 0.0001 and delta1 > 0.0001:
        return True
    return False

def compute_date(date0,date1):
    d1 = datetime.strptime(date0,'%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(date1,'%Y-%m-%d %H:%M:%S')
    hours = ((d2-d1).days * 24 *3600 + (d2-d1).seconds)/3600
    return hours

def find_stop_place(mmsi,data):
    rows,cols = data.shape
    # print data
    i = 0
    while i < rows:
        if float(data.iloc[i]['Speed']) <=0.05 and float(data.iloc[i]['Speed']) >=0:
            j = i
            while i < rows and j < rows:
                if float(data.iloc[j]['Speed']) > 1 and compare(data.iloc[j-1]['X'],data.iloc[j-1]['Y'],data.iloc[j][
                    'X'],data.iloc[j]['Y']):
                    break
                j += 1

            mean_lon = np.mean(data.iloc[i:j,1].values)
            if mean_lon >=180:
                mean_lon -= 360
            mean_lat = np.mean(data.iloc[i:j,2].values)
            # MMSI,Jindu,Weidu,Start_time,End_time,Point nums,Hours
            string = str(mmsi) + ',' + str(mean_lon) + ',' + str(mean_lat)+ ',' + data.iloc[i]['Date'] + ',' \
                     + data.iloc[j-1]['Date'] + ',' + str(int(j-i)) + ',' +\
                     str(compute_date(str(data.iloc[i]['Date']),str(data.iloc[j-1]['Date'])))
            print string
            with open('./ShipLineTest/ais_stop.txt', 'a') as f:  # ST
                 f.write(string + '\n')
            i = j
        i += 1

def scatter(fileName):
    colums = np.array([u'MMSI',u'Longtitude',u'Latitude',u'Start_time',u'End_time',u'PointNum',u'Hours'])
    table = pd.read_csv(fileName,sep=',',header=None,names=colums)
    x = table['Longtitude'].values
    y = table['Latitude'].values
    PointNum = table['PointNum'].values

    rows = x.shape
    for i in range(rows[0]):
        if x[i] <= 0:
            x[i] = 360 + x[i]


    map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    map.drawmapboundary(fill_color='black')
    x, y = map(x, y)
    map.scatter(x, y, 25, cmap=plt.cm.jet, marker='o', edgecolors='none', zorder=10)
    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    map.fillcontinents(color='grey', lake_color='black')
    plt.title('China Ship Map')
    plt.show()

def DBSCAN_scatter(fileName):
    colums = np.array([u'MMSI', u'Longtitude', u'Latitude', u'Start_time', u'End_time', u'PointNum', u'Hours'])
    table = pd.read_csv(fileName, sep=',', header=None, names=colums)
    x = table['Longtitude'].values.reshape(-1,1)
    y = table['Latitude'].values.reshape(-1,1)
    PointNum = table['PointNum'].values

    rows = x.shape
    for i in range(rows[0]):
        if x[i] <= 0:
            x[i] = 360 + x[i]

    data = np.hstack((x,y))
    model = DBSCAN(eps=0.09,min_samples=3)
    model.fit(data)
    y_hat = model.labels_

    core_indices = np.zeros_like(y_hat,dtype=bool)
    core_indices[model.core_sample_indices_] = True

    y_unique = np.unique(y_hat)
    print y_hat.size
    print model.labels_,y_unique.size
    print model.core_sample_indices_  # Belongs to which class
    map = Basemap(projection='mill', lon_0=180, width=12000000, height=9000000)
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    map.drawmapboundary(fill_color='white')
    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    map.fillcontinents(color='coral', lake_color='blue')
    data[:,0], data[:,1] = map(data[:,0], data[:,1])
    clrs = plt.cm.Spectral(np.linspace(0,0.8,y_unique.size))

    for k,clr in zip(y_unique,clrs):
        cur = (y_hat == k)
        if k == -1:
            # map.scatter(data[cur,0],data[cur,1],s=20,c='k') # nosie
            continue
        map.scatter(data[cur,0],data[cur,1],s=20,c=clr,edgecolors='k')
        map.scatter(data[cur & core_indices][:,0],data[cur & core_indices][:,1],60, c=clr, marker='*',
                    edgecolors='none', zorder=10)
    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    # map.fillcontinents(color='grey', lake_color='black')
    plt.title('DBSCAN Ship Stop')
    plt.show()

def MeanShift_scatter(fileName):
    colums = np.array([u'MMSI', u'Longtitude', u'Latitude', u'Start_time', u'End_time', u'PointNum', u'Hours'])
    table = pd.read_csv(fileName, sep=',', header=None, names=colums)
    x = table['Longtitude'].values.reshape(-1,1)
    y = table['Latitude'].values.reshape(-1,1)
    PointNum = table['PointNum'].values

    rows = x.shape
    for i in range(rows[0]):
        if x[i] <= 0:
            x[i] = 360 + x[i]

    data = np.hstack((x,y))
    model = MeanShift(bin_seeding=True,bandwidth=4,n_jobs=-2)
    ms = model.fit(data)
    centers = ms.cluster_centers_
    y_hat = model.labels_

    y_unique = np.unique(y_hat)
    print model.labels_,y_unique.size
    # map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
    # map.drawcoastlines()
    # map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    # map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    # map.drawmapboundary(fill_color='black')
    # data[:,0], data[:,1] = map(data[:,0], data[:,1])
    clrs = plt.cm.Spectral(np.linspace(0,255,y_unique.size))
    for k,clr in zip(y_unique,clrs):
        cur = (y_hat == k)
        plt.scatter(data[cur,0],data[cur,1],s=20,c = 'r',edgecolors='none')
    plt.scatter(centers[:,0],centers[:,1],s=60,c=clrs,marker='*',edgecolors='k')
    # map.drawcoastlines(linewidth=0.5, color='y')
    # map.drawcountries(color='y')
    # map.drawstates(color='y')
    # map.fillcontinents(color='grey', lake_color='black')
    plt.title('MeanShift Ship Stop')
    plt.show()

def AP_scatter(fileName):
    colums = np.array([u'MMSI', u'Longtitude', u'Latitude', u'Start_time', u'End_time', u'PointNum', u'Hours'])
    table = pd.read_csv(fileName, sep=',', header=None, names=colums)
    x = table['Longtitude'].values.reshape(-1,1)
    y = table['Latitude'].values.reshape(-1,1)
    PointNum = table['PointNum'].values

    rows = x.shape
    for i in range(rows[0]):
        if x[i] <= 0:
            x[i] = 360 + x[i]

    data = np.hstack((x,y))
    m = euclidean_distances(data,squared=True)
    preferences = -np.median(m)

    model = AffinityPropagation(affinity='euclidean',preference=preferences)
    ms = model.fit(data)
    centers = ms.cluster_centers_
    y_hat = model.labels_

    y_unique = np.unique(y_hat)
    print model.labels_,y_unique.size
    map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    map.drawmapboundary(fill_color='black')
    data[:,0], data[:,1] = map(data[:,0], data[:,1])
    clrs = plt.cm.Spectral(np.linspace(0,255,y_unique.size))
    for k,clr in zip(y_unique,clrs):
        cur = (y_hat == k)
        map.scatter(data[cur,0],data[cur,1], 10, cmap=clr, marker='o', edgecolors='none', zorder=10)
    map.scatter(centers[:,0],centers[:,1],180,cmap=plt.cm.jet,marker='*')
    map.drawcoastlines(linewidth=0.5, color='y')
    map.drawcountries(color='y')
    map.drawstates(color='y')
    # map.fillcontinents(color='grey', lake_color='black')
    plt.title('AP Ship Stop')
    plt.show()

def Classification_By_Speed(PathName,Output):
    data_paths = [os.path.join(PathName, s) for s in os.listdir(PathName)]
    speed_distribution = {}
    for file in data_paths:
        one_MMSI = []
        parse.get_data_DY(file,one_MMSI)
        sp = one_MMSI[0]['DynamicInfo'][0]['Speed']

        if sp <=0:
            continue

        if speed_distribution.has_key(int(sp)):
            speed_distribution[int(sp)] += 1
        else:
            speed_distribution[int(sp)] = 1
    print speed_distribution
    with open(Output,'w') as f:
        json.dump(speed_distribution,f)

def plot_hist(filePath,X_label,Y_label,title):
    speed_bins = []
    speed_count = []
    with open(filePath,'r') as f:
        speed_distribution = f.readlines()[0]
        speed_distribution = json.loads(speed_distribution)
        d = OrderedDict(sorted(speed_distribution.items(),key=lambda x:int(x[0])))
        # keys = d.keys()
        # sorted(keys,key=lambda x:int(x[0]))
        # d = [[key,d[key]] for key in keys]
        # sorted(speed_distribution.items(),lambda x,y:cmp(int(x[0]),int(y[0])))
        # print speed_distribution
    for key,value in d.items():
        if int(key) <= 0:
            continue
        speed_bins.append(int(key))
        speed_count.append(value)
        print key,value
    speed_bins = np.array(speed_bins).flatten()
    speed_count = np.array(speed_count).flatten()
    # plt.hist(speed_count,bins=16,normed=1)
    print speed_bins,len(speed_bins)
    print speed_count,len(speed_count)

    plt.plot(speed_bins,speed_count,'r-')
    plt.bar(speed_bins,speed_count,color='b')
    plt.xlabel(X_label)
    plt.ylabel(Y_label)
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    all_MMSI = []
    one_MMSI = []
    center_x = 139.59
    center_y = 35.26
    theta = 5
    center_lux = center_x-theta
    center_luy = center_y+theta
    center_rdx = center_x+theta
    center_rdy = center_y-theta

    ##########################################
    # data_paths = [os.path.join("./InterstTarget/", s) for s in os.listdir('./InterstTarget/')]
    # for file in data_paths:
    #     one_MMSI = []
    #     parse.get_data_DY(file,one_MMSI)
    #     mmsi,data = formatShipLine(one_MMSI) # one Shipline
    #     find_stop_place(mmsi,data)
    # scatter('./ShipLineTest/ais_stop.txt')
    # DBSCAN_scatter('./ShipLineTest/ais_stop.txt')
    #########################################
    # one_MMSI = []
    # parse.get_data_DY('./days/366576000',one_MMSI)
    # mmsi,data = formatShipLine(one_MMSI) # one Shipline
    # find_stop_place(mmsi,data)
    #########################################
    # AP_scatter('./ShipLineTest/ais_stop.txt')
    # Classification_By_Speed('./ShipGARGO/','./ShipLineTest/cls_gargo_speed.txt')
    # plot_hist('./ShipLineTest/cls_gargo_speed.txt',"Speed","Speed Count","The Speed Counter of ShipGARGO")
    # Classification_By_Speed('./ShipTANKER/','./ShipLineTest/cls_tanker_speed.txt')
    plot_hist('./ShipLineTest/cls_tanker_speed.txt',"Speed","Speed Count","The Speed Counter of Ship TANKER")