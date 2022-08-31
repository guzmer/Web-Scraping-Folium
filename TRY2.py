import folium
import pandas as pd 
from folium.plugins import MarkerCluster
from folium.plugins import Search

import json



mapObj = folium.Map(location=[33.886917, 9.537499],
                    zoom_start=6)


informations= pd.read_csv('Data.csv')
informations.columns = informations.columns.str.replace(' ', '')

marker_cluster = MarkerCluster(control=False).add_to(mapObj)


informations.reset_index(drop=True, inplace=True)
informations['geocode'] = [[informations['Latitude'][i],informations['Longitude'][i]] for i in range(len(informations)) ]





for point in informations.index: # loop through the plots
    html = """
        <h4>{Nom}</h4>
        <h5>Governorat: {Governorat}</h5>
        <h5>Type: {Type}</h5>
        <h5>Adresse: {Adresse}</h5>
        <h5>Email: {Email}</h5>
        <h5>Fax: {Fax}</h5>
        <h5>Tel1: {Tel1}</h5>
        <h5>Tel2: {Tel2}</h5>
        """
    popup_contents = folium.Html(html.format(Nom = informations.loc[point, 'Nom'], Governorat= informations.loc[point, 'Governorat'],Type = informations.loc[point, 'Type'],Adresse = informations.loc[point, 'Adresse'],  Email = informations.loc[point, 'Email'], Fax = informations.loc[point, 'Fax'],Tel1 = informations.loc[point, 'Tel1'], Tel2 = informations.loc[point, 'Tel2']), script = True)

    popup = folium.Popup(popup_contents, max_width=1500)
    
# mark every addresses in the map from the data
    folium.Marker(informations['geocode'][point], popup=popup).add_to(marker_cluster)
    ListLoc= [informations.loc[point,'Latitude'], informations.loc[point, 'Longitude']]

folium.LayerControl(tiles = None).add_to(mapObj)


mapObj.save('Try2.html')
