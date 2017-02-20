# -*- coding: utf-8 -*-
"""
    coursera python coursework file
    
    @author: Mansoor Nusrat
"""

import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt

#Set PANDAS to show all columns in DataFrame
pandas.set_option('display.max_columns', None)
#Set PANDAS to show all rows in DataFrame
pandas.set_option('display.max_rows', None)

# bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format', lambda x:'%f'%x)


# Just some logging to show program has started (and is loading data ... takes
# a looooong time to load.
print("Loading source data...\n")
alldata = pandas.read_csv("nesarc_pds.csv", low_memory=False)

samplesize = len(alldata)

print("Sample size:%d" %samplesize)

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

WhenWentToDetoxKey = key_lookup["WhenWentToDetox"]["variable"]
WhenWentToOutpatientKey = key_lookup["WhenWentToOutpatient"]["variable"]
ManicAfterUseKey = key_lookup["ManicAfterUse"]["variable"]


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
                                   WhenWentToDetoxKey,
                                   WhenWentToOutpatientKey,
                                   ManicAfterUseKey
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


# recode ManicAfterUse so that response of 0 indicates No, and 1 indicates yes
HasEverUsedData[ManicAfterUseKey] = HasEverUsedData[ManicAfterUseKey].replace(2, 0)

seaborn.countplot(x=ManicAfterUseKey, data=HasEverUsedData)
plt.xlabel("Was manic after use")
plt.title("Experienced mania after drug use")


# want to just know if they had treatment in the last 12 months
HasEverUsedData[WhenWentToDetoxKey] = HasEverUsedData[WhenWentToDetoxKey].replace(3, 1)
HasEverUsedData[WhenWentToOutpatientKey] = HasEverUsedData[WhenWentToOutpatientKey].replace(3, 1) 

# Collapse outpatient and detox recovery into one variable:HasHadTreatment
def has_had_treatment(row):
    if row[WhenWentToDetoxKey]==1:
        return 1
    if row[WhenWentToOutpatientKey]==1:
        return 1
    return 0

HasEverUsedData["HasHadTreatment"] = HasEverUsedData.apply(lambda row: has_had_treatment(row), axis=1)

# Turn it into a categorical variable
HasEverUsedData["HasHadTreatment"] = HasEverUsedData["HasHadTreatment"].astype("category")
HasEverUsedData["HasHadTreatment"] = HasEverUsedData["HasHadTreatment"].cat.rename_categories(["no", "yes"])

# distribution plot of the the variable "HasHadTreatment"
seaborn.countplot(x="HasHadTreatment", data=HasEverUsedData)
plt.xlabel("Has had treatment")
plt.title("Has had any treatment in the last 12 months")


description = HasEverUsedData["HasHadTreatment"].describe()
print(description)

# use the group by method to get variable distribution (instead of value_counts)
frequency = HasEverUsedData.groupby("HasHadTreatment").size()
percentage = (frequency / len(HasEverUsedData)) * 100

print(frequency)
print(percentage)             


seaborn.factorplot(x="HasHadTreatment",
                   y=ManicAfterUseKey,
                   data=HasEverUsedData,
                   kind="bar",
                   ci=None)

plt.xlabel("Has had treatment in last 12 months")
plt.ylabel("Was manic after drug use")

