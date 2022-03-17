import re
from unidecode import unidecode
from constants import list_of_user_agents, list_xpaths
import random

def normalizing_text(string):
    #With this regex we extract symbols and special characters
    regex_symbols = '[\$\#\?\¿\!\¡\-\"\'\:\;]'
    
    title = string.replace('\n',' ').replace(',','.')
    #Removing accents and putting everything in uppercase
    title = unidecode(title).lower()
    
    #Extracting special characters
    title = re.sub(regex_symbols,'', title)
    
    #Analyzing if we have the . or , between numbers:
    #With this logic, we remove the symbol if it inst inside numbers
    list_title = title.split(' ')
    for index in range(len(list_title)):
        if list_title[index].find('.'):
            if bool(re.match('[0-9](\.)[0-9]',list_title[index])) == True: #If its true, that means we shouldnt remove that . or ,
                  continue
            else:
                word = re.sub('[\.]','', list_title[index])
                list_title[index] = word
    
    title = ' '.join(list_title)
    
    return title

def selecting_random_useragent():
    return random.choice(list_of_user_agents)

def finding_xpath_per_channel(response:list):
    for xpath in list_xpaths:
        if response[1] in xpath[1]: #response[1] and xpath[1] are the names of the sites
            return xpath #Its the xpath tuple with expresion and name
