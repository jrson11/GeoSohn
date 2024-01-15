p-y curve
==========

History
--------

The concept of p-y curves for analyzing the lateral response of piles dates back to the early 20th century, but their widespread application in offshore geotechnical engineering for clay and sand soils began in the latter half of the 20th century. Here's a breakdown of the key milestones:

1950s-1960s:
.............

- **Early developments**: 'Winkler (1867) <https://www.issmge.org/uploads/publications/1/35/1981_02_0020.pdf>'_ and Fleming (1940) introduced the concept of subgrade reaction, which forms the basis for p-y curves. They proposed that the lateral resistance of a soil-pile system can be represented by the following equation:

  F=k⋅δ,
  where 
    - F is the lateral soil resistance, 
    - k is the subgrade modulus, and 
    - δ is the lateral deflection of the pile.

- **Field tests and empirical correlations**: Poulos & Davis (1968) conducted field tests on piles and established empirical correlations between soil properties and p-y curve parameters. These correlations helped relate the subgrade modulus 

- **Early analytical models**: Reese and Matlock (1956) developed early analytical models that often used simple linear or hyperbolic relationships to represent the lateral response of piles. These models were based on the concept of linear-elastic behavior.

1970s-1980s:
............

- **Refinement of empirical correlations**: Matlock (1970) and Coyle & Reese (1977) refined empirical correlations for clay and sand, taking into account factors like soil type, density, and loading direction. These correlations improved the accuracy of p-y curves.

- **Limit equilibrium methods**: API RP 2A (1977) introduced limit equilibrium methods for offshore platform design, incorporating p-y curves to analyze pile stability under lateral loads. These methods are based on the concept of equilibrium between lateral forces and soil resistance.

- **Finite element modeling**: Early developments in finite element software allowed for more sophisticated simulations of soil-pile interaction, but computational limitations restricted widespread use. Finite element analysis involves solving the differential equation governing pile-soil interaction.

1990s-2000s:
.............

- **Calibration and validation of p-y curves**: Jardine & Chow (1991) emphasized calibrating and validating existing p-y curves through back-analysis of field data and centrifuge tests. This involved adjusting the parameters in the p-y curve equations to match observed behavior.

- **Development of advanced constitutive models**: Dafalias & Manzari (2004) developed more complex constitutive models for clays and sands, considering factors like dilatancy, strain-softening, and cyclic loading. These models improved the accuracy of p-y curve predictions.

- **Advancements in numerical modeling**: Increased computational power enabled more realistic finite element simulations with advanced constitutive models, improving p-y curve accuracy and applicability. Numerical models often incorporate nonlinear soil behavior.

2010s-Present:
...............

- **Continued refinement of constitutive models**: Ongoing research continues to refine existing constitutive models and develop new ones for specific soil types and loading conditions. These models aim to capture the full complexity of soil behavior.

- **Probabilistic approaches**: Integration of probabilistic methods into design considers uncertainties in soil properties and p-y curve parameters. Probabilistic design involves assessing the likelihood of different outcomes.

- **Machine learning and AI**: Emerging techniques like machine learning and artificial intelligence are being explored for p-y curve prediction and validation based on large datasets. These methods can help improve the efficiency of p-y curve generation.

Key challenges and future directions:
......................................

- **Variability of soil behavior**: Accurately capturing the complex and often-variable behavior of clays and sands, especially under cyclic loading and long-term performance, remains a challenge. Advanced constitutive models aim to address this variability.

- **Model-soil interaction and calibration**: Improving the interaction between constitutive models and numerical simulations is crucial for robust p-y curve predictions. Calibration ensures that the models accurately represent real-world behavior.

- **Data acquisition and sharing**: Wider availability of well-documented field data and standardized testing procedures for calibration and validation of p-y curves is essential for advancing the field of geotechnical engineering.

In conclusion, the development of p-y curves for offshore clay and sand soils has evolved from early empirical correlations to sophisticated numerical models and advanced constitutive models. Ongoing research and emerging technologies continue to enhance the accuracy and applicability of p-y curves, ensuring the safe design of offshore structures in challenging marine environments.


Empirical equation
--------------------

Matlock's Equation (1970):
..........................

Matlock developed empirical equations for different soil types, taking into account soil properties such as cohesion (c) and friction angle (φ). This is a more refined representation of p-y curves.

.. math::
   p = k \cdot y

  Where:

  - :math:`p` is the lateral soil resistance (force per unit length, kN/m or lb/ft).

  - :math:`k` is the subgrade modulus, representing the soil's stiffness (kN/m³ or lb/ft³).



  \[
  k = c \cdot \left(\frac{R}{N_q}\right) + \sigma_v \cdot \tan(\phi) \cdot \left(\frac{R}{N_\gamma}\right)
  \]

Where:
- :math:`c` is the cohesion of the soil (kN/m² or lb/ft²).

- :math:`\sigma_v` is the vertical effective stress (kN/m² or lb/ft²).

- :math:`\phi` is the friction angle of the soil (degrees).

- :math:`R` is the pile radius or equivalent diameter (m or ft).

- :math:`N_q` and :math:`N_\gamma` are bearing capacity factors.

