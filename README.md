# parlasent_analysis
Code for ParlaSent research note


# 2024-06-10T12:43:25

* ~~I'm losing countries in turning tables. Fix.  Lose per-party stats~~
* ~~Country of choice need term info extracted and searchable~~
* Try speeding up by loading compressed speeches.csv -> turns out it's 0.6dB slower, but we save 13.4dB on disk space. Will keep it compressed.