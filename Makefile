TSTS=\
		test_Reference.py\
		test_Substance.py\
		test_Principle.py\
		test_Chronicle.py\
		test_Transduce.py\
		test_Visualize.py
SRCS=$(patsubst test_,,$(TSTS))

all:	$(TSTS) $(SRCS) Makefile
	@python3 -m unittest

#	@python3 test_Reference.py
#	@echo version | ./Reference.py | ./void

