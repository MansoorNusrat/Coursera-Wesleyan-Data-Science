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

# aliases for the variable names, so they are easier to identify
key_lookup = {
    "WhenWentToDetox":{
            "variable":"S3DQ2B3",
            "description":"When went to drug/alcohol detox ward/clinic\n"
                          "1 = during last 12 months\n"
                          "2 = before last 12 months\n"
                          "3 = 1 & 2\n"
                          "nan = no data or didn't go at all"
            },
    "WhenWentToOutpatient":{
            "variable":"S3DQ2B5",
            "description":"When went to outpatient clinic (including outpatient program\n"
                          "1 = during last 12 months\n"
                          "2 = before last 12 months\n"
                          "3 = 1 & 2\n"
                          "nan = no data or didn't go at all"
            },            
    "ManicAfterUse":{
            "variable":"S5Q16GR",
            "description":"Continued to feel manic for 1+ months after stop drinking/drug use...\n"
                          "1 = yes\n"
                          "2 = no\n"
                          "nan = no data or n/a"
            }
    }


"""
    A dictionary which associates easy to recognize keys with variable names
    for a given substance
"""
substance_variable_lookup = {
        "Tranquilizer":{
                    "HaveEverUsed":"S3BQ1A2",
                    "UsedInPrev24Months":"S3BD2Q2B"
                },
        "Opioids":{
                    "HaveEverUsed":"S3BQ1A3",
                    "UsedInPrev24Months":"S3BD3Q2B"
                },
        "Amphetamines":{
                    "HaveEverUsed":"S3BQ1A4",
                    "UsedInPrev24Months":"S3BD4Q2B"
                },
        "Cannabis":{
                    "HaveEverUsed":"S3BQ1A5",
                    "UsedInPrev24Months":"S3BD5Q2B"
                },
        "Cocaine/crack":{
                    "HaveEverUsed":"S3BQ1A6",
                    "UsedInPrev24Months":"S3BD6Q2B"
                },
        "Hallucinogens":{
                    "HaveEverUsed":"S3BQ1A7",
                    "UsedInPrev24Months":"S3BD7Q2B"
                },
        "Inhalants":{
                    "HaveEverUsed":"S3BQ1A8",
                    "UsedInPrev24Months":"S3BD8Q2B"
                },
        "Heroin":{
                    "HaveEverUsed":"S3BQ1A9A",
                    "UsedInPrev24Months":"S3BD9Q2B"
                },
        "Other":{
                    "HaveEverUsed":"S3BQ1A10A",
                    "UsedInPrev24Months":"S3BD10Q2B"
                }
        }


def convert_and_prune(variable):
    "converts variable to numeric and prunes unwanted response (of 9)"                                                                    
    #pandas.to_numeric(alldata[variable]) # convert the value to numerical

    #print("Converting and pruning %s" %variable)
    alldata[variable] = alldata[variable].convert_objects(convert_numeric=True)
    # convert response of 9 to invalid
    alldata[variable] = alldata[variable].replace(9, numpy.nan)
    

convert_and_prune(key_lookup["WhenWentToDetox"]["variable"])
convert_and_prune(key_lookup["WhenWentToOutpatient"]["variable"])
convert_and_prune(key_lookup["ManicAfterUse"]["variable"])


"""
make sure all the variable types we're interested have been sanitized
"""
for substance,keys in substance_variable_lookup.items():
    variable = keys["UsedInPrev24Months"]
    convert_and_prune(variable)

    
def has_used_any(row):
    """
    Function which determines if subject has used any substance in the last
    24 months
    1 = yes
    2 = no
    """
    for substance,keys in substance_variable_lookup.items():
        key = keys["UsedInPrev24Months"]
        value = row[key]
        if (numpy.isnan(value)==False):
            value = int(value)
            if (value>=1 & value<=3):
                return 1
        
    return 2


# Want to aggregate use of any substance into one variable
print("Creating a new variable 'HasEverUsed'\n")
alldata["HasEverUsed"] = alldata.apply(lambda row: has_used_any(row), axis=1)

"""
Want to create a new data frame which only includes subjects (rows) where
any substance has been used by the subject
"""
print("Creating reduced data frame (only includes subjects that have used any substance)\n")
HasEverUsedData = alldata[(alldata["HasEverUsed"]==1)]
print("Have reduced population size of %d\n" %len(HasEverUsedData))


"""
Want to reduce our variables to only include the ones we are interested in
"""
print("Creating reduced variable dataframe\n")
HasEverUsedData = HasEverUsedData[["IDNUM",
                                   key_lookup["WhenWentToDetox"]["variable"],
                                   key_lookup["WhenWentToOutpatient"]["variable"],
                                   key_lookup["ManicAfterUse"]["variable"]
                                 ]]

print("First 10 rows of new data frame:")
print(HasEverUsedData.head(n=10))

# show variable distributions for what we are interested in
print("\nVariable distributions:\n")
for variable,info in key_lookup.items():
    print("Variable '{}'\n{}".format(variable, info["description"]))
    counts = HasEverUsedData[info["variable"]].value_counts(
                sort=True,
                dropna=False)
    print("Frequency:\n{}".format(counts))
    counts = HasEverUsedData[info["variable"]].value_counts(
                sort=True,
                dropna=False,
                normalize=True)
    print("Percentages:\n{}\n".format(counts))
