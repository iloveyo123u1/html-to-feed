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

    channel = dict([kv for kv in rules['channel'].items()])

    def get_text(elem):
        try:
            return elem.text_content()
        except AttributeError:
            return elem
    
    parsed_items = []
    for item in items:
        parsed_item = {}
        for field_name in rules['item']['sub']:
            vals = parsing.fetch_item_field(rules['url'], item,
                    rules['item']['sub'][field_name])

            if len(vals) > 0:
                field_value = ' '.join([get_text(x) for x in vals])
            else:
                field_value = ''
            
            parsed_item[field_name] = field_value

        parsed_items.append(parsed_item)

    resp = make_response(render_template('feed.xml',
        channel=channel,
        items=parsed_items))
    resp.headers['Content-Type'] = 'text/xml; charset=utf-8'

    return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
