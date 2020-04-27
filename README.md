# Sentime

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