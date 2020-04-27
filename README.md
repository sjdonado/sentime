# Sentime

## How to run?
* Server
```
  docker-compose up
```
* Client
```
  npm start
```

## Model training
1. Run training/scraper.py
  ```bash
    # Example
    python3 training/scraper.py
  ```
2. Run training/preprocess.py ${TODAY_DATE}
  ```bash
    # Example
    python3 training/preprocess.py 2020_04_26
  ```
3. Download AWS Comprehend output and rename as ${TODAY_DATE}_output.json 
4. Run training/merge_results.py ${TODAY_DATE}
  ```bash
    # Example
    python3 training/merge_results.py 2020_04_26
  ```