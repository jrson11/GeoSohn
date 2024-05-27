6.Numerical Modeling
===================

6.1 Paxis3D
---------

6.1.1 Soil Constitutive Models
.........

a. Linear Elastic (LE) model

  a.1. LE represents soil behavior using Hooke's law, treating soils as isotropic linear elastic materials with parameters like elastic modulus (E) and Poisson's ratio (v).

  a.2. Limitations: While useful for certain applications, the LE model may not fully account for the mechanical behavior of soils, especially in scenarios involving non-linear and plasticity.

b. Mohr-Coulomb (MC) model

6.1.1 Mudmat
.........

6.1.2. Suction pile
...............

- Note

  - Benchmark: Edger, Andresen, and Jostad, 2008, "Capacity analysis of suction anchors in clay by Plaxis 3D foundation"
  - Range of mooring line angle at padeye: 15 ~ 45 (API RP 2SK-R2015, Figure E.3)


6.2 Slope Stability
..................

- Slope 2D
- Slope 3D

6.3 Python
------

6.3.1. Groundhog
............

6.3.2. GeoSohn
..........

6.3 Others
-------

6.3.1. NGI
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


6.3.2. Fugro
........

- AGSPANC: pile capacity analyses

  - Randolph,2020, "A Lifetime of Offshore Geotechnics - Career Reflections and Lessons Learned" has AGSPANC in Fig. 12.


6.3.3.Delmar
.........

- DEAP: Suction pile by PLE

  - API RP 2SK D.10 5th requirement, PLE may NOT be suitable for LAYERED soil profile.
  - API RP 2SK E., 3.2.3.2 is also skeptical in PLE.

6.3.4 DNV
......

- SESAM

  - Fixed structure
  - Floating structure
  - Pipeline
