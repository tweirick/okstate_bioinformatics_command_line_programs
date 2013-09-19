#!/bin/bash
#This script will parse data out of the html files contained in the directories described below. 
#This is to help keep track of the conditions. 
                                  
                           
python3.2 mascot_parser_0.6.py --file_set "Proteins_bound_to_BG/*pradefinal.htm" --file_group_name "Proteins_bound_to_BG_1-7.dsv"

python3.2 mascot_parser_0.6.py --file_set "Cellulose_36_h/*pradefinal.htm" --file_group_name "Cellulose_36_h_8-13.dsv"

python3.2 mascot_parser_0.6.py --file_set "Xylan_+_Cellulose_36_h/*pradefinal.htm" --file_group_name "Xylan_p_Cellulose_36_h_14-19.dsv"

python3.2 mascot_parser_0.6.py --file_set "BG_no_hemi/*pradefinal.htm" --file_group_name "BG_no_hemi_20-25.dsv"

python3.2 mascot_parser_0.6.py --file_set "Cellulose_60_h/*pradefinal.htm" --file_group_name "Cellulose_60_h_26-31.dsv"

python3.2 mascot_parser_0.6.py --file_set "Xylan_+_Cellulose_36_h_Repeat/*pradefinal.htm" --file_group_name "Xylan_p_Cellulose_36_h_Repeat_42-47.dsv"

python3.2 mascot_parser_0.6.py --file_set "Xylan_36_h/*pradefinal.htm" --file_group_name "Xylan_36_h_48-53.dsv"

python3.2 mascot_parser_0.6.py --file_set "BG_Innatura/*pradefinal.htm" --file_group_name "BG_Innatura_54-59.dsv"

python3.2 mascot_parser_0.6.py --file_set "Cellulose_60_Repeat/*pradefinal.htm" --file_group_name "Cellulose_60_Repeat_60-65.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Fermentor_Avicel_Bound/*pradefinal.htm" --file_group_name "CF_AB_71-75.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Fermentor_Bagasse_Bound/*pradefinal.htm" --file_group_name "CF_BB_66-70.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Fermentor_raw/*pradefinal.htm" --file_group_name "CF_R_108-113.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Shaker_100ml_Avicel_Bound/*pradefinal.htm" --file_group_name "CS100ml_AB_91-95.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Shaker_100ml_Bagasse_Bound/*pradefinal.htm" --file_group_name "CS100ml_BB_86-90.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Shaker_100ml_raw/*pradefinal.htm" --file_group_name "CS100ml_R_102-107.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Shaker_500ml_Avicel_Bound/*pradefinal.htm" --file_group_name "CS500ml_AB_81-85.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Shaker_500ml_Bagasse_Bound/*pradefinal.htm" --file_group_name "CS500ml_BB_76-80.dsv"

python3.2 mascot_parser_0.6.py --file_set "Consortium_Shaker_500ml_raw/*pradefinal.htm" --file_group_name "CS500ml_R_96-100.dsv"

python3.2 mascot_parser_0.6.py --file_set "question_mark/*pradefinal.htm" --file_group_name "Qmark_114-119.dsv"

python3.2 mascot_parser_0.6.py --file_set "SOIL/*pradefinal.htm" --file_group_name "SOIL_120-126.dsv"
 