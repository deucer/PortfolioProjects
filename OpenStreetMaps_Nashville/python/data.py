import csv
import codecs
import re
import xml.etree.cElementTree as ET
import cerberus
import schema

#We're using the sample data for faster load and validation times
OSM_PATH = "nashville_sample.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    if element.tag == 'node':
        for key in element.attrib.keys():
            if key in node_attr_fields:
                node_attribs[key] = element.attrib[key]
        for child in element:
            if child.tag == 'tag':
                if problem_chars.search(child.attrib['k']):
                    pass
                else:
                    tags_list = {}
                    tags_list['id'] = element.attrib['id']
                    if child.attrib['k'] == 'name:en':
                        tags_list['value'] = update_name(child.attrib['v'], mapping)
                    else:
                        tags_list['value'] = child.attrib['v']
                    if LOWER_COLON.search(child.attrib['k']):
                        colon_position = child.attrib['k'].find(':')
                        tags_list['key'] = child.attrib['k'][colon_position+1:]
                        tags_list['type'] = child.attrib['k'][:colon_position]
                    else:
                        tags_list['key'] = child.attrib['k']
                        tags_list['type'] = 'regular'
                    tags.append(tags_list)    
        
    if element.tag == 'way':
        for key in element.attrib.keys():
            if key in way_attr_fields:
                way_attribs[key] = element.attrib[key]
        position = 0
        for child in element:
            
            if child.tag == 'nd':
                way_nodes_list = {}
                way_nodes_list['id'] = element.attrib['id']
                way_nodes_list['node_id'] = child.attrib['ref']
                way_nodes_list['position'] = position
                position += 1
                way_nodes.append(way_nodes_list)
            if child.tag == 'tag':
                if problem_chars.search(child.attrib['k']):
                    pass
                else:
                    tags_list = {}
                    tags_list['id'] = element.attrib['id']
                    if child.attrib['k'] == 'name:en':
                        tags_list['value'] = update_name(child.attrib['v'], mapping)
                    else:
                        tags_list['value'] = child.attrib['v']
                    if LOWER_COLON.search(child.attrib['k']):
                        colon_position = child.attrib['k'].find(':')
                        tags_list['key'] = child.attrib['k'][colon_position+1:]
                        tags_list['type'] = child.attrib['k'][:colon_position]
                    else:
                        tags_list['key'] = child.attrib['k']
                        tags_list['type'] = 'regular'
                    tags.append(tags_list)  
            
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.items())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, bytes) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""
    

    with codecs.open(NODES_PATH, 'w', encoding="utf-8") as nodes_file, \
        codecs.open(NODE_TAGS_PATH, 'w', encoding="utf-8") as nodes_tags_file, \
        codecs.open(WAYS_PATH, 'w', encoding="utf-8") as ways_file, \
        codecs.open(WAY_NODES_PATH, 'w', encoding="utf-8") as way_nodes_file, \
        codecs.open(WAY_TAGS_PATH, 'w', encoding="utf-8") as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])



# Note: Validation is ~ 10X slower. For the project consider using a small
# sample of the map when validating.
    
process_map(OSM_PATH, validate=True)
print('Successfully Processed {} Map'.format(OSM_PATH[:-4]))