import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.colors
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

class ais_elane:
    def __init__(self,input_path="",input_path_dir=""):
        self.input_path = input_path
        self.input_path_dir = input_path_dir
        self.all_MMSI = []
        self.stop_MMSI = []
        self.seg_tab = []

        if input_path !="": # simple file
            self.read_data(input_path)
            self.mapscatter()
        if input_path_dir !="": # all files
            self.read_from_dir()

    def read_from_dir(self):
        file_path = [os.path.join(self.input_path_dir, s) for s in os.listdir(self.input_path_dir)]
        for file in file_path:
            print file
            self.seg_tab = []
            self.all_MMSI = []
            self.stop_MMSI = []
            self.read_data(file)
            self.mapscatter()

    def segment_table_by_dest(self):
        split = []
        for idx in range(len(self.table) - 1):
            if str(self.table.iloc[idx]['Dest']) != str(self.table.iloc[idx + 1]['Dest']):
                split.append(idx)

        for idx in range(len(split)-1):
            tmp = self.table[split[idx]+1:split[idx+1]-1]
            self.seg_tab.append(tmp)

    def read_data(self,input_path):
        def conv_map(Longitude):
                if Longitude <= 0:
                    Longitude += 360  # correct longtitude
                return Longitude

        colums = np.array(["ShipName","CallSign","IMO","MMSI","ShipTypeCN","ShipTypeEN","NavStatusCN","NavStatusEN","Length",
                   "Width","Draught","Heading","Course","Speed","Lon","Lat","Rot","Dest","ETA","Receivedtime","UnixTime",
                           "Lon_d","Lat_d"])
        self.table = pd.read_csv(input_path,sep=',',names=colums,header=0,encoding='GB2312')
        # print table['ShipTypeCN'],table['Lon_d'],table['Lat_d']
        print type(self.table)
        self.segment_table_by_dest()

        for tab in self.seg_tab:
            one_ship_line = []
            for ix,row in tab.iterrows():
                mmsi = row['MMSI']
                LastTime = row['Receivedtime']
                Latitude = row['Lat_d']
                Longitude = conv_map(row['Lon_d'])
                Speed = row['Speed']
                course = row['Course']
                HeadCourse = row['Course']
                AngularRate = row['Rot']
                NaviStatus = row['NavStatusEN']
                Dest = row['Dest']
                ShipData = {'MMSI': mmsi, 'DynamicInfo': []}
                ShipData['DynamicInfo'].append({'LastTime': str(LastTime), 'Latitude': Latitude, 'Longitude': Longitude,
                                                'Speed': Speed,
                                                'course': course, 'HeadCourse': HeadCourse, 'AngularRate': AngularRate,
                                                'NaviStatus': NaviStatus})
                if mmsi < 100000000:
                    continue

                if NaviStatus == "Moored":
                    self.stop_MMSI.append(ShipData)
                    continue

                one_ship_line.append(ShipData)
            self.all_MMSI.append(one_ship_line)

    def mapscatter(self):
        map = Basemap(projection='mill', lon_0=180, width=12000000, height=9000000)
        map.drawcoastlines()
        map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
        map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
        # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
        map.drawmapboundary(fill_color='white')
        map.drawcoastlines(linewidth=0.5, color='y')
        map.drawcountries(color='y')
        map.drawstates(color='y')
        map.fillcontinents(color='grey', lake_color='blue')
        x_list = []
        y_list = []

        # all Ship Trajectory Stop
        MMSI = self.stop_MMSI[0]['MMSI']
        for shipdata in self.stop_MMSI:
            x = shipdata['DynamicInfo'][0]['Longitude']  # jingdu
            y = shipdata['DynamicInfo'][0]['Latitude']  # weidu

            x_list.append(x)
            y_list.append(y)

        x = np.array(x_list)
        y = np.array(y_list)

        x, y = map(x, y)
        map.scatter(x, y, 60, c='black', marker='*', edgecolors='none', zorder=10)

        # all Ship Trajectory
        MMSI = self.all_MMSI[0][0]['MMSI']
        for one_line in self.all_MMSI:
            x_list = []
            y_list = []
            for shipdata in one_line:
                x = shipdata['DynamicInfo'][0]['Longitude'] #jingdu
                y = shipdata['DynamicInfo'][0]['Latitude']  #weidu
                LastTime = shipdata['DynamicInfo'][0]['LastTime']

                x_list.append(x)
                y_list.append(y)

            x = np.array(x_list)
            y = np.array(y_list)

            if x!=[] and y!=[]:
                x, y = map(x, y)
                current_label = LastTime
                # print (x.tolist()[0])
                if len(x.tolist()) > 1000 and len(y.tolist()) >1000:
                    plt.text(x.tolist()[0], y.tolist()[0], current_label)
                map.scatter(x, y, 10, cmap=plt.cm.jet, marker='o', edgecolors='none', zorder=10)

        plt.title('Ship %d Trajectory'%(MMSI))
        plt.show()
        plt.cla()

if __name__ == "__main__":

    a = ais_elane('/media/xxxx/x/elane_ais/JP_US/20171129090537_353368000.csv')



