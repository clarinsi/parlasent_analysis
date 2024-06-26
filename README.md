# parlasent_analysis
Code for ParlaSent research note


# 2024-06-10T12:43:25

* ~~I'm losing countries in turning tables. Fix.  Lose per-party stats~~
* ~~Country of choice need term info extracted and searchable~~
* Try speeding up by loading compressed speeches.csv -> turns out it's 0.6dB slower, but we save 13.4dB on disk space. Will keep it compressed.

# 2024-06-21T11:34:31

* country stats: add parties too. Leave the analysis for Michal (Old vs new democracies.) Do HR and NL for approximately the same period.
* time trends: will be skipped for now
*

# 2024-06-24T13:26:24
First notebook:
Timetrends, like Michal. X scale from 2015 - 2020 (like Michal, check his scale), fixed y
Three plots per graph: share of positive, negative, and neutral
Lose the maps?
Highlights for COVID: march 2020-spring 2022
XXX not this, no other data: Vertical line at the start of the UA invasion


Third notebook:
Implement a Europe-wide stats, use percentage_of_negative instead of averaging.
Add a filter for char_length >= 100
