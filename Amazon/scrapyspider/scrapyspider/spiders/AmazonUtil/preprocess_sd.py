import re

def remove_pricing(title):
	m = re.search(r'( ?(?:\$[\d\.]+) ?)', title)
	if m is not None:
		title = title.replace(m.group(0), ' ')
		title = title.strip()
		return title

def wrangle_title(title):
	title = remove_pricing(title)
	return title