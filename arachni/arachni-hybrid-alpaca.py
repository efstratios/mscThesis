# -*- coding: utf-8 -*-

import os, re, csv, random, argparse, datetime
import subprocess
from subprocess import check_output
import urllib.request
from functools import lru_cache

# REGEX / Search patterns
HYPERLINK = re.compile("\"(.*?)\"")
PAGE_SIZE = re.compile("(?<=\[).?\d{2,}") 
DEPENDENCIES = re.compile("(?<=Downloaded: )(.*)(?= files)")
TOTAL_SIZE = re.compile("(?<=, )(.*)(?= in)")
ALPACA_PADDING_FLAG = re.compile("alpaca-padding")

csv_header =["OnionWebsite", "URL", "URLPageSize", "NumberOfDependencies", "TotalSize", "ObjectPageSize", "LoadedPagesSize"]

RNG = random.Random(0)

dt = str(datetime.datetime.now())

def main(): 
	
	parser = argparse.ArgumentParser(description='Onion URLs & HTTP request percentage input for arachni crawler.')
	parser.add_argument("--csv", required=True,
						help="Onion CSV format example: onion_exact_example.csv")
	args = parser.parse_args()

	onion_input_csv = args.csv
	
	if os.path.exists("alpaca-latest-50k-features.csv"): 
	   	os.rename("alpaca-latest-50k-features.csv","alpaca-50k-features-"+dt+".csv")

	with open(onion_input_csv, 'r') as onioncsv: 
		onions = csv.reader(onioncsv, delimiter=',') 
		next(onions) 
		with open('alpaca-latest-50k-features.csv', 'a', newline='') as outcsv:
			writer = csv.writer(outcsv) 
			writer.writerow(i for i in csv_header)
			for row in onions:
				(onion_webpage, onion_files) = page_requisites(str(row[0]))
				n_requests=float(row[1])  
				if "http://ynvs3km32u33agwq" in str(row[0]):
					features = list(features_extractor(onion_webpage,onion_files,n_requests)) 
					for i in features:
						writer.writerow(i)
				else: 
					features = list(features_extractor_cached(onion_webpage,onion_files,n_requests)) # LRU
					for i in features:
						writer.writerow(i)
	os.system("rm -rf *.onion")  
	

# Extract specific features from wget command -- CHOSEN site has alpaca enabled.
def features_extractor(onion_webpage,onion_files,n_requests): 

	n_requests=int((n_requests*50)*1000) 
	
	for i in range(n_requests):
		if RNG.choice([True, False]): # Main index.html file

			success, output = page_load_raw(onion_webpage)
			if not success:
				print("Couldn't fetch %s" % onion_webpage)
				return
			
			index = onion_webpage+"/index.html" 
			
			success, index_output = page_load_raw(index)
			if not success:
				print("Couldn't fetch %s" % index)
				return
			page_size = PAGE_SIZE.findall(str(index_output))
			page_size = [int(i) for i in page_size] 
			index_page_size = int(page_size[0])

			dependencies = DEPENDENCIES.findall(str(index_output))
			number_of_dependencies = [str(i) for i in dependencies] 
			total_dependencies = int("".join(number_of_dependencies)) - 1  
			total_size = sum(page_size)
			obj_size= (total_size-index_page_size)

			yield onion_webpage, index, index_page_size, total_dependencies, total_size, obj_size, page_size
		
		else: # any other file contained inside html-list rather than index.html file 
			
			random_dependency = RNG.choice(onion_files)
			onion_dependency = onion_webpage +'/'+ random_dependency 
			success, dependency_output = page_load_raw(onion_dependency) 
			alpaca_padding = ALPACA_PADDING_FLAG.findall(str(dependency_output))
			if (not success) or (not alpaca_padding): 
				print("-------- Couldn't fetch %s" % onion_dependency) 
			page_size = PAGE_SIZE.findall(str(dependency_output))
			page_size = [int(i) for i in page_size]
			onion_page_size = int(page_size[0])

			dependencies = DEPENDENCIES.findall(str(dependency_output))
			number_of_dependencies = [str(i) for i in dependencies] 
			total_dependencies = int("".join(number_of_dependencies)) 
			total_size = sum(page_size)
			obj_size= (total_size-onion_page_size)

			yield onion_webpage, onion_dependency, onion_page_size, total_dependencies, total_size, obj_size, page_size

# Extract specific features from wget command
def features_extractor_cached(onion_webpage,onion_files,n_requests): 

	n_requests=int((n_requests*50)*1000) # convert to integer
	
	for i in range(n_requests):
		if RNG.choice([True, False]): # Main index.html file

			success, output = page_load(onion_webpage)
			if not success:
				print("Couldn't fetch %s" % onion_webpage)
				return

			index = onion_webpage+"/index.html" # we need to HIT only the ".html" files that are available on the html-list "provided" file

			success, index_output = page_load(index)
			if not success:
				print("Couldn't fetch %s" % index)
				return
			page_size = PAGE_SIZE.findall(str(index_output))
			page_size = [int(i) for i in page_size] 
			index_page_size = int(page_size[0]) 

			dependencies = DEPENDENCIES.findall(str(index_output))
			number_of_dependencies = [str(i) for i in dependencies] 
			total_dependencies = int("".join(number_of_dependencies)) - 1  
			total_size = sum(page_size)
			obj_size= (total_size-index_page_size)

			yield onion_webpage, index, index_page_size, total_dependencies, total_size, obj_size, page_size
		
		else: # any other file contained inside html-list rather than index.html file 
			
			random_dependency = RNG.choice(onion_files)
			onion_dependency = onion_webpage +'/'+ random_dependency 
			success, dependency_output = page_load(onion_dependency) 
			if not success: # original
				print("!!!!!!!!!! Couldn't fetch %s" % onion_dependency)
			page_size = PAGE_SIZE.findall(str(dependency_output))
			page_size = [int(i) for i in page_size] 
			onion_page_size = int(page_size[0]) 

			dependencies = DEPENDENCIES.findall(str(dependency_output))
			number_of_dependencies = [str(i) for i in dependencies] 
			total_dependencies = int("".join(number_of_dependencies)) 
			total_size = sum(page_size)
			obj_size= (total_size-onion_page_size)

			yield onion_webpage, onion_dependency, onion_page_size, total_dependencies, total_size, obj_size, page_size


def page_requisites(url): 
	html_list = url+"/html-list" 
	response = urllib.request.urlopen(html_list).read().decode('UTF-8').splitlines() 
	length = len(response) 
	for i in range(length): 
		if response[i] == "index.html":
			response[i], response[0] = response[0], response[i]
	return url, response

def wget(args):
	try:
		return (True, check_output(["wget"] + args, stderr=subprocess.STDOUT))
	except subprocess.CalledProcessError as e:
		return (False, e.output)

#  wget command fired: wget <URL> --page-requisites --no-verbose -e 'robots=off' --no-cookie --no-dns-cache -4 --no-cache

@lru_cache(None) # LRU Cache enabled for other sites
def page_load(url):
	try:
		return wget([url, "--page-requisites", "--no-verbose", "-e", "robots=off", "--no-cookie", "--no-dns-cache", "-4", "--no-cache", "--content-on-error", "--delete-after"])
	except subprocess.CalledProcessError as e:
		return (False, e.output)

def page_load_raw(url): # No cache for chosen onion site.
	try:
		return wget([url, "--page-requisites", "--no-verbose", "-e", "robots=off", "--no-cookie", "--no-dns-cache", "-4", "--no-cache", "--content-on-error", "--delete-after"])
	except subprocess.CalledProcessError as e:
		return (False, e.output)

if __name__ == "__main__":
	main()