


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





