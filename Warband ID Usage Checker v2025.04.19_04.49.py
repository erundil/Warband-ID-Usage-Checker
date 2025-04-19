#-*-coding:utf-8-*-
#Make sure to give the same name to this *.py file and the *.bat file, then run the *.bat file.

#The main weakness of this program (other than its glacial speed) are ID names with = character in them.
#(Tons of that in vanilla string IDs - that's not allowed in IDs actually, and gets converted to underscore.)
#I recommend renaming those IDs, my program will count them as unused).
#As long as your IDs consist only of alphanumeric characters, it should work fine.
#As an exception capital letters (A-Z) and exclamation mark (!) are also expected in ID names.
#If any other characters are used, that could throw off the program (but also cause problems with the engine itself, so stick to alphanumeric please).

import os #standard file system operations
import sys #screen manipulation
import re #regex
import shutil #deleting folders that aren't empty
import math #math
path = "./" #same as our file

#read module files and clean them up from things that can throw off the search (comments, strings that contain #, etc.)
os.system('cls')
print "\
########################################################################################################################\n\
#\033[38;2;255;255;000mNOTICE:                                                                                                               \033[0m#\n\
#\033[38;2;255;255;000mThis program only searches for occurences of IDs in module files.                                                     \033[0m#\n\
#\033[38;2;255;255;000mIt doesn't search for unused constant declarations, unused mission trigger definitions, or other unused special code. \033[0m#\n\
#\033[38;2;255;255;000mMake sure to clean them from your module.constants.py, module.mission_templates.py and other files.                   \033[0m#\n\
#\033[38;2;255;255;000mIf you don't, it will throw off the search, and you will get false positives - unused IDs counted as used.            \033[0m#\n\
#\033[38;2;255;255;000mAlso notice that objects that aren't called by ID name can still be called by ID number, either using math            \033[0m#\n\
#\033[38;2;255;255;000mto shift through a range of IDs, or by calling the ID by numerical value (in vanilla happens a lot for trp_player=0). \033[0m#\n\
#\033[38;2;255;255;000mIn other words, \"not found\" doesn't necessarily mean \"unused\", so double-check before removing something.             \033[0m#\n\
########################################################################################################################\n\
#\033[38;2;064;160;255mTIP: To quickly check just 1 type of objects, temporarily move the other ID files out of the module system.           \033[0m#\
########################################################################################################################\n"
#determine mode of operation
use_subfolders = False
if not os.path.exists(path+"\\module_info.py"): #if module_info.py not found in same folder as this file
	use_subfolders = True
if not os.path.exists(path+"\\module\\info.py") and use_subfolders==True: #if module\info.py not found in same folder as this file
	print "\033[38;2;255;000;000mNO FILES TO WORK ON!\nPUT THIS FILE IN YOUR MODULE SYSTEM!\033[0m"
	exit(1)
#establish values to use
if use_subfolders==True:
	module_path = path+"\\module"
	id_path = path+"\\id"
	temp_path = path+"\\temp"
	out_path = path+"\\out"
	module_prefix = "module\\"
	id_prefix = "id\\"
	temp_prefix = "temp\\"
	out_prefix = "out\\"
	module_match_prefix = ""
	id_match_prefix = ""
	temp_match_prefix = ""
	info_on_finish = "\033[38;2;000;255;000mFINISHED.\033[0m Check the contents of the \"\\out\" folder for results."
else:
	module_path = path
	id_path = path
	temp_path = path
	out_path = path
	module_prefix = "module_"
	id_prefix = "ID_"
	temp_prefix = "temp_"
	out_prefix = "out_"
	module_match_prefix = "module_"
	id_match_prefix = "ID_"
	temp_match_prefix = "temp_"
	info_on_finish = "\033[38;2;000;255;000mFINISHED.\033[0m Check the out_*.py files for results."
done = "\033[38;2;000;255;000mDONE.\033[0m"
print "Creating temp files to work on... \033[38;2;255;000;000m0%\033[0m",
line_curr = -1 #indexing from 0 for better math
lines_max = len(os.listdir(module_path))
last_int_percent = 0
for module_filename in os.listdir(module_path):
	#count % to display
	line_curr += 1
	new_int_percent = int(100*line_curr/lines_max)
	if last_int_percent<new_int_percent:
		last_int_percent = new_int_percent
		print "\rCreating temp files to work on... \033[38;2;"+str(int(round(max(0,min(255.0*math.sqrt((100.0-last_int_percent)/50.0),255.0)))))+";"+str(int(round(max(0,min(255.0*math.sqrt(last_int_percent/50.0),255.0)))))+";000m"+str(last_int_percent)+"%\033[0m",
	module_matches = re.match(module_match_prefix+"(.+)\.py",module_filename) #the contents of the (1st and only) capture group can be retrieved with module_matches.group(1)
	if module_matches:
		#open module file
		module_file = open(module_prefix+module_matches.group(1)+".py","r") #open module file
		module_lines = module_file.readlines() #read its contents
		module_file.close() #close module file
		#write cleaned temp files (we want to remove everything that could throw off our search, like comments, and strings containing #, and if anything else is removable that will make the file smaller, then why not remove that too)
		if not os.path.exists(temp_path): os.makedirs(temp_path) #create folder
		temp_file = open(temp_prefix+module_matches.group(1)+".py","w") #open temp file
		temp_prev = ""
		line_break = "" #no line break before 1st line
		for temp_line in module_lines: #repeat for all lines
			temp_line = re.sub("\\n+","",temp_line) #remove the line break from the end, this will make it easier to search for \ at the ends of lines (Python seems to auto-convert \r\n to \n for the purpose of internal operations, and then store \n at the end of string, but ignore the \n at the end when printing the line to file)
			#deal with escaped characters that could throw off the search
			temp_line = re.sub("(\\\\\\\\)+"," ",temp_line) #remove escaped \ (replace with space, because this could only have happened in string that isn't an ID, and spaces are also not allowed in IDs) replace \\ using regex: (\\\\)+
			temp_line = re.sub("\\\\\""," ",temp_line) #remove escaped " (replace with space, because this could only have happened in string that isn't an ID, and spaces are also not allowed in IDs) replace \" using regex: \\"
			#merge with previous line
			temp_line=temp_prev+temp_line
			#remove comments - we can't split it into removing # from strings and then removing everything after the first found #, because regex #(?=[^"]*"(?:[^"]*"[^"]*")*[^"]*$) counts if the number of " after # is an odd number and fails on lines that have \ at the end splitting the string into multiple lines (and we can't just merge every line ending with \ with the next one, because if the line ends with a comment, \ does not split the comment into the 2nd line)
			temp_line_fragments = temp_line.split("\"") #split on each " - this produces a list in which strings alternate with stuff between strings, with delimiter " removed (if " starts the string, the 1st element after split will be an empty string, similar if it ends with ") - we will re-add the " when putting the line back together
			comment_reached = False
			comment_start_fragment = -1 #largest number that is a string of 9s that can fit in 32 bits
			for i in range(0,len(temp_line_fragments),2): #iterate over elements in range 0~len, incrementing by 2 (so only stuff between strings, ignoring what's in the strings)
				if re.match(".*#",temp_line_fragments[i]): #re.matches the given pattern with the beginning of string, so we need .*
					comment_reached = True #found a # that isn't in a string - this is where the comment starts
					temp_line_fragments[i] = re.sub("#.*","",temp_line_fragments[i]) #remove the comment
					comment_start_fragment = i #note to ignore further fragments
					break #leave loop
			if comment_reached: #comment found
				temp_line_fragments = temp_line_fragments[:comment_start_fragment+1] #truncate the list of fragments
			temp_line = "\"".join(temp_line_fragments) #merge fragments back into one string, adding " at the joining points (if there was " at the beginning of string, the 1st fragment would be an empty string, similar for " at the end, so we aren't losing data here)
			#deal with lines ending with \ (now that comments are removed, \ at the end of line always means continuation into next line)
			if re.match(".*\\\\$",temp_line): #regex is simply .*\\$ because we don't need to check if there is more than one consecutive \ since we've already dealth with escaped backslashes (and the .* is there because re.match matches the pattern to beginning of string)
				temp_prev = re.sub("\\\\$"," ",temp_line) #replace with space rather than just remove, to avoid creating something that could look like ID when this line gets merged with the next one
				continue
			else: temp_prev = ""
			temp_line = temp_line.strip() #remove leading and trailing whitespaces
			temp_line = re.sub("\\s+"," ",temp_line) #replace multiple consecutive whitespace characters with just 1 space (because they might have occured not only at the beginning or end) using regex: \s+
			if not re.match("^$",temp_line): #don't write empty lines (we don't check if it has whitespace characters, because those are already eliminated)
				temp_file.write(str(line_break+temp_line))
				line_break = "\n" #will be added before next line
		#end of loop through all lines in temp_file, deal with leftovers in temp_prev if there are any
		if not temp_prev=="": #flush temp_prev if no further lines exist (this shouldn't normally happen, but might)
			temp_prev = temp_prev.strip() #remove leading and trailing whitespaces
			temp_prev = re.sub("\\s+"," ",temp_prev) #replace multiple consecutive whitespace characters with just 1 space (because they might have occured not only at the beginning or end) using regex: \s+
			temp_file.write(str(line_break+temp_prev))
		temp_file.close()
		if os.path.getsize(temp_prefix+module_matches.group(1)+".py")==0: #we can't refer to temp_file variable, we have to refer to the actual file on the disk
			os.remove(temp_prefix+module_matches.group(1)+".py")
print "\rCreating temp files to work on... "+done
print "\n------------------------------------------------------------------------------------------------------------------------\n"
#read ID files, and for each ID do a search in temp files for occurences
if not os.path.exists(out_path): os.makedirs(out_path) #create folder
overwrite_prev_prnt = False
for id_filename in os.listdir(id_path):
	id_matches = re.match(id_match_prefix+"(.+)\.py",id_filename) #the contents of the (1st and only) capture group can be retrieved with id_matches.group(1)
	if id_matches:
		#open ID file
		id_file = open(id_prefix+id_matches.group(1)+".py","r")
		id_lines = id_file.readlines() #read its contents
		id_file.close()
		#write out file with the results
		out_file = open(out_prefix+id_matches.group(1)+".py","w") #open out file
		if overwrite_prev_prnt==False:
			print "Searching for IDs from: "+id_filename+"... \033[38;2;255;000;000m0%\033[0m",
		else:
			print "\r                                                                                                                       ", #clear the line
			print "\rSearching for IDs from: "+id_filename+"... \033[38;2;255;000;000m0%\033[0m",
		line_break = "" #no line break before 1st line
		line_curr = -1 #indexing from 0 for better math
		lines_max = len(id_lines)
		last_int_percent = 0
		for id_line in id_lines: #repeat for all lines
			#count % to display
			line_curr += 1
			new_int_percent = int(100*line_curr/lines_max)
			if last_int_percent<new_int_percent:
				last_int_percent = new_int_percent
				print "\rSearching for IDs from: "+id_filename+"... \033[38;2;"+str(int(round(max(0,min(255.0*math.sqrt((100.0-last_int_percent)/50.0),255.0)))))+";"+str(int(round(max(0,min(255.0*math.sqrt(last_int_percent/50.0),255.0)))))+";000m"+str(last_int_percent)+"%\033[0m",
			#prepare for actual searching
			id_line = re.sub("\\n+","",id_line) #remove the line break from the end
			id_line_matches = re.match("^([^\\s=]+)\\s*=\\s*(\\d+)\\s*(?:$|;|#)",id_line) #start of line, id name = id number, and then either end of line ($), comment (#) or next command (;) - all of that with whitespace possible inbetween
			if not id_line_matches: continue #this line doesn't contain ID (possibly comment, or empty, or some other code)
			id_name =   id_line_matches.group(1) #retrieve ID name from 1ˢᵗ capture group
			id_number = id_line_matches.group(2) #retrieve ID number from 2ⁿᵈ capture group (it's actually a string, not int)
			if re.match("^qsttag_",id_name): continue #don't search for questtags, no point
			if id_matches.group(1)=="game_menus": id_name = re.sub("^menu_","^mnu_",id_name) #correct menu_/mnu_ inconsistency
			if id_matches.group(1)=="mission_templates": id_name = re.sub("^mst_","^mt_",id_name) #correct mst_/mt_ inconsistency
			occurences = 0
			#search for IDs in all temp files
			for temp_filename in os.listdir(temp_path):
				temp_matches = re.match(temp_match_prefix+"(.+)\.py",temp_filename) #the contents of the (1st and only) capture group can be retrieved with temp_matches.group(1)
				if temp_matches:
					temp_file = open(temp_prefix+temp_matches.group(1)+".py","r")
					temp_lines = temp_file.readlines() #read its contents
					temp_file.close()
					for temp_line in temp_lines: #repeat for all lines
						occurences += len(re.findall("(?<![a-z0-9_A-Z!])"+id_name+"(?![a-z0-9_A-Z!])",temp_line))
			#construct output line
			out_line = str(occurences)+"\toccurences of\t"+id_name+"\t=\t"+id_number
			#print "\n"+out_line, #this would write to console what we are writing to file, uncommenting it will break the % display and make the console output a bit chaotic
			#write comments at the ends of appropriate lines (some IDs are hardcoded by ID number, meaning the game engine will use the nᵗʰ element, numbering from zero, while other IDs are hardcoded by ID name, and some are even hardcoded by both)
			comment = ""
			id_number = int(id_number) #from now on more useful as int
			#id_name = e.g. script_game_start   id_number = e.g. 0   id_matches.group(1) - e.g. scripts
			#animations: all are hardcoded
			if id_matches.group(1)=="animations": comment = "\t#all animations are hardcoded by ID number"
			#dialogs: can't check, no ID file is produced
			#factions:
			elif id_matches.group(1)=="factions" and id_number<3: comment = "\t#hardcoded by numer"
			#info_pages: nothing hardcoded
			#items:
			elif id_matches.group(1)=="items":
				if   id_number== 0: comment = "\t#hardcoded by ID number"
				elif id_number==16:
					if occurences>0: comment = "\t#not hardcoded, unless you enabled food slot in module.ini (it doesn't function well, so don't), in which case this item should be Horse Meat, because this is what game engine turns a horse into, if you put it into the food slot"
					elif occurences==0: comment = "\t#feel free to remove it, unless it's referenced in SCO files, or you have the food slot enabled in module.ini (it doesn't function well, so don't), in which case this item should be Horse Meat, because this is what game engine turns a horse into, if you put it into the food slot"
			#map_icons: nothing hardcoded
			#menus:
			elif id_matches.group(1)=="menus" and id_number<5:
				if   id_number==0:        comment = "\t#hardcoded by ID number - this menu opens after clicking New Game in main menu, reusable if you disabled singleplayer in module.ini"
				elif id_number==1:        comment = "\t#hardcoded by ID number - this menu opens after creating our character (stats, name and face), reusable if you disabled singleplayer in module.ini"
				elif id_number==2:        comment = "" #used to be hardcoded for Custom Battle in original M&B, but in WB Custom Battle button in main menu directs to prsnt_game_custom_battle_designer instead
				elif id_number==3:        comment = "\t#hardcoded by ID number - this menu opens after clicking Tutorial in main menu, reusable if you disabled tutorial in module.ini"
				elif id_number==4:        comment = "\t#hardcoded by ID number - this menu opens after clicking Reports button in singleplayer, reusable if you disabled singleplayer in module.ini"
				elif id_name=="mnu_camp": comment = "\t#hardcoded by ID name - this menu opens after clicking Camp button in singleplayer, reusable if you disabled singleplayer in module.ini"
			#meshes:
			elif id_matches.group(1)=="meshes":
				hardcoded_by_name = ["mesh_main_menu_background","mesh_loading_background",]
				if id_name in hardcoded_by_name: comment = "\t#hardcoded by ID name"
			#mission_templates:
			elif id_matches.group(1)=="mission_templates" and id_number<2: comment = "\t#hardcoded by ID number"
			#music: 3 tracks (most likely) hardcoded by ID name, see hardcoded_by_name list
			elif id_matches.group(1)=="music":
				hardcoded_by_name = ["track_bogus","track_mount_and_blade_title_screen","track_ambushed_by_neutral"]
				if id_name in hardcoded_by_name: comment = "\t#hardcoded by ID name"
			#particle_systems:
			elif id_matches.group(1)=="particle_systems":
				hardcoded_by_name = ["psys_game_rain","psys_game_snow","psys_game_blood","psys_game_blood_2","psys_game_hoof_dust","psys_game_hoof_dust_snow","psys_game_hoof_dust_mud","psys_game_water_splash_1","psys_game_water_splash_2","psys_game_water_splash_3"]
				if id_number<10 or id_name in hardcoded_by_name: comment = "\t#most likely hardcoded (both by ID number and ID name)"
			#parties:
			elif id_matches.group(1)=="parties":
				hardcoded_by_name = ["p_main_party","p_temp_party","p_camp_bandits"]
				if id_number<3 or id_name in hardcoded_by_name: comment = "\t#hardcoded by ID name and ID number"
			#party_templates:
			elif id_matches.group(1)=="party_templates" and id_number<4: comment = "\t#hardcoded by ID number"
			#postfx_params:
			elif id_matches.group(1)=="postfx_params":
				if id_number==0:              comment = "\t#might be hardcoded by ID number, better leave it as it is"
				if id_name=="pfx_map_params": comment = "\t#hardcoded by ID name, used for world map"
				if id_name=="pfx_indoors":    comment = "\t#hardcoded by ID name, used for indoor scenes"
				elif occurences==0:           comment = "\t#might be referenced by ID name by skyboxes"
			#presentations:
			elif id_matches.group(1)=="presentations":
				hardcoded_by_name = ["prsnt_game_escape","prsnt_game_credits","prsnt_game_profile_banner_selection","prsnt_game_custom_battle_designer","prsnt_game_multiplayer_admin_panel","prsnt_game_before_quit"]
				if id_name=="prsnt_game_start": comment = "\t#hardcoded by ID number and ID name"
				if id_name in hardcoded_by_name: comment = "\t#hardcoded by ID name"
			#quests: nothing hardcoded
			#scene_props:
			elif id_matches.group(1)=="scene_props":
				if id_number==0:    comment = "\t#hardcoded by ID number"
				elif occurences==0: comment = "\t#might still be referenced by ID name in SCO files"
			#scenes:
			elif id_matches.group(1)=="scenes":
				hardcoded_by_name = ["scn_random_scene","scn_conversation_scene","scn_random_scene_steppe","scn_random_scene_plain","scn_random_scene_snow","scn_random_scene_desert","scn_random_scene_steppe_forest","scn_random_scene_plain_forest","scn_random_scene_snow_forest","scn_random_scene_desert_forest"]
				if id_name in hardcoded_by_name: comment = "\t#hardcoded by ID name, requires SCO file of the same name to work"
				elif occurences>0: comment = "\t#requires SCO file of the same name to work"
			#scripts:
			elif id_matches.group(1)=="scripts":
				hardcoded_by_name = ["script_game_start","script_game_quick_start","script_game_set_multiplayer_mission_end","script_game_get_use_string","script_game_enable_cheat_menu","script_game_event_party_encounter","script_game_event_simulate_battle","script_game_event_battle_end","script_game_get_item_buy_price_factor","script_game_get_item_sell_price_factor","script_game_event_buy_item","script_game_event_sell_item","script_game_get_troop_wage","script_game_get_total_wage","script_game_get_join_cost","script_game_get_upgrade_xp","script_game_get_upgrade_cost","script_game_get_prisoner_price","script_game_check_prisoner_can_be_sold","script_game_get_morale_of_troops_from_faction","script_game_event_detect_party","script_game_event_undetect_party","script_game_get_statistics_line","script_game_get_date_text","script_game_get_money_text","script_game_get_party_companion_limit","script_game_reset_player_party_name","script_game_get_troop_note","script_game_get_center_note","script_game_get_faction_note","script_game_get_quest_note","script_game_get_info_page_note","script_game_get_scene_name","script_game_get_mission_template_name","script_game_receive_url_response","script_game_get_cheat_mode","script_game_receive_network_message","script_game_get_multiplayer_server_option_for_mission_template","script_game_multiplayer_server_option_for_mission_template_to_string","script_game_multiplayer_event_duel_offered","script_game_get_multiplayer_game_type_enum","script_game_multiplayer_get_game_type_mission_template","script_game_get_party_prisoner_limit","script_game_get_item_extra_text","script_game_on_disembark","script_game_context_menu_get_buttons","script_game_event_context_menu_button_clicked","script_game_get_skill_modifier_for_troop","script_game_check_party_sees_party","script_game_get_party_speed_multiplier","script_game_get_console_command","script_game_missile_launch","script_game_missile_dives_into_water","script_game_troop_upgrades_button_clicked","script_game_character_screen_requested","script_add_troop_to_cur_tableau","script_add_troop_to_cur_tableau_for_character","script_add_troop_to_cur_tableau_for_inventory","script_add_troop_to_cur_tableau_for_profile","script_add_troop_to_cur_tableau_for_party"]
				if id_name in hardcoded_by_name: comment = "\t#hardcoded by ID name"
			#simple_triggers: nothing hardcoded, and has no ID file
			#skills:
			elif id_matches.group(1)=="skills": comment = "\t#hardcoded by ID number"
			#skins: has no ID file
			#sounds:
			elif id_matches.group(1)=="sounds":
				hardcoded_by_name = ["snd_click","snd_gong","snd_quest_taken","snd_quest_completed","snd_quest_succeeded","snd_quest_concluded","snd_quest_failed","snd_quest_cancelled","snd_hide","snd_unhide","snd_money_received","snd_money_paid","snd_gallop","snd_battle","snd_sword_clash_1","snd_sword_clash_2","snd_sword_clash_3","snd_sword_swing","snd_draw_sword","snd_put_back_sword","snd_draw_greatsword","snd_put_back_greatsword","snd_draw_axe","snd_put_back_axe","snd_draw_greataxe","snd_put_back_greataxe","snd_draw_spear","snd_put_back_spear","snd_draw_crossbow","snd_put_back_crossbow","snd_draw_revolver","snd_put_back_revolver","snd_draw_dagger","snd_put_back_dagger","snd_draw_bow","snd_put_back_bow","snd_draw_shield","snd_put_back_shield","snd_draw_other","snd_put_back_other","snd_hit_wood_wood","snd_hit_metal_metal","snd_hit_wood_metal","snd_block_fist","snd_metal_hit_low_armor_low_damage","snd_metal_hit_low_armor_high_damage","snd_metal_hit_high_armor_low_damage","snd_metal_hit_high_armor_high_damage","snd_wooden_hit_low_armor_low_damage","snd_wooden_hit_low_armor_high_damage","snd_wooden_hit_high_armor_low_damage","snd_wooden_hit_high_armor_high_damage","snd_man_hit_blunt_weak","snd_man_hit_blunt_strong","snd_man_hit_pierce_weak","snd_man_hit_pierce_strong","snd_man_hit_cut_weak","snd_man_hit_cut_strong","snd_blunt_hit","snd_shield_hit_wood_wood","snd_shield_hit_metal_metal","snd_shield_hit_wood_metal","snd_shield_hit_metal_wood","snd_shield_broken","snd_footstep_grass","snd_footstep_wood","snd_footstep_water","snd_jump_begin","snd_jump_end","snd_jump_begin_water","snd_jump_end_water","snd_horse_walk","snd_horse_trot","snd_horse_canter","snd_horse_gallop","snd_footstep_horse","snd_footstep_horse_1b","snd_footstep_horse_1f","snd_footstep_horse_2b","snd_footstep_horse_2f","snd_footstep_horse_3b","snd_footstep_horse_3f","snd_footstep_horse_4b","snd_footstep_horse_4f","snd_footstep_horse_5b","snd_footstep_horse_5f","snd_horse_jump_begin","snd_horse_jump_end","snd_horse_jump_begin_water","snd_horse_jump_end_water","snd_reload_crossbow","snd_reload_crossbow_continue","snd_pull_bow","snd_pull_arrow","snd_release_bow","snd_release_crossbow","snd_release_crossbow_medium","snd_release_crossbow_far","snd_throw_javelin","snd_throw_axe","snd_throw_knife","snd_throw_stone","snd_pistol_shot","snd_bullet_hit_body","snd_player_hit_by_bullet","snd_arrow_hit_body","snd_player_hit_by_arrow","snd_mp_arrow_hit_target","snd_arrow_pass_by","snd_bolt_pass_by","snd_javelin_pass_by","snd_stone_pass_by","snd_axe_pass_by","snd_knife_pass_by","snd_bullet_pass_by","snd_incoming_arrow_hit_ground","snd_incoming_bolt_hit_ground","snd_incoming_javelin_hit_ground","snd_incoming_stone_hit_ground","snd_incoming_axe_hit_ground","snd_incoming_knife_hit_ground","snd_incoming_bullet_hit_ground","snd_outgoing_arrow_hit_ground","snd_outgoing_bolt_hit_ground","snd_outgoing_javelin_hit_ground","snd_outgoing_stone_hit_ground","snd_outgoing_axe_hit_ground","snd_outgoing_knife_hit_ground","snd_outgoing_bullet_hit_ground","snd_body_fall_small","snd_body_fall_big","snd_horse_body_fall_begin","snd_horse_body_fall_end","snd_man_grunt","snd_man_breath_hard","snd_man_stun","snd_man_grunt_long","snd_man_yell","snd_man_warcry","snd_man_victory","snd_man_hit","snd_man_die","snd_woman_hit","snd_woman_die","snd_woman_yell","snd_horse_breath","snd_horse_snort","snd_horse_low_whinny","snd_neigh","snd_rain"]
				if id_name in hardcoded_by_name: comment = "\t#hardcoded by ID name"
			#strings:
			elif id_matches.group(1)=="strings" and id_number<4: comment = "\t#hardcoded by ID number (possibly also by ID name)"
			#tableau_materials:
			elif id_matches.group(1)=="tableau_materials":
				hardcoded_by_name = ["tableau_game_character_sheet","tableau_game_inventory_window","tableau_game_profile_window","tableau_game_party_window","tableau_game_troop_label_banner"]
				if id_name in hardcoded_by_name: comment = "\t#hardcoded by ID name"
			#triggers: nothing hardcoded, and has no ID file
			#troops:
			elif id_matches.group(1)=="troops" and id_number<4:
				if   id_number==0: comment = "\t#hardcoded by ID number, but reusable in multiplayer"
				elif id_number==1: comment = "\t#hardcoded by ID number, but reusable in singleplayer"
				elif id_number==2: comment = "\t#hardcoded by ID number, but reusable in singleplayer"
				elif id_number==3: comment = "\t#hardcoded by ID number"
			#apply comment to line and write it
			out_line = out_line+comment
			out_file.write(line_break+out_line)
			line_break = "\n" #will be added before next line
		out_file.close()
		if os.path.getsize(out_prefix+id_matches.group(1)+".py")==0: #we can't refer to out_file variable, we have to refer to the actual file on the disk
			overwrite_prev_prnt = True
			os.remove(out_prefix+id_matches.group(1)+".py")
		else:
			overwrite_prev_prnt = False
			print "\rSearching for IDs from: "+id_filename+"... "+done
if overwrite_prev_prnt==True:
	print "\r                                                                                                                       ", #clear the line
print "\n------------------------------------------------------------------------------------------------------------------------\n"
#remove temp files
print "Removing temp files... \033[38;2;255;000;000m0%\033[0m",
if use_subfolders==True:
	shutil.rmtree(temp_prefix,ignore_errors=True)
else:
	for filename in os.listdir(path):
		if re.match(temp_prefix+".+\.py",filename):
			os.remove(filename)
print "\rRemoving temp files... "+done
print "\n------------------------------------------------------------------------------------------------------------------------\n"
#show info on finish
print info_on_finish