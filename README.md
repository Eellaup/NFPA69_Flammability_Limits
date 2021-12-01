# NFPA 69 Flammability Limit (2019)

These are notes taken by `Paul Lee` on how to approximate LFL and UFL limits based on varying gas compositions.

### Efects on Flammabilities

- Pressure & Temperature: Increase in pressure and temperature results in increase in UFL and slight decrease in LFL
- Inert Gases: CO2 > H2O > N2 > He in terms of effectiveness for reducing flammability
- LFL: Amount of fuel controls the limit
- UFL: Amount of oxygen controls the limit

![Inert_Gas_FL]("img/Effect of Inert Gas on FL.png")

### Estimation of FL based on thermal balance method (Ma 2011)

- Heating factor (H) and a quenching factor (Q) from the flammable limits for each componet and then use a molar average of these two factors to estimate the flammable limits of the mixture

Nomenclature:

- H_f : Heating Factor
- C_o : Stoichiometric amount of oxygen consumed by combustion
- H_o : Heat of oxidation specific to the fuel
- Q_f : Fuel quenching factor relative to air
- x_L : Lower flammability limit of species in air
- x_U : Upper flammability limit of species in air
- 4.773 is the inverse of 0.2095 (mole fraction of oxygen in air)

Calculation Method

Lower Flammability Limit

![LFL]("img/lfl.png")

Upper Flammability Limit

![UFL]("img/ufl.png")

where....

Heat of Oxidation (Flammable Species)

![HoO]("img/heat_of_oxidation.png")

Heat of Oxidation (Flammable Mixture)

![HoO_mix]("img/heat_of_oxidation_mix.png")

Quenching Factor (Flammable Species)

![QF]("img/quenching_factor.png")

Quenching Factor (Flammable Mixture)

![QF_mix]("img/quenching_factor_mix.png")

Stoichiometric Amount of Oxygen (Flammable mixture)

![CO]("img/stoich_o2_mix.png")

Heating Factor (Flammable Mixture)

![HF]("img/heating_factor_mix.png")
