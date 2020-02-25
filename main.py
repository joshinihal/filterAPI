from flask import Flask, request, jsonify
import os
import json
import geopy.distance

app = Flask(__name__)
app.config["DEBUG"] = True


filename = os.path.join(app.static_folder, 'assignment.json')
with open(filename) as file:
  data = json.load(file)

@app.route('/',methods=['GET'])
def home():
    return 'Home!'

# send a req to /search?lat={latitude}&long={longitude}&type={category}
@app.route('/search',methods=['GET'])
def search():
    resultData=[]
    # check if entered params are correct
    if(request.args.get('lat') and request.args.get('long') and request.args.get('type') != None):
      for each in data["0-4"]["HotelSearchResult"]["HotelResults"]:
        if(each["TripAdvisor"]!= None ):
          coords_1 = (request.args.get('long'), request.args.get('lat'))
          coords_2 = (each["Longitude"], each["Latitude"])
          # find the distance and check if less than 100kms
          dist= geopy.distance.distance(coords_1, coords_2).km
          # print(dist)
          if(dist<100):
            for every in each["TripAdvisor"]["trip_types"]:
              if(every["name"]== request.args.get('type')):
                resultData.append(each)
      return jsonify(resultData)
    else:
      return "enter correct parameters"

app.run(host='0.0.0.0', port=5000)