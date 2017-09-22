import pickle
import json
import re
from datetime import datetime, date
with open("result.pkl","rb") as f:
  data = pickle.load(f)
summary = json.dumps(data.get('summary'))

json_data = {}
json_data['summary'] = data.get('summary')
for item in ['trades', 'portfolio', 'benchmark_portfolio', 'stock_account', 'stock_positions']:
  item_data = data.get(item)
  rows = []
  header = ['key']
  for col in item_data.keys().values.tolist():
    header.append(col)
  rows.append(header)
  for tr in item_data.iterrows():
    row = []
    if(hasattr(tr[0], 'strftime')):
      t = tr[0] 
      if isinstance(t, date):
        t = datetime.combine(t, datetime.min.time())
      micro_seconds = int((t - datetime(1970,1,1)).total_seconds() * 1000)
      row.append(micro_seconds)
    else:
      if isinstance(tr[0], str) and re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", tr[0]):
        t = datetime.strptime(tr[0], "%Y-%m-%d %H:%M:%S")
        micro_seconds = int((t - datetime(1970,1,1)).total_seconds() * 1000)
        row.append(micro_seconds)
      else:
        row.append(tr[0])
    for v in tr[1].values.tolist():
      row.append(v)
    rows.append(row)
  json_data[item] = rows
print(json.dumps(json_data))
