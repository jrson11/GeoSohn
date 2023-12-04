Numerical Modeling
===================

Plaxis3D
---------

1. Mudmat
.........

2. Suction pile
...............

- Note

  - Benchmark: Edger, Andresen, and Jostad, 2008, "Capacity analysis of suction anchors in clay by Plaxis 3D foundation"
  - Range of mooring line angle at padeye: 15 ~ 45 (API RP 2SK-R2015, Figure E.3)


3. Slope Stability
..................

- Slope 2D
- Slope 3D

Python
------

1. Groundhog
............

2. GeoSohn
..........

Others
-------

1. NGI
.....

- Bifurc: 2D suction pile
- ChainConfig: Mooring chain configuration
- AnchorPEN: pile embedment calculation
- CAP: 2D mudmat

  - Inputs

    - Shear strength
    - V, Hx and My
    - V, Hy and Mx

  - Outputs

    - Safety factor versus Depth
    - Force calculated for critical surface


2. Fugro
........

- AGSPANC: pile capacity analyses

  - Randolph,2020, "A Lifetime of Offshore Geotechnics - Career Reflections and Lessons Learned" has AGSPANC in Fig. 12.


3.Delmar
.........

- DEAP: Suction pile by PLE

  - API RP 2SK D.10 5th requirement, PLE may NOT be suitable for LAYERED soil profile.
  - API RP 2SK E., 3.2.3.2 is also skeptical in PLE.

4. DNV
......

- SESAM

  - Fixed structure
  - Floating structure
  - Pipeline
