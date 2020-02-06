'''
Created on Oct 12, 2015

@author: mentzera

'''

# es_host = '9d230a39473f4abe9f0db0dc15d81c86.us-west1.gcp.cloud.es.io' #without the https - for example: search-es-twitter-demo-xxxxxxxxxxxxxxxxxxx.us-east-1.es.amazonaws.com
es_host = 'https://superturbo:M1nuteMa1d@9d230a39473f4abe9f0db0dc15d81c86.us-west1.gcp.cloud.es.io' #without the https - for example: search-es-twitter-demo-xxxxxxxxxxxxxxxxxxx.us-east-1.es.amazonaws.com
# es_port = 80
es_port = 9243
es_bulk_chunk_size = 1000  #number of documents to index in a single bulk operation

