from tissus import Tissus
from point_matcher import Point_matcher
from stats import Stats
from helper import CsvWriter
from dash_app import dash_scatter
from draw_graph import Graph

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e','--ecru', help='chemin vers le csv de l\'ecru', required=False)
parser.add_argument('-f','--fini', help='chemin vers le csv du produit fini', required=False)
parser.add_argument('-vOff','--vertical-offset', help='déplace verticalement tous les défauts du tissus traité de la valeur indiquée. Si laissé blanc,sera calculé automatiquement', required=False)
parser.add_argument('-hOff','--horizontal-offset', help='déplace verticalement tous les défauts du tissus traité de la valeur indiquée.', required=False)
parser.add_argument('-long','--long-param', help='facteur à appliquer dans la longueur.Si laissé blanc,sera calculé automatiquement', required=False)
parser.add_argument('-haut','--haut-param', help='facteur à appliquer dans la hauteur.Si laissé blanc,sera calculé automatiquement', required=False)
parser.add_argument('-r','--rotation', help='rotation du tissus traité.Si laissé blanc,sera calculé automatiquement.Valeur attendue parmi :{no,flip,invert,flip+invert}', required=False)
parser.add_argument('-che','--cut-hauteur-ecru', help='largeur à supprimer de tissus de part et d\'autre de l\'ecru dans la hauteur', required=False)
parser.add_argument('-chf','--cut-hauteur-fini', help='épaisseur à supprimer de tissus de part et d\'autre du produit fini dans la hauteur', required=False)
parser.add_argument('-cle','--cut-longueur-ecru', help='épaisseur à supprimer de tissus de part et d\'autre de l\'ecru dans la hauteur', required=False)
parser.add_argument('-clf','--cut-longueur-fini', help='épaisseur à supprimer de tissus de part et d\'autre du produit fini dans la hauteur', required=False)
args = parser.parse_args()

args.ecru = "Matching/31/output_final_tdm_31.csv"
args.fini = "Matching/31/output_final_tsj_F31.csv"
args.horizontal_offset=11
# args.cut_hauteur_ecru=30
# args.cut_longueur_fini=100
# args.cut_longueur_ecru=100
ecru_name = args.ecru
traite_name = args.fini
ecru=Tissus(ecru_name)
traite=Tissus(traite_name)

traite.remove_duplicates()

ecru.remove_duplicates()

if args.rotation:
    traite.rotate(args.rotation)
else:
    args.rotation =Point_matcher.find_orientation(ecru,traite)
    traite.rotate(args.rotation)

if args.horizontal_offset:
    traite.move_defects_for_broken_cam(0,int(args.horizontal_offset)) #pour TDM/TSJ 31 : 0,+11 (-11 ecru)

if args.cut_hauteur_ecru:
    ecru.cut_hauteur(int(args.cut_hauteur_ecru))

if args.cut_longueur_ecru:
    ecru.cut_longueur(int(args.cut_longueur_ecru))

if args.cut_hauteur_fini:
    traite.cut_hauteur(int(args.cut_hauteur_ecru))

if args.cut_longueur_fini:
    traite.cut_longueur(int(args.cut_longueur_ecru))
params=Point_matcher.find_best_match(ecru,traite,args.vertical_offset,args.long_param,args.haut_param)

origin = params[0]
traite.move_origin(origin)
traite.moveData(params[1],params[2])
match,not_match_ecru=Point_matcher.find_corresponding_defect_list(ecru,traite)
# not_match_traite=Point_matcher.find_corresponding_defect_list(traite,ecru,1)[1]

# figure=Graph.draw(match[:,0,:],match[:,1,:])
# Graph.draw(no_match)
stats=Stats(ecru,traite)
# print(stats. qualif_comparison())
print("rotation : ",args.rotation)
print("paramètres superposition : ",params)
print("Taux de rétention des défauts : ", stats.staying_rates())
print("Défauts apparus : ", stats.appearing_defects())


# CsvWriter.create_unduplicated_csv(ecru,traite)
# CsvWriter.create_matching_csv(stats.match,ecru,traite)
# CsvWriter.create_not_matching_csv(stats.not_match_ecru,stats.not_match_traite,ecru,traite)
figure=Graph.draw(ecru.data,traite.data,traite_name,args.rotation,long_tot=ecru.long_tot,larg_tot=ecru.larg_tot)
figure2=Graph.draw(match[:,0,:],match[:,1,:],long_tot=ecru.long_tot,larg_tot=ecru.larg_tot)

dash_scatter(figure,ecru,traite,stats,figure2).run_server(debug=True)

