import pandas as pd
import sklearn
import seaborn as sns

import processData

JOB_POSTINGS_PATH = 'RawDataFiles/job_postings.csv'


def load_data(path):
    try:
        with open(path, "r") as f:
            data = pd.read_csv(path)
            return data
    except IOError:
        print('file does not exist')


# do what you want if there is an error with the file opening

if __name__ == '__main__':
    job_postings_df = load_data(JOB_POSTINGS_PATH)
    job_postings_df = processData.drop_columns(job_postings_df)
    job_postings_df = processData.alter_columns(job_postings_df)
    job_postings_df = processData.convert_to_monthly_pay(job_postings_df)
    job_postings_df = processData.drop_pay_columns(job_postings_df)
    job_postings_df = processData.get_job_location(job_postings_df)
    print(job_postings_df)
