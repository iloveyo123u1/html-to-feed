from flask import Flask, make_response
from flask import render_template

import lxml.html
import json

import parsing

app = Flask(__name__)

@app.route('/feed/<int:feed_id>')
def show_feed(feed_id):
    with open('rules/%d.json' % feed_id) as f:
        rules = json.load(f)
    doc = lxml.html.parse(rules['url'])
    root = doc.getroot()

    items = root.cssselect(rules['item']['selector'])
    
    parsed_items = []
    for item in items:
        parsed_item = {}
        for field_name in rules['item']['sub']:
            vals = parsing.fetch_item_field(rules['url'], item,
                    rules['item']['sub'][field_name])

            if len(vals) > 0:
                field_value = ' '.join([x.text_content() for x in vals])
            else:
                field_value = ''
            
            parsed_item[field_name] = field_value

        parsed_items.append(parsed_item)

    resp = make_response(render_template('feed.xml', feed=parsed_items))
    resp.headers['Content-Type'] = 'text/xml; charset=utf-8'

    return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
