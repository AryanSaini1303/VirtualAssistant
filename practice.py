import spacy

nlp = spacy.load("en_core_web_lg")

# sentence2 = "goodbye jarvis "
# sentence1 = "okay goodbye jarvis"
# # sentence3="jarvis, please open youtube"

# doc1 = nlp(sentence1)
# doc2 = nlp(sentence2)
# # doc3=nlp(sentence3)

# # print(doc2.similarity(doc3))
# # print(doc1.similarity(doc3))
# print(doc1.similarity(doc2))

closing1=nlp("thank you, goodbye jarvis")
closing2=nlp("bye")
closing3=nlp("close jarvis")
closing4=nlp("goodbye jarvis")
closing5=nlp("that's all for now goodbye jarvis")
text="that's all for now jarvis goodbye"
if (((nlp(text.lower())).similarity(closing1)>=0.7) or ((nlp(text.lower())).similarity(closing2)>=0.7) or ((nlp(text.lower())).similarity(closing4)>=0.7) or ((nlp(text.lower())).similarity(closing3)>=0.7) or ((nlp(text.lower())).similarity(closing5)>=0.7)):
    print("hello")