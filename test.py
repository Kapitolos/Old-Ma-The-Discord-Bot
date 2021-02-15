import json

with open("Journal.log", mode='r+') as file:
    lines = (file.readlines())
    dline = json.loads(lines[0])

    for i in range(len(lines)):
        dline2 = json.loads(lines[i])
        if dline2['event'] == "Location":
            location = json.dumps(dline2)
            grabstat = json.loads(location)
            global StarSystem
            StarSystem = grabstat["StarSystem"]

        elif dline2['event'] == "Commander":
            commander = json.dumps(dline2)
            grabstat = json.loads(commander)
            global Commander_name
            Commander_name = grabstat["Name"]

        elif dline2['event'] == "Friends":
            Friends = json.dumps(dline2)
            grabstat = json.loads(Friends)
            global Friend_name
            global Friend_online
            Friend_name = grabstat["Name"]
            Friend_online = grabstat["Status"]


        else:
            pass
