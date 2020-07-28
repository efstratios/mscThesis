# Self-Defense Against Website Fingerprinting Using ALPaCA

# Project structure:

```
|--alpaca_config/		# Contains alpaca configurations, priors, distributions, plots & experimental results
|--arachni/			# Web crawler & datasets per exact/binary classification problem
|--self-defense-onions/		# Static .onion sites 
|--wf-classifier/		# ML classifiers
|--alpaca-conf-eval.py          # ALPaCA settings evaluation program 
|--nginx_template.conf          # Template nginx configuration file
|--README.md			# Readme file
|--requirements.txt             # Virtual environment requirements 
|--run-experiments.sh		# Bash script to run experiments for 100 priors (do not forget to use sudo & modify filepaths at p-alpaca configurations)
```

## How to run:

General program usage: `alpaca-conf-eval.py [-h] -ac AC -cl {binary,exact} -r R` 
	
```
  -h, --help            show this help message and exit
  -ac AC                this is the alpaca configuration file, which settings we want to evaluate.
  -cl {binary,exact}    type of classifier, binary or exact.
  -r R                  input onion CSV file containing the onion URLs & browsing percentage per onion site i.e. the number of times that
                        arachni will crawl & generate the selected features per onion site. Sample file: onion_exact_example.csv
```
&nbsp;    
  
Example of a run for the `exact` classifier, generation of a dataset with the selected features, based upon [exact_priors_sample.csv](https://github.com/efstratios/eskleparis_MSc_Thesis/blob/master/arachni/exact_priors_sample.csv) priors

	`sudo wf/bin/python alpaca-conf-eval.py -ac <alpaca.conf> -cl exact -r arachni/exact_priors_sample.csv`
