
Files:

1)
USA-location.csv
Latitute and longitude of the 381 metropolitan areas. Manual inspection using online maps reveal that the location is typically at the centre of the largest city.


2) USmetro_gdp_pop_2013
From previous paper
381 Metropolitan areas, different from 1);
population and gdp
States

3) metropolitan-miles.csv
from previous paper
Same file seems to be online at:
https://www.fhwa.dot.gov/policyinformation/statistics/2013/pdf/hm71.pdf

484 metropolitan areas, population and miles


Merge:

To attribute location to each city, the information in file 1 was added to files 2 and 3. In case of file 2, this was straightforward as both cases correspond to the same metropolitan areas. In the case of file 3, this was done with some manual input. The output was a new file:

4) miles-location.csv
Contains Road length and location of 362 metropolitan areas in the USA, obtained after merging files 1 and 3 as described above.





