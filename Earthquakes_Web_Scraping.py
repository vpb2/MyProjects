import requests
import lxml.html
import re
import pandas as pd
import numpy as np
from time import sleep

def construct_url(lat, long, rad, start_yr, end_yr) -> str:  #This function constructs and returns an url using parameters

    base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=xml&orderby=time-asc&minmagnitude=4&eventtype=earthquake&starttime='
    start_year = str(start_yr)
    end_year = str(end_yr)
    r_lat = str(lat)
    r_long = str(long)
    r_rad = str(rad)

    #The below operation is constructing url dynamically for one year at a time, based on parameters passed
    final_url = base_url + start_year + '-01-01&endtime=' + end_year + '-12-31&latitude=' + r_lat + '&longitude=' + r_long + '&maxradiuskm=' + r_rad

    return final_url

def get_page_tree(url): #This function constructs and returns tree from the xml document being downloaded

    url_string = url
    year = re.findall('(\d{4})-\d{2}-\d{2}', url_string)[0] #To capture the year, in order to display along with status code
    page_tree = None
    while page_tree is None:
        try:
            req = requests.get(url)
            print("Status code from server response for year {}: ".format(year), req.status_code)

            #The following if statement checks the status code to confirm if the response from server is right or not
            if req.status_code == 200:
                page_tree = lxml.html.fromstring(req.content)

            else:
                page_tree = None
                print("Reason of failure for year {}: ".format(year), req.reason)

            break

        except (ConnectionError, ConnectionRefusedError) as e:
            print('Error retrieving web page.  Retrying in 10 seconds...')
            sleep(10)

    return page_tree

def get_list_eq_per_yr(lati, longi, radi): #This function creates and returns a list of list containing Earthquake data for every year

    start_year = 1950
    end_year = 2019

    r_lati = lati
    r_longi = longi
    r_radi = radi

    list_of_all_eq = []
    count_dict = {}

    for yr in range(start_year, end_year + 1):

        url = construct_url(r_lati, r_longi, r_radi, yr, yr)
        page_data = get_page_tree(url)

        if page_data != None:

            eq_rows = page_data.xpath("//text")
            mag_rows = page_data.xpath("//mag/value")
            list_eq_per_yr = []
            count_per_year = 0

            for item in range(0,len(eq_rows)): #Constructs a list for every Earthquake with region and magnitude

                eq_name = eq_rows[item].text
                eq_mag = mag_rows[item].text
                elem = [eq_name, eq_mag]
                list_eq_per_yr.append(elem)
                count_per_year += 1

            count_dict[yr] = count_per_year
            count_dict_elem = [{yr: count_dict[yr]}]
            list_eq_per_yr.append(count_dict_elem) #Adds a dictionary item of form {year: count} at the end of each year's list
            list_of_all_eq.append(list_eq_per_yr)

        else: #This else part executes when the page tree doesn't have any data

            #When there are no Earthquakes in a particular year, the following code adds count=0 for that year in the list
            list_eq_per_yr = []
            count_dict[yr] = 0
            count_dict_elem = [{yr : count_dict[yr]}]
            list_eq_per_yr.append(count_dict_elem)
            list_of_all_eq.append(list_eq_per_yr)


    return list_of_all_eq

def get_mag_dict(list_of_eqs): #This function creates and returns a dictionary of form {magnitude_range : count}

    mag_dict = {}
    count_list = [0,0,0,0,0,0]

    for year_data in list_of_eqs:
        for individual_eq in year_data:
            if len(individual_eq) == 2:

                #Following statements categorise each Earthquake by magnitude and increase that corresponding count
                if float(individual_eq[1])>=4 and float(individual_eq[1])<5:
                    count_list[0] += 1
                elif float(individual_eq[1])>=5 and float(individual_eq[1])<6:
                    count_list[1] += 1
                elif float(individual_eq[1])>=6 and float(individual_eq[1])<7:
                    count_list[2] += 1
                elif float(individual_eq[1])>=7 and float(individual_eq[1])<8:
                    count_list[3] += 1
                elif float(individual_eq[1])>=8 and float(individual_eq[1])<9:
                    count_list[4] += 1
                else:
                    count_list[5] += 1

    for i in range(len(count_list)):
        mag_dict[i+4] = count_list[i]

    return mag_dict

def create_yr_df(lst1, lst2): #This function creates and returns a dataframe for the Year data(output 1)

    start = 1950

    year_df_r1 = pd.DataFrame(columns=['Year', 'Region_1'])
    for year_data in lst1:
        for individual_eq in year_data:
            if len(individual_eq) == 1:
                elem = individual_eq[0]
                for key, value in elem.items():
                    year_df_r1.loc[key- start] = [key, value]

    year_df_r2 = pd.DataFrame(columns=['Year', 'Region_2'])
    for year_data2 in lst2:
        for individual_eq2 in year_data2:
            if len(individual_eq2) == 1:
                elem2 = individual_eq2[0]
                for key2, value2 in elem2.items():
                    year_df_r2.loc[key2 - start] = [key2, value2]


    year_df = pd.merge(year_df_r1, year_df_r2, on=['Year'])
    return year_df

def create_mag_df(mag_dict1, mag_dict2): #This function creates and returns a dataframe for the Magnitude data(output 2)

    mag_df_r1 = pd.DataFrame(columns=["Magnitude", "Region_1"])
    for k,v in mag_dict1.items():
        mag_df_r1.loc[k-4] = [k, v]

    mag_df_r2 = pd.DataFrame(columns=["Magnitude", "Region_2"])
    for k2, v2 in mag_dict2.items():
        mag_df_r2.loc[k2 - 4] = [k2, v2]

    mag_df = pd.merge(mag_df_r1, mag_df_r2, on=['Magnitude'])
    return mag_df

def print_decade_data(df): #This function prints the output table 1 (Earthquakes classified by decade)

    decades = df.groupby((df["Year"] / 10).astype('int64')).sum()
    decades['Decade'] = decades.index
    decades['Decade'] = decades['Decade'].apply(str)
    decades.Decade = decades.Decade + '0s'
    decades = decades[["Decade", "Region_1", "Region_2"]].reset_index(drop=True)

    decades["Reg1_Per"] = (decades["Region_1"] / (decades["Region_1"] + decades["Region_2"] +.000000001) * 100).apply(int)
    decades["Reg2_Per"] = (decades["Region_2"] / (decades["Region_1"] + decades["Region_2"] +.000000001) * 100).apply(int)
    decades.loc[decades['Reg2_Per'] != 0, 'Reg2_Per'] = decades["Reg2_Per"] + 1

    decades = decades[["Decade", "Region_1", "Reg1_Per", "Region_2", "Reg2_Per"]]

    total = decades.apply(np.sum)
    total['Decade'] = 'Total'
    total["Reg1_Per"] = int((total["Region_1"]/ (total["Region_1"]+total["Region_2"])) * 100)
    total["Reg2_Per"] = int((total["Region_2"]/ (total["Region_1"]+total["Region_2"])) * 100) + 1

    decades = pd.concat([decades, total.to_frame().T],ignore_index=True)

    decades["Reg1_Per"] = decades["Reg1_Per"].apply(str)
    decades.Reg1_Per = decades.Reg1_Per + '%'
    decades["Reg2_Per"] = decades["Reg2_Per"].apply(str)
    decades.Reg2_Per = decades.Reg2_Per + '%'

    print("-------------------------------------------------------------------")
    print("--- Total earthquakes per region per decade with magnitude >= 4 ---")
    print("-------------------------------------------------------------------")
    print(decades)
    print("-------------------------------------------------------------------\n\n")

def print_mag_data(mags): #This function prints the output table 2 (Earthquakes classified by Magnitude range)

    mags['Magnitude'] = mags['Magnitude'].apply(str)
    mags.Magnitude = mags.Magnitude + '.00-' + mags.Magnitude + '.99'

    mags["R1_Per"] = (mags["Region_1"] / (mags["Region_1"] + mags["Region_2"] +.000000001) * 100).apply(int)
    mags["R2_Per"] = (mags["Region_2"] / (mags["Region_1"] + mags["Region_2"] +.000000001) * 100).apply(int)
    mags.loc[mags['R2_Per'] != 0, 'R2_Per'] = mags["R2_Per"] + 1

    total1 = mags.apply(np.sum)
    total1['Magnitude'] = 'Total'
    total1["R1_Per"] = int((total1["Region_1"] / (total1["Region_1"] + total1["Region_2"])) * 100)
    total1["R2_Per"] = int((total1["Region_2"] / (total1["Region_1"] + total1["Region_2"])) * 100) + 1

    mags = pd.concat([mags, total1.to_frame().T], ignore_index=True)

    mags["R1_Per"] = mags["R1_Per"].apply(str)
    mags.R1_Per = mags.R1_Per + '%'
    mags["R2_Per"] = mags["R2_Per"].apply(str)
    mags.R2_Per = mags.R2_Per + '%'

    mags = mags[["Magnitude", "Region_1", "R1_Per", "Region_2", "R2_Per"]]
    print("-------------------------------------------------------------------")
    print("-------- Total earthquakes per region per magnitude range ---------")
    print("-------------------------------------------------------------------")
    print(mags)
    print("-------------------------------------------------------------------")


#Main function
region_1_lat = input("Enter the latitude co-ordinates for Region 1 (Ex: Bangalore = 12.97): ")
region_1_long = input("Enter the longitude co-ordinates for Region 1 (Ex: Bangalore = 77.59): ")
region_2_lat = input("Enter the latitude co-ordinates for Region 2 (Ex: Chicago = 41.87): ")
region_2_long = input("Enter the longitude co-ordinates for Region 2 (Ex: Chicago = 87.62): ")
radius = input("Enter the radius of the circular area (in kms, Ex: 1000): ")

print("\n--------------------- Region 1 ----------------------")
region_1 = get_list_eq_per_yr(region_1_lat,region_1_long,radius)
print("-----------------------------------------------------\n")
print("\n--------------------- Region 2 ----------------------")
region_2 = get_list_eq_per_yr(region_2_lat,region_2_long,radius)
print("-----------------------------------------------------\n")

region_1_mag_dict = get_mag_dict(region_1)
region_2_mag_dict = get_mag_dict(region_2)

year_dataframe = create_yr_df(region_1, region_2)
magnitude_dataframe = create_mag_df(region_1_mag_dict, region_2_mag_dict)

print_decade_data(year_dataframe)
print_mag_data(magnitude_dataframe)








