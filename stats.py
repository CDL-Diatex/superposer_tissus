class Stats:
    def __init__(self,match,not_match,ecru):
        self.match=match
        self.not_match=not_match
        self.ecru=ecru
        self.defect_categories=len(ecru.data[:,3])
    def total_amount_defect(self,category):
        tot = 0
        for defect in self.ecru.data:
            if defect[3]==category:
                tot+=1
        return tot

    def staying_rates(self):
        rates={}
        for def_category in set(self.ecru.data[:,3]):
            rates[def_category]=[0,0]
            for defect_couple in self.match:
                if defect_couple[0,3]==def_category: #on prend le type de défaut écru
                    rates[def_category][0]+=1
                    rates[def_category][1]+=1
            rates[def_category][0]=rates[def_category][0]/self.total_amount_defect(def_category)
        return rates

    def qualif_comparison(self): #compares the qualif of the matching results
        corresp = {1: [13,24], 2: [26,28,15],3 :[29,27,15]}
        rates={}
        for def_category in corresp.keys():
            tot=0
            corresp_amount=0
            for defect_couple in self.match:
                if defect_couple[0,3]==def_category:
                    tot+=1
                    if defect_couple[1,2] in corresp[def_category]:
                        corresp_amount+=1
            if corresp_amount==0:
                rates[def_category]=0
            else:
                rates[def_category]=corresp_amount/tot
        return rates