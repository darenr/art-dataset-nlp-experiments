# -*- encoding: utf-8 -*-
import base64
import json
import os
import sys
import codecs

if len(sys.argv) != 4:
  print "usage: <kadist corpus json> <webpage filename> <json dict of tags>"
  sys.exit(-1)

def load_json():
  with codecs.open(sys.argv[1], 'rb', 'utf-8') as f:
    data = json.loads(f.read())
    return data

def save_web(html):
  with codecs.open(sys.argv[2], 'wb', 'utf-8') as f:
    f.write(html)

with codecs.open(sys.argv[3], 'rb', 'utf-8') as f:
  tag_db = json.loads(f.read())


html = u'''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap 101 Template</title>

    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">

    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

  <style>
    body {{
      margin: 20px;
    }}
  </style>

  </head>
  <body>
    <h1>{0}</h1>

    {1}

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
  </body>
</html>
'''

j = load_json()

elements = []

for row in j:
  
  if row['major_tags'] and row['worktype'] and row['description'] and row['imgurl']:
    major_tags = ' '.join(['<span class="label label-primary">{0}</span>'.format(tag_db[str(tag_id)]['name']) for tag_id in row['major_tags']])
    alchemy_tags = 'not yet'
    #alchemy_tags = ' '.join(['<span class="label label-primary">{0}</span>'.format(tag) for tag in row['alchemy_tags']])
    elements.append(u'''<div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title">{0} - {1} [Ref: {2}]</h3>
      </div>
      <div class="panel-body">
        <img src="{3}" class="thumbnail">
        <div class="caption"><h2><small>{4}</small></h2></div>
        {5}
        <h3>Kadist Tags: {6}</h3>
        <h3>Alchemy Tags: {7}</h3>
      </div>
    </div>'''.format(row['title'], 
                     row['year'], 
                     row['id'], 
                     row['imgurl'],
                     row['worktype'],
                     row['description'],
                     major_tags,
                     alchemy_tags))

save_web(html.format('Kadist - AlchemyAPI Concept Tagged', '\n'.join(elements)))
