import csv
# def create_csv_matching(matching,ecru,traite):
#     with open("ecru_matching.csv","w") as ecru_m, open("traite_matching.csv","w") as traite_m:
#         for match in matching:
#
class CsvWriter:

    @staticmethod
    def create_unduplicated_csv(ecru,traite): #ecris le CSV des défauts après la suppression des duplicata et l'application des paramètres pour la superposition pour le produit fini.
        with open(ecru.dataframe["id"].iloc[0].strip('\'')+"-"+str(ecru.dataframe["roule"].iloc[0])+"-UD.csv","w",newline='') as ecru_u, open(traite.dataframe["id"].iloc[0].strip('\'')+"-"+str(traite.dataframe["roule"].iloc[0])+"-UD.csv","w",newline='') as traite_u:
            ecru_writer = csv.writer(ecru_u)
            traite_writer=csv.writer(traite_u)
            for defect in ecru.data:
                original_line=ecru.dataframe.loc[ecru.dataframe["image"]==defect[4]].values.tolist()[0] #on utilise le numéro d'image comme identifiant pour retrouver toutes les infos liees au défaut
                original_line[10],original_line[11]=round(defect[0],3),round(defect[1],3)#on met a jour les données qui ont changé(la position)
                ecru_writer.writerow(original_line)
            for defect in traite.data:
                original_line=traite.dataframe.loc[traite.dataframe["image"]==defect[4]].values.tolist()[0] #on utilise le numéro d'image comme identifiant pour retrouver toutes les infos liees au défaut
                original_line[10],original_line[11]=round(defect[0],3),round(defect[1],3)#on met a jour les données qui ont changé(la position)
                traite_writer.writerow(original_line)


    @staticmethod
    def create_matching_csv(matching,ecru,traite): #écris les deux csv recensant les défauts d'écru et de de produit fini qui matchent. Par exemple Le défaut ligne 11 du csv écru correpond au défaut ligne 11 du csv du produit fini
        with open(ecru.dataframe["id"].iloc[0].strip('\'')+"-"+str(ecru.dataframe["roule"].iloc[0])+"-M.csv","w",newline='') as ecru_m, open(traite.dataframe["id"].iloc[0].strip('\'')+"-"+str(traite.dataframe["roule"].iloc[0])+"-M.csv","w",newline='') as traite_m:
            ecru_writer = csv.writer(ecru_m)
            traite_writer=csv.writer(traite_m)
            for match in matching:
                original_ecru_line=ecru.dataframe.loc[ecru.dataframe["image"]==int(match[0][4])].values.tolist()[0] #on utilise le numéro d'image comme identifiant pour retrouver toutes les infos liees au défaut
                original_traite_line=traite.dataframe.loc[traite.dataframe["image"]==int(match[1][4])].values.tolist()[0] #on utilise le numéro d'image comme identifiant pour retrouver toutes les infos liees au défaut
                original_ecru_line[10],original_ecru_line[11]=round(match[0][0],3),round(match[0][1],3)#on met a jour les données qui ont changé(la position)
                original_traite_line[10],original_traite_line[11]=round(match[1][0],3),round(match[1][1],3)#on met a jour les données qui ont changé(la position)
                ecru_writer.writerow(original_ecru_line)
                traite_writer.writerow(original_traite_line)

    @staticmethod
    def create_not_matching_csv(not_match_e,not_match_t,ecru,traite): #écris les deux csv recensant les défauts d'écru et de de produit fini qui matchent. Par exemple Le défaut ligne 11 du csv écru correpond au défaut ligne 11 du csv du produit fini
        with open(ecru.dataframe["id"].iloc[0].strip('\'')+"-"+str(ecru.dataframe["roule"].iloc[0])+"-NM.csv","w",newline='') as ecru_m, open(traite.dataframe["id"].iloc[0].strip('\'')+"-"+str(traite.dataframe["roule"].iloc[0])+"-NM.csv","w",newline='') as traite_m:
            ecru_writer = csv.writer(ecru_m)
            traite_writer=csv.writer(traite_m)
            for defect in not_match_e:
                original_line=ecru.dataframe.loc[ecru.dataframe["image"]==defect[4]].values.tolist()[0] #on utilise le numéro d'image comme identifiant pour retrouver toutes les infos liees au défaut
                original_line[10],original_line[11]=round(defect[0],3),round(defect[1],3)#on met a jour les données qui ont changé(la position)
                ecru_writer.writerow(original_line)
            for defect in not_match_t:
                original_line=traite.dataframe.loc[traite.dataframe["image"]==defect[4]].values.tolist()[0] #on utilise le numéro d'image comme identifiant pour retrouver toutes les infos liees au défaut
                original_line[10],original_line[11]=round(defect[0],3),round(defect[1],3)#on met a jour les données qui ont changé(la position)
                traite_writer.writerow(original_line)


