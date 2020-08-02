# Dev Key - df4338f9-e659-40fa-ba32-244e7dc3d882
# newspai - e122d722038042529cf99dba207ca492
# link this with the model and use it to classify how many articles match with the given headline!!



# Dev Key - df4338f9-e659-40fa-ba32-244e7dc3d882
# newspai - e122d722038042529cf99dba207ca492

from newsapi import NewsApiClient
from bs4 import BeautifulSoup
from newspaper import Article
import Levenshtein

Levenshtein.distance('Levenshtein Distance', 'Levenshtein Distance')
sentences = ['This is a sentence', 'Hello']
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def cleanString(text):
	text = ''.join([word for word in text if word not in string.punctuation])
	text = text.lower()
	text = ''.join([word for word in text.split() if word not in stopwords])
	return text

def cosine_sim_vectors(vec1, vec2):
	vec1 = vec1.reshape(1, -1)
	vec2 = vec2.reshape(1, -1)
	return cosine_similarity(vec1, vec2)[0][0]

cleaned = list(map(cleanString, sentences))
vectorizer = CountVectorizer().fit_transform(cleaned)
vectors = vectorizer.toarray()
print(vectors)
csim = cosine_similarity(vectors)
print(csim)
print(cosine_sim_vectors(vectors[0], vectors[1]))

def load_model(url):
    article = Article(url)
    article.download()
    article.parse()
    var = str(article.text)

    model = pickle.load(open('final_model.sav', 'rb'))
    prediction = model.predict([var])
    prob = model.predict_proba([var])
    # truth = prob[0][1]
    return [prediction[0], prob[0][1]]



newsapi = NewsApiClient(api_key='e122d722038042529cf99dba207ca492')
news_sources = newsapi.get_sources()
for source in news_sources['sources']:
    print(source['name'])

all_articles = newsapi.get_everything(
    q='England won 2019 Cricket World Cup',
    language='en',   
)

# Extracting all realted news article
for article in all_articles['articles']:
    print('Source : ',article['source']['name'])
    print('Title : ',article['title'])
    print('Description : ',article['description'],'\n\n')



    
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


