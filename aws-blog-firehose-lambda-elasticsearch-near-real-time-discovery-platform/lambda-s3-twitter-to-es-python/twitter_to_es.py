'''
Created on Oct 8, 2015

@author: mentzera
'''
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, parallel_bulk
import config
from elasticsearch.exceptions import ElasticsearchException
from tweet_utils import get_tweet, id_field, get_tweet_mapping, tweet_mapping_v5, tweet_mapping

import requests
from requests.auth import HTTPBasicAuth


index_name = 'twitter'
doc_type = 'tweet'
# mapping = {doc_type: tweet_mapping
#            }
bulk_chunk_size = config.es_bulk_chunk_size

host = 'http://ec2-18-237-54-177.us-west-2.compute.amazonaws.com:9200'  # the Amazon ES domain, including https://
# host = 'https://9d230a39473f4abe9f0db0dc15d81c86.us-west1.gcp.cloud.es.io'  # the Amazon ES domain, including https://
# index = 'lambda-kine-index'
# type = 'lambda-kine-type'
url = host + '/' + index_name + '/' + doc_type + '/'

headers = {"Content-Type": "application/json"}


def create_index(es,index_name,mapping):
    print('creating index {}...'.format(index_name))
    es.indices.create(index_name, body = {'mappings': mapping})


def load(tweets):
    # es = Elasticsearch(host='9d230a39473f4abe9f0db0dc15d81c86.us-west1.gcp.cloud.es.io', port=9243, verify_certs=False,
    #               scheme="https", http_auth=('superturbo', 'M1nuteMa1d'))
    # es = Elasticsearch(hosts = config.es_host)
    # es = Elasticsearch(host = config.es_host, port = config.es_port, http_auth=('superturbo', 'M1nuteMa1d'))
    # es_version_number = es.info()['version']['number']
    # tweet_mapping = get_tweet_mapping(es_version_number)

    # mapping = {doc_type: tweet_mapping
    #            }
    #
    # if es.indices.exists(index_name):
    #     print ('index {} already exists'.format(index_name))
    #     try:
    #         es.indices.put_mapping(doc_type, tweet_mapping, index_name)
    #     except ElasticsearchException as e:
    #         print('error putting mapping:\n'+str(e))
    #         print('deleting index {}...'.format(index_name))
    #         es.indices.delete(index_name)
    #         create_index(es, index_name, mapping)
    # else:
    #     print('index {} does not exist'.format(index_name))
    #     create_index(es, index_name, mapping)
    
    counter = 0
    bulk_data = []
    list_size = len(tweets)
    for doc in tweets:
        tweet = get_tweet(doc)
        id = tweet[id_field]
        # print(tweet)
        bulk_doc = {
            "_index": index_name,
            "_type": doc_type,
            "_id": tweet[id_field],
            "_source": tweet
            }
        bulk_data.append(bulk_doc)
        counter+=1

        requests.put(url + id, json=tweet, headers=headers, auth=HTTPBasicAuth('superturbo', 'M1nuteMa1d'))

        # es = Elasticsearch(host='9d230a39473f4abe9f0db0dc15d81c86.us-west1.gcp.cloud.es.io', port=9243,
        #                    verify_certs=False,
        #                    scheme="https", http_auth=('superturbo', 'M1nuteMa1d'))
        # success, _ = es.index(index=index_name, doc_type=doc_type, body=tweet)
        # time.sleep(1)
        
        # if counter % bulk_chunk_size == 0 or counter == list_size:
        #     print("ElasticSearch bulk index (index: {INDEX}, type: {TYPE})...".format(INDEX=index_name, TYPE=doc_type))
        #     success, _ = es.index(index=index_name, doc_type=doc_type, body=)
        #     # success, _ = bulk(es, bulk_data)
        #     # success, _ = parallel_bulk(es, bulk_data)
        #     print('ElasticSearch indexed %d documents' % success)
        #     bulk_data = []
