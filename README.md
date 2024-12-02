# Charlotte Mecklenberg Police Department (CMPD) Traffic Stops

## Introduction
### Traffic Stops in Charlotte

The second page of this analysis provides insight into traffic stop data for the CMPD. The analysis includes data pertinent to: traffic stops, traffic searches, use of force in these events, and the rate at which contraband was ultimately found (as a result of a traffic search). Any citizen can be stopped, but those who are searched also have to have been stopped. Likewise, use of force can only happen if they have been stopped, and contraband can only be found if they are searched.

### Charlotte's Population

The third page of the analysis dives into the overall population of Charlotte, and looks at the rate of traffic stops and traffic searches based on the entire population. The goal here is to highlight the differences between ethnicities, especially when accounting for the overarching % of population each ethnicity in Charlotte has. This data includes government census information for the past 10 years

### Data/operation abstraction design
I got my data for traffic stops from a publicly available website: https://www.opendatapolicingnc.com/report?var=stopPurposeTitle:Investigation&var=agencyTitle:Charlotte-Mecklenburg+Police+Department&var=stateAbbreviation:NC#divStopCountTotal

I got my data for the Charlotte population from: https://datausa.io/profile/geo/charlotte-nc/

I had to do a fair bit of work to modify the traffic stops data sets, as many of the rates are based on custom calculations and the format of the data was not optimal when I originally downloaded it. There were a lot of custom splits I needed to do in Tableau to account for this. The census data was in pretty good shape but I needed to do some additional work to manually define some of the ethnicities to ensure they were in the same groups that I already had for the traffic stop data.

### Future Work

I would like to further analyze the differences in types of traffic stops, and how that may be impacted by ethnicity. If possible, I am also hoping to look into different by division and location within the city of Charlotte.
