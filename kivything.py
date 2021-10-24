import cv2
from kivy.uix.behaviors import button
from kivy.uix.label import Label
from pyzbar.pyzbar import decode
import numpy as np
import winsound
import http.client
import pprint
import re
import requests
import json
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.actionbar import ActionBar,ActionButton,ActionItem, ActionView
from kivy.properties import StringProperty
from kivy.lang import Builder



def recipeappfunction(): #main logic go to line 41 where it actually starts
    global recipe_labels
    def jsonStripper(thingToStrip,whatToStripInStrip):
        data =json.loads(thingToStrip)
        dataToPrint = []
        for recipe1 in data["hits"]:
            dataToPrint.append(recipe1["recipe"][whatToStripInStrip])
        with open('data.txt', 'w') as outfile:
            json.dump(data["hits"][0], outfile)
        return dataToPrint
    url = "https://edamam-recipe-search.p.rapidapi.com/search"
    i=True
    food={}
    #cam=cv2.VideoCapture("http://192.168.1.4:8080/video")
    cam=cv2.VideoCapture(0)                                     #makes the camera pop up for the scanning of barcode
    conn = http.client.HTTPSConnection("edamam-food-and-grocery-database.p.rapidapi.com")
    headers = {
        'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com",
        'x-rapidapi-key': "da66f99cf6msh0256ef4567f1ffbp1ea5dejsn972563a3211b"
        }
                                                                                    #APIs used 
    recipeheaders = {
        'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com",
        'x-rapidapi-key': "da66f99cf6msh0256ef4567f1ffbp1ea5dejsn972563a3211b"
        }

    '''
    while cam.isOpened():
        ret,frame=cam.read()
        for barcode in decode(frame):
            if i==True:
                labeldata=barcode.data.decode("utf-8")
                conn.request("GET", f"/parser?upc={labeldata}", headers=headers)
                res = conn.getresponse()                                            #Scanning Barcode Logic Commented out because testing and too lazy to scan every time
                data = res.read()
                food_info=data.decode()
                i=False
        if i==False:
                break
        if cv2.waitKey(10)==ord("q"):
            break
        cv2.imshow("Camera", frame)'''
    conn.request("GET", f"/parser?upc=0737628005000", headers=headers)              #sample barcode for testing
    res = conn.getresponse()
    data = res.read()
    food_info=data.decode()
    where_label=food_info.find("label")
    where_nutrients=food_info.find("nutrients")
    where_calorie=food_info.find("ENERC_KCAL")          #When barcode scans prints out huge string, the where variables find each nutrient and the food variables break it apart
    where_fat=food_info.find("FAT")
    where_saturatedfat=food_info.find("FASAT")
    where_protein=food_info.find("PROCNT")
    where_sugar=food_info.find("SUGAR")
    where_fiber=food_info.find("FIBTG")
    where_carbs=food_info.find("CHOCDF")
    where_sugar=food_info.find("SUGAR")
    where_sodium=food_info.find("NA")
    where_calcium=food_info.find('''"CA" :''')
    where_cholestorol=food_info.find("CHOLE")
    where_brand=food_info.find("brand")
    where_category=food_info.find("category")
    food_label=food_info[where_label:where_nutrients]
    food_calories=food_info[where_calorie:where_fat]
    food_fat=food_info[where_fat:where_saturatedfat]
    food_carbs=food_info[where_carbs:where_fiber]
    food_fiber=food_info[where_fiber:where_sugar]
    food_sugar=food_info[where_sugar:where_protein]
    food_protein=food_info[where_protein:where_cholestorol]
    food_sodium=food_info[where_sodium:where_calcium]
    food_brand=food_info[where_brand:where_category]
    if "brand" in food_brand:
        food_brand=food_brand.replace('''brand" :''',"")
    if '''"''' in food_brand:
        food_brand=food_brand.replace('''"''',"")                   #To clean out the food label because it will go into api and it cant have spaces or quotations
        food_brand=food_brand.lstrip()
        food_brand=food_brand.rstrip()
    if food_brand in food_label:
        food_label=food_label.replace(food_brand,"")
    if "label" in food_label:
        food_label=food_label.replace("label","")
    food_label=food_label.lstrip()
    food_label=food_label.rstrip() 
    food_label= re.sub('[\W_]+',' ', food_label)
    food["Name"]=food_label
    food["Calories"]=food_calories
    food["Fat"]=food_fat
    food["Protein"]=food_protein                                     #Adding the each nutrient part to dictionary on line 38
    food["Fiber"]=food_fiber
    food["Carbohydrates"]=food_carbs
    food["Sugar"]=food_sugar
    food["Sodium"]=food_sodium



    pprint.pprint(food)
    querystring = {"q":f"{food_label}"}                         #calling second api to look up the food label in it to find recipes

    response = requests.request("GET", url, headers=recipeheaders, params=querystring)
    recipes=response.text
    #pprint.pprint(recipes)
    #find_where_all_substrings_are(recipes,'''"uri":''')
    #print(type(recipes))
    recipe_labels=jsonStripper(recipes,"label")
    recipe_calories=jsonStripper(recipes,"calories")
    recipe_health=jsonStripper(recipes,"healthLabels")              #This API also returns a long string so jsonStripper(lines 28-35) breaks it 
    recipe_cuisine=jsonStripper(recipes,"cuisineType")
    recipe_allergens=jsonStripper(recipes,"cautions")
    recipe_ingredients=jsonStripper(recipes,"ingredientLines")
    print(recipe_labels)
class HomeButton(Button,ActionItem):            
    pass                                    #Each class is are the screens of the app
class MenuBar(ActionBar):
    pass
class MainWindow(Screen):
    pass
class FoodTrackingWindow(Screen):
    pass
class RecipeWindow(Screen):
    def on_button_click(self):
        recipeappfunction()

class RecipeList(Screen):
    buttonlist=[]

    def on_show_recipe_button_click(self, **kwargs):
        super().__init__(**kwargs)
        layout=BoxLayout(orientation="vertical")     #Makes layout to put buttons for recipes         
        self.add_widget(layout)
        actionbar=ActionBar(size_hint=(None,None),size=(layout.width,dp(100)),pos_hint={'top':1})       
        layout.add_widget(actionbar)                                                                      
        for i in range(0,10):
            b=Button(text=str(recipe_labels[i]),size_hint=(1,.1))       #Adds the 10 buttons 


    
            
        
        
class WindowManager(ScreenManager):
    pass
                                     


kv=Builder.load_file("My.kv")
class MyApp(App):
    def build(self):
        return kv
MyApp().run()

