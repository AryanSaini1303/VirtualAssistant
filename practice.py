# import spacy

# nlp = spacy.load("en_core_web_lg")

# sentence2 = "thank you, goodbye jarvis"
# sentence1 = "thanks a lot jarvis goodbye"
# # sentence3="jarvis, please open youtube"

# doc1 = nlp(sentence1)
# doc2 = nlp(sentence2)
# # doc3=nlp(sentence3)

# # print(doc2.similarity(doc3))
# # print(doc1.similarity(doc3))
# print(doc1.similarity(doc2))

response="Sure, I can do that. I found Mankha Musa I, also known as Mansa Musa, was the tenth Mansa of the Mali Empire in the 14th century. Is there anything else I can do for you?"
if "sure, i can do that." in response.lower():
    print("hello")
