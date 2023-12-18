from hybridtfidf import HybridTfidf
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spacy
nlp = spacy.load("en_core_web_sm")


PREFIX = "STOIC: "
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "howdy", "ghbdtn", "privet", "hey", "toki", "pona")
GOODBYE_INPUTS = ("goodbye", "bye", "quit", "exit", "poka", "mi tawa")

def initialize() -> None:
    
    with open("./stoic_data.txt", "r") as stoic_file:
        sentences = stoic_file.readlines()
    replies = sentences

    sent_tokens = []
    for sent in sentences:
        lemm_sent = [word.lemma_ for word in nlp(sent) if not word.is_stop and word.text.isalpha()]
        sent_tokens.append(" ".join(lemm_sent))

    print("Initialized successfully!\n_________________________\n\n")
    return sent_tokens, replies

def response(user_response: str, sent_tokens: list, replies: list) -> str:
    sent_tokens.append(user_response)

    hybridtfidf = HybridTfidf(threshold=7)
    hybridtfidf.fit(sent_tokens)

    tfidf = np.array(hybridtfidf.transform(sent_tokens))
    
    vals = cosine_similarity(tfidf[-1].reshape(1, -1), tfidf)
    
    idx = vals.argsort()[0][-2]
    
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if(req_tfidf == 0):
        robo_response =  "I am sorry! I don't understand you"
    else:
        robo_response = replies[idx]
        
    sent_tokens.remove(user_response)
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
    
    print(response(user_response, sent_tokens, replies))
    main()

try:
    sent_tokens, replies = initialize()
    main()

except Exception as e:
    print(e)