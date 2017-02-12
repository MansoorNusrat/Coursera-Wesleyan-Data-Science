# -*- coding: utf-8 -*-
"""
    coursera python coursework file
    
    @author: Mansoor Nusrat
"""

import pandas
import numpy

# Just some logging to show program has started (and is loading data ... takes
# a looooong time to load.
print("Loading source data...\n")
alldata = pandas.read_csv("nesarc_pds.csv", low_memory=False)

samplesize = len(alldata)

print("Sample size:{}".format(samplesize))

# dictionary that contains the variable distributions
countdata = {}

# dictionary that contains the reduced subsets of data which we are focusing on
subsets = {}

def add_count(variable, label):
    """
    function to create an entry in the countdata table for the given variable
    each entry has a title, a frequency, and a percentage (normalised 0..1)
    The function also returns the subset of the subjects that use the specified
    substance
    """
    
    pandas.to_numeric(alldata[variable]) # convert the value to numerical
    
    entry = {"title":label, 
             "frequency":alldata[variable].value_counts(sort=False,
                                                        dropna=True), 
             "percentage":alldata[variable].value_counts(sort=False, 
                                                         normalize=True,
                                                         dropna=True)
            }
    countdata[variable] = entry
      
    """
    make a copy of the subset of data where the subject has used the designated 
    substance
    """
    subsets[label] = alldata[(alldata[variable])==1].copy()
             


""" 
add counts for variables we are interested in, and make a subset of the data
for subjects that only use that substance
"""

add_count("S3BQ1A2", "Tranquilizer")
add_count("S3BQ1A3", "Opioids")
add_count("S3BQ1A7", "Hallucinogens")
add_count("S3BQ1A8", "Inhalants")
add_count("S3BQ1A9A", "Heroin")
add_count("S3BQ1A10A", "Other drug")
add_count("S3BQ1A5", "Cannabis")
add_count("S3BQ1A4", "Amphetamines")
add_count("S3BQ1A6", "Cocaine/crack")


def print_variable_distribution(variable, countentry):
    "Function to print out the variables distribution"
    
    print("Has ever used {}. 1=yes 2=no 9=n/a".format(countentry["title"]))
    print("Frequency\n{}".format(countentry["frequency"]))
    total=0
    for v in countentry["frequency"]:
        total += v
    print("Freqency total={}".format(total))
    print("Percentage\n{}".format(countentry["percentage"]))
    total=0
    for v in countentry["percentage"]:
        total += v
    print("Percentage total={}".format(total))
    print("\n") # insert a line between each variable

    

# print out all the variables we have collected counts for
for variable,distribution in countdata.items():
    print_variable_distribution(variable, distribution)
    


