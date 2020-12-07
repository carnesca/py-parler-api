import os
import sys
import pandas as pd

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from parler import Parler

# Returns top 20 hashtags and shows them in a data frame
def pageHashtags():
	q = input('Enter search term: ')
	dict1 = {}
	dict1['tag'] = []
	dict1['totalPosts'] = []
	print('Collecting hashtags that contain ' + q + '..')
	fetch = Parler().getHashtags(q)
	for x in fetch['tags']:
		dict1['tag'].append(x['tag'])
		dict1['totalPosts'].append(x['totalPosts'])
	df_tags = pd.DataFrame.from_dict(dict1)
	print(df_tags)

pageHashtags()
