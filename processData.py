import math
import statesList
import pandas as pd


def get_job_location(job_postings_df):
    # print(job_postings_df['location'])
    job_postings_df['location'] = [x[-2:] if x != 'United States' else 'GN' for x in job_postings_df['location']]
    job_postings_df['location'] = [statesList.STATES.get(x) for x in job_postings_df['location']]
    job_postings_df = job_postings_df.join(pd.get_dummies(job_postings_df.location, dtype=int)).drop(
        ['location'],
        axis=1)
    return job_postings_df


def drop_columns(job_postings_df):
    # print(job_postings_df)
    job_postings_df = job_postings_df.drop(
        ['compensation_type', 'title', 'description', 'job_posting_url', 'application_url', 'application_type',
         'currency', 'sponsored', 'posting_domain', 'listed_time', 'skills_desc', 'closed_time', 'expiry', 'views',
         'original_listed_time', 'applies', 'scraped', 'formatted_work_type'], axis=1)
    return job_postings_df


def alter_columns(job_postings_df):
    # print(job_postings_df)
    # print(job_postings_df[job_postings_df['company_id'].isnull()])

    # job_postings_df['company_id'] = [0 if pd.isna(x) else int(x) for x in job_postings_df['company_id']]
    # print(job_postings_df[job_postings_df['company_id'].isnull()])
    job_postings_df = job_postings_df.join(pd.get_dummies(job_postings_df.formatted_experience_level, dtype=int)).drop(
        ['formatted_experience_level'],
        axis=1)
    job_postings_df = job_postings_df.join(pd.get_dummies(job_postings_df.work_type, dtype=int)).drop(
        ['work_type'],
        axis=1)
    job_postings_df = job_postings_df.join(pd.get_dummies(job_postings_df.pay_period, dtype=int)).drop(
        ['pay_period'],
        axis=1)
    job_postings_df['min_salary'] = [0 if math.isnan(x) else x for x in job_postings_df['min_salary']]
    job_postings_df['med_salary'] = [0 if math.isnan(x) else x for x in job_postings_df['med_salary']]
    job_postings_df['max_salary'] = [0 if math.isnan(x) else x for x in job_postings_df['max_salary']]
    job_postings_df['remote_allowed'] = [0 if math.isnan(x) else 1 for x in job_postings_df['remote_allowed']]
    job_postings_df = job_postings_df[
        (job_postings_df['max_salary'] > 0) | (job_postings_df['min_salary'] > 0) | (job_postings_df['med_salary'] > 0)]

    return job_postings_df


def calculate_median_salary(row):
    if row['med_salary'] != 0:
        return row['med_salary']
    else:
        return (row['min_salary'] + row['max_salary']) / 2


def convert_hourly_to_monthly(hourly_rate, work_hours_per_month=186):
    return hourly_rate * work_hours_per_month


def convert_yearly_to_monthly(yearly_rate):
    return yearly_rate / 12


def convert_weekly_to_monthly(weekly_rate, weeks_per_year=52):
    return (weekly_rate * weeks_per_year) / 12


def convert_to_monthly_pay(job_postings_df):
    # print(job_postings_df['ONCE'].value_counts())
    job_postings_df['med_salary'] = [row['med_salary'] if row['med_salary'] != 0 else calculate_median_salary(row) for
                                     _, row in job_postings_df.iterrows()]
    job_postings_df['mid_monthly_salary'] = [
        convert_hourly_to_monthly(row['med_salary']) if row['HOURLY'] == 1 and row['med_salary'] != 0
        else convert_yearly_to_monthly(row['med_salary']) if row['YEARLY'] == 1 and row['med_salary'] != 0
        else convert_weekly_to_monthly(row['med_salary']) if row['WEEKLY'] == 1 and row['med_salary'] != 0
        else row['med_salary']  # Default case
        for _, row in job_postings_df.iterrows()
    ]

    return job_postings_df


def drop_pay_columns(job_postings_df):
    # print(job_postings_df)
    job_postings_df = job_postings_df.drop(
        ['max_salary', 'med_salary', 'min_salary', 'HOURLY', 'WEEKLY', 'ONCE', 'WEEKLY', 'MONTHLY', 'OTHER', 'CONTRACT',
         'YEARLY',
         'TEMPORARY', 'VOLUNTEER', 'FULL_TIME', 'INTERNSHIP', 'PART_TIME'], axis=1)
    return job_postings_df


def fix_nan(job_postings_df):
    job_postings_df.fillna(0, inplace=True)

    # print(job_postings_df)
    # print('check for nan values')
    # print(job_postings_df[job_postings_df.isnull().any(axis=1)])

    return job_postings_df
