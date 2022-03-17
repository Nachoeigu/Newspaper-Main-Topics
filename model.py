from requests_html import AsyncHTMLSession
import re
import nltk
from nltk import bigrams
from nltk.corpus import stopwords
from collections import Counter
from functions import selecting_random_useragent, finding_xpath_per_channel, normalizing_text
import pandas as pd
nltk.download("punkt")
nltk.download('stopwords')

class Data_Extraction:
    
    def __init__(self, urls:list):
        self.asession = AsyncHTMLSession()
        self.urls = urls

    #This function is useful for those cases we need to render Javascript content
    async def request(self, url):
        print(f"Making request for {url}")
        response = await self.asession.get(url = url, headers = selecting_random_useragent())
        # Check if we can render these two sites because they have more articles
        # try:
        #     if bool(url.find('lanacion')) | bool(url.find('destape')):
        #         pass
        #         await response.html.arender(timeout = 20)
        # except: 
        #     pass
        print(f"Request done for {url}")
        return [response, url]

    #This function executes the asynchronous requests
    def main(self, urls):
        print("Starting extraction from the server")
        self.list_of_responses = self.asession.run(*[lambda url = url: self.request(url) for url in self.urls])
        print("Finished extraction from the server")

class Data_Parsing(Data_Extraction):
    
    def __init__(self, data_extractor):
        self.list_of_responses = data_extractor.list_of_responses
        self.titles = []

    def __special_case_pagina12(self, articles):
        for article in articles:
            try:
                article_1 = article.xpath('//div[@class="element title"]')[0] #For the start of the title
                article_1 = normalizing_text(article_1.text)
            except IndexError:
                try:
                    article_1 = re.search('>([A-z0-9\s\,\.áéíóú]+).+?\<span.*', article.html).group(1)
                    article_1 = normalizing_text(article_1)
                except:
                    article_1 = normalizing_text(article.text)

            try:
                article_2 = normalizing_text(article.xpath('//div[@class="element title-suffix" or @class="element title-preffix"]')[0].text) #For the start of the title
                final_article = article_1 + ' ' + article_2
            except IndexError:
                try:
                    article_2 = normalizing_text(article.xpath('//span')[-1].text)
                    final_article = article_1 + ' ' + article_2
                except:
                    final_article = normalizing_text(article.text)
            self.titles.append(final_article)

    def extracting_titles_from_response(self):
        print("Extracting the title from the responses")
        for index, response in enumerate(self.list_of_responses):
            #Response is a list of two element: first one the content and second one the url
            xpath_tuple = finding_xpath_per_channel(response = response)
            #xpath_tuple[0] is the xpath expression xpath_tuple[1] is the name of the site
            xpath_expression = xpath_tuple[0]
            site_name = xpath_tuple[1]
            
            articles = response[0].html.xpath(xpath_expression)
            
            if site_name == 'pagina12':
                #This is a special case:
                self.__special_case_pagina12(articles)
            else:
                for article in articles:
                    self.titles.append(normalizing_text(article.text))  

    def creating_one_big_string(self):
        print("Joining all the titles in a big one string")
        self.all_words = ' '.join(self.titles)
        self.all_words = self.all_words.replace(' %','%') #This is for cases where they are one word but they are separated

class Data_Analysis(Data_Parsing):

    def __init__(self, data_parsing):
        self.all_words = data_parsing.all_words

    def __creating_stopwords_list(self):
        list_of_stopwords = stopwords.words("spanish")
        #Adding some more words in the list_of_stopwords
        words_to_add_in_stopwords = ['tras','despues','luego']

        for added_word in words_to_add_in_stopwords:
            list_of_stopwords.append(added_word)

        self.list_of_stopwords = [normalizing_text(element) for element in list_of_stopwords]    

    def filtering_stopwords(self):
        print("Loading the stopwords")
        #First we create stopwords list
        self.__creating_stopwords_list()

        tokens = self.all_words.strip().split(' ')
        print("Filtering words in the stopwords")
        self.tokens = [word.upper() for word in tokens if (not word in self.list_of_stopwords)&(word != '')&(len(word) > 2)]

    #A collocation is a combination of words that are used together
    def analyzing_collocations(self):
        print("Finding collocations")
        #Finding collocations
        bgs = bigrams(self.tokens)
        #Calculating the most common collocations
        fdist = nltk.FreqDist(bgs)
        collocations = fdist.most_common()

        #With this loop we define which collocations are the most relevant and how many occurences they have
        self.collocation_values = []
        self.collocation_sentences = []
        for collocation in collocations:
            if collocation[-1] < 6:
                break
            else:
                first_word = collocation[0][0]
                second_word = collocation[0][1]
                sentence = first_word + ' ' + second_word
                self.collocation_sentences.append(sentence)
                self.collocation_values.append(collocation[-1])


    def finding_most_common_words(self,top_n:int):
        print("Finding most common words in the big one string")
        #We calculate the most common words
        word_count = Counter(self.tokens)
        word_count = word_count.most_common(top_n)
        self.word_count = [list(element) for element in word_count]

    def __asigning_collocations(self):
        print("Replacing unique words that are part of a collocation")
        already_assigned = []
        for index in range(len(self.word_count)): 
            for sentence in self.collocation_sentences:
                #if we already analyze that collocation
                if sentence in already_assigned:
                    #If the new word contains a word of a past collocation, we mark it so later we can delete them
                    if (sentence.split(' ')[0] == self.word_count[index][0])|(sentence.split(' ')[1] == self.word_count[index][0]):
                        self.word_count[index][0] = ''
                        break
                    else:
                        continue
                words = sentence.split(' ')
                if (words[0] == self.word_count[index][0])|(words[1] == self.word_count[index][0]):
                    self.word_count[index][0] = sentence
                    already_assigned.append(sentence)
                    break
                    
    def most_common_words_with_collocations(self):
        print("Structing the top words (with collocations)")
        self.__asigning_collocations()
        #We put everything in a new list, without the duplicated words from collocations
        self.most_common_word = []
        for index in range(len(self.word_count)):
            if (self.word_count[index][0] == '')|(len(self.word_count[index][0]) < 4):
                continue
            else:
                self.most_common_word.append(self.word_count[index])

    def list_to_csv(self):
        print('Exporting to csv file')       
        df = pd.DataFrame({'content':self.most_common_word})
        df['content'] = [element[0] + '.--.' + str(element[1]) for element in df['content']]
        df = df['content'].str.split('.--.', expand=True)
        df = df.rename({0:'word',
                1:'frequency'}, axis = 1)

        df.to_csv('top_words_in_newspapers.csv')
