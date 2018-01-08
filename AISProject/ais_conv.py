import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import numpy as np

NationDict = {307: 'Aruba', 401: 'Afghanistan', 601: 'South Africa (Rep. of)', 603: 'Angola (Rep. of)', 301: 'Anguilla',
              201: 'Albania (Rep. of)', 605: 'Algeria (People\'s Democratic Rep. of)', 303: 'Alaska (State of)',
              607: 'Saint Paul and Amsterdam Islands', 202: 'Andorra (Principality of)', 701: 'Argentine Rep.',
              216: 'Armenia (Rep. of)', 403: 'Saudi Arabia (Kingdom of)', 608: 'Ascension Island',
              304: 'Antigua and Barbuda',
              305: 'Antigua and Barbuda', 306: 'Netherlands Caribbean', 503: 'Australia', 203: 'Austria',
              423: 'Azerbaijani Rep.',
              204: 'Azores', 710: 'Brazil (Federative Rep. of)', 308: 'Bahamas (Commonwealth of the)', 309: 'Bahamas ('
                                                                                                            'Commonwealth of the)',
              311: 'Bahamas (Commonwealth of the)', 609: 'Burundi (Rep. of)', 205: 'Belgium', 610: 'Benin (Rep. of)',
              310: 'Bermuda', 633: 'Burkina Faso', 405: 'Bangladesh (People\'s Rep. of)', 408: 'Bahrain (Kingdom of)',
              478: 'Bosnia and Herzegovina', 206: 'Belarus (Rep. of)', 312: 'Belize',
              720: 'Bolivia (Plurinational State of)',
              611: 'Botswana (Rep. of)', 314: 'Barbados', 506: 'Myanmar (Union of)', 508: 'Brunei Darussalam',
              410: 'Bhutan ('
                   'Kingdom of)',
              207: 'Bulgaria (Rep. of)', 612: 'Central African Rep', 316: 'Canada', 514: 'Cambodia (Kingdom of)',
              515: 'Cambodia '
                   '(Kingdom of)',
              725: 'Chile', 412: 'China (People\'s Rep. of)', 413: 'China (People\'s Rep. of)',
              414: 'China (People\'s Rep. of)',
              516: 'Christmas Island (Indian Ocean)', 518: 'Cook Islands', 730: 'Colombia (Rep. of)', 417: 'Sri Lanka ('
                                                                                                           'Democratic '
                                                                                                           'Socialist Rep. of)',
              613: 'Cameroon (Rep. of)', 676: 'Democratic Rep. of the Congo', 615: 'Congo (Rep. of the)',
              616: 'Comoros (Union '
                   'of the)',

              617: 'Cape Verde (Rep. of)', 618: 'Crozet Archipelago', 619: 'Cote d\'Ivoire (Rep. of)',
              321: 'Costa Rica',
              323: 'Cuba', 208: 'Vatican City State', 319: 'Cayman Islands', 209: 'Cyprus (Rep. of)',
              210: 'Cyprus (Rep. of)',
              212: 'Cyprus (Rep. of)', 270: 'Czech Rep.', 211: 'Germany (Federal Rep. of)',
              218: 'Germany (Federal Rep. of)',
              621: 'Djibouti (Rep. of)', 325: 'Dominica (Commonwealth of)', 219: 'Denmark', 220: 'Denmark',
              327: 'Dominican Rep.',
              224: 'Spain', 225: 'Spain', 622: 'Egypt (Arab Rep. of)', 735: 'Ecuador', 625: 'Eritrea',
              276: 'Estonia (Rep. of)',
              624: 'Ethiopia (Federal Democratic Rep. of)', 226: 'France', 227: 'France', 228: 'France', 230: 'Finland',
              520: 'Fiji (Rep. of)', 740: 'Falkland Islands (Malvinas)', 231: 'Faroe Islands',
              510: 'Micronesia (Federated '
                   'States of)',
              232: 'United Kingdom of Great Britain and Northern Ireland', 233: 'United Kingdom of Great Britain and '
                                                                                'Northern Ireland',
              234: 'United Kingdom of Great Britain and Northern Ireland', 235: 'United Kingdom of Great Britain and '
                                                                                'Northern Ireland',
              626: 'Gabonese Rep.', 213: 'Georgia', 627: 'Ghana', 236: 'Gibraltar', 329: 'Gambia (Rep. of the)',
              629: 'Guadeloupe ('
                   'French Department of)',
              630: 'Guinea-Bissau (Rep. of)', 631: 'Equatorial Guinea (Rep. of)', 237: 'Greece', 239: 'Greece',
              240: 'Greece',
              241: 'Greece', 330: 'Grenada', 331: 'Greenland', 332: 'Guatemala (Rep. of)',
              745: 'Guiana (French Department of)',
              632: 'Guinea (Rep. of)', 750: 'Guyana', 477: 'Hong Kong (Special Administrative Region of China)',
              334: 'Honduras (Rep. of)',
              243: 'Hungary', 244: 'Netherlands (Kingdom of the)', 245: 'Netherlands (Kingdom of the)',
              246: 'Netherlands ('
                   'Kingdom of the)',
              238: 'Croatia (Rep. of)', 336: 'Haiti (Rep. of)', 247: 'Italy', 523: 'Cocos (Keeling) Islands',
              419: 'India (Rep. '
                   'of)',
              525: 'Indonesia (Rep. of)', 250: 'Ireland', 422: 'Iran (Islamic Rep. of)', 425: 'Iraq (Rep. of)',
              251: 'Iceland',
              428: 'Israel (State of)', 431: 'Japan', 432: 'Japan', 339: 'Jamaica',
              438: 'Jordan (Hashemite Kingdom of)',
              436: 'Kazakhstan (Rep. of)', 634: 'Kenya (Rep. of)', 635: 'Kerguelen Islands', 451: 'Kyrgyz Rep.',
              529: 'Kiribati ('
                   'Rep. of)',
              341: 'Saint Kitts and Nevis (Federation of)', 440: 'Korea (Rep. of)', 441: 'Korea (Rep. of)',
              445: 'Democratic '
                   'People\'s '
                   'Rep. of Korea',
              447: 'Kuwait (State of)', 531: 'Lao People\'s Democratic Rep.', 450: 'Lebanon', 636: 'Liberia (Rep. of)',
              637: 'Liberia (Rep. of)', 642: 'Libya', 343: 'Saint Lucia', 252: 'Liechtenstein (Principality of)',
              644: 'Lesotho ('
                   'Kingdom of)',
              277: 'Lithuania (Rep. of)', 253: 'Luxembourg', 275: 'Latvia (Rep. of)',
              453: 'Macao (Special Administrative '
                   'Region of China)',
              645: 'Mauritius (Rep. of)', 254: 'Monaco (Principality of)', 214: 'Moldova (Rep. of)',
              647: 'Madagascar (Rep. '
                   'of)', 255: 'Madeira',
              345: 'Mexico', 538: 'Marshall Islands (Rep. of the)', 274: 'The Former Yugoslav Rep. of Macedonia',
              533: 'Malaysia',
              455: 'Maldives (Rep. of)', 649: 'Mali (Rep. of)', 215: 'Malta', 229: 'Malta', 248: 'Malta', 249: 'Malta',
              256: 'Malta',
              262: 'Montenegro', 457: 'Mongolia', 650: 'Mozambique (Rep. of)',
              536: 'Northern Mariana Islands (Commonwealth of '
                   'the)',
              242: 'Morocco (Kingdom of)', 347: 'Martinique (French Department of)', 248: 'Montserrat',
              654: 'Mauritania ('
                   'Islamic Rep. of)',
              655: 'Malawi', 350: 'Nicaragua', 540: 'New Caledonia', 656: 'Niger (Rep. of the)',
              657: 'Nigeria (Federal Rep. of)',
              542: 'Niue', 659: 'Namibia (Rep. of)', 257: 'Norway', 258: 'Norway', 259: 'Norway',
              459: 'Nepal (Federal Democratic '
                   'Rep. of)',
              544: 'Nauru (Rep. of)', 512: 'New Zealand', 546: 'French Polynesia', 461: 'Oman (Sultanate of)',
              463: 'Pakistan ('
                   'Islamic Rep. of)',
              548: 'Philippines (Rep. of the)', 511: 'Palau (Rep. of)', 553: 'Papua New Guinea',
              351: 'Panama (Rep. of)',
              352: 'Panama (Rep. of)', 353: 'Panama (Rep. of)', 354: 'Panama (Rep. of)', 355: 'Panama (Rep. of)',
              356: 'Panama (Rep. of)',
              357: 'Panama (Rep. of)', 370: 'Panama (Rep. of)', 371: 'Panama (Rep. of)', 372: 'Panama (Rep. of)',
              373: 'Panama ('
                   'Rep. of)',
              261: 'Poland (Rep. of)', 263: 'Portugal', 755: 'Paraguay (Rep. of)', 760: 'Peru', 443: 'Palestine',
              555: 'Pitcairn '
                   'Island',
              358: 'Puerto Rico', 466: 'Qatar (State of)', 660: 'Reunion (French Department of)', 264: 'Romania',
              661: 'Rwanda ('
                   'Rep. of)',
              273: 'Russian Federation', 265: 'Sweden', 266: 'Sweden', 662: 'Sudan (Rep. of the)',
              663: 'Senegal (Rep. of)',
              664: 'Seychelles (Rep. of)', 665: 'Saint Helena', 557: 'Solomon Islands', 359: 'El Salvador (Rep. of)',
              559: 'American Samoa', 561: 'Samoa (Independent State of)', 268: 'San Marino (Rep. of)',
              563: 'Singapore (Rep. of)',
              564: 'Singapore (Rep. of)', 565: 'Singapore (Rep. of)', 566: 'Singapore (Rep. of)',
              666: 'Somali Democratic Rep.',
              361: 'Saint Pierre and Miquelon (Territorial Collectivity of)', 279: 'Serbia (Rep. of)',
              667: 'Sierra Leone',
              668: 'Sao Tome and Principe (Democratic Rep. of)', 269: 'Switzerland (Confederation of)',
              765: 'Suriname (Rep. '
                   'of)',
              267: 'Slovak Rep.', 278: 'Slovenia (Rep. of)', 669: 'Swaziland (Kingdom of)', 468: 'Syrian Arab Rep.',
              364: 'Turks '
                   'and Caicos Islands',
              670: 'Chad (Rep. of)', 671: 'Togolese Rep.', 567: 'Thailand', 472: 'Tajikistan (Rep. of)',
              434: 'Turkmenistan',
              570: 'Tonga (Kingdom of)', 362: 'Trinidad and Tobago', 672: 'Tunisia', 271: 'Turkey', 572: 'Tuvalu',
              674: 'Tanzania ('
                   'United Rep. of)',
              677: 'Tanzania (United Rep. of)', 470: 'United Arab Emirates', 675: 'Uganda (Rep. of)', 272: 'Ukraine',
              770: 'Uruguay (Eastern Rep. of)', 338: 'United States of America', 366: 'United States of America',
              367: 'United '
                   'States of America',
              368: 'United States of America', 369: 'United States of America', 437: 'Uzbekistan (Rep. of)',
              375: 'Saint '
                   'Vincent and the Grenadines',
              376: 'Saint Vincent and the Grenadines', 377: 'Saint Vincent and the Grenadines',
              775: 'Venezuela (Bolivarian '
                   'Rep. of)',
              379: 'United States Virgin Islands', 378: 'British Virgin Islands', 574: 'Viet Nam (Socialist Rep. of)',
              576: 'Vanuatu (Rep. of)', 577: 'Vanuatu (Rep. of)', 578: 'Wallis and Futuna Islands',
              416: 'Taiwan (Province of '
                   'China)',
              501: 'Adelie Land', 473: 'Yemen (Rep. of)', 475: 'Yemen (Rep. of)', 678: 'Zambia (Rep. of)',
              679: 'Zimbabwe (Rep. of)'
              }

ShipTypeDict = {5:'Navy',6:'Carrier',7:'Cargo',8:'Tanker'}

def getNationFlag(MMSI):
    num = long(MMSI)
    num /=1000000

    if num not in NationDict:
        return 'unknown'
    return NationDict[num]

def getShipType(type):
    num = int(type)
    num /=10
    if num not in ShipTypeDict:
        return 'unknown'
    return ShipTypeDict[num]

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
        write_data_DY(ShipData)
        # all_MMSI.append(ShipData)

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

        write_data_ST(ShipData)
        # all_MMSI.append(ShipData)

def write_data_DY(ShipData):
    MMSI = ShipData['MMSI']
    string = str(MMSI) + ',' + ShipData['DynamicInfo'][0]['LastTime'] + ',' + str(ShipData['DynamicInfo'][0]['Latitude'])\
             + ',' + str(ShipData['DynamicInfo'][0]['Longitude']) + ',' + str(ShipData['DynamicInfo'][0]['Speed']) + \
             ',' + str(ShipData['DynamicInfo'][0]['course']) + ',' + str(ShipData['DynamicInfo'][0]['NaviStatus'])
    with open('./ShipLineTest/ais_dy.txt', 'a') as f:  # DY
        f.write(string + '\n')

def write_data_ST(ShipData):
    MMSI = ShipData['MMSI']
    tmp = str(ShipData['StaticInfo'][0]['Length']) + ' x ' + str(ShipData['StaticInfo'][0]['Width']) + ' m|'
    string = str(MMSI) + '|' + ShipData['StaticInfo'][0]['Name'] + '|' + getNationFlag(MMSI) + '|' + getShipType(
        ShipData['StaticInfo'][0]['ShipType']) + '|N/A|N/A|N/A|' + str(MMSI) + '|' + ShipData['StaticInfo'][0][
        'CallSign'] + '|' + tmp + str(ShipData['StaticInfo'][0]['Draught']) + ' m|'+ str(ShipData['StaticInfo'][0][
                                                                                                         'IMO'])
    with open('./ShipLineTest/ais_st.txt', 'a') as f:  # ST
        f.write(string + '\n')

def Classfication_By_Nation(input_path,Nations):
    import shutil
    print input_path
    if 0 == int(os.path.getsize(input_path)):
        return
    et = ET.parse(input_path)
    element = et.getroot()
    element_Ships = element.findall('Ship')
    for ship in element_Ships:
        mmsi = long(ship.find("MMSI").text)
        if getNationFlag(mmsi) != Nations:
            break
        shutil.copyfile(input_path, './Japan_Tanker/' + os.path.split(input_path)[1])

def Classfication_By_Draught(input_path,draught):
    import shutil
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

    if draught.has_key(int(Draught)):
        draught[int(Draught)] += 1
    else:
        draught[int(Draught)] = 1

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


if __name__ == "__main__":
    all_MMSI_DY=[]
    all_MMSI_ST=[]
    data_paths_dy = []
    data_paths_st = []
    draught = {}


    from matplotlib import pyplot as plt
    from matplotlib.ticker import MultipleLocator


    from matplotlib import pyplot as plt
    from matplotlib.ticker import MultipleLocator
    speed_list = []
    draught_list = []
    for file in [os.path.join('/media/xxxx/xx/AISProject/Japan_Tanker', s) for s in os.listdir(
            '/media/xxxx/xx/AISProject/Japan_Tanker')]:
        X,Y = Classfication_By_WS(file)
        speed_list.append(X)
        draught_list.append(Y)

    speed_list = np.array(speed_list)
    draught_list = np.array(draught_list)
    plt.scatter(speed_list,draught_list,25,cmap=plt.cm.jet,marker='o',edgecolors='k',zorder=10,alpha=0.7)
    plt.xticks(np.arange(0,400000,20000))
    plt.yticks(np.arange(6,25,2))
    plt.xlabel("Ship Tanker Tonnage")
    plt.ylabel("Speed")
    plt.title("Japanese Ship Tanker Tonnage/Speed Scatter")
    plt.grid()
    plt.show()