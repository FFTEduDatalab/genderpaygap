# genderpaygap
Analysis of government gender pay gap reporting data

Takes three files as input:
- **UK Gender Pay Gap Data - 2017 to 2018.csv**
A copy of the gender pay gap data, downloaded from [the Government's gender pay gap portal](https://gender-pay-gap.service.gov.uk/). Accessed at 2PM on 2 April 2018.
- **SFR25_2017_Underlying_Data.csv**
A copy of the underlying data from [the Department for Education's _School workforce in England: November 2016_ statistical first release](https://www.gov.uk/government/statistics/school-workforce-in-england-november-2016), edited to extract just the school-level data. This is used, in combination with the grouplinks file, to identify academy trusts that had 250 employees or more in November 2016 - the latest date for which data is available.
- **grouplinks_edubaseallacademiesandfree20170403.csv**
A copy of the download file from [Get Information About Schools (EduBase)](https://get-information-schools.service.gov.uk/Downloads) that contains details of academy trusts and the schools that belong to them. Downloaded 3 April 2017, and therefore close in date to the 31 March 2017 date on which gender pay gap reporting is supposed to be based.

The grouplinks file is used to identify employers in the pay gap data that are academy trusts. Together with the school workforce data, it is also used to look at how many trusts may have been within the scope of the gender pay gap reporting excercise, but which had not filed data.

The script outputs three files:
- **trustsgenderpaygap.csv**
A table giving full gender pay gap data for all identified academy trusts.
- **trustsgenderpaygapforchart.csv**
A slimmed-down version of the above, containing just median hourly wage gender pay gap data for the 19 academy trusts in England that have more than 25 schools, as at the time of carrying out the analysis.
- **missingtrusts.csv**
An attempt to look at how many trusts may have been within the scope of the gender pay gap reporting excercise, but which had not filed data.
