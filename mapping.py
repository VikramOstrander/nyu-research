# ------------
# program to generate geographic visualizations
# cleaned geodata from state_data and zip_data in data/shapefiles
# ------------

import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import contextily as cx

from pysal.lib import weights
from pysal.explore import esda
from pysal.viz import splot
from splot import esda as esdaplot
from pysal.model import spreg

# import geodata
geodata_state = gpd.read_file("C:\\Users\\vikra\\NYU_2023\\data\\shapefiles\\state_data\\state.shp")
geodata_state.to_crs("EPSG:3857", inplace=True)

geodata_zip = gpd.read_file("C:\\Users\\vikra\\NYU_2023\\data\\shapefiles\\zip_data\\zip.shp")
geodata_zip.to_crs("EPSG:3857", inplace=True)

geodata_doc = gpd.read_file("C:\\Users\\vikra\\NYU_2023\\data\\shapefiles\\doc_data\\doc.shp")
geodata_doc.to_crs("EPSG:3857", inplace=True)

geodata_doc = geodata_doc[geodata_doc.State != 'AS']
geodata_doc = geodata_doc[geodata_doc.State != 'GU']
geodata_doc = geodata_doc[geodata_doc.State != 'VI']
geodata_doc = geodata_doc[geodata_doc.State != 'MP']

geodata_doc['rated'] = np.where(geodata_doc['Rating'] >= 4, True, False)
geodata_doc['accepts'] = np.where(geodata_doc['Accepts Me'] == True, True, False)
geodata_doc['both'] = geodata_doc['rated'] & geodata_doc['accepts']

geodata_zip = geodata_zip[geodata_zip['pop'] != 0]
geodata_zip['doc_total'] = geodata_zip['doc']
geodata_zip['doc'] = geodata_zip['doc'] / geodata_zip['pop']
geodata_zip = geodata_zip[geodata_zip['doc'] <= 0.5]


# isolate cities
geodata_zip.ZCTA = geodata_zip.ZCTA.astype('int')
geodata_doc.Zipcode = geodata_doc.Zipcode.astype('int')
NYC = [10001, 10451, 10002, 10452, 10003, 10453, 10004, 10454, 10005, 10455, 10006, 10456, 10007, 10457, 10009, 10458, 10010, 10459, 10011, 10460, 10012, 10461, 10013, 10462, 10014, 10463, 10015, 10464, 10016, 10465, 10017, 10466, 10018, 10467, 10019, 10468, 10020, 10469, 10021, 10470, 10022, 10471, 10023, 10472, 10024, 10473, 10025, 10474, 10026, 10475, 10027, 11201, 10028, 11203, 10029, 11204, 10030, 11205, 10031, 11206, 10032, 11207, 10033, 11208, 10034, 11209, 10035, 11210, 10036, 11211, 10037, 11212, 10038, 11213, 10039, 11214, 10040, 11215, 10041, 11216, 10044, 11217, 10045, 11218, 10048, 11219, 10055, 11220, 10060, 11221, 10069, 11222, 10090, 11223, 10095, 11224, 10098, 11225, 10099, 11226, 10103, 11228, 10104, 11229, 10105, 11230, 10106, 11231, 10107, 11232, 10110, 11233, 10111, 11234, 10112, 11235, 10115, 11236, 10118, 11237, 10119, 11238, 10120, 11239, 10121, 11241, 10122, 11242, 10123, 11243, 10128, 11249, 10151, 11252, 10152, 11256, 10153, 10001, 10154, 10002, 10155, 10003, 10158, 10004, 10161, 10005, 10162, 10006, 10165, 10007, 10166, 10009, 10167, 10010, 10168, 10011, 10169, 10012, 10170, 10013, 10171, 10014, 10172, 10015, 10173, 10016, 10174, 10017, 10175, 10018, 10176, 10019, 10177, 10020, 10178, 10021, 10199, 10022, 10270, 10023, 10271, 10024, 10278, 10025, 10279, 10026, 10280, 10027, 10281, 10028, 10282, 10029, 10301, 10030, 10302, 10031, 10303, 10032, 10304, 10033, 10305, 10034, 10306, 10035, 10307, 10036, 10308, 10037, 10309, 10038, 10310, 10039, 10311, 10040, 10312, 10041, 10314, 10044, 10451, 10045, 10452, 10048, 10453, 10055, 10454, 10060, 10455, 10069, 10456, 10090, 10457, 10095, 10458, 10098, 10459, 10099, 10460, 10103, 10461, 10104, 10462, 10105, 10463, 10106, 10464, 10107, 10465, 10110, 10466, 10111, 10467, 10112, 10468, 10115, 10469, 10118, 10470, 10119, 10471, 10120, 10472, 10121, 10473, 10122, 10474, 10123, 10475, 10128, 11004, 10151, 11101, 10152, 11102, 10153, 11103, 10154, 11104, 10155, 11105, 10158, 11106, 10161, 11109, 10162, 11201, 10165, 11203, 10166, 11204, 10167, 11205, 10168, 11206, 10169, 11207, 10170, 11208, 10171, 11209, 10172, 11210, 10173, 11211, 10174, 11212, 10175, 11213, 10176, 11214, 10177, 11215, 10178, 11216, 10199, 11217, 10270, 11218, 10271, 11219, 10278, 11220, 10279, 11221, 10280, 11222, 10281, 11223, 10282, 11224, 11101, 11225, 11102, 11226, 11103, 11228, 11004, 11229, 11104, 11230, 11105, 11231, 11106, 11232, 11109, 11233, 11351, 11234, 11354, 11235, 11355, 11236, 11356, 11237, 11357, 11238, 11358, 11239, 11359, 11241, 11360, 11242, 11361, 11243, 11362, 11249, 11363, 11252, 11364, 11256, 11365, 11351, 11366, 11354, 11367, 11355, 11368, 11356, 11369, 11357, 11370, 11358, 11371, 11359, 11372, 11360, 11373, 11361, 11374, 11362, 11375, 11363, 11377, 11364, 11378, 11365, 11379, 11366, 11385, 11367, 11411, 11368, 11412, 11369, 11413, 11370, 11414, 11371, 11415, 11372, 11416, 11373, 11417, 11374, 11418, 11375, 11419, 11377, 11420, 11378, 11421, 11379, 11422, 11385, 11423, 11411, 11426, 11412, 11427, 11413, 11428, 11414, 11429, 11415, 11416, 11432, 11417, 11433, 11418, 11434, 11419, 11435, 11420, 11436, 11421, 11691, 11422, 11692, 11423, 11693, 11426, 11694, 11427, 11697, 11428, 10301, 11429, 10302, 10303, 11432, 10304, 11433, 10305, 11434, 10306, 11435, 10307, 11436, 10308, 11691, 10309, 11692, 10310, 11693, 10311, 11694, 10312, 11697, 10314, 10065, 10075]
LA = [90031, 90032, 90041, 90042, 90065, 91204, 91205, 90004, 90005, 90006, 90012, 90013, 90014, 90015, 90017, 90019, 90021, 90029, 90026, 90027, 90028, 90035, 90036, 90038, 90039, 90046, 90048, 90057, 90068, 90069, 90071, 90022, 90023, 90031, 90032, 90033, 90063, 90024, 90025, 90034, 90035, 90049, 90056, 90064, 90066, 90067, 90077, 90094, 90210, 90212, 90230, 90232, 90272, 90291, 90292, 90401, 90402, 90010, 90020, 90211, 90403, 90404, 90405, 90001, 90002, 90003, 90008, 90011, 90016, 90018, 90037, 90043, 90044, 90047, 90059, 90061, 90062, 90007, 90220, 90305, 90040, 90058, 90201, 90220, 90221, 90240, 90241, 90242, 90255, 90262, 90270, 90280, 90623, 90604, 90605, 90606, 90638, 90640, 90650, 90660, 90670, 90701, 90703, 90706, 90723, 90045, 90245, 90249, 90250, 90254, 90260, 90261, 90266, 90274, 90275, 90277, 90278, 90293, 90301, 90302, 90303, 90304, 90501, 90503, 90504, 90505, 90506, 90717, 90220, 90221, 90502, 90710, 90712, 90713, 90715, 90716, 90731, 90732, 90744, 90745, 90746, 90755, 90802, 90803, 90804, 90805, 90806, 90807, 90808, 90810, 90813, 90814, 90815, 90822, 90831, 90840, 90846, 90248, 90247, 90222]
CHI = [60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60609, 60610, 60611, 60612, 60613, 60614, 60615, 60616, 60617, 60618, 60619, 60620, 60627, 60621, 60622, 60623, 60624, 60625, 60626, 60628, 60629, 60630, 60630, 60630, 60631, 60632, 60633,60633, 60634, 60634, 60634, 60636, 60642, 60637, 60638, 60638, 60639, 60640, 60641, 60643,60643, 60644, 60645, 60645,60646, 60646, 60647, 60649, 60651, 60652, 60653, 60654, 60655, 60655, 60655, 60656, 60656, 60656, 60657, 60659, 60659, 60660, 60661, 60664, 60666, 60680, 60681, 60690, 60691]
HOU = [77002, 77003, 77004, 77005, 77006, 77007, 77008, 77009, 77010, 77011, 77012, 77013, 77014, 77015, 77016, 77017, 77018, 77019, 77020, 77021, 77022, 77023, 77024, 77025, 77026, 77027, 77028, 77029, 77030, 77031, 77032, 77033, 77034, 77035, 77036, 77037, 77038, 77039, 77040, 77041, 77042, 77043, 77044, 77045, 77046, 77047, 77048, 77049, 77050, 77051, 77053, 77054, 77055, 77056, 77057, 77058, 77059, 77060, 77061, 77062, 77063, 77064, 77065, 77066, 77067, 77068, 77069, 77070, 77071, 77072, 77073, 77074, 77075, 77076, 77077, 77078, 77079, 77080, 77082, 77083, 77084, 77085, 77086, 77087, 77088, 77089, 77090, 77092, 77093, 77094, 77095, 77096, 77098, 77099, 77091, 77401]


# global vars and dicts
ATTRIBUTES = {'pop': 'Population', 'pov': 'Poverty Rate', 'doc': 'Number of Doctors'}
FILTERS = {'rated': 'Rated Well', 'accepts': 'Accept Medicaid', 'both': 'Rated Well and Accept Medicaid'}
CMAP = 'coolwarm'
COLOR = 'blue'
K = 1


# print instructions for map generation
def instructions(attr = None):
    intro = False
    codes = False
    tag = False
    filter = False
    ex = False

    match attr:
        case 'attributes':
            codes = True
        case 'tags':
            tag = True
        case 'filter':
            filter = True
        case 'examples':
            ex = True
        case _:
            intro = True
            codes = True
            tag = True
            filter = True
            ex = True
    
    print("\n" + "-"*40)

    if intro:
        print("for a specific instruction: type 'help' followed by 'attributes', 'tags', 'filter', or 'examples'\n")
        print("- input a location code followed by an attribute code and optionally a tag")
        print("- location codes are 2 letter state abbreviations, 'US', 'NYC', 'LA', or 'HOU'")
    if codes:
        print("- attribute codes are:"
              + "\n\t> 'POP' for population choropleth" 
              + "\n\t> 'POV' for poverty rate choropleth"
              + "\n\t> 'DOC' for doctors choropleth"
              + "\n\t> 'DIST' for doctors distribution")
    if tag:
        print("- tags are:"
              + "\n\t> '-LOG' to logarithmically scale and normalize a choropleth attributes"
              + "\n\t> '-HEAT' to create a heatmap for a distribution"
              + "\n\t> '-SA' to perform spatial analysis on a choropleth attributes"
              + "\n\t> '-SABV' to perform bivariate spatial analysis on two choropleth attributes (separated by '_')"
              + "\n\t> '-NSIG' to ignore significance filtering for spatial analysis"
              + "\n\t> '-FILTER=____' to add a filter to doctors"
              + "\n\t> '-COLOR=____' to change the point color"
              + "\n\t> '-CMAP=____' to change the color map for all maps")
    if filter:
        print("- filters are:"
              + "\n\t> '-FILTER=rated' for doctors with over 3 stars and over 5 reviews"
              + "\n\t> '-FILTER=accepts' for doctors that accept medicaid"
              + "\n\t> '-FILTER=both' for doctors rated well that accept medicaid")
    if ex:
        print("\n  examples:"
              + "\n\t> 'US POP' generates a map of population by state in the US"
              + "\n\t> 'NY POV -LOG' generates a map of poverty rates by logarithmically normalized poverty rates by zipcode in NY"
              + "\n\t> 'VA DIST -FILTER=accepts' generates a map of doctors by their medicaid acceptance in VA"
              + "\n\t> 'CA DIST -HEAT' generates a heatmap of doctors in CA"
              + "\n\t> 'US DOC -SA' generates a Moran's I visualizations for doctors in the US"
              + "\n\t> 'US POV_DOC -FILTER=rated -SABV' generates a Moran's I visualizations for poverty and doctors in the US")
    
    print("-"*40 + "\n")


# generate a choropleth map
def attr_map(key, attr, filter, log):

    x = attr
    attr = ATTRIBUTES[attr]

    if key == 'US':
        dataset = geodata_state
        dataset = dataset[dataset['state'] != 'AK']
        dataset = dataset[dataset['state'] != 'HI']
        dataset = dataset[dataset['state'] != 'PR']
    elif key == 'NYC':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(NYC)]
    elif key == 'LA':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(LA)]
    elif key == 'HOU':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(HOU)]
    else:
        dataset = geodata_zip[geodata_zip['STATE'] == key]

    if filter and x == 'doc':
        x = filter
        attr += f" ({FILTERS[filter]})"
    
    fig, ax = plt.subplots(1, 1, figsize=(9,6))
    plt.title(f"Map of {key} by {attr}")
    ax.set_axis_off()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.1)

    norm = None
    logtext = ""
    if log:
        norm = colors.LogNorm(vmin=max(0.1, dataset[x].min()), vmax=dataset[x].max(), clip=True)
        logtext += " - Logarithmically Normalized"

    if key == 'US':
        map = dataset.to_crs(epsg=3857).plot(column=x, ax=ax, cmap=CMAP, legend=True, edgecolor='k', linewidth=0.1, cax=cax, norm=norm)
        plt.ylabel(f"{attr} by State" + logtext)
    else:
        map = dataset.to_crs(epsg=3857).plot(column=x, ax=ax, cmap=CMAP, legend=True, cax=cax, norm=norm)
        plt.ylabel(f"{attr} by Zipcode" + logtext)
    cx.add_basemap(map, source=cx.providers.CartoDB.PositronNoLabels, attribution_size=4)
    plt.show()


# generate a distribution map
def doc_map(key, filter, heat):

    if key == 'US':
        doctors = geodata_doc
        doctors = doctors[doctors['State'] != 'AK']
        doctors = doctors[doctors['State'] != 'HI']
        doctors = doctors[doctors['State'] != 'PR']
    elif key == 'NYC':
        doctors = geodata_doc[geodata_doc['Zipcode'].isin(NYC)]
    elif key == 'LA':
        doctors = geodata_doc[geodata_doc['Zipcode'].isin(LA)]
    elif key == 'HOU':
        doctors = geodata_doc[geodata_doc['Zipcode'].isin(HOU)]
    else:
        doctors = geodata_doc[geodata_doc['State'] == key]

    fig, ax = plt.subplots(1, 1, figsize=(9,6))
    ax.set_axis_off()

    if filter is None:
        if heat:
            plt.title(f"Heatmap of Doctors in {key}")
            sns.kdeplot(ax=ax, x=doctors.to_crs(epsg=3857)['geometry'].x, y= doctors.to_crs(epsg=3857)['geometry'].y, fill=True, cmap=CMAP, alpha=0.6)
        else:
            plt.title(f"Doctors in {key}")
            doctors.to_crs(epsg=3857).plot(color=COLOR, ax=ax, marker='o', markersize=1, alpha=0.25)
    else:
        if heat:
            plt.title(f"Heatmap of Doctors in {key} ({FILTERS[filter]})")
            doctors = doctors[doctors[filter] == True]
            sns.kdeplot(ax=ax, x=doctors.to_crs(epsg=3857)['geometry'].x, y= doctors.to_crs(epsg=3857)['geometry'].y, fill=True, cmap=CMAP, alpha=0.6)
        else:
            plt.title(f"Doctors in {key} ({FILTERS[filter]})")
            map = doctors.to_crs(epsg=3857).plot(column=filter, cmap=CMAP, ax=ax, marker='o', markersize=1, alpha=0.25, categorical=True, legend=True)
    cx.add_basemap(ax, crs='EPSG:3857', source=cx.providers.CartoDB.PositronNoLabels, attribution_size=4)
    plt.show()


# perform spatial autocorrelation
def spatial_autocorr(key, attr, filter, nsig):

    x = attr
    attr = ATTRIBUTES[attr]

    if key == 'US':
        dataset = geodata_zip
        dataset = dataset[dataset['STATE'] != 'AK']
        dataset = dataset[dataset['STATE'] != 'HI']
        dataset = dataset[dataset['STATE'] != 'PR']
    elif key == 'NYC':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(NYC)]
    elif key == 'LA':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(LA)]
    elif key == 'CHI':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(CHI)]
    elif key == 'HOU':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(HOU)]
    else:
        dataset = geodata_zip[geodata_zip['STATE'] == key]

    if filter and x == 'doc':
        x = filter
        attr += f" ({FILTERS[filter]})"
    
    neighbors = len(dataset)**(1/2) if K == 1 else K
    neighbors = int(neighbors) if int(neighbors) % 2 == 1 else int(neighbors) + 1
    w = weights.distance.KNN.from_dataframe(dataset, k=neighbors)
    w.transform = "R"

    moran = esda.moran.Moran(dataset[x], w)
    print(f"--The Moran's I Score is {round(moran.I, 4)} with a P-Value of {round(moran.p_sim, 4)}")
    if moran.p_sim < 0.05:
        print(f"--There is Spatial Autocorrelation in {attr}")
    else:
        print(f"--There is no Spatial Autocorrelation in {attr}")
    
    print(f"--The Graph Shows the Relationship between {attr} and its Spatial Lag")
    fig, ax = plt.subplots(figsize=(9, 9))
    esdaplot.moran_scatterplot(moran, ax=ax)
    plt.ylim([-2, 2])
    plt.xlim([-10, 10])
    plt.show()

    print(f"--HH = Region with Positive Spatial Autocorrelation (Clusters of High {attr})")
    print(f"--HL = Region with no Spatial Autocorrelation")
    print(f"--LH = Region with no Spatial Autocorrelation")
    print(f"--LL = Region with Negative Spatial Autocorrelation (Clusters of Low {attr})")
    print(f"--ns = Not Significant")
    fig, ax = plt.subplots(1, 1, figsize=(9,6))
    lisa = esda.moran.Moran_Local(dataset[x], w)
    esdaplot.lisa_cluster(lisa, dataset.to_crs(epsg=3857), p=max(0.05, 1*nsig), ax=ax)
    cx.add_basemap(ax, crs='EPSG:3857', source=cx.providers.CartoDB.PositronNoLabels, attribution_size=4)
    plt.show()


# perform bivariate spatial autocorrelation
def spatial_autocorr_bv(key, attr1, attr2, filter, nsig):

    x = attr1
    y = attr2
    attr1 = ATTRIBUTES[attr1]
    attr2 = ATTRIBUTES[attr2]

    if key == 'US':
        dataset = geodata_zip
        dataset = dataset[dataset['STATE'] != 'AK']
        dataset = dataset[dataset['STATE'] != 'HI']
        dataset = dataset[dataset['STATE'] != 'PR']
    elif key == 'NYC':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(NYC)]
    elif key == 'LA':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(LA)]
    elif key == 'CHI':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(CHI)]
    elif key == 'HOU':
        dataset = geodata_zip[geodata_zip['ZCTA'].isin(HOU)]
    else:
        dataset = geodata_zip[geodata_zip['STATE'] == key]

    if filter:
        if x == 'doc':
            x = filter
            attr1 += f" ({FILTERS[filter]})"
        elif y == 'doc':
            y = filter
            attr2 += f" ({FILTERS[filter]})"    

    neighbors = len(dataset)**(1/2) if K == 1 else K
    neighbors = int(neighbors) if int(neighbors) % 2 == 1 else int(neighbors) - 1
    w = weights.distance.KNN.from_dataframe(dataset, k=neighbors)
    w.transform = "R"
    
    moran_bv = esda.moran.Moran_BV(dataset[x], dataset[y], w)
    print(f"--The Moran's I Score is {round(moran_bv.I, 4)} with a P-Value of {round(moran_bv.p_sim, 4)}")
    if moran_bv.p_sim < 0.05:
        print(f"--There is Spatial Correlation between {attr1} and {attr2}")
    else:
        print(f"--There is no Spatial Correlation between {attr1} and {attr2}")
    print(f"--The Graph Shows the Relationship between {attr1} and the Spatial Lag of {attr2}")
    fig, ax = plt.subplots(figsize=(9, 9))
    esdaplot.moran_scatterplot(moran_bv, ax=ax)
    plt.xlim([-5, 5])
    plt.ylim([-2, 2])
    plt.show()

    print(f"--HH = Region with High {attr1} and {attr2}")
    print(f"--HL = Region with High {attr1} and Low {attr2}")
    print(f"--LH = Region with Low {attr1} and High {attr2}")
    print(f"--LL = region with Low {attr1} and {attr2}")
    fig, ax = plt.subplots(1, 1, figsize=(9,6))
    lisa = esda.moran.Moran_Local_BV(dataset[x], dataset[y], w)
    esdaplot.lisa_cluster(lisa, dataset.to_crs(epsg=3857), p=max(0.05, 1*nsig), ax=ax)
    cx.add_basemap(ax, crs='EPSG:3857', source=cx.providers.CartoDB.PositronNoLabels, attribution_size=4)

    if not nsig:
        dataset["p-sim"] = lisa.p_sim
        sig = 1 * (lisa.p_sim < 0.05)
        dataset["sig"] = sig
        spots = lisa.q * sig
    else:
        spots = lisa.q

    spots_labels = {0: "Non-Significant", 1: "HH", 2: "LH", 3: "LL", 4: "HL"}
    dataset["labels"] = pd.Series(spots,index=dataset.index).map(spots_labels)

    if not nsig:
        dataset = dataset[dataset["sig"] == 1]
    
    dataset_hh = dataset[dataset["labels"] == "HH"]
    dataset_hl = dataset[dataset["labels"] == "HL"]
    dataset_lh = dataset[dataset["labels"] == "LH"]
    dataset_ll = dataset[dataset["labels"] == "LL"]

    total_h = dataset_hh["doc_total"].sum() + dataset_hl["doc_total"].sum()
    total_l = dataset_lh["doc_total"].sum() + dataset_ll["doc_total"].sum()

    rated_h = dataset_hh["rated"].sum() + dataset_hl["rated"].sum()
    rated_l = dataset_lh["rated"].sum() + dataset_ll["rated"].sum()

    accepts_h = dataset_hh["accepts"].sum() + dataset_hl["accepts"].sum()
    accepts_l = dataset_lh["accepts"].sum() + dataset_ll["accepts"].sum()

    both_h = dataset_hh["both"].sum() + dataset_hl["both"].sum()
    both_l = dataset_lh["both"].sum() + dataset_ll["both"].sum()

    print(f"proportion of all {attr1} in ZCTAs surrounded by high {attr2} is {total_h/(total_h + total_l)}")
    print(f"proportion of rated {attr1} in ZCTAs surrounded by high {attr2} is {rated_h/(rated_h + rated_l)}")
    print(f"proportion of accepts {attr1} in ZCTAs surrounded by high {attr2} is {accepts_h/(accepts_h + accepts_l)}")
    print(f"proportion of both {attr1} in ZCTAs surrounded by high {attr2} is {both_h/(both_h + both_l)}")
    
    plt.show()


instructions()
while True:
    str = input("> ")
    str = str.split()

    attr = None
    filter = None

    log = False
    heat = False
    sa = False
    sabv = False
    nsig = False
    failed = False

    match len(str):
        case 0:
            key = 'invalid'
        case 1:
            key = str[0].upper()
        case 2:
            key = str[0].upper()
            attr = str[1].lower()
        case _:
            key = str[0].upper()
            attr = str[1].lower()
            
            for i in range (2, len(str)):
                if str[i].lower() == '-log':
                    log = True
                elif str[i].lower() == '-heat':
                    heat = True
                elif str[i].lower() == '-sa':
                    sa = True
                elif str[i].lower() == '-sabv':
                    sabv = True
                elif str[i].lower() == '-nsig':
                    nsig = True

                elif str[i].lower().find('-filter=') != -1:
                    filter = str[i].lower()[str[i].find('=')+1:]
                    if filter not in FILTERS:
                        key = 'invalid'
                elif str[i].lower().find('-cmap=') != -1:
                    CMAP = str[i].lower()[str[i].find('=')+1:]
                    print(f'--color map set to {CMAP}')
                elif str[i].lower().find('-color=') != -1:
                    COLOR = str[i].lower()[str[i].find('=')+1:]
                    print(f'--color set to {COLOR}')
                elif str[i].lower().find('-k=') != -1:
                    K = int(str[i].lower()[str[i].find('=')+1:])
                    print(f'--k set to {K}')

    match key:
        case _ if key in geodata_state.state.tolist() or key in ['US', 'NYC', 'LA', 'CHI', 'HOU']:
            if attr == 'dist':
                doc_map(key, filter, heat)
            elif attr in ATTRIBUTES:
                if sa:
                    spatial_autocorr(key, attr, filter, nsig)
                else:
                    attr_map(key, attr, filter, log)
            elif sabv:
                attrs = attr.split('_')
                if len(attrs) == 2 and attrs[0] in ATTRIBUTES and attrs[1] in ATTRIBUTES:
                    if sabv:
                        spatial_autocorr_bv(key, attrs[0], attrs[1], filter, nsig)
                else:
                    failed = True
            else:
                failed = True
        case 'EXIT':
            break
        case 'HELP':
            instructions(attr)
        case _:
            failed = True

    if failed:
        print('--invalid input, try again')
