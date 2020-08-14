# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# imports firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from time import gmtime, strftime
from os import environ, path, getcwd
from base64 import b64decode


class MyCrawlerPipeline:

    def load_spider(self, spider):
        self.crawler = spider.crawler
        self.settings = spider.settings

    def open_spider(self, spider):
        # self.file = open('boletim.txt', 'w')
        # print("teste - open_spider")

        self.load_spider(spider)

        filename = path.normpath(path.join(getcwd(), 'ServiceAccountKey.json'))
        with open(filename, "wb") as json_file:
            json_file.write(b64decode(self.settings['FIREBASE_SECRETS']))

        configurarion = {
            'credential': credentials.Certificate(filename),
            'options': {'databaseURL': self.settings['FIREBASE_DATABASE']}
        }

        firebase_admin.initialize_app(**configurarion)
        

        # connecting to firestore   
        # cred = credentials.Certificate("./ServiceAccountKey.json")
        # cred = credentials.Certificate(data)
        # app = firebase_admin.initialize_app(cred)

        
        self.store = firestore.client()
        # document_name = strftime("%Y-%m-%d", gmtime())
        # self.doc_ref = store.collection(u'cases').document(document_name)


    def process_item(self, item, spider):

        item['date'] = item['date'].replace(" ","")
        item['positivos'] = "".join(c for c in item['positivos'] if c.isdigit())
        item['curados'] = "".join(c for c in item['curados'] if c.isdigit())
        item['obitos'] = "".join(c for c in item['obitos'] if c.isdigit())

        line = json.dumps(dict(item)) + '\n'
        # self.file.write(line)

        ano = item['date'][6:10]
        mes = item['date'][3:5]
        dia = item['date'][0:2]

        document_name = ano + "-" + mes + "-" + dia
        self.doc_ref = self.store.collection(u'cases').document(document_name)
        self.doc_ref.set(item)

        return item


    def close_spider(self, spider):
    # self.file.close()
        pass