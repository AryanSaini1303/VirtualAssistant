import spacy

nlp = spacy.load("en_core_web_lg")

sentence2 = "jarvis what time is it?"
sentence1 = "what is the time?"
# sentence3="jarvis, please open youtube"

doc1 = nlp(sentence1)
doc2 = nlp(sentence2)
# doc3=nlp(sentence3)

# print(doc2.similarity(doc3))
# print(doc1.similarity(doc3))
print(doc1.similarity(doc2))

