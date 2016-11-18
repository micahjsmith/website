Title: I ran a race and made some graphs
Date: 2016-11-17
Category: dataviz
Tags: dataviz, running, julia
Slug: cambridge-half-analysis
Authors: Micah Smith

The Cambridge Half Marathon was this past Sunday and I was able to race with a couple of
friends. It was a gorgeous day and very nice course. As always, I was inspired by the
diversity of runners.

After finishing, I was happy to see that the full results were dumped in one not-too-poorly
formatted text file. I whipped it into a Julia DataFrame to do a bit of analysis.

## How fast are old people?

It's a thrill to get passed by older women and men who are pacing along by themselves or
running with their daughters or sons. How fast were the older runners in this race,
especially compared to runners in their "primes"? To answer this, I plot the estimated
distribution of pace (minutes per mile) across age groups.

<object data="{filename}/images/density_age_v2.js.svg" type="image/svg+xml"></object>

It's interesting to note that, besides the literal elderly, runners from very different age
groups have similar distributions of paces. Sure, there's a little more mass on faster paces for the youngest
runners (20 years old or younger) and a bit more mass on slower paces for the 51-65 year
old runners. But the five age categories in the middle show quite similar distributions, and
the modes are almost identical at around 9:00 minutes per mile.

I haven't looked at the science for how pace changes with increased age in general — though
presumably it converges to 0 when we die — nor looked at data from other races, so I'm
interested to see if this phenomenon is seen more widely. I would expect that for the older
age groups, there is a fair amount of self-selection in which more dedicated runners compete
and the "recreational" runners stay home. This could balance out the natural decreases in
pace from aging.

## How fast are young people?

With those oldies speeding by, it's important not to lose track of my own peers. Below, I plot the
estimated distribution of pace for the group of 23-year old males, and show the pace of
several key individuals.

<object data="{filename}/images/density_micah.js.svg" type="image/svg+xml"></object>

I turn out to not be the last of the pack for my group, for which I'm relieved. However,
while I handily beat the oldest racer of the day — a 71-year old man —, I get crushed by
the youngest racer of the day — a 9-year old boy, who runs an amazing 7:14 pace.  

It's inspiring to take part in a race with such a diverse group of racers in terms of age,
experience, and ability. A special shout out as well to the eight visually impaired runners and
two wheelchair racers who completed the course.

The data and code can be seen on my
[GitHub](https://github.com/micahjsmith/cambridge-half-analysis).
