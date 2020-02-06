#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 20, 2015

@author: mentzera
'''
import re
from textblob import TextBlob
from datetime import datetime

class Sentiments:
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'
    CONFUSED = 'Confused'
    
id_field = 'id_str'
emoticons = {Sentiments.POSITIVE:'😀|😁|😂|😃|😄|😅|😆|😇|😈|😉|😊|😋|😌|😍|😎|😏|😗|😘|😙|😚|😛|😜|😝|😸|😹|😺|😻|😼|😽',
             Sentiments.NEGATIVE : '😒|😓|😔|😖|😞|😟|😠|😡|😢|😣|😤|😥|😦|😧|😨|😩|😪|😫|😬|😭|😾|😿|😰|😱|🙀',
             Sentiments.NEUTRAL : '😐|😑|😳|😮|😯|😶|😴|😵|😲',
             Sentiments.CONFUSED: '😕'
             }

tweet_mapping = {'properties': 
                    {'timestamp_ms': {
                                  'type': 'date'
                                  },
                     'text': {
                                  'type': 'string'
                              },
                     'coordinates': {
                          'properties': {
                             'coordinates': {
                                'type': 'geo_point'
                             },
                             'type': {
                                'type': 'string',
                                'index' : 'not_analyzed'
                            }
                          }
                     },
                     'user': {
                          'properties': {
                             'id': {
                                'type': 'long'
                             },
                             'name': {
                                'type': 'string'
                            }
                          }
                     },
                     'sentiments': {
                                  'type': 'string',
                                  'index' : 'not_analyzed'
                              }
                    }
                 }


#https://www.elastic.co/blog/strings-are-dead-long-live-strings
tweet_mapping_v5 = {'properties':
                    {'timestamp_ms': {
                                  'type': 'date'
                                  },
                     'text': {
                                  'type': 'text'
                              },
                     'coordinates': {
                          'properties': {
                             'coordinates': {
                                'type': 'geo_point'
                             },
                             'type': {
                                'type': 'keyword'
                            }
                          }
                     },
                     'user': {
                          'properties': {
                             'id': {
                                'type': 'long'
                             },
                             'name': {
                                'type': 'text'
                            }
                          }
                     },
                     'sentiments': {
                                  'type': 'keyword'
                              }
                    }
                 }


def _sentiment_analysis(tweet):
    tweet['custom_fields']['emoticons'] = []
    tweet['custom_fields']['sentiments'] = []
    # _sentiment_analysis_by_emoticons(tweet)
    if len(tweet['custom_fields']['sentiments']) == 0:
        _sentiment_analysis_by_text(tweet)


def _sentiment_analysis_by_emoticons(tweet):
    for sentiment, emoticons_icons in emoticons.items():
        matched_emoticons = re.findall(emoticons_icons, tweet['text'].encode('utf-8'))
        if len(matched_emoticons) > 0:
            tweet['custom_fields']['emoticons'].extend(matched_emoticons)
            tweet['custom_fields']['sentiments'].append(sentiment)
    
    if Sentiments.POSITIVE in tweet['sentiments'] and Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['custom_fields']['sentiments'] = Sentiments.CONFUSED
    elif Sentiments.POSITIVE in tweet['sentiments']:
        tweet['custom_fields']['sentiments'] = Sentiments.POSITIVE
    elif Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['custom_fields']['sentiments'] = Sentiments.NEGATIVE

def _sentiment_analysis_by_text(tweet):
    blob = TextBlob(tweet['text'])
    # blob = TextBlob(tweet['text'].decode('ascii', errors="replace"))
    sentiment_polarity = blob.sentiment.polarity
    if sentiment_polarity < 0:
        sentiment = Sentiments.NEGATIVE
    elif sentiment_polarity <= 0.2:
                sentiment = Sentiments.NEUTRAL
    else:
        sentiment = Sentiments.POSITIVE
    tweet['custom_fields']['sentiments'] = sentiment
    
def get_tweet(doc):
    doc['custom_fields'] = {}
    doc['custom_fields']['hashtags'] = list(map(lambda x: x['text'],doc['entities']['hashtags']))
    doc['custom_fields']['timestamp'] = doc['timestamp_ms']
    doc['custom_fields']['processed_time'] = datetime.now().isoformat()
    doc['custom_fields']['mentions'] = re.findall(r'@\w*', doc['text'])

    # tweet = {}
    # tweet[id_field] = doc[id_field]
    # tweet['hashtags'] = list(map(lambda x: x['text'],doc['entities']['hashtags']))
    # tweet['coordinates'] = doc['coordinates']
    # tweet['timestamp_ms'] = doc['timestamp_ms']
    # tweet['text'] = doc['text']
    # tweet['user'] = {'id': doc['user']['id'], 'name': doc['user']['name']}
    # tweet['mentions'] = re.findall(r'@\w*', doc['text'])

    _sentiment_analysis(doc)
    return doc

def get_tweet_mapping(es_version_number_str):
    major_number = int(es_version_number_str.split('.')[0])
    if major_number >= 5:
        return tweet_mapping_v5
    return tweet_mapping