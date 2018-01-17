def change_wall_paper(path):
	import ctypes
	SPI_SETDESKWALLPAPER = 20 
	r = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
	if not r:
		print(ctypes.WinError())

def load_photos_from_500px():
	import time
	from urllib import request
	import json
	
	_FEATURES = ('popular', 'highest_rated', 'upcoming', 'editors', 'fresh_today', 'fresh_yesterday', 'fresh_week')
	_500PX = 'https://api.500px.com/v1/photos?feature=%s&rpp=%s&page=%s&only=Travel&image_size=1600&consumer_key=YLOgPNFqx2yrQvLxJ6cdo2OVZyGwXLemCaGU07jI'
	
	rand_pg = str(int(time.time()) % 100)
	rand_ft = int(time.time()) % len(_FEATURES)
	rand_rp = str((int(time.time()) % 20) + 20)

	while True:
		with request.urlopen(_500PX  % (_FEATURES[rand_ft], rand_rp, rand_pg)) as req:
			result = json.loads(req.read().decode())
		photos = result['photos']
		if result['photos']:
			return result['photos']
		rand_pg = str(int(time.time() % result['total_pages']))
		
def get_dir_path():
	import os
	return os.path.dirname(os.path.abspath(__file__))
	
def join_dir(*paths):
	import os
	return os.path.join(*paths)
	
def download_image(url, image_path):
	from urllib import request
	with request.urlopen(url) as req:
		with open(image_path, mode='wb') as img:
			img.write(req.read())

def find_best_match_ratio(photos, width=1920, height=1080):
	good_ratio = width / height
	ratios = [photo['width'] / photo['height'] for photo in photos]
	best_diff = ratios[0] - good_ratio
	best_ind = 0
	for i, ratio in enumerate(ratios[1:], 1):
		diff = (ratio - good_ratio)
		if diff < best_diff:
			best_diff = diff
			best_ind = i
		
	return photos[best_ind]
	
def find_widest(photos):
	best_diff = max([(photo['width'] - photo['height'], i) for i, photo in enumerate(photos)])
	return photos[best_diff[1]]
	
	
if __name__ == '__main__':
	photo = find_widest(load_photos_from_500px())
	image_path = join_dir(get_dir_path(), photo['name'] + '.' + photo['images'][0]['format'])
	download_image(photo['image_url'], image_path)
	change_wall_paper(image_path)
	