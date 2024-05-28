 ## Application Usage Guide
To use this application, you need to have a dataset in 
CSV format. Normally, these datasets have the following structure:
- **3 columns**:
- One for the start date of the data validity.
- One for the end date of the data validity.
- One for the useful value for analysis.
To standardize the application and make it as flexible as possible, 
I have determined a specific dataset format that works for 
datasets from all the sites from which they are downloaded.
### Required Column Names
- **Start Date of Validity**: `date_start`
- **End Date of Validity**: `date_end`
- **Useful Value**:
- **Rain Dataset**: `rain`
- **Temperature Dataset**: `temperature`
- **Wind Speed Dataset**: `speed`
- **Wind Direction Dataset**: `direction`
### Example Dataset Structure
| date_start | date_end   | rain  |
|------------|------------|-------|
| 2023-01-01 | 2023-01-02 | 5.6   |

| date_start | date_end   | temperature |
|------------|------------|-------------|
| 2023-01-01 | 2023-01-02 | 18.3        |

| date_start | date_end   | speed |
|------------|------------|-------|
| 2023-01-01 | 2023-01-02 | 12.4  |

| date_start | date_end   | direction |
|------------|------------|-----------|
| 2023-01-01 | 2023-01-02 | 150        |