import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def model_action(df):
    # Assuming 'df' is your original DataFrame
    df_cleaned = df.dropna(subset=['mid_monthly_salary'])  # Drop rows with missing values in the target variable

    # One-Hot Encoding for 'job_id'
    onehot_encoder_job = OneHotEncoder(sparse=False, drop='first')  # drop the first column to avoid multicollinearity
    job_id_encoded = onehot_encoder_job.fit_transform(df_cleaned[['job_id']])
    df_encoded = pd.concat(
        [df_cleaned, pd.DataFrame(job_id_encoded, columns=onehot_encoder_job.get_feature_names_out(['job_id']))],
        axis=1)
    df_encoded = df_encoded.drop(['job_id'], axis=1)

    # Label Encoding for 'company_id' (if it's not one-hot encoded as part of 'job_id')
    # ...

    # Assuming 'mid_monthly_salary' is your target variable
    features = df_encoded.drop(['mid_monthly_salary'], axis=1)
    target = df_encoded['mid_monthly_salary']

    # Define a ColumnTransformer to handle missing values
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), features.columns)
        ])

    # Create a pipeline with the preprocessor and the RandomForestRegressor
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1))
    ])

    # Split the data into training and testing sets
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    imputer = SimpleImputer(strategy='mean')
    y_test = imputer.fit_transform(y_test.values.reshape(-1, 1))
    y_test = pd.Series(y_test.squeeze(), index=range(len(y_test)))  # Convert to Series with proper index
    X_test = X_test.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)
    X_test = X_test.loc[y_test.index]

    # Print information about missing values in y_train
    # print("Missing values in y_train:")
    # print(target.isnull().sum())

    # Drop missing values from target variable y_train
    y_train = y_train.dropna()

    # Drop corresponding rows from features X_train
    X_train = X_train.loc[y_train.index]

    # Train the model using the pipeline
    pipeline.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = pipeline.predict(X_test)

    print('now evaluating mean squared error:')
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    return df_encoded
