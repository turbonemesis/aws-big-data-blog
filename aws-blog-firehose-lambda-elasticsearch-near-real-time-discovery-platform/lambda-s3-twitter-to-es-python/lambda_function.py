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
# import twitter_to_es
import github_to_es

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
        resource_array = ','.join(s3_file_content.decode().split('\n'))

        if resource_array.endswith(','):
            resource_array = resource_array[:-1]

        resources_str = '['+resource_array+']'
        resources = json.loads(resources_str)
   
    except Exception as e:
        print(e)
        print('Error loading json from object {} in bucket {}'.format(key, bucket))
        raise e
    
    # Load data into ES
    try:
        github_to_es.load(resources)

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
					    "name": "github-data-lake"
				    },
				    "object": {
					    "key": "raw/2020/02/09/08/github-data-lake-IngestionFirehoseStream-1-2020-02-09-08-13-35-43864005-20d6-4bad-87c4-3b978c6297a4"
				    }
			    }
		    }
	    ]
    }
    lambda_handler(event, None)
