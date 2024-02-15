import DBHandler


def load_original_data(original_df, db_cursor):
    db_cursor.execute(
        'CREATE TABLE original_data (job_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")')
    pass
