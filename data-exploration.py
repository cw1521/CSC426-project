import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import math
import random
import json
import csv



# def get_pos_vector_df(pos_vector_string):
#     pos_vector_list = []
#     pos_vector_string = pos_vector_string.strip("]").strip("[")
#     pos_vector_string = pos_vector_string.replace("'", "\"")
#     pos_vector_string = pos_vector_string.replace("datetime.datetime(", "[")
#     pos_vector_string = pos_vector_string.replace(")", "]")
#     pos_vector_string = pos_vector_string.replace('"Trak": None', '"Trak": 0')
#     pos_vector_string = pos_vector_string.replace("},", "},,")

#     for elem in pos_vector_string.split(",,"):
#         # print(elem)
#         elem = json.loads(elem)
#         pos_vector_list.append(elem)

#     return pd.DataFrame(pos_vector_list)


def in_bounds(pos_vector_df, bounds):
    if pos_vector_df["Lat"].min() >= bounds[2] and pos_vector_df["Lat"].max() <= bounds[3]:
        if pos_vector_df["Long"].min() >= bounds[0] and pos_vector_df["Long"].max() <= bounds[1]:
            return True
    return False


def filter_pos_vector_df(pos_vector_df, bounds):
    # print(pos_vector)
    df = pd.DataFrame(pos_vector_df)
    in_bounds = (df["Lat"] >= bounds[2]) & (df["Lat"] <= bounds[3]) & (df["Long"] <= bounds[1]) & (df["Long"] >= bounds[0])
    # print(in_bounds)
    # # df = df[df[in_bounds]]

    return df[in_bounds]


def get_distance(coords):
    distance = 0
    for i in range(len(coords)):
        if i < len(coords) - 1:
            distance += math.sqrt((coords[i+1][1]-coords[i][1])**2+(coords[i+1][0]-coords[i][0])**2)
    return distance





if __name__ == "__main__":
    input_dir = "./input/"

    # flightDf = pd.read_csv(input_dir+"flight-vector.csv", encoding="latin-1", low_memory=False)

    flightDf = pd.read_json(input_dir+"flight-vector.json")

    fedDf = pd.read_json(input_dir+"fed-list.json")

    # print(flightDf.head())

    # fedFlightDf = flightDf[flightDf["type_registrant"] == 5]

    b_box = (-89, -87, 30, 32)

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(b_box, crs=ccrs.PlateCarree())
    # plt.rcParams["figure.figsize"] = (8,8)
    ax.coastlines()
    ax.stock_img()

    ax.add_feature(cfeature.STATES)
    

    distances = []

    for index, row in flightDf.iterrows():
        # print(row["pos_vector_array"])
        pos_vector_df = pd.DataFrame(row["pos_vector_array"])
        # print(pos_vector_df)
        if in_bounds(pos_vector_df, b_box):
            # pos_vector_df = filter_pos_vector_df(pos_vector_df, b_box)
            long, lat = pos_vector_df["Long"], pos_vector_df["Lat"]
            longArr = long.to_numpy()
            latArr = lat.to_numpy()
            coords = np.stack((longArr, latArr), axis=1)
            
            distance = get_distance(coords)
            # distances.append(distance)
            # print(row["Op"], row["type_registrant"], distance)
            if distance < 0.8:

                r = random.random()
                b = random.random()
                g = random.random()
                # print(row["Op"], row["type_registrant"])
                color = (r, g, b)
                plt.scatter(longArr, latArr, color=color)

    # plt.hist(distances)
    plt.show()
    


    # print(fedFlightDf)



    # for index, row in fedDf.iterrows():
    #     # print(row["pos_vector_array"])
    #     pos_vector_df = pd.DataFrame(row["pos_vector"])

    #     # print(pos_vector_df["Lat"].min(), pos_vector_df["Lat"].max(), pos_vector_df["Long"].min(), pos_vector_df["Long"].min())
    #     # print(pos_vector_df)
    #     if in_bounds(pos_vector_df, b_box):
    #         # pos_vector_df = filter_pos_vector_df(pos_vector_df, b_box)
    #         long, lat = pos_vector_df["Longitude"], pos_vector_df["Latitude"]
    #         longArr = long.to_numpy()
    #         latArr = lat.to_numpy()

    #         print(longArr, latArr)

        
    #         coords = np.stack((longArr, latArr), axis=1)
            
    #         distance = get_distance(coords)
    #         # distances.append(distance)
    #         # print(row["Op"], row["type_registrant"], distance)
            


    #         # if distance < 0.8:

    #         #     r = random.random()
    #         #     b = random.random()
    #         #     g = random.random()
    #         #     # print(row["Op"], row["type_registrant"])
    #         #     color = (r, g, b)
    #         #     plt.scatter(longArr, latArr, color=color)



    #         r = random.random()
    #         b = random.random()
    #         g = random.random()
    #         # print(row["Op"], row["type_registrant"])
    #         color = (r, g, b)
    #         plt.scatter(longArr, latArr, color=color)

    # # plt.hist(distances)
    # plt.show()