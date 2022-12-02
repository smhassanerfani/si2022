# TAURAAT: The Attribute table of USGS (Surface-water: Field measurements) for Rivers And Associated Tributaries

## Dataset Description

TAURAAT can be considered as an updated version of 
[HYDRoSWOT](https://www.sciencebase.gov/catalog/item/57435ae5e4b07e28b660af55) 
– HYDRoacoustic dataset in support of Surface Water Oceanographic Topography. 
TAURAAT includes 10050 site stations (out of 10081 sites represented by HYDRoSWOT), 
and represents five important channel geometry and characteristics of stream flow (i.e., streamflow, stage, channel 
width, channel area, and channel velocity) collected from the USGS stream gaging station (Surface-water: Field 
measurements) network and includes 2,802,532 records of all different types of USGS field measurements methods
(Table 1). The time span of the records starts from `1845-05-05 14:00:00` to `2022-10-24 12:58:01`.

Table 1. The different types of USGS field measurements methods.

| Method  | Frequency | Method | Frequency | Method | Frequency |
|---------|-----------|--------|-----------|--------|-----------|
| Unknown | 1466349   | VELC   | 17984     | VIPYG  | 265       |
| VADCP   | 452725    | VPYG   | 17304     | VOTT   | 26        |
| VADV    | 373597    | VIPAA  | 955       | VTIME  | 16        |
| VPAA    | 104457    | VICE   | 431       | VOPT   | 1         |

TAURAAT includes 11,876 records that do not provide any field measurements. As it is mentioned before, 31 site stations
of HYDRoSWOT are not included in TAURAAT. 17 of these stations are operated by an agency other than USGS, and the data
of other 14 stations are not available in USGS website anymore. Figure 1 shows the location and site number of these
sites on the map.

<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/excluded_sites.jpg">
    Figure 1. Locations of 31 site stations of HYDRoSWOT which are not included in TAURAAT.
</p>

## Dataset Analysis
After removing zero and missing values of three important columns including `discharge_va`, `gage_height_va`, and
`chan_width` that represent streamflow, river stage and channel width, respectively, 2,312,896 records remain.
Moreover, to conduct significant statistics, sites with more than 50 observations are selected from valid records
(out of no zero/missing records). Eventually, 2,279,530 observations (represented by 7,446 sites) are
considered for following analyses. 

### Sites with Positive Discharge
2,199,163 observations (represented by 7,098 sites) include only positive values for discharge. The river stage verses
discharge plot for some sample sites are as follows:

<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/tau_pos_dis.png">
    Figure 2. Site locations including only positive values for discharge.
</p>

### Sites with Negative Discharge
80,367 observations (represented by 348 sites) include both negative and positive values for discharge. The river stage
verses discharge plot for some sample sites are as follows:

<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/tau_neg_dis_v2.png">
    Figure 3. Site locations including both negative and positive values for discharge.
</p>

Among sites having negative discharge in their records, there are still some cases that the relation between stage and
discharge is more like sites with positive discharge.

<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/tau_neg_dis_v1.png">
    Figure 4. Site with negative/positive discharge that follow the behavior of sites with only positive discharge.
</p>

These sites are generally located near the costal area or control points. We will omit these site locations from all 
following analyses.

<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/neg_dis.jpg">
    Figure 5. Location of sites that includes both negative and positive values for discharge.
</p>

## Channel Geometry analysis
The role of channel (bankfull) geometry representation in hydrological modeling is important.
Bankfull discharge, for instance, is considered to be the most effective flow for moving sediment, forming 
or removing bars, forming or changing bends and meanders, and generally doing work that results in the average 
morphological characteristics of channels (Dunne and Leopold, 1978).
According to the definition, 
"In the case of rivers with floodplains, river stage tends to increase rapidly with increasing water discharge when all
the flow is confined to the channel, but much less rapidly when the flow spills significantly onto the floodplain. The 
rollover (i.e., sudden change of slope) in the curve defines bankfull discharge" 
[Gary Parker, Morphodynamics e-book](http://hydrolab.illinois.edu/people/parkerg/powerpoint_lectures.htm).
However, as it is shown in the Figure 2, finding those observations that represent bankfull characteristics
is not always an easy task.

Here, instead of selecting one observation to represent the channel in a specific state (e.g., bankfull), the best 
fitted distribution to the important properties of the channel (discharge, stage and width) are calculated. 
Thus, each site station is represented by the best fitted distribution parameters associated with channel geometry of
that site. Let’s assume normal distribution is the best fit for the whole observations of discharge in a hypothetical
site station. So, two values (i.e., mean and std) can represent all of those observations for discharge. Through this
way, all observations of a site can be summarized in one record. 

### Discharge Distribution 
The histogram of discharge observations for 16 site stations which were randomly selected is shown in the Figure 6. 

<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/tau_discharge_dist.png">
    Figure 6. The histogram of discharge observations for different site stations.
</p>

Ten most common distributions 
(i.e., `cauchy`, `chi2`, `expon`, `exponpow`, `gamma`, `lognorm`, `norm`, `powerlaw`, `rayleigh`, `uniform`)
were fitted to discharge observations of 7,098 sites (including only positive values for discharge). The frequency 
of best fitted distribution is shown in the Figure 7. This figure shows `lognorm` is the best fit for more than 50%
of the site stations.  

<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/dist_freq_discharge.png">
    Figure 7. The frequency of best fitted distribution for channel discharge.
</p>

### Width Distribution 
The same statistical analysis was done for channel width. The histogram of channel width observations for 16 different
site stations is shown in Figure 8. Compared with channel discharge, channel width distribution of different site 
stations does not follow same pattern. In some cases (indicated by red squares), channel width distributions have more
than one peak.

<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/tau_width_dist.png">
    Figure 8.
</p>

The frequency of best fitted distribution for channel width is shown in the Figure 9.  This figure shows `cauchy` is
the best fit for around 4000 of the site stations. 
<p align="center">
    <img width="100%" height="100%" src="https://github.com/smhassanerfani/si2022/blob/main/tauraat/data/dist_freq_width.png">
    Figure 9. The frequency of best fitted distribution for channel width.
</p>






TAURAAT is publicly availble in 
[Google Drive](https://drive.google.com/file/d/1DhKbouaWy1t3VQ4BzWvyX0KIpaemFdW7/view?usp=sharing).
