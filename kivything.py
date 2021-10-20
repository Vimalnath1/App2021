import cv2
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
from kivy.uix.actionbar import ActionBar,ActionButton,ActionItem
from kivy.lang import Builder
import time
from threading import *
iffalse=True
def recipeappfunction():
    global recipe_labels, iftrue
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
    cam=cv2.VideoCapture(0)

    conn = http.client.HTTPSConnection("edamam-food-and-grocery-database.p.rapidapi.com")
    headers = {
        'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com",
        'x-rapidapi-key': "da66f99cf6msh0256ef4567f1ffbp1ea5dejsn972563a3211b"
        }

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
                res = conn.getresponse()
                data = res.read()
                food_info=data.decode()
                i=False
        if i==False:
                break
        if cv2.waitKey(10)==ord("q"):
            break
        cv2.imshow("Camera", frame)'''
    conn.request("GET", f"/parser?upc=0737628005000", headers=headers)
    res = conn.getresponse()
    data = res.read()
    food_info=data.decode()
    where_label=food_info.find("label")
    where_nutrients=food_info.find("nutrients")
    where_calorie=food_info.find("ENERC_KCAL")
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
        food_brand=food_brand.replace('''"''',"")
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
    food["Protein"]=food_protein
    food["Fiber"]=food_fiber
    food["Carbohydrates"]=food_carbs
    food["Sugar"]=food_sugar
    food["Sodium"]=food_sodium



    pprint.pprint(food)
    querystring = {"q":f"{food_label}"}

    response = requests.request("GET", url, headers=recipeheaders, params=querystring)
    recipes=response.text
    #pprint.pprint(recipes)
    #find_where_all_substrings_are(recipes,'''"uri":''')
    #print(type(recipes))
    recipe_labels=jsonStripper(recipes,"label")
    recipe_calories=jsonStripper(recipes,"calories")
    recipe_health=jsonStripper(recipes,"healthLabels")
    recipe_cuisine=jsonStripper(recipes,"cuisineType")
    recipe_allergens=jsonStripper(recipes,"cautions")
    recipe_ingredients=jsonStripper(recipes,"ingredientLines")
    iftrue=True
class HomeButton(Button,ActionItem):
    pass
class MenuBar(ActionBar):
    pass
class MainWindow(Screen):
    pass
class FoodTrackingWindow(Screen):
    pass
class RecipeWindow(Screen):
    def on_button_click(self):
        recipeappfunction()
if iffalse==False:
    class RecipeList(Screen):
        def __init__(self, **kwargs):
            super(RecipeList,self).__init__(**kwargs)
            layout=BoxLayout(orientation="vertical")        
            self.add_widget(layout)
            try:
                for i in range(len(recipe_labels)):
                    b=Button(text=recipe_labels[i],size_hint=(1,1))
                    self.add_widget(b) 
            except NameError:
                pass
class WindowManager(ScreenManager):
    pass
class WidgetforApp(GridLayout):
    def on_food_tracker_button_click(self):
        #clear page
        print("Clear Page and ask about nutrition goals and ask to scan and add to food tracker")
    def on_recipes_button_click(self):
        #clear page
        print("Clear Page and ask to scan food and then show recipes")
class WidgetsExample(GridLayout):
    number=0
    def on_button_click(self):
        self.number+=1
        print(self.number)
    def security_camera(self):
            cam=cv2.VideoCapture(0)
            while cam.isOpened():
                ret, frame1=cam.read()
                ret, frame2=cam.read()
                diff=cv2.absdiff(frame1,frame2)
                gray=cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
                blur=cv2.GaussianBlur(gray,(5,5),0)
                _,thresh=cv2.threshold(blur, 20,255, cv2.THRESH_BINARY)
                dilate=cv2.dilate(thresh, None, iterations=3)
                contours,_=cv2.findContours(dilate,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
                for c in contours:
                    if cv2.contourArea(c)<5000:
                        continue
                    x,y,w,h=cv2.boundingRect(c)
                    cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
                    winsound.PlaySound("alarm.wav", winsound.SND_ASYNC)
                if cv2.waitKey(10)==ord("q"):
                    break
                cv2.imshow("Camera", frame1)


kv=Builder.load_file("My.kv")
class MyApp(App):
    def build(self):
        return kv

MyApp().run()

