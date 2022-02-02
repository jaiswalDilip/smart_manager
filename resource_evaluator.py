# -*- coding: utf-8 -*-
"""resource_evaluator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vDdzMLlP61_w7Sz19DQiRB2pM908UEBw

# || Import Library ||
"""

import glob
import random
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

"""# || Supporting Methods ||"""

def get_utilization_result(current_row):
    try:
        if current_row.between(90, 100).all():
            return 1
        elif current_row.between(1, 49).all():
            return -1
        else:
            return 0
    except:
        return random.choice([1, -1, 0])

new_cols = ["Iteration%s" % x for x in range(1,21)]
def generate_input_file(smart_manager_path):
    all_files = glob.glob(os.path.join(smart_manager_path, "sample-data/*.csv"))
    final_file = os.path.join(smart_manager_path, "sample-data/sample_input.csv")
    all_files = [x for x in all_files if x != final_file]
    new_df = pd.DataFrame(columns=new_cols)
    for each_file_path in all_files:
        df = pd.read_csv(each_file_path)
        for each_col in list(df.columns)[1:]:
            tmp_df = pd.DataFrame(df[each_col].values.reshape(-1, 20), columns=new_cols)
            new_df = pd.concat([new_df, tmp_df])
    range_dict = [(90, 101, 1500), (50, 90, 1003), (1, 50, 1200), (35, 65, 900), (75, 99, 1700), (0, 110, 937)]
    for i_ in range(len(range_dict)):
        lower_limit, upper_limit, no_of_records = range_dict[i_]
        tmp_df = pd.DataFrame(np.random.randint(lower_limit, upper_limit, size=(no_of_records, 20)), columns=new_cols)
        new_df = pd.concat([new_df, tmp_df])
        mixed_choice = list(range(lower_limit, upper_limit)) + list("GAR_B AGE") + [None, " "]
        tmp_df2 = pd.DataFrame(np.random.choice(mixed_choice, size=(300, 20)), columns=new_cols)
        new_df = pd.concat([new_df, tmp_df2])
    new_df = new_df.sample(frac=1)
    new_df['utilisation'] = new_df.apply(lambda row: get_utilization_result(row), axis=1)
    new_df.to_csv(final_file, index=False)
    print("Writing Completed")

# generate_input_file(smart_manager_path="/content/drive/MyDrive/smart_manager")

"""# || Analyzing Data || Read the Exported CSV file ||"""

final_file = '/content/drive/MyDrive/smart_manager/sample-data/sample_input.csv'
df = pd.read_csv(final_file)
df

"""# || Data Wrangling is to remove null or [ _ ] or empty data, cleaning data set ||"""

df.info()

print("Before Cleanups")
df.isnull().sum()

"""# || DROP Rows containing SPACE, EMPTY-STRINGS, UNDERSCORE, GARBAGE-CHARACTERS ||

### UNDERSCORE DROPS
"""

old = int(df.shape[0])
print("Rows Before UNDERSCORE Drops: %s" % df.shape[0])
for each_col in new_cols:
    df = df[df[each_col] != "_"]
print("Rows After UNDERSCORE Drops: %s" % df.shape[0])
print("Total Rows Dropped with UNDERSCORE: %s" % int(old - df.shape[0]))

"""### SPACE DROPS"""

old = int(df.shape[0])
print("Rows Before SPACE Drops: %s" % df.shape[0])
for each_col in new_cols:
    df = df[df[each_col] != " "]
print("Rows After SPACE Drops: %s" % df.shape[0])
print("Total Rows Dropped with SPACE: %s" % int(old - df.shape[0]))

"""### NaN DROPS"""

print("Dropping NaN")
df[pd.isnull(df).any(axis=1)]

old = int(df.shape[0])
print("Rows Before NaN Drops: %s" % df.shape[0])
df.dropna(subset=new_cols, axis=0, inplace=True)
print("Rows After NaN Drops: %s" % df.shape[0])
print("Total Rows Dropped with NaN: %s" % int(old - df.shape[0]))

print("After NA Drops")
df.isnull().sum()

"""### DUPLICATE DROPS"""

old = int(df.shape[0])
print("Rows Before DUPLICATE Drops: %s" % df.shape[0])
df = df.drop_duplicates(subset=new_cols)
print("Rows After DUPLICATE Drops: %s" % df.shape[0])
print("Total DUPLICATE Rows Dropped : %s" % int(old - df.shape[0]))

"""### GARBAGE CHARACTER DROPS"""

old = int(df.shape[0])
print("Rows Before CHARACTER Drops: %s" % df.shape[0])
for each_col in new_cols:
    df = df[df[each_col].apply(lambda x: str(x).replace(".", "", 1).isdigit())]
print("Rows After CHARACTER Drops: %s" % df.shape[0])
print("Total Rows Dropped with CHARACTER: %s" % int(old - df.shape[0]))

"""# || Convert Whole Data to Numerics ||"""

df = df.apply(pd.to_numeric, errors='raise')

"""# || Filter invalid Data of percentage more than 100% ||"""

old = int(df.shape[0])
print("Rows Before INVALID Drops: %s" % df.shape[0])
for each_col in new_cols:
    df = df[df[each_col].apply(lambda x: x <= 100)]
print("Rows After INVALID Drops: %s" % df.shape[0])
print("Total Rows Dropped with INVALID: %s" % int(old - df.shape[0]))

"""# ||Train and Test ||

### Divide appropriate Columns
"""

df.head(5)

X = df.drop("utilisation", axis=1)
y = df["utilisation"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)

"""### MODEL FITTINGS"""

logmodel = LogisticRegression(max_iter=6000)
logmodel.fit(X_train, y_train)

predictions = logmodel.predict(X_test)

print(classification_report(y_test, predictions))

confusion_matrix(y_test, predictions)

"""# || Accuracy CHECK ||"""

from sklearn.metrics import accuracy_score
accuracy_score(y_test, predictions)



