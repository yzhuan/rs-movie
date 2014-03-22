rs-movie
========

recommender system for movie; data sources: MovieLens

Need:
	numpy
	scipy
Infomation:
	do_experiment.py: the entry of this program
	rslib: the library for calculating
Example:
	$ cd Recommender System
	$ python
	>>> import do_experiment as test
	
	# start for calculating
	# you can change the parameters in do_experiment.py
	# like options, M, seed
	>>> test.Start()
	# waiting for few minutes
	# it will create a folder yyyymmdd-hhtt
	# then create several folder for cross validation
	# then create a result.txt for recording(MAE,time,options)
	
	
	# start for user recommend
	>>> test.GetRecommend()
