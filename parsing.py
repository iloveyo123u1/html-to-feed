import lxml.html
from urllib.parse import urljoin

def fetch_item_field(cur_url, itemelement, field_rules):
    elements = [itemelement]

    for rule in field_rules:
        elements = select_by_rules(elements, rule)

        if 'modifiers' in rule:
            for modifier in rule['modifiers']:
                if modifier == 'join-link':
                    elements = [urljoin(cur_url, el) for el in elements]
                elif modifier == 'follow-link':
                    elements = [load_url(el) for el in elements]
                elif modifier == 'strip-tags':
                    # remove script and style elements
                    for element in elements:
                        for to_delete in element.xpath("//script"):
                            to_delete.getparent().remove(to_delete)
                        for to_delete in element.xpath("//style"):
                            to_delete.getparent().remove(to_delete)

    return elements

def load_url(url):
    doc = lxml.html.parse(url)
    root = doc.getroot()

    return root

def select_by_rules(htmlelements, rule):
    if not 'selector-type' in rule:
        raise Exception("selector-type missing in rules")

    all_res = []

    for htmlelement in htmlelements:
        if rule['selector-type'] == 'css':
            res = htmlelement.cssselect(rule['selector'])
        elif rule['selector-type'] == 'xpath':
            res = htmlelement.xpath(rule['selector'])
        else:
            raise Exception("Unknown rule '%s'" % rule['selector-type'])

        all_res += res

    return all_res
