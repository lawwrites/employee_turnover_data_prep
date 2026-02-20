#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import the libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import datetime
from scipy import stats


# In[408]:


#load the csv files
edt = pd.read_csv('/Users/lawhea1214/Documents/WGU/599_Data/task1/data/Employee Turnover Dataset.csv')


# In[287]:


#verify the data loaded correctly
edt.head()


# In[289]:


#explore the columns, nulls, and dtypes
edt.info()


# In[291]:


#obtain the shape of the data
edt.shape


# In[293]:


#explore the dataframes mean, count, standard deviation, and quartiles
edt.describe()


# In[295]:


#check for duplicates
edt.duplicated().sum()


# In[297]:


#drop duplicates
edt.drop_duplicates(inplace=True)


# In[299]:


#verify all duplicates dropped
edt.duplicated().any()


# In[301]:


#remove trailing white spaces from the column names. 
edt.columns = edt.columns.str.strip()


# In[303]:


#verify white spaces removed
edt.columns


# In[305]:


#remove the trailing white spaces from the data rows
for col in edt.columns:
    if edt[col].dtype == "object":
        edt[col] = edt[col].str.strip()
        


# In[307]:


#convert the HourlyRate and HoursWeekly columns to floats and integers
columns = ["HourlyRate", "HoursWeekly"]

for col in columns:
    if edt[col].dtype == "object":
        edt[col] =edt[col].str.replace("$","", regex=False).str.strip()
        edt[col] = edt[col].astype("float")


# In[309]:


#verify HourlyRate and HoursWeekly are floats and integers
edt.info()


# In[311]:


#checking for nan values
edt.isna().any()


# In[313]:


#checking for the unique values in each column
edt.nunique()


# In[357]:


#printing out each column to explore the unique values for inconsistencies
print('Job Role')
print(edt['JobRoleArea'].value_counts())
print()
print('Gender')
print(edt['Gender'].value_counts())
print()
print('Marital Status')
print(edt['MaritalStatus'].value_counts())
print()
print('Paycheck Method')
print(edt['PaycheckMethod'].value_counts())


# In[369]:


edt['PaycheckMethod'].unique()


# In[377]:


df_col = edt['PaycheckMethod']
cor_col = 'PaycheckMethod'
lst = ['Mail Check',
       'Direct Deposit']
val = "Direct Deposit"
inconsistencies(edt, df_col, cor_col,lst,val)


# In[379]:


def inconsistencies(df, df_col, col, lst, val):
    for idx, row in df_col.items():
        if row not in lst:
            df.at[idx, col] = val


# In[381]:


print(edt['PaycheckMethod'].value_counts())
print()
print(edt['JobRoleArea'].value_counts())


# In[383]:


#check for null values
edt.isnull().sum()


# In[385]:


#calculate the mean values for the numeric columns with null values
edt_mean = edt[["NumCompaniesPreviouslyWorked","AnnualProfessionalDevHrs"]].mean(numeric_only=True)
edt_mean


# In[387]:


#replace the null values with the mean data for the columns
edt["NumCompaniesPreviouslyWorked"] = edt["NumCompaniesPreviouslyWorked"].fillna(edt_mean.iloc[0])
edt["AnnualProfessionalDevHrs"] = edt["AnnualProfessionalDevHrs"].fillna(edt_mean.iloc[1])


# In[389]:


#check for null values
edt.isnull().sum()


# In[391]:


#use IQR to eliminate outliers and inconsistent data from the DrivingCommuterDistance column
dcd_q1 = edt["DrivingCommuterDistance"].quantile(.25)
dcd_q3 = edt["DrivingCommuterDistance"].quantile(.75)
upper_bound = dcd_q3 + (dcd_q3*1.5)
lower_bound = (dcd_q1*1.5) - dcd_q1

edt["DrivingCommuterDistance"] = edt["DrivingCommuterDistance"].where(
 (edt["DrivingCommuterDistance"] >= lower_bound) & (edt["DrivingCommuterDistance"] <= upper_bound), np.nan
)


# In[393]:


#verify it worked
edt["DrivingCommuterDistance"].describe()


# In[395]:


#use IQR to eliminate outliers and inconsistent data from the AnnualSalary column
as_q1 = edt["AnnualSalary"].quantile(.25)
as_q3 = edt["AnnualSalary"].quantile(.75)
ub = as_q3 + (as_q3*1.5)
lb = (as_q1*1.5) - as_q1

edt["AnnualSalary"] = edt["AnnualSalary"].where(
    (edt["AnnualSalary"] >= lb) & (edt["AnnualSalary"] <= ub), np.nan
)


# In[397]:


#verify it worked
edt["AnnualSalary"].describe()


# In[399]:


#calculate the mean values for the numeric columns with null values
edt_mean2 = edt[["DrivingCommuterDistance","AnnualSalary"]].mean(numeric_only=True)
edt_mean2


# In[401]:


edt["AnnualSalary"] = edt["AnnualSalary"].fillna(edt_mean2.iloc[1])
edt["DrivingCommuterDistance"] = edt["DrivingCommuterDistance"].fillna(edt_mean2.iloc[0])


# In[403]:


edt.isnull().any()


# In[405]:


#create the filepath to save the cleaned data
today = datetime.date.today()
file_path = "/Users/lawhea1214/Documents/WGU/599_Data/task1/data"
file_name = "cleaned-employee-turnover-dataset"
version = "v2"
file_type = "csv"
full_path = f"{file_name}_{today}_{version}.{file_type}"
create_path = os.path.join(file_path, full_path)
try:
    os.makedirs(file_path, exist_ok=True)
    edt.to_csv(create_path)
    print(f"{file_name} successfully saved")
except Exception as e:
    print("File failed to create:", e)

