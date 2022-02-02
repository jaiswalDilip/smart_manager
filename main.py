import glob
import random
import pandas as pd
import numpy as np
import os

new_cols = ["Iteration%s" % x for x in range(1,21)]


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


def filter_all(df):
    print("Before Cleanups")
    print(df.isnull().sum())
    # ====================
    old = int(df.shape[0])
    print("Rows Before UNDERSCORE Drops: %s" % df.shape[0])
    for each_col in new_cols:
        df = df[df[each_col] != "_"]
    print("Rows After UNDERSCORE Drops: %s" % df.shape[0])
    print("Total Rows Dropped with UNDERSCORE: %s" % int(old - df.shape[0]))
    # ====================
    old = int(df.shape[0])
    print("Rows Before SPACE Drops: %s" % df.shape[0])
    for each_col in new_cols:
        df = df[df[each_col] != " "]
    print("Rows After SPACE Drops: %s" % df.shape[0])
    print("Total Rows Dropped with SPACE: %s" % int(old - df.shape[0]))
    # ====================
    old = int(df.shape[0])
    print("Rows Before NaN Drops: %s" % df.shape[0])
    df.dropna(subset=new_cols, axis=0, inplace=True)
    print("Rows After NaN Drops: %s" % df.shape[0])
    print("Total Rows Dropped with NaN: %s" % int(old - df.shape[0]))
    # ====================
    old = int(df.shape[0])
    print("Rows Before DUPLICATE Drops: %s" % df.shape[0])
    df = df.drop_duplicates(subset=new_cols)
    print("Rows After DUPLICATE Drops: %s" % df.shape[0])
    print("Total DUPLICATE Rows Dropped : %s" % int(old - df.shape[0]))
    # ====================
    old = int(df.shape[0])
    print("Rows Before CHARACTER Drops: %s" % df.shape[0])
    for each_col in new_cols:
        df = df[df[each_col].apply(lambda x: str(x).replace(".", "", 1).isdigit())]
    print("Rows After CHARACTER Drops: %s" % df.shape[0])
    print("Total Rows Dropped with CHARACTER: %s" % int(old - df.shape[0]))


def generate_input_file(smart_manager_path):
    all_files = glob.glob(os.path.join(smart_manager_path, "sample-data/*.csv"))
    final_file = os.path.join(smart_manager_path, "sample-data/sample_input.csv")
    all_files = [x for x in all_files if x != final_file]
    new_df = pd.DataFrame(columns=new_cols, dtype=int)
    print(new_cols)
    for each_file_path in all_files:
        df = pd.read_csv(each_file_path)
        # print(df.columns)
        for each_col in list(df.columns)[1:]:
            tmp_df = pd.DataFrame(df[each_col].values.reshape(-1, 20), columns=new_cols)
            new_df = pd.concat([new_df, tmp_df])
    range_dict = [(90, 101, 1500), (50, 90, 1003), (1, 50, 1200), (35, 65, 900), (75, 99, 1700), (95, 110, 1000)]
    # for i_ in range(len(range_dict)):
    #     lower_limit, upper_limit, no_of_records = range_dict[i_]
    #     tmp_df = pd.DataFrame(np.random.randint(lower_limit, upper_limit, size=(no_of_records, 20)), columns=new_cols)
    #     new_df = pd.concat([new_df, tmp_df])
    #     mixed_choice = list(range(lower_limit, upper_limit)) + list("GAR_B AGE") + [None, " "]
    #     tmp_df2 = pd.DataFrame(np.random.choice(mixed_choice, size=(300, 20)), columns=new_cols)
    #     new_df = pd.concat([new_df, tmp_df2])
    new_df = new_df.sample(frac=1)
    new_df['utilisation'] = new_df.apply(lambda row: get_utilization_result(row), axis=1)
    new_df.to_csv(final_file, index=False)
    filter_all(new_df)
    print("Writing Completed")


# generate_input_file(smart_manager_path="/content/drive/MyDrive/smart_manager")
generate_input_file(smart_manager_path=r"/Users/jaiswald/OneDrive - VMware, Inc/Acer Laptop Backup/Docx/Personal Documents/Educational/M-Tech/Materials/Sem-IV/smart_manager")
