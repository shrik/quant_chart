from flask import Flask, Response
from flask import render_template
app = Flask(__name__)

@app.route("/hello")
def hello():
    f = open("tmp.json","r")
    str = f.read()
    f.close()
    resp = Response(response=str,
                    status=200,
                    mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/quant_chart/<name>")
def graph(name):
    if name.endswith("pkl"):
        f = open("./%s" % name,"rb")
        result = read_pkl(f)
        f.close()
        return render_template('quant.html', data=result, summary=result["summary"])
    else:
        return "wrong name"





import pickle
import json
import re
from datetime import datetime, date


def read_pkl(pkl_file):
    data = pickle.load(pkl_file)
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
    return json_data
