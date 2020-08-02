# Dev Key - df4338f9-e659-40fa-ba32-244e7dc3d882
# newspai - e122d722038042529cf99dba207ca492
# link this with the model and use it to classify how many articles match with the given headline!!


from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='e122d722038042529cf99dba207ca492')
news_sources = newsapi.get_sources()
for source in news_sources['sources']:
    print(source['name'])

all_articles = newsapi.get_everything(
    q='Smart India Hackathon',
    language='en',   
)

# Extracting all realted news article
for article in all_articles['articles']:
    print('Source : ',article['source']['name'])
    print('Title : ',article['title'])
    print('Description : ',article['description'],'\n\n')


