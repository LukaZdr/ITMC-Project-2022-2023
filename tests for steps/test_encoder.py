from encoder import Encoder
from sklearn.metrics.pairwise import cosine_similarity

encoder = Encoder()
sentence = ['ein satz der verschlüsselt weden muss', 'texte encoden bringt ist wichtig', 'mein auto ist kaputt', 'ich muss in die Werkstatt']

list = encoder.run(sentence)

print(cosine_similarity(list,list))

