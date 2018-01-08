#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ais_parse as parse
import ais_draw  as draw


if __name__ == "__main__":
    all_MMSI_cargo = []
    all_MMSI_tanker = []
    cargo_path = "xxx"
    tanker_path = "xxx"

    tmp_cargo = [os.path.join(cargo_path + os.sep, s) for s in os.listdir(cargo_path + os.sep)]
    tmp_tanker = [os.path.join(tanker_path + os.sep, s) for s in os.listdir(tanker_path + os.sep)]

    for file in tmp_cargo:
        parse.get_data_DY(file, all_MMSI_cargo)
    for file in tmp_tanker:
        parse.get_data_DY(file, all_MMSI_tanker)

    # print all_MMSI_cargo,all_MMSI_tanker
    draw.mapscatter(all_MMSI_cargo,all_MMSI_tanker)