#!/usr/bin/env python

import pystache
import yaml


    
class Publish:

    def __init__(self, config_file='config.yml'):
        self.templates_dir = 'templates'
        self.data_dir = 'data'
        self.publishing_list = []
        self.config_file = config_file
        self.load_config()
        print self.publishing_list
    
    def load_config(self):
        fd = open(self.config_file, 'r')
        config_txt = fd.read()
        fd.close()
        config_data = yaml.load(config_txt)
        for out_file, out_file_params in config_data.items():
            publish_item = {}
            publish_item['out_file'] = out_file
            publish_item['title'] = out_file_params['title']
            publish_item['data_file'] = self.construct_filename(out_file_params['data'], 'data')
            publish_item['template_file'] = self.construct_filename(out_file_params['template'], 'template')
            self.publishing_list.append(publish_item) 
        
        
    def construct_filename(self, filename, filetype):
        if filetype == 'data':
            return self.data_dir + '/' + filename 
        elif filetype == 'template':
            return self.templates_dir + '/' + filename
        else:
            return filename
            
    def parse_data(self, filename):
        data = []
        fd = open(filename, 'r')
        for line in fd.readlines():
            if not line:
                pass
            elif line.startswith('='):
                section_name = line[1:].strip()
                section_data = {}
                section_data['name'] = section_name
                section_data['items'] = []
            elif line.startswith('*'):
                item_name, item_url = line[1:].strip().split(',') 
                item_data = {
                    'name': item_name.strip(),
                    'url': item_url
                }
                section_data['items'].append(item_data)
            elif line.startswith('_'):
                data.append(section_data)
            else:
                pass
        fd.close()
        return {'sections': data}
    
    def publish_index(self):
        index_template = 'templates/index.mustache'
        index_out_file = 'index.html'
        template_data = {'pages': self.publishing_list}
        fd = open(index_template, 'r')
        template_html = fd.read()
        fd.close()
        publish_html = pystache.render(template_html, template_data)
        fd = open(index_out_file, 'w')
        fd.write(publish_html)
        fd.close()

                
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
    p.publish_index()
    #p.publish(publishing_list)

if __name__ == '__main__':

    main()