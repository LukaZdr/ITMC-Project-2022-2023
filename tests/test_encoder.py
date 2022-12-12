from encoder_flair import EncoderFlair
from encoder import Encoder
from sklearn.metrics.pairwise import cosine_similarity

encoder = EncoderFlair()
sentences = ['ein satz der verschlüsselt weden muss', 'texte encoden bringt ist wichtig', 'mein auto ist kaputt', 'ich muss in die Werkstatt']

list = encoder.run(sentences)
print(cosine_similarity(list,list))

encoder = Encoder()
list = encoder.run(sentences)
print(cosine_similarity(list,list))
