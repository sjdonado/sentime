# Sentime

## Datasets
2020_04_27_dataset.csv: 30633 tweets:
- 9959 Positive
- 6123 Negative

2020_05_24_dataset.csv: 53366 tweets:
- 19534 Neutral
- 17483 Positive
- 12376 Negative
- 3972 Mixed

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
Go to model folder and follow the next steps:
1. Setup
  - Install virtualenv `pip install virtualenv`
  - Create new virtual env `virtualenv .` and activate it `source bin/activate`
  - Install dependencies `pip install emoji`
2. Run model/scraper.py
  ```bash
    # Example
    python3 model/scraper.py
  ```
3. Run model/preprocess.py ${TODAY_DATE}
  ```bash
    # Example
    python3 model/preprocess.py 2020_04_27
  ```
4. Send tweets_parsed to AWS Comprehend, download the output and rename it as `aws_output`, finally move it to model/data/${TODAY_DATE} folder
5. Run model/generate_dataset.py ${TODAY_DATE}
  ```bash
    # Example
    python3 model/generate_dataset.py 2020_04_27
  ```
6. Create a folder called Sentime in Google Drive and open sentime.ipynb in Colab
7. Upload the generated datasets to `sentime/${TODAY_DATE}/train/data.csv` and `sentime/${TODAY_DATE}/test/data.csv`

## Connect with database using pgAdmin
1. Go to http://localhost:5431
2. Login with email: `admin@test.com` and password: `root_12345`
3. Create a new server
4. Fill the form as follows:
  - Use `db`instead of `localhost` in the address field
  - User: `sentime_user`
  - Password: `root_12345`