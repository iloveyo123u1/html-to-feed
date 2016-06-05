from flask import Flask, Markup
from flask import render_template, request, send_from_directory

import lxml.html
import json

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
        title = item.cssselect(rules['item']['sub']['title']['selector'])
        if len(title) > 0:
            title = title[0].text_content()
        else:
            title = 'missing'

        parsed_item = {'title': title}
        parsed_items.append(parsed_item)

    return render_template('feed.xml',
            feed = parsed_items)

if __name__ == '__main__':
    app.debug = True
    app.run()
