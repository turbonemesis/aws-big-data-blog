# -*- coding: utf-8 -*-
'''
Created on Oct 8, 2015

@author: mentzera
'''

import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import json
import boto3
import twitter_to_es

s3 = boto3.client('s3', aws_access_key_id='AKIAUNEM5XJCISE637RI',
    aws_secret_access_key='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')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Getting s3 object
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
              
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    
    # Parse s3 object content (JSON)
    try:
        s3_file_content = response['Body'].read()
        #clean trailing comma
        tweet_array = ','.join(s3_file_content.decode().split('\n'))

        if tweet_array.endswith(','):
            tweet_array = tweet_array[:-1]

        tweets_str = '['+tweet_array+']'
        tweets = json.loads(tweets_str)
   
    except Exception as e:
        print(e)
        print('Error loading json from object {} in bucket {}'.format(key, bucket))
        raise e
    
    # Load data into ES
    try:
        twitter_to_es.load(tweets)

    except Exception as e:
        print(e)
        print('Error loading data into ElasticSearch')
        raise e    


if __name__ == '__main__':
    event = {
	    "Records": [
		    {
			    "s3": {
				    "bucket": {
					    "name": "botvador-data-lake-tweetsbucket-1gzszvp00ooua"
				    },
				    "object": {
					    "key": "raw/2020/01/23/07/botvador-data-lake-IngestionFirehoseStream-3DIDVNM2X421-1-2020-01-23-07-12-19-a4f81ff3-c16b-4da8-ae14-05964668e719"
				    }
			    }
		    }
	    ]
    }
    lambda_handler(event, None)
