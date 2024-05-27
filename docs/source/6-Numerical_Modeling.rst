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

  b.1. MC represents stress-strain behavior in an elasto-plastic form, requiring specification of five material parameters: Elastic modulus (E), Poisson's ratio (v), cohesion (c), internal friction angle (phi), and dilation angle (psi).

  b.2. Limitations: Selecting the correct lateral earth pressure coefficient at rest (K0)  is crucial factors to define soil properties accurately.

c. Soft Soil (SS) model

  c.1. SS designed for analyzing high-compressibility soils like consolidated clayey soils, peat soils, and clayey silt soils, which exhibit unique stress-strain behavior. Suitable for primary consolidation.

  c.2. Key parameters: Internal friction angle (phi), cohesion (c), dilatation angle (psi), modified compaction index (lambda*), and modified swelling index (k*).

d. Soft Soil Creep (SSC) model

  d.1. SSC tailored for time-dependent behavior in soils like consolidated clays. Crucial for calculating settlement evaluation in foundations, embankments, and assessing tunnel stability.

  d.2. Key parameters: All in the SS model, and modified creep index (mu*)

e. Hardening Soil (HS) model

  e.1. HS enhances accuracy for both soft and hard soil behavior. This requires observed data from drained triaxial pressure stests.

  e.2. Key parameters: three elastic moduli: Secant elastic modulus (E50), Unloaded/Reloaded elastic modulus (Eur), and Oedometer elastic (Eoed).

f. Hardening Soil model with Small-Strain Stiffness (HSsmall)

  f.1. HSsmall enhances precision in representing soil behavior at very low strain. Valuable for settlement during construction, where early-stage soil response is crucial. Also particularly suitablee for dynamic analysis, offering a comprehensive method for capturing soil behavior in various loading conditions.

  f.2. Key parameters: Power for stress-level dependency of stiffness (m), E50, Eur, Eoed in HS model, and shear modulus at very small strains (G0), and threshold shear strain at Gs (=0.722*G0).

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
