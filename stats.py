from point_matcher import Point_matcher
import math


class Stats:

    def __init__(self, ecru, traite):
        self.match, self.no_match = Point_matcher.find_corresponding_defect_list(ecru, traite, 2)[0], \
                                    Point_matcher.find_corresponding_defect_list(ecru, traite, 2)[1]
        self.ecru = ecru
        self.traite = traite
        if self.match.any():
            if math.isnan(
                    self.match[0, 0, 3]):  # si les défauts d'écru ont été requalifés c'est la colonne 2 sinon la 3
                self.defect_qualification_col = 2
            else:
                self.defect_qualification_col = 3
            self.defect_categories = len(ecru.data[:, self.defect_qualification_col])

    def total_amount_defect(self, category):
        tot = 0
        for defect in self.ecru.data:
            if defect[self.defect_qualification_col] == category:
                tot += 1
        return tot

    def staying_rates(self):  # calcule,pour chaque type de défaut, le taux qui reste après traitement
        rates = {}
        if not self.match.any():  # si aucun défaut n'est resté
            return rates
        for def_category in set(self.ecru.data[:, self.defect_qualification_col]):  # pour chaque catégorie de défaut
            rates[def_category] = [0, 0]
            for defect_couple in self.match:  # pour chaque couple de défaut qui matchent
                if defect_couple[0, self.defect_qualification_col] == def_category:  # on prend le type de défaut écru
                    rates[def_category][0] += 1
            rates[def_category][1] = self.total_amount_defect(def_category)
            if self.total_amount_defect(def_category) != 0:
                rates[def_category][0] = rates[def_category][0] / rates[def_category][1]
            else:
                print("no defect in category " + str(def_category))
                rates[def_category][0] = 0
        return rates

    def qualif_comparison(
            self):  # compares the qualif of the matching results. Ne marche que pour les défauts requalifiés
        corresp = {1: [13, 24], 2: [26, 28, 15], 3: [29, 27, 15]}
        rates = {}
        for def_category in corresp.keys():
            tot = 0
            corresp_amount = 0
            for defect_couple in self.match:
                if defect_couple[0, 3] == def_category:
                    tot += 1
                    if defect_couple[1, 2] in corresp[def_category]:
                        corresp_amount += 1
            if corresp_amount == 0:
                rates[def_category] = 0
            else:
                rates[def_category] = corresp_amount / tot
        return rates
