# Sentime

## Current Dataset
2020_04_27_dataset.csv: 30.633 tweets:
- 9.959 Positive
- 6.123 Negative

## How to run?
* Server
Go to server folder and run:
```
  docker-compose up
```
* Client
Go to client folder and run:
```
  npm start
```

## Model preprocessing
1. Run model/scraper.py
  ```bash
    # Example
    python3 model/scraper.py
  ```
2. Run model/preprocess.py ${TODAY_DATE}
  ```bash
    # Example
    python3 model/preprocess.py 2020_04_26
  ```
3. Download AWS Comprehend output and rename as ${TODAY_DATE}_output.json, then move it to model/data
4. Run model/merge_results.py ${TODAY_DATE}
  ```bash
    # Example
    python3 model/merge_results.py 2020_04_26
  ```
5. Create a folder called Sentime in Google Drive and open sentime.ipynb in Colab
6. Upload the generated model/data/${TODAY_DATE}_dataset.csv to the folder created above

## Connect with database using pgAdmin
1. Go to http://localhost:5431
2. Login with email: `admin@test.com` and password: `root_12345`
3. Create a new server
4. Fill the form as follows:
  - Use `db`instead of `localhost` in the address field
  - User: `sentime_user`
  - Password: `root_12345`