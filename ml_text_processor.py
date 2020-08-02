import stock_quote
import media_parser
import nltk
import string
from nltk.tokenize import word_tokenize
import re
#nltk.download('stopwords')
#nltk.download('wordnet')

class Text_Processor:
    def __init__(self,dataset):
        self.dataset=dataset
        self.stopwords=nltk.corpus.stopwords.words('english')
        
    def strip_punctuation(self,raw_text):
        return "".join(char for char in raw_text if char not in string.punctuation)

    def tokenize(self,unpunctuated_text):
        return re.split("\W+",unpunctuated_text)

    def strip_stopwords(self,tokenized_text):
        return [word for word in tokenized_text if word not in self.stopwords]

    def stem_text(self,tokenized_text):
        stemmer=nltk.PorterStemmer()
        return [stemmer.stem(word) for word in tokenized_text]

    def lemmatize_text(self,tokenized_text):
        lemmatizer=nltk.WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in tokenized_text]

    def process_text(self,raw_text):
        unpunctuated_text=self.strip_punctuation(raw_text)
        tokenized_text=self.tokenize(unpunctuated_text)
        stripped_tokenized_text=self.strip_stopwords(tokenized_text)
        stemmed_text=self.stem_text(stripped_tokenized_text)
        return stemmed_text


    


test=[]
x=Text_Processor(test)
print(x.strip_punctuation("asdf, sdte. they're"))
print(x.tokenize("asdf sdte theyre"))
print(x.strip_stopwords(["the", "fat", "cat", "went", "over", "the", "hill", "to", "find", "the", "big", "dragon", "as" ,"he", "slept"]))
print(x.stem_text(["studied", "tried", "have", "had", "lick", "licking", "licked", "licker"]))
print(x.lemmatize_text(["studied", "tried", "have", "had", "licks", "licking", "licked", "licker"]))
y=media_parser.CNNParser("https://www.cnn.com/2020/07/29/politics/donald-trump-suburbs-housing/index.html")
print(x.process_text(y.get_body_text()))