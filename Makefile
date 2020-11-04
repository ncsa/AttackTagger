all: test

test:
	nosetests -s tests.test_split_training_testing:test_split_training_testing

dev:
	ipython notebook --pylab=inline	&

test_eval:
	nosetests -s tests.test_all:test_eval_detection_timeliness

test_factg:
	nosetests -s tests.test_all:test_factg

test_factg_all:
	nosetests -s tests.test_all:test_factg_all

plot:
	nosetests -s tests.test_plot:test_plot_from_result

test_datasets:
	nosetests -s tests.test_datasets

perceptron:
	nosetests -s tests/test_structured_perceptron.py

test_powergrid:
	nosetests -s tests.test_all:test_eval_powergrid

test_variation:
	nosetests -s tests.test_all:test_attack_variation

test_nb:
	nosetests -s tests.test_nb:test_nb_main


test_stats:
	nosetests -s tests.test_stats:test_stats
