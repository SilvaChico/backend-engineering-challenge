# Backend Engineering Challenge

## Run CLI:

Make sure you have python installed on your machine:
[Install python](https://www.python.org/downloads/)

### Run:

```
python src/main.py --input_file <file.json> --window_size <size of window>
```

Check output.json for the output file

### Test:

```
python3 -m unittest tests/main.py
```

## Assumptions

- Several events can occur in the course of one minute
- Input format will be in the JSON format like so:

```json
[
  {
    "timestamp": "2018-12-26 18:11:08.509654",
    "translation_id": "5aa5b2f39f7254a75aa5",
    "source_language": "en",
    "target_language": "fr",
    "client_name": "airliberty",
    "event_name": "translation_delivered",
    "nr_words": 30,
    "duration": 20
  },
  {
    "timestamp": "2018-12-26 18:15:19.903159",
    "translation_id": "5aa5b2f39f7254a75aa4",
    "source_language": "en",
    "target_language": "fr",
    "client_name": "airliberty",
    "event_name": "translation_delivered",
    "nr_words": 30,
    "duration": 31
  },
  {
    "timestamp": "2018-12-26 18:23:19.903159",
    "translation_id": "5aa5b2f39f7254a75bb3",
    "source_language": "en",
    "target_language": "fr",
    "client_name": "taxi-eats",
    "event_name": "translation_delivered",
    "nr_words": 100,
    "duration": 54
  }
]
```
