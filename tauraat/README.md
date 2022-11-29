# TAURAAT: The Attribute table of USGS (Surface-water: Field measurements) for Rivers And Associated Tributaries

TAURAAT can be considered as an updated version of 
[HYDRoSWOT](https://www.sciencebase.gov/catalog/item/57435ae5e4b07e28b660af55) 
– HYDRoacoustic dataset in support of Surface Water Oceanographic Topography. 
TAURAAT includes 10050 site stations (out of 10081 sites represented by HYDRoSWOT), 
and aggregates channel geometry and characteristics of stream flow collected from the USGS stream gaging station 
(Surface-water: Field measurements) network and includes 2,802,532 records of all different types of USGS field
measurements methods (Table 1). The time span of the records starts from `1845-05-05 14:00:00` to `2022-10-24 12:58:01`.

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

TAURAAT is publicly availble in 
[Google Drive](https://drive.google.com/file/d/1DhKbouaWy1t3VQ4BzWvyX0KIpaemFdW7/view?usp=sharing).
