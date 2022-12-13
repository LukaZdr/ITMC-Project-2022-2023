from modules.searcher import Searcher

searcher = Searcher()
results = searcher.run('Was ist WWW?')
for score, text in results:
  print(score, text)