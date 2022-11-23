from crawler import Crawler
from preprocessor import Preprocessor
from transformer import Transformer

# Selection
seed_urls = ['https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)']
crawler = Crawler()
texts = crawler.run(seed_urls)

# Preprocessing
preprocessor = Preprocessor()
preprocessed_paragraphs = preprocessor.run(texts)

# Transformation
transformer = Transformer()
transformed_texts = transformer.run(preprocessed_paragraphs)
print(len(transformed_texts))

# Data mining

# Interpretation