import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from test import StarSystem, Commander_name, Friend_name, Friend_online

client = discord.Client()

# bad_words = os.getenv('bad_words_list')

# angrymother = os.getenv('angrymother_list')

bad_words = ["shit","shitting","shat","fuck","Fuck","fucking","fucked","piss","pissed","cunt","asshole","dick","cock","pussy","God","god","damn","jeez","motherfucker","assclown","cheeseburger","bitch","whore","bastard","wiener","fart","tits","tit","ass","poop","pee","urine","Jesus","Christ","hell","godammit","heck","dammit","damn","slut","skank"]

angrymother = ["Hey now that's not called for.", "Wash out that mouth buster!", "That language is uncalled for.", "Swearing demotes the soul","Was that neccesary?","I'm going to forget you said that.",'Woah woah woah I didn\'t realize this conversation was rated R!!!',"I'll wash your mouth out with soap for that talk!","Back in my day you'd get the belt for that kind of talk!","You kids better clean up your act!","Bunch of filthy perverts."]


if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]['a']
  return(quote)

# def get_weather():
#   response = requests.get("http://api.openweathermap.org/data/2.5/weather?q={Toronto}&appid={4aff648fe3d03031f477707a40d7e666}")
#   wdata = json.loads(response.text)
#   print(wdata) 
#   return(wdata)
KEY = os.getenv('WEATHER2')


def get_weather(query):
  response = requests.get(f"\nhttp://api.weatherstack.com/current?access_key={KEY}&query={query}")
  wdata = json.loads(response.text)
  place = wdata['request']['query']
  temp = wdata['current']['temperature']
  cond = wdata['current']['weather_descriptions']
  cond2 = str(cond).strip('[]').lower()
  weather = f"\nIt is currently {temp} and {cond2} in {place} dear." 
  return(weather)
  

def star_system():
  return(StarSystem)

def Commander_namefunc():
  return(Commander_name)

def Friend_namefunc():
  friendnews = "Your friend " + Friend_name + " is " + Friend_online
  return(friendnews)

def get_food():
  response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
  json_data = json.loads(response.text)
  food = json_data['meals'][0]["strMeal"] + " -" + json_data['meals'][0]['strInstructions']
  return(food)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    msg = message.content

    if message.content.startswith('$weather'):
      query = message.content.split(' ')
      weather = get_weather(query)
      await message.channel.send(weather)
    
    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    if message.content.startswith('$location'):
      await message.channel.send(StarSystem)

    if message.content.startswith('$myname'):
      await message.channel.send(Commander_name)

    if message.content.startswith('$Friend'):
      friendnews = Friend_namefunc()
      await message.channel.send(friendnews)

    if message.content.startswith('$dinner'):
      food = get_food()
      await message.channel.send(food)
    
    if db["responding"]:
      options = angrymother
      if "encouragements" in db.keys():
        options = options + db["encouragements"]

      if any (word in msg for word in bad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New message added.")

    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragements(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith('$list'):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$responding"):
      value = msg.split("$responding ", 1)[1]

      if value.lower() == "true":
        db["responding"] == True
        await message.channel.send("Responding is on.")
      else:
        db["responding" == False]
        await message.channel.send("Resonding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))

