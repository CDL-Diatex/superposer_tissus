import csv
# def create_csv_matching(matching,ecru,traite):
#     with open("ecru_matching.csv","w") as ecru_m, open("traite_matching.csv","w") as traite_m:
#         for match in matching:
#
class CsvWriter:

    @staticmethod
    def create_unduplicated_csv(ecru,traite):
        with open(ecru.dataframe["id"].iloc[0].strip('\'')+"-"+str(ecru.dataframe["roule"].iloc[0])+".csv","w",newline='') as ecru_u, open(traite.dataframe["id"].iloc[0].strip('\'')+"-"+str(traite.dataframe["roule"].iloc[0])+".csv","w",newline='') as traite_u:
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

    def create_matching_csv(matching,ecru,traite):
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




