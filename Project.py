
from sqlite3 import Timestamp
import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
import pandas as pd 
from folium.plugins import MarkerCluster
from folium.features import CustomIcon
from folium import FeatureGroup

try:

    P_link = requests.get("https://www.biat.com.tn/nos-agences", timeout= 10)
    print(P_link)


    soup = BeautifulSoup(P_link.text, "html.parser")

    containers = soup.find('div', class_="geolocation-common-map-locations").find_all('div', class_="location-content")

    container = containers[0]
    column = ['Nom','Governorat','Type','Adresse','Email','Fax','Tel1', 'Tel2']
    Agences = pd.DataFrame(columns = column)

    for container in containers:

        #Nom
        nom = container.find('div', class_="field field--name-node-title field--type-ds field--label-hidden field__item").h2.text.strip()

        #Governorat

        governorat= container.find('div', class_="field field--name-field-gouvernorat field--type-entity-reference field--label-inline").find('div', class_="field__item").text.strip()

        #Type
        tA = container.find('div', class_="field field--name-field-type-agence field--type-entity-reference field--label-inline")
        if tA == None:
            typeA = 'None'
        else :
            typeA= tA.find('div', class_='field__item').text.strip()
        
        #Adresse
        adresse = container.find('div', class_="field field--name-field-adresse field--type-string field--label-inline").find('div', class_="field__item").text.strip().replace(',','')

        #Email
        eA = container.find('div', class_="field field--name-field-email field--type-email field--label-inline")
        if eA == None:
            email = 'None'
        else :
            email= eA.find('div', class_='field__item').text.strip()
        
        #Fax
        fA = container.find('div', class_="field field--name-field-fax field--type-string field--label-inline")
        if fA == None:
            fax = 'None'
        else :
            fax= fA.find('div', class_='field__item').text.strip()
        
        #Tel
        ListTel = container.find('div', class_="field field--name-field-tel- field--type-string field--label-inline").find('div', class_="field__item").text.strip().split('-')
        if len(ListTel) == 2:
            Tel1 = ListTel[0]
            Tel2 = ListTel[1]
        if len(ListTel)== 1:
            Tel1 = ListTel[0]
            Tel2 = 'None'


        Data = pd.DataFrame([[nom ,governorat , typeA, adresse , email, fax,Tel1, Tel2]])
        Data.columns = column
        Agences = Agences.append(Data, ignore_index = True)



    #Les coordoonnées

    coordinates = soup.find('div', class_="geolocation-common-map-locations").find_all('meta')



    coordinate = coordinates[0]
    Listlat=[]
    Listlongi=[]

    for coordinate in coordinates:
        if coordinate['property']== 'latitude':
            latcoord= coordinate['content']
            lat= float(latcoord)
            Listlat.append(lat)
        if coordinate['property']== 'longitude':
            longicoord= coordinate['content']
            longi= float(longicoord)
            Listlongi.append(longi)

    result= zip(Listlat,Listlongi)
    Lcoord= list(result)
    coord= pd.DataFrame(Lcoord, columns=['Latitude', 'Longitude'])

    coord.to_csv("locationsTry1.csv", index = None)

    result = pd.concat([Agences, coord], axis=1)

    result.to_csv("Data.csv", index = None )

    #creation map
    mapObj = folium.Map(location=[33.886917, 9.537499],
                        zoom_start=6)


    #lecture du fichier 
    informations= pd.read_csv('Data.csv')
    informations.columns = informations.columns.str.replace(' ', '')


    #initiliser marker cluster
    marker_cluster = MarkerCluster(control=False).add_to(mapObj)


    informations.reset_index(drop=True, inplace=True)
    informations['geocode'] = [[informations['Latitude'][i],informations['Longitude'][i]] for i in range(len(informations)) ]


    #feature group : ajouter une liste à choix multiple

    Tunis = folium.FeatureGroup(name="Tunis", show= False)
    Ariana = folium.FeatureGroup(name="Ariana", show = False)
    BenArous= folium.FeatureGroup(name="Ben Arous", show= False)
    Manouba= folium.FeatureGroup(name="La Manouba", show= False)
    Nabeul = folium.FeatureGroup(name="Nabeul", show= False)
    Bizerte = folium.FeatureGroup(name="Bizerte",show= False)
    Jendouba= folium.FeatureGroup(name="Jendouba",show= False)
    Beja = folium.FeatureGroup(name="Béja",show= False)
    Kef= folium.FeatureGroup(name="Le Kef",show= False)
    Siliana = folium.FeatureGroup(name="Siliana",show= False)
    Kairouan= folium.FeatureGroup(name="Kairouan",show= False)
    Kasserine = folium.FeatureGroup(name="Kasserine",show= False)
    SidiBouzid= folium.FeatureGroup(name="Sidi Bouzid",show= False)
    Gafsa = folium.FeatureGroup(name="Gafsa",show= False)
    Tozeur =folium.FeatureGroup(name="Tozeur",show= False) 
    Kebili = folium.FeatureGroup(name="Kébili",show= False)
    Tataouine = folium.FeatureGroup(name="Tataouine",show= False)
    Medenine = folium.FeatureGroup(name="Medenine",show= False)
    Sfax = folium.FeatureGroup(name="Sfax",show= False)
    Sousse = folium.FeatureGroup(name="Sousse",show= False)
    Mahdia = folium.FeatureGroup(name="Mahdia",show= False)
    Monastir = folium.FeatureGroup(name="Monastir",show= False)
    Zaghouan = folium.FeatureGroup(name="Zaghouan",show= False)
    Gabes = folium.FeatureGroup(name="Gabès",show= False)



    #parcourir le fichier csv, localisation des agences et les autres informations
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
    # folium.Marker(informations['geocode'][point], popup=popup).add_to(marker_cluster)
        ListLoc= [informations.loc[point,'Latitude'], informations.loc[point, 'Longitude']]

    #ajouter des points aux "feature group"

        if informations.loc[point,'Governorat']== 'Tunis':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Tunis)
        
        if informations.loc[point,'Governorat']== 'Ariana':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Ariana)
        
        if informations.loc[point,'Governorat']== 'Sfax':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Sfax)
        
        if informations.loc[point,'Governorat']== 'Nabeul':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Nabeul)
        
        if informations.loc[point,'Governorat']== 'La Manouba':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Manouba)
        
        if informations.loc[point,'Governorat']== 'Mahdia':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Mahdia)
        
        if informations.loc[point,'Governorat']== 'Ben Arous':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(BenArous)
        
        if informations.loc[point,'Governorat']== 'Kasserine':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon,popup=popup).add_to(Kasserine)

        if informations.loc[point,'Governorat']== 'Gafsa':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon,popup=popup).add_to(Gafsa)

        if informations.loc[point,'Governorat']== 'Gabès':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Gabes)

        if informations.loc[point,'Governorat']== 'Kébili':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Kebili)

        if informations.loc[point,'Governorat']== 'Jendouba':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Jendouba)

        if informations.loc[point,'Governorat']== 'Bizerte':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Bizerte)

        if informations.loc[point,'Governorat']== 'Sousse':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Sousse)

        if informations.loc[point,'Governorat']== 'Zaghouan':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Zaghouan)
        
        if informations.loc[point,'Governorat']== 'Monastir':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Monastir)

        if informations.loc[point,'Governorat']== 'Sidi Bouzid':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(SidiBouzid)
        
        if informations.loc[point,'Governorat']== 'Tataouine':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Tataouine)
        
        if informations.loc[point,'Governorat']== 'Béja':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon,  popup=popup).add_to(Beja)

        if informations.loc[point,'Governorat']== 'Le Kef':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Kef)

        if informations.loc[point,'Governorat']== 'Siliana':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Siliana)

        if informations.loc[point,'Governorat']== 'Tozeur':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Tozeur)
        
        if informations.loc[point,'Governorat']== 'Kairouan':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Kairouan)
        
        if informations.loc[point,'Governorat']== 'Médenine':
            icon=folium.Icon(color='darkblue',icon_color='#0f056b', prefix='fa')
            folium.Marker(ListLoc, icon=icon, popup=popup).add_to(Medenine)


#ajouter les feature group au map

    mapObj.add_child(Tunis)
    mapObj.add_child(Ariana)
    mapObj.add_child(BenArous)
    mapObj.add_child(Manouba)
    mapObj.add_child(Beja)
    mapObj.add_child(Sfax)
    mapObj.add_child(Kairouan)
    mapObj.add_child(Mahdia)
    mapObj.add_child(Nabeul)
    mapObj.add_child(Medenine)
    mapObj.add_child(Kebili)
    mapObj.add_child(Sousse)
    mapObj.add_child(Kasserine)
    mapObj.add_child(Gafsa)
    mapObj.add_child(Gabes)
    mapObj.add_child(Bizerte)
    mapObj.add_child(Jendouba)
    mapObj.add_child(SidiBouzid)
    mapObj.add_child(Tozeur)
    mapObj.add_child(Siliana)
    mapObj.add_child(Tataouine)
    mapObj.add_child(Kef)
    mapObj.add_child(Monastir)
    mapObj.add_child(Zaghouan)



#ajouter les couches
    folium.LayerControl(collapsed= False).add_to(mapObj)


    mapObj.save('MAp-Data.html')

except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)



   


    
    
    
    
    
