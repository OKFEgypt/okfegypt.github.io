#!/usr/bin/env python

import json
import pystache
import yaml


    
class Publish:

    def __init__(self, config_file='config.yml'):
        self.templates_dir = 'templates'
        self.data_dir = 'data'
        self.publishing_list = []
        self.config_file = config_file
        self.load_config()
        #print self.publishing_list
    
    def load_config(self):
        fd = open(self.config_file, 'r')
        config_txt = fd.read()
        fd.close()
        config_data = yaml.load(config_txt)
        for out_file, out_file_params in config_data.items():
            publish_item = {}
            publish_item['out_file'] = out_file
            publish_item['json_file'] = 'json/' + out_file.rsplit('.',1)[0] + '.json'
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
    
    def parse_yaml(self, filename):
        fd = open(filename, 'r')
        config_txt = fd.read()
        fd.close()
        config_data = yaml.load(config_txt)
        return config_data
    
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

    def publish(self):
        for pub_item in self.publishing_list:
            #print pub_item
            data = {
                'title': pub_item['title'],
                'sections': self.parse_yaml(pub_item['data_file'])
            }
            #print data
            fd = open(pub_item['template_file'], 'r')
            template = fd.read()
            fd.close()
            publish_html = pystache.render(template, data)
            #print publish_html
            fd = open(pub_item['out_file'],'w')
            fd.write(publish_html)
            fd.close()
            fd = open(pub_item['json_file'],'w')
            fd.write(json.dumps(data))
            fd.close()
        
        

def main():
    p = Publish()
    p.publish_index()
    p.publish()

if __name__ == '__main__':

    main()
    
    