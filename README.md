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


# 2024-06-27T08:09:21

Hi Peter, just checking the graphs, they look fine but I agree 3 months is maybe a too wide time span for a parliamentary life cycle. I've had good results with datemonths in the past (Jan, Feb, March ...) but it might make sense to try also dateweek. I am curious what will come out of it. It is really funny to see how little positive sentiment occurs in the national parliaments.

Minor comments:
- For y-axis, spell out full percentage (0%, 25%, 75%, 100%) and maybe make it a bit higher. The graphs look a bit squished. ✓
- For x-axis reduce the number of ticks, to make it more readable, or fully rotate the years. ✓
- When you do the averages, can you also calculate confidence intervals and plot them as a ribbon with the trend line? It would be good to see how spread our data are. ✓
- I would prefer a slightly fancier colors for sentiment -  here is a color pallet I usually work with in R. My favorite crayons :D https://kbroman.wordpress.com/wp-content/uploads/2014/05/crayons.png. Anyway, maybe something like "maroon" for positive sentiment, "cornflower" for negative sentiment, and "manatee" for neutral. ✓
- The covid period is not very visible. What about combination of line thickness and alpha? ✓
For the last point I meant something like this. I made it in R using ggplot2.
For the second notebook, maybe Netherlands is not the best example then. The Dutch parliament was paralyzed by long government formations in the recent years. That might explain why we have so few speeches there. Still, it is a problem as this is not something normal. Can we try France? It does not really matter to me as I am not an expert on either one of them. -> FR seems very well populated
Skimming through the most negative/positive MPs, it is clear we need to filter out the outliers (very few speeches) from the overview. Rather than normalizing what we have there and explaining what we did and how, let's simply focus on "average" MPs. For MPs, let's focus on individuals with "count" within one or two standard deviation from the mean.
I would do the same thing for the European level political parties (1 or 2 SD). For national parties (like the table for the Dutch parliament), I would keep everything as it is.
Overall, this is a very good start 👏

Reply:
Minor comments have been implemented in the latest commit. The colors were scraped from the png you provided, and I think they might be too pastel for this use case (esp. with the confidence interval behind the lines and changing opacity, sometimes I felt like my eyes went bad :D).

For the confidence interval I now plot plus/minus one standard deviation. Some words have to be said about what precisely I'm plotting: I first calculate 1-day percentage_of_negative, percentage_of_positive, and percentage_of_neutral. I linearly interpolate the days where we have no data, and then calculate a rolling mean and standard deviations over 30 days for smoothing. Standard deviation is then used for confidence interval. This works nicely, but obviously gives no idea about the missing data periods we might have. Happy to hear your thoughts on this on this. Also, have you envisioned a better confidence interval estimator than +/- one sigma?

Regarding the third notebook: I now compare France and Croatia; it's much better populated. The filtration by one or two standard deviations is implemented, but I noticed that due to the long tail of the distribution, even one standard deviation is too big and the infrequent speakers still pop in. I implemented interquartile filtering, so that only Q2 and Q3 speakers make it in the final output. Now I think this should be changed to only limiting the infrequent speakers/parties, what do you think?

As proposed, the per-country stats are left unfiltered.

# 2024-06-28T07:28:46

ok, new suggestion, let's eliminate speakers in q1 -  those infrequent/irrelevant
and you can limit the printout to 50 most prominent actors
applies to both parties and MPs
Maybe try smoothing the trend line even more for less structure in the data (my "EKG" picture  was not a good example in that sense )

3rd notebook: The q1 filtering is now used for the corpus-wide stats.
1st notebook: Smoothing was now extended to a year. I used https://medialab.github.io/iwanthue/ for the colors. I was toying with still including the standard deviation, but it's hard to see anything in the non-covid area. How about twin vertical bars, especially since the UA invasion pretty much matches what we decided would be the end of the COVID perios?


# Whence the discrepancy between Nikola's speadsheet and my results?

* Summarisation is already too late, our data differs before, already on speaker level.

* Nikola deals with raw texts, and here we deal Nikola's aggregate numbers (speeches.csv.zip, this already has logits pondered and logits averaged, but does not propagate number of sentences or distributions of their lenghts). This alone could be the cause for the difference, given that we're doing person averages based on per-speech averages, while Nikola can access the entries directly.

* Nikola seems to use filtering on sentence level, in line 47 of sentiment_per_speaker.py and take speakers that have >= 100 sentences regardless of Coalition/Opposition status, while here we cannot do that as we don't have the sentences.