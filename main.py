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
parser.add_argument('-che','--cut-hauteur-ecru', help='largeur à supprimer du tissus de part et d\'autre de l\'ecru dans la hauteur', required=False)
parser.add_argument('-chf','--cut-hauteur-fini', help='épaisseur à supprimer du tissus de part et d\'autre du produit fini dans la hauteur', required=False)
parser.add_argument('-cle','--cut-longueur-ecru', help='épaisseur à supprimer du tissus de part et d\'autre de l\'ecru dans la hauteur', required=False)
parser.add_argument('-clf','--cut-longueur-fini', help='épaisseur à supprimer du tissus de part et d\'autre du produit fini dans la hauteur', required=False)
args = parser.parse_args()


args.ecru = "Matching/27/03 389902-27.csv"
args.fini = "Matching/27/03 389902_74582-2537.csv"
# args.cut_hauteur_ecru=100
# args.horizontal_offset=11
# args.long_param=1.05
# args.haut_param=1.086
# args.vertical_offset=72
# args.rotation="invert"
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
# params=129, 1.0499999999999978, 1.0439999999999985
params=Point_matcher.find_best_match(ecru,traite,args.vertical_offset,args.long_param,args.haut_param)

origin = params[0]
traite.move_origin(origin)
traite.moveData(params[1],params[2])
match=Point_matcher.find_corresponding_defect_list(ecru,traite,1)[0]
# figure=Graph.draw(match[:,0,:],match[:,1,:])
# Graph.draw(no_match)
stats=Stats(ecru,traite)
# print(stats. qualif_comparison())
print("rotation : ",args.rotation)
print("paramètres superposition : ",params)
print("Taux de rétention des défauts : ", stats.staying_rates())

CsvWriter.create_unduplicated_csv(ecru,traite)
CsvWriter.create_matching_csv(match,ecru,traite)

figure=Graph.draw(ecru.data,traite.data,traite_name,args.rotation)


dash_scatter(figure,ecru,traite,stats).run_server(debug=True)

