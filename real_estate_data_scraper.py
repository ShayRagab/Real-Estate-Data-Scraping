import requests
from bs4 import BeautifulSoup
import pandas

r = requests.get("https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
    
con = r.content

soup = BeautifulSoup(con, "html.parser")

rows = soup.find_all("div", class_="propertyRow")

page_nr = soup.find_all("a", class_="Page")[-1].text


def there_is(item, tag):
    if item != None:
        return item.find(tag).text
    else:
        return None


data=[]

base_url = "https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
# looping through the pages
for page in range(0, int(page_nr)*10, 10):
    req = requests.get(base_url+str(page)+".html")
    page_con = req.content
    soup = BeautifulSoup(page_con, "html.parser")
    rows = soup.find_all("div", class_="propertyRow")
    
    #looping through the rows/properties
    for item in rows:
        d = {}
        d["Price"] = item.find("h4", class_="propPrice").text.strip() #can use: replace("\n","") instead of strip())
        d["Address"] = item.find_all("span", class_="propAddressCollapse")[0].text
        d["Locality"] = item.find_all("span", class_="propAddressCollapse")[1].text

        beds = item.find("span", class_="infoBed") 
        sqft = item.find("span", class_="infoSqFt")
        full_bath = item.find("span", class_="infoValueFullBath")
        half_bath = item.find("span", class_="infoValueHalfBath")
        column_group = item.find_all("div", class_="columnGroup")


        d["Beds"] = there_is(beds, "b")
        d["Area"] = there_is(sqft, "b")
        d["Full Bath"] = there_is(full_bath, "b")
        d["Half Bath"] = there_is(half_bath, "b")

        for i in column_group:
            features = i.find_all("span", class_="featureGroup")
            for feature in features:
                if "Lot Size" in feature.text:
                    d["Lot Size"] = i.find("span", class_="featureName").text

        data.append(d)


df = pandas.DataFrame(data)
df.to_csv("real_estate_data.csv")




