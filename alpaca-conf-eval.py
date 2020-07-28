# -*- coding: utf-8 -*-

import sys, os, argparse, subprocess, random, datetime, csv

#########################################################################################################################################
############################################ Script Description. ########################################################################
#                                                                                                           		                #
# Provide: alpaca configuration file, type of classifier & user browsing profile (priors) 						#
# Based on provided alpaca configuration file-> change nginx configuration /etc/nginx/sites-available/default   		        #
# Restart nginx	web server										    		                #
# Run arachni to gather the website related features 				    		                			#
# Use obtained features (HTML & Object size) to train the ML classifiers							    	#
# Report the information leakage							    		                		#
#                           										    		                #
#########################################################################################################################################
#########################################################################################################################################

def main(): # Main function 
    
    parser = argparse.ArgumentParser(description=' . . : ALPaCA Settings Evaluation Program. Note: Do not forget to use sudo : . . ')
    parser.add_argument("-ac", 
                    required=True,
                    help="this is the alpaca configuration file, which settings we want to evaluate.")
    parser.add_argument("-cl", 
                    choices=["binary", "exact"],
                    required=True, 
                    help="type of classifier, binary or exact.")
    parser.add_argument("-r", 
                    required=True,
                    help="user browsing profiles (priors). Sample file: arachni/exact_priors_sample.csv")
    args = parser.parse_args()

    alpaca_conf_file = args.ac
    rule_case = args.cl
    onion_input_csv = args.r

    FNULL = open(os.devnull, 'w') #redirect output to /dev/null
    prob = extract_prob(onion_input_csv)

    dt = str(datetime.datetime.now())

    # for block in get_all_blocks('path/to/alpaca.conf'):
    for block in get_all_blocks(alpaca_conf_file):
        if (rule_case=="binary"):
                replace_in_file('nginx_template.conf', '/etc/nginx/sites-available/default', '<<ALPACA_BLOCK>>', block)
                subprocess.run("sudo /etc/init.d/nginx restart", shell=True, check=True)
                print ("## Arachni started crawling.. ## ")
                subprocess.run(["./wf/bin/python3", "arachni/arachni-hybrid-alpaca.py","--csv",onion_input_csv], check=True)
                subprocess.run(["cut", "-d," , "-f" , "1,3,6", "alpaca-latest-50k-features.csv"], stdout=FNULL, check=True)
                print ("## RF Classifier.. ## ")
                with open('binary-rf-accuracy.txt', 'w') as fp:
                    subprocess.Popen(["echo", '\n . .:Binary Rule - htmlSize & objSize Features:. . \n'], stdout=fp)
                    subprocess.Popen(["echo","## Current alpaca configuration ## \n\n", block , "\n\n## Accuracy report ##\n"], stdout=fp)
                    subprocess.run(["./wf/bin/python3","wf-classifier/binary/rf-binary-classifier.py","--train", "alpaca-latest-50k-features.csv"], stdout=fp, check=True)
                accuracy = extract_accuracy('binary-rf-accuracy.txt')
                append_to_results(alpaca_conf_file, rule_case, onion_input_csv, prob, accuracy)
        elif (rule_case=="exact"):
                replace_in_file('nginx_template.conf', '/etc/nginx/sites-available/default', '<<ALPACA_BLOCK>>', block)
                subprocess.run("sudo /etc/init.d/nginx restart", shell=True, check=True)
                print ("## Arachni started crawling.. ## ")
                subprocess.run(["./wf/bin/python3", "arachni/arachni-hybrid-alpaca.py","--csv",onion_input_csv], check=True)
                subprocess.run(["cut", "-d," , "-f" , "1,3,6", "alpaca-latest-50k-features.csv"], stdout=FNULL, check=True)
                print ("## RF Classifier.. ## ")
                with open('exact-rf-accuracy.txt', 'w') as fp:
                    subprocess.Popen(["echo", '\n . .:Exact Rule - htmlSize & objSize Features:. . \n'], stdout=fp)
                    subprocess.Popen(["echo","## Current alpaca configuration ## \n\n", block , "\n\n## Accuracy report ##\n"], stdout=fp)
                    subprocess.run(["./wf/bin/python3","wf-classifier/exact/rf-exact-classifier.py","--train", "alpaca-latest-50k-features.csv"], stdout=fp, check=True)
                accuracy = extract_accuracy('exact-rf-accuracy.txt')
                append_to_results(alpaca_conf_file, rule_case, onion_input_csv, prob, accuracy)
    os.system("rm -rf *.onion")  #clear downloaded .onion dirs & files
    

def extract_accuracy(filepath):
    with open(filepath) as accuracy_file:
        for l in accuracy_file:
            parts = [p.strip() for p in l.split()]
            if len(parts) > 0 and parts[0] == 'accuracy' :
                return float(parts[1])

def extract_prob(onions):
    with open(onions) as onions_file:
        onions_csv = csv.reader(onions_file, delimiter=',')
        for row in onions_csv:
            if row[0] == 'http://ynvs3km32u33agwq.onion':
                return float(row[1])


# the following function returns a list with all the blocks 
def get_all_blocks(path_to_aplaca_conf):
    blocks = []
    block_bounds = {
            ('alpaca_deter ', 'alpaca_max_obj_size '),
            ('alpaca_prob ', 'alpaca_dist_obj_size '),
            ('alpaca_prob off', 'alpaca_deter off'),
    }

    with open(path_to_aplaca_conf) as alpaca_conf:
        block_lines = []
        cur_block_end = None
        for line in alpaca_conf.read().splitlines():
            if cur_block_end is None:
                # not in a block, check if a block is starting
                for block_begin, block_end in block_bounds:
                    if line.startswith(block_begin):
                        cur_block_end = block_end
                        block_lines.append(line)
                        break
            else:
                # in a block
                block_lines.append(line)

                if line.startswith(cur_block_end):
                    cur_block_end = None
                    blocks.append('\n'.join(block_lines))
                    block_lines = []
    return blocks

def append_to_results(alpaca_conf_file, rule, onions, prob, accuracy):
    with open('results.csv', 'a') as results_file:
        w = csv.writer(results_file)
        
        prior_vuln = prob if rule == 'exact' else 1.0 - prob
        leakage = accuracy / prior_vuln
        w.writerow([alpaca_conf_file, rule, onions, leakage])


def replace_in_file(in_file_path, out_file_path, replace_what, replace_with):
    with open(in_file_path) as in_file:
        with open(out_file_path, 'w') as out_file:
            out_file.write(in_file.read().replace(replace_what, replace_with))

if __name__ == "__main__":
	main()
