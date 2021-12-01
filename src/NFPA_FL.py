# Calculate Flammability Limits based on NFPA 69 (2019)
class NFPA_FL:
    # flam: dictionary of flammable gases : concentrations (decimals)
    # dil: dictionary of diluent gases : concentrations (decimals)
    def __init__(self,flam: dict,dil: dict):
        self.flam = flam
        self.dil = dil
    
    # NFPA 69 Lower Flammability Limit
    def LFL(self) -> float:
        self.__refactor_gas()
        if sum(self.flam.values()) == 0:
            return 0
        H_f_mix = self.__H_f_mix_calc()
        Q_f_mix = self.__Q_f_mix_calc()
        Q_d_mix = self.__Q_d_mix_calc()
        R = sum(self.dil.values()) / sum(self.flam.values())
        
        lfl = 1 / (1 + (H_f_mix / (1+R)) - (Q_f_mix / (1+R)) - (R*Q_d_mix / (1+R)) )

        return round(lfl * 100,4)

    # NFPA 69 Upper Flammability Limit
    def UFL(self) -> float:
        self.__refactor_gas()
        if sum(self.flam.values()) == 0:
            return 0
        H_o_mix = self.__H_o_mix_calc()
        Q_f_mix = self.__Q_f_mix_calc()
        Q_d_mix = self.__Q_d_mix_calc()
        R = sum(self.dil.values()) / sum(self.flam.values())
        
        heat_of_oxid = (H_o_mix / inv_mol_frac_air) - 1
        ufl = heat_of_oxid / (heat_of_oxid + (Q_f_mix / (1+R)) + (R*Q_d_mix / (1+R)))

        return round(ufl * 100,4)
    
    # refactor if gas sum does not equal 1
    def __refactor_gas(self):
        # convert o2 to n2 ratio to air
        self.__o2_to_air()
        # sum of total gas
        total_gas = sum(self.flam.values()) + sum(self.dil.values())
        # is sum greater than 1?
        if total_gas != 1:
            print('...Refactoring Gas')
            for key,val in self.flam.items():
                self.flam[key] = val / total_gas
            for key,val in self.dil.items():
                self.dil[key] = val / total_gas
    
    # convert o2 and n2 to air
    def __o2_to_air(self) -> dict:
        # ratio of N2 to O2
        n2_o2_ratio = 78./21
        # if o2 and n2 are in inputGas
        if 'O2' in self.dil and 'N2' in self.dil:
            o2 = float(self.dil.get('O2'))
            n2 = float(self.dil.get('N2'))
            # O2 limited
            if (n2/o2) >= n2_o2_ratio:
                # calculate how much N2 is left after factoring for air
                n2_leftover = n2 - (o2 * n2_o2_ratio)
                # delete O2 from input gas
                self.dil.pop('O2')
                # redefine n2
                self.dil['N2'] = n2_leftover
                # add air
                # inputGas['air'] = 100 - sum(inputGas.values())
            else:
                print('wtf more o2 than n2?')

    # Quenching Factor for Fuel
    def __Q_f_calc(self, lfl: float, C_o: float, H_o: float) -> float:
        return 1 - (1/lfl) + C_o*H_o

    # Heat of Oxidation
    def __H_o_calc(self, lfl: float, ufl:float, C_o: float) -> float:
        return (ufl- lfl) / (C_o*ufl*lfl - (1-ufl)*lfl/inv_mol_frac_air)

    # Stoichiometric amt of O2 during combustion of the mix
    def __C_o_mix_calc(self) -> float:
        # edge case: no flam
        if sum(self.flam.values()) == 0:
            return 0
        C_o_mix = 0
        # calculate weighted avgs
        for gas in self.flam:
            C_o = C_o_index[gas]
            C_o_mix += self.flam[gas] * C_o
        C_o_mix /= sum(self.flam.values())

        return C_o_mix

    # Heating factor for Mixture
    def __H_f_mix_calc(self) -> float:
        # edge case: no flam
        if sum(self.flam.values()) == 0:
            return 0
        H_f_mix = 0.0
        # calculate weighted avgs 
        for gas in self.flam:
            lfl = lfl_index[gas]
            ufl = ufl_index[gas] 
            C_o = C_o_index[gas]
            H_f_mix += self.flam[gas] * C_o * self.__H_o_calc(lfl,ufl,C_o)
        H_f_mix /= sum(self.flam.values())

        return H_f_mix

    # heat of Oxidation for the mixture
    def __H_o_mix_calc(self) -> float:
        # edge case: no flam
        if sum(self.flam.values()) == 0:
            return 0
        H_o_mix = self.__H_f_mix_calc() / self.__C_o_mix_calc()
        return H_o_mix

    def __Q_f_mix_calc(self) -> float:
       # edge case: no flam
        if sum(self.flam.values()) == 0:
            return 0
        Q_f_mix = 0
        # calculate weighted avgs
        for gas in self.flam:
            lfl = lfl_index[gas]
            ufl = ufl_index[gas]
            C_o = C_o_index[gas]
            H_o = self.__H_o_calc(lfl, ufl, C_o)
            Q_f_mix += self.flam[gas] * self.__Q_f_calc(lfl,C_o,H_o)
        Q_f_mix /= sum(self.flam.values())
        return Q_f_mix

    def __Q_d_mix_calc(self) -> float:
        # edge case: no dil
        if sum(self.dil.values()) == 0:
            return 0
        Q_d_mix = 0
        # calculate weighted avgs
        for gas in self.dil:
            Q_d = Q_d_index[gas]
            Q_d_mix += self.dil[gas] * Q_d
        Q_d_mix /= sum(self.dil.values())
        return Q_d_mix

### Helper variables
# Quenching factor for diluents
Q_d_index = {
    'air' : 1.00,
    'He' : 0.643,
    'Ar' : 0.643,
    'N2' : 0.996,
    'O2' : 1.052,
    'CO2' : 1.751,
    'H2O' : 1.259,
    'CCl4' : 3.166
}
# Stoichiometric amount of O2 during combustion
C_o_index = {
    'H2' : 0.5,
    'CO' : 0.5,
    'CH4' : 2.0,
    'C4H8O2' : 5.0,
    'C2H5OH' : 3.0,
    'C7H8' : 9.0
}
# LFL index of gases
lfl_index = {
    'H2':4.0 / 100,
    'CO':12.5 / 100,
    'CH4':5.0 / 100,
    'C3H8':1.7 / 100,
    'C2H6':3.0 / 100,
    'C4H8O2' : 2.0 / 100,
    'C2H5OH' : 3.3 / 100,
    'C7H8' : 1.1 / 100
}
# UFL index of gases
ufl_index = {
    'H2':75.0 / 100,
    'CO':74.0 / 100,
    'CH4':15.0 / 100,
    'C3H8':9.5 / 100,
    'C2H6':12.4 / 100,
    'C4H8O2' : 11.5 / 100,
    'C2H5OH' : 19.0 / 100,
    'C7H8' : 7.1 / 100
}
# Inverse Ratio of O2 in Air (1/0.2095)
inv_mol_frac_air = 4.773