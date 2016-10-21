import pandas as pd
from lxml import objectify
from sklearn.preprocessing import Imputer
import math
import numpy as np



#functions for preprocessing data

#replace function, replace old value with new value
def replace(dataframe, old_value, new_value,line=-1):
    if line >-1:
        dataframe[line] = dataframe[line].replace(old_value,new_value)
    elif len(dataframe) > 1:
        for i in range(0, len(dataframe)):
            dataframe[i] = dataframe[i].replace(old_value, new_value)
    else:
        dataframe = dataframe.replace(old_value,new_value)

    return dataframe

#deletes a line from a dataframe
def del_line(dataframe, line):
    del(dataframe[line])
    return dataframe


#converts a read file to a dataframe
def convert_df(file, row_sep, line_sep="\n", columns=None):
    #splits the file into lines
    file = file.split(line_sep)
    start = 0

    if columns == None:
        columns = file[0].split(row_sep)
        start = 1

    data = list()
    #split the lines into row_variables
    for i in range(start,len(file)):
        data.append(file[i].split(row_sep))
    dataframe = pd.DataFrame(data, columns=columns)

    del(file,data)
    return dataframe

#converts a xml file to a pandas dataframe
def xml_to_df(xml_file, columns=None):
    if columns == None:
        return "Specify columns for the dataframe"
    xml = objectify.parse(xml_file)
    root = xml.getroot()
    df = pd.DataFrame(columns=columns)
    column_number = len(columns)
    root_number = len(root.getchildren())

    for i in range(0,root_number):
        obj = root.getchildren()[i].getchildren()
        texts = []
        for i in range(0,len(obj)):
            texts.append(obj[i].text)
        row = dict(zip(columns,texts))
        series = pd.Series(row)
        series.name = i
        df = df.append(series)

    return df

#deletes duplicates in a dataframe
def del_dublicates(dataframe):
    dataframe.drop_duplicates()
    return dataframe

#group by function to get a better description of the dataset
#via reduction you can print the dataframe with only the selected variables
def group_desc(dataframe,groupby,loc=None, unstacked=False):
    group_desc = dataframe.groupby(groupby).describe()
    if unstacked:
        group_desc = group_desc.unstack()
    if loc:
        group_desc = group_desc.loc[:,(slice(None),loc),]
    return group_desc




#function for missing variables in a dataframe
#only rows means that we only get the single rows where values are missing
def missing_values_df(dataframe,only_rows=False):
    if only_rows:
        return dataframe[dataframe.isnull()]
    else:
        return dataframe.isnull()


def missing_values_column(dataframe, column,only_rows=False):
    if only_rows:
        return dataframe[column][dataframe[column].isnull()]
    else:
        return dataframe[column].isnull()

#function for droping rows with missing
def drop_na(dataframe):
    dataframe = dataframe.dropna()
    return dataframe

#function for deleting columns
def del_columns(dataframe, column):
    del(dataframe[column])
    return dataframe


#imputer function for filling missing values
def impute(dataframe, strategy,axis=0,columns=None):
    if columns and "list"  in str(type(columns)):
        for column in columns:
            dataframe[column] = pd.to_numeric(dataframe[column])
            training_list = []
            for number in dataframe[column]:
                if math.isnan(number) == False:
                    training_list.append(number)
            mean = np.mean(training_list)
            for i in range(0, len(dataframe[column]) - len(training_list)):
                training_list.append(mean)

            #init imputer object and train it
            imp = Imputer(missing_values="NaN",strategy=strategy,axis=axis)
            imp.fit(training_list)
            #transform the column
            new_series = pd.Series(imp.transform(dataframe[column]).tolist()[0])
            dataframe[column] = new_series


        return dataframe

    else:
        if columns:
            series = dataframe[columns]
        else:
            series = dataframe
        series = pd.to_numeric(series)
        training_list = []

        for number in series:
            if math.isnan(number) == False:
                training_list.append(number)
        mean = np.mean(training_list)
        for i in range(0,len(series)-len(training_list)):
            training_list.append(mean)

        #init imputer and train it
        imp = Imputer(missing_values="NaN",strategy=strategy,axis=axis)
        imp.fit(training_list)

        #create new series with transformed data
        new_series = pd.Series(imp.transform(series).tolist()[0])

        if columns:
            dataframe[columns] = new_series
            return dataframe
        else:
            return new_series













