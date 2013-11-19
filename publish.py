#!/usr/bin/env python

import pystache

publishing_list = [
    'ddj-toolbox'
    ]
    
class Publish:

    def __init__(self):
        self.template_files = {
            'dir': 'templates',
            'ext': 'html'
        }
        self.data_files = {
            'dir': 'data',
            'ext': 'txt'
        }
    
    def construct_filename(self, filename, filetype):
        if filetype == 'data':
            return self.data_files['dir'] + '/' + filename + '.' + self.data_files['ext']
        elif filetype == 'template':
            return self.template_files['dir'] + '/' + filename +  '.' + self.template_files['ext']
        else:
            return filename +  '.' + self.template_files['ext']
            
    def parse_data(self, filename):
        data = []
        fd = open(filename, 'r')
        for line in fd.readlines():
            if not line:
                pass
            elif line.startswith('='):
                section_name = line[1:].title()
                section_data = {}
                section_data['name'] = section_name
                section_data['items'] = []
            elif line.startswith('*'):
                item_name, item_url = line[1:].split(',') 
                item_data = {
                    'name': item_name.title(),
                    'url': item_url
                }
                section_data['items'].append(item_data)
            elif line.startswith('_'):
                data.append(section_data)
            else:
                pass
        fd.close()
        return {'sections': data}
            
    def publish(self, publishing_list):
        for file in publishing_list:
            data_filename = self.construct_filename(file, 'data')
            template_filename = self.construct_filename(file, 'template')
            publish_filename = self.construct_filename(file, 'publish')
            template_data = self.parse_data(data_filename)
            #print template_data
            fd = open(template_filename, 'r')
            template_html = fd.read()
            fd.close()
            publish_html = pystache.render(template_html, template_data)
            fd = open(publish_filename, 'w')
            fd.write(publish_html)
            fd.close()
        

def main():
    p = Publish()
    p.publish(publishing_list)

if __name__ == '__main__':

    main()