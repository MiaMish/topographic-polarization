PEW RESEARCH CENTER FOR THE PEOPLE & THE PRESS
AUGUST POLITICAL SURVEY
August 9-16, 2016
N=2,010

***************************************************************************************************************************

This dataset includes cell phone interviews conducted using an RDD sample of cell phone numbers. 
Cell phone interviews include households that are cell-only as well as those that also have a landline phone. 
The dataset contains several weight variables. 

WEIGHT is the weight for the combined sample of all landline and cell phone interviews. 
Data for all Pew Research Center reports are analyzed using this weight.

Two other weights can be used to compare the combined sample with the landline sample by itself 
and with the cell phone sample by itself.

LLWEIGHT is for analysis of the landline RDD sample only. Interviews conducted by cellphone are not 
given a weight and are excluded from analysis when this weight is used.

CELLWEIGHT is for analysis of the cell RDD sample only. Interviews conducted by landline are not
given a weight and are excluded from analysis when this weight is used.

***************************************************************************************************************************

Beginning in the Fall of 2008, the Pew Research Center started using respondents’ self-reported zip code as  
the basis for geographic variables such as region, state and county. We do this because the error rate in the original 
geographic information associated with the sample is quite high, especially for respondents from the cell phone sample. 

For respondents who do not provide a zip code or for those we cannot match, we use the sample geographic information. 
We continue to include the original sample geographic variables in the datasets (these variables are preceded by an ‘s’) 
for archival purposes only.

To protect the privacy of respondents, telephone numbers, county of residence and zip code have been removed from the data file.

***************************************************************************************************************************

Releases from this survey:

August 18, 2016. "Clinton, Trump Supporters Have Starkly Different Views of a Changing Nation."
http://www.people-press.org/2016/08/18/clinton-trump-supporters-have-starkly-different-views-of-a-changing-nation/

August 25, 2016. "On Immigration Policy, Partisan Differences but Also Some Common Ground"
http://www.people-press.org/2016/08/25/on-immigration-policy-partisan-differences-but-also-some-common-ground/

August 26, 2016. "Opinions on Gun Policy and the 2016 Campaign."
http://www.people-press.org/2016/08/26/opinions-on-gun-policy-and-the-2016-campaign/


***************************************************************************************************************************


SYNTAX

***The following syntax is for constructed demographic variables***.

*The combined race variable (racecmb) was computed using the following syntax:
recode race_1 (1=1) (2=2) (3=3) (4 thru 7=5) (8 thru 9=9) into racecmb.
if race_2>0 and race_2 <8 racecmb=4.
variable label racecmb "Combining Race".
value label racecmb
1 "White"
2 "Black or African-American"
3 "Asian or Asian-American"
4 "Mixed Race"
5 "Or some other race"
9 "Don’t know/Refused (VOL.)".

*The race-ethnicity variable (racethn) was computed using the following syntax:
if racecmb=1 and hisp ge 2 racethn=1.
if racecmb=2 and hisp ge 2 racethn=2.
if (racecmb ge 3 and racecmb le 5) and (hisp ge 2) racethn=4.
if racecmb=9 racethn=9.
if hisp=1 racethn=3.
variable label racethn “Race-Ethnicity”.
value label racethn
1 “White non-Hispanic”
2 “Black non-Hispanic”
3 “Hispanic”
4 “Other”
9 “Don’t know/Refused (VOL.)”.




*********************************************************************************.
***The data set includes additional variables for presidential vote preference***.

*Q13HORSE combines vote preference for REGISTERED VOTERS using the following syntax:
do if REG=1.
compute Q13HORSE=0.
if (q13=1 or q13a=1) Q13HORSE=1.
if (q13=2 or q13a=2) Q13HORSE=2.
if (q13=3 or q13a=3) Q13HORSE=3.
if (q13=4 or q13a=4) Q13HORSE=4.
if (q13=5 and q13a ge 5) Q13HORSE=5.
if (q13=9 and q13a=9) q13HORSE=9.
end if.
exe.

var lab Q13HORSE ‘2016 preference with leaners’.
val lab Q13HORSE 1 ‘Clinton/lean Clinton’ 2 ‘Trump/lean Trump’ 3 ‘Johnson/lean Johnson’ 4 ‘Stein/lean Stein’ 5 ‘Other-refused to lean’ 9 ‘DK-refused to lean’.


*Q13HORSEGP combines vote preference for the GENERAL POPULATION using the following syntax:
compute Q13HORSEGP=0.
if (q13=1 or q13a=1) Q13HORSEGP=1.
if (q13=2 or q13a=2) Q13HORSEGP=2.
if (q13=3 or q13a=3) Q13HORSEGP=3.
if (q13=4 or q13a=4) Q13HORSEGP=4.
if (q13=5 and q13a ge 5) Q13HORSEGP=5.
if (q13=9 and q13a=9) q13HORSEGP=9.
end if.
exe.

var lab Q13HORSEGP ‘2016 preference with leaners’.
val lab Q13HORSEGP 1 ‘Clinton/lean Clinton’ 2 ‘Trump/lean Trump’ 3 ‘Johnson/lean Johnson’ 4 ‘Stein/lean Stein’ 5 ‘Other-refused to lean’ 9 ‘DK-refused to lean’.


*Q14HORSE2 combines the two-way vote preference (no third-party) for REGISTERED VOTERS using the following syntax:
do if REG=1.
compute Q14HORSE2=0.
if (q13=1 or q13a=1) or (Q14=1 or Q14a=1) Q14HORSE2=1.
if (q13=2 or q13a=2) or (Q14=2 or Q14a=2) Q14HORSE2=2.
if (q14=3 or q14a=3) Q14HORSE2=3.
if (q14=9 or q14a=4) Q14HORSE2=9.
end if.
exe.

var lab Q14HORSE2 ‘2016 2-way preference with leaners’.
val lab Q14HORSE2 1 ‘Clinton/lean Clinton’ 2 ‘Trump/lean Trump’ 3 ‘Other-refused to lean’ 9 ‘DK-refused to lean’.

