import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import matplotlib as mpl
import matplotlib.colors
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import ais_parse as parse
from itertools import cycle

# LastTime Segment
def ais_seg(input_path):
    all_MMSI = []
    tmp_dict = {}

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
        all_MMSI.append(ShipData)
        targetName = os.path.split(input_path)[1] + '-' +str(LastTime).split(' ',1)[0]
        if tmp_dict.has_key(targetName):
            tmp_dict[targetName].append(ShipData)
        else:
            tmp_dict[targetName] = [ShipData]

    return tmp_dict

def dump_data(tmp_dict):
    for idx,key in enumerate(tmp_dict.keys()):
        SD = tmp_dict[key]
        AIS  = ET.Element('AIS')
        for shipdata in SD:
            Ship = ET.SubElement(AIS,'Ship')
            MMSI = ET.SubElement(Ship,'MMSI')
            MMSI.text = str(shipdata['MMSI'])
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

        tree = ET.tostring(AIS,'utf-8')
        tree = minidom.parseString(tree)

        with open(os.path.split(input_path)[0] + os.sep + key,'w+') as f: # DY
           tree.writexml(f,addindent="    ",newl="\n",encoding='utf-8')

if __name__ == "__main__":
    input_path = './InterstTarget/366576000'
    tmp_dict = ais_seg(input_path)
    dump_data(tmp_dict)