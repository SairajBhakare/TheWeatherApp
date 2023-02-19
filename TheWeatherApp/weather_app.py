from tkinter import *
from configparser import ConfigParser
from tkinter import messagebox
import requests
from PIL import Image, ImageTk

# Accessing the api through url
url_api = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
api_file = 'weather.key'
file_a = ConfigParser()
file_a.read(api_file)
api_key = file_a['api_key']['key']


# Accessing the data from the json file
def weather_find(city):
    final = requests.get(url_api.format(city, api_key))
    if final:
        json_file = final.json()
        city = json_file['name']
        country_name = json_file['sys']['country']
        k_temperature = json_file['main']['temp']
        c_temperature = k_temperature - 273.15
        f_temperature = (k_temperature-273.15)*9/5+32
        weather_display = json_file['weather'][0]['main']
        result = (city,country_name,c_temperature,f_temperature,weather_display)

        return result

    else:
        return None


# Displaying the acquired data
def print_weather():
    city = search_city.get()
    weather = weather_find(city)
    if weather:
        location_entry['text'] = '{}, {}'.format(weather[0],weather[1])
        temperature_entry['text'] = '{:.2f} C, {:.2f} F'.format(weather[2],weather[3])
        weather_entry['text'] = weather[4]

    else:
        messagebox.showerror('Error', 'Please enter a valid city name!')


# Creating the GUI
root = Tk()
root.title("TheWeatherApp")

# Setting image as background
bg = Image.open('./bg.png')
re_bg = bg.resize((700,400))
img = ImageTk.PhotoImage(re_bg)
label1 = Label(image=img)
label1.bg = img
label1.place(x=0,y=0)

root.geometry("700x400")
icon = PhotoImage(file='./icon.png')
root.iconphoto(False,icon)


# Used to convert input to uppercase
def caps(event):
    search_city.set(search_city.get().upper())


# Adding the elements to GUI
search_city = StringVar()
enter_city = Entry(root,justify=CENTER, textvariable=search_city, fg="red",font=("Times New Roman", 30,"bold"))
enter_city.pack()
enter_city.bind("<KeyRelease>",caps)
search_button = Button(root, text='SEARCH WEATHER',width=20,bg='skyblue',fg='white',font=('Times New Roman',25,'bold')
            ,command=print_weather,foreground='black',background='gold',activeforeground='white',activebackground='red')
search_button.pack()

location_entry = Label(root, text='',font=('Times New Roman',35,'bold'),bg='lightblue')
location_entry.pack()

temperature_entry = Label(root, text='',font=("Times New Roman",35,'bold'),bg='lightpink')
temperature_entry.pack()

weather_entry = Label(root, text='', font=('Times New Roman',35,'bold'),bg='lightgreen')
weather_entry.pack()


root.mainloop()
