from model import Data_Analysis, Data_Extraction, Data_Parsing
from constants import media_urls

data_extractor = Data_Extraction(urls = media_urls)

data_extractor.main(media_urls)

data_parsing = Data_Parsing(data_extractor)

data_parsing.extracting_titles_from_response()

data_parsing.creating_one_big_string()

data_analysis = Data_Analysis(data_parsing)

data_analysis.filtering_stopwords()

data_analysis.analyzing_collocations()

data_analysis.finding_most_common_words(top_n=50)

data_analysis.most_common_words_with_collocations()

data_analysis.list_to_csv()


