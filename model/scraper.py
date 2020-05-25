import os
import json
import math
from datetime import date
# from datetime import timedelta

import twint
from geopy.distance import distance

with open(os.path.join(os.getcwd(), 'server/app/static/data/colombia_departments_capitals_locations.json')) as f:
  cities = json.load(f)

def midpoint(x1, y1, x2, y2):
  lat1 = math.radians(x1)
  lon1 = math.radians(x2)
  lat2 = math.radians(y1)
  lon2 = math.radians(y2)

  bx = math.cos(lat2) * math.cos(lon2 - lon1)
  by = math.cos(lat2) * math.sin(lon2 - lon1)
  lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), \
          math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) \
          + bx) + by**2))
  lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)

  return [round(math.degrees(lat3), 2), round(math.degrees(lon3), 2)]

if __name__ == '__main__':
  data_folder = os.path.join(os.getcwd(), 'data', date.today().strftime('%Y_%m_%d'))
  if not os.path.exists(data_folder):
    os.makedirs(data_folder)
  output_path = os.path.join(data_folder, "tweets.csv")

  # num_days = 30
  for idx, city in enumerate(cities):
    c = twint.Config()
    # c.Since = (date.today() - timedelta(days=num_days)).strftime('%Y-%m-%d %H:%M:%S')
    c.Popular_tweets = True
    c.Limit = 3000
    c.Filter_retweets = True
    c.Store_object = True
    c.Location = True
    c.Hide_output = True
    c.Show_hashtags = False
    c.Lang = 'es'
    northeastBound = (city['geometry']['bounds']['northeast']['lat'],city['geometry']['bounds']['northeast']['lng'])
    southwestBound = (city['geometry']['bounds']['southwest']['lat'],city['geometry']['bounds']['southwest']['lng'])
    latCenter, lngCenter = midpoint(northeastBound[0],southwestBound[0],northeastBound[1],southwestBound[1])
    radius = ((math.sin(45)*(distance(northeastBound,southwestBound).km / 2)))/math.sin(45)
    geo = "{},{},{}km".format(
      latCenter,
      lngCenter,
      radius
    )
    c.Geo = geo
    c.Store_csv = True
    c.Output = output_path

    twint.run.Search(c)
    print("{} - {}/32 - DONE!".format(city['formatted_address'], idx + 1), flush=True)

  print("{} saved successfully".format(output_path))
