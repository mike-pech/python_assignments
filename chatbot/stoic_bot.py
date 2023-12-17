# import nltk
# nltk.download("punkt")
# nltk.download("wordnet")
# lemmer = nltk.stem.WordNetLemmatizer()
# from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
nlp = spacy.load("en_core_web_sm")
# from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from hybridtfidf import HybridTfidf

hybridtfidf = HybridTfidf(threshold=7)


PREFIX = "STOIC: "
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "howdy", "ghbdtn", "privet", "hey", "toki", "pona")
GOODBYE_INPUTS = ("goodbye", "bye", "quit", "exit", "poka", "mi tawa")

def initialize() -> None:
    with open("./stoic_data.txt", "r") as stoic_file:
        # temp_tokens = list(nlp(stoic_file.read()).sents)
        # print(type(temp_tokens[0]))
        # for sent in temp_tokens:
        #     sent = " ".join([word for word in nlp(str(sent)) if not word.is_stop])
        #     sent_tokens.append(sent)
        sent_tokens = " ".join([token.text for token in nlp(stoic_file.read()) if not token.is_stop])
    print("Initialized successfully!\n_________________________\n\n")
    return sent_tokens

# def lemTokens(tokens):
#     return [lemmer.lemmatize(token) for token in tokens]

# def lemNormalize(text):
#     remove_punct_dict = dict((ord(punct), None) for punct in punctuation)
#     return lemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def cosine_similarity(a, b):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def response(user_response: str, sent_tokens) -> str:
    sent_tokens = sent_tokens + user_response
    # TfidfVec = TfidfVectorizer(
    #     tokenizer = lemNormalize, 
    #     token_pattern = None,
    #     stop_words = "english")
    
    # tfidf = TfidfVec.fit_transform(sent_tokens) 
    hybridtfidf.fit(sent_tokens)
    tfidf = np.array(hybridtfidf.transform(sent_tokens)) 
    
    vals = cosine_similarity(tfidf[-1].reshape(-1, 1), tfidf)
    
    idx = vals.argsort()[0][-2]
    
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if(req_tfidf == 0):
        robo_response =  "I am sorry! I don't understand you"
    else:
        robo_response = sent_tokens[idx]
        
    sent_tokens = sent_tokens.replace(user_response, "")
    return robo_response

def main() -> None:
    user_response = input("YOU: ").lower()

    if user_response in GREETING_INPUTS:
        print(f"{PREFIX}Greetings!")
        main()

    if user_response in GOODBYE_INPUTS:
        print(f"{PREFIX}Goodbye!")
        quit()
    
    if "thanks" in user_response or "thank you" in user_response:
        print(f"{PREFIX}You are welcome!")
        main()
    
    print(response(user_response, sent_tokens))
    main()

# try:
sent_tokens = initialize()
main()
# except Exception as e:
#     print(e)
    # quit()