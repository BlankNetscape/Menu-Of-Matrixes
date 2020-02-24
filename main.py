import sys, os, curses, numpy as np
## My ######################
import cursedUI as cUI
import myMenu
import matrixCalc as mtrxC
############################
menu_all = []
# Input history
history = []
history_slots = 4
def addHistory(string):
    history.pop()
    # history.insert(0, str(string.decode("utf-8")))
    history.insert(0, str(string))
# Matrixes
mtrx_all = []
mtrx_all_slots = 3
# mtrx_my = [[],[]]
rows = 0
cols = 0
# Render
key = 0
focus = 0
# instr = ''
############################
for i in range(history_slots): history.append('')
for i in range(mtrx_all_slots): mtrx_all.append([])
## Menus ###################
menu_all.append(['Create matrix', 'Load matrix', 'Print slots', 'Save matrix', 'Replace matrix'])
menu_all.append(['Delta', 'Minor', 'Minor matrix', 'Cofactor', 'Inverse', 'Multiply by \'k\''])
menu_all.append(["Mltply by mtrx", "Sbstrct fr cur mtrx", "Add to cur mtrx"])
menu_all.append(["Settings", "Exit"])
############################
# menu_menu >>> length = max_item_len + arrow + 3
# menu_input >> default len >> 23
## Choises #################
def menu_chs(stdscr, start_x, start_y, menu_array, mtrx_all_slots, current_row, current_menu, step):
    global key, focus, instr, mtrx_all, mtrx_my
    
    ## Menu 0 ########################
    if current_menu == 0: ### MENU 0 #
        ## Create matrix # Step 0 ####
        if current_row == 0 and step == 0: # Create matrix
            focus = 1
        ## Create matrix # Step 1 ####
        if current_row == 0 and step == 1:
            # Get ROWS ###############
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter rows(>1): ]")
            rows = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            rows = rows.decode("utf-8")
            addHistory(rows)
            # Get COLS ###############
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter cols(>1): ]")
            cols = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            cols = cols.decode("utf-8")
            addHistory(cols)
            # Get ENTRIES ############
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enties by rows({} items): ]".format(int(cols) * int(rows)))
            entr = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            entr = entr.decode("utf-8")
            addHistory(entr)
            entr = list(map(int, entr.split()))
            # Get SAVE ACT SLOT ######
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            addHistory(to_slot)
            # to ACTIVE SLOT #########
            mtrx_all[int(to_slot)] = mtrxC.toMatrix(int(rows), int(cols), entr)
            stdscr.refresh() 
        ## Load matrix # Step 0 ######
        if current_row == 1 and step == 0: # Load matrix
            focus = 1
        if current_row == 1 and step == 1:
            # Get SAVE SLOT ##########
            slotID = print_slot(stdscr, 'write')
            slotID = slotID.decode("utf-8")
            # Render after clear #####
            cUI.menu_list(stdscr, start_x, start_y, menu_all, current_row, current_menu, 99)
            cUI.menu_input(stdscr, start_x, start_y, history, 99)
            cUI.menu_mtrxs(stdscr, start_x, start_y, mtrx_all, mtrx_all_slots, 99 )
            # Get ACTIVE SLOT ########
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[  Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            # reassign by LOAD #######
            mtrx_all[int(to_slot)] = mtrxC.loadMatrix(slotID)
        ## Print matrix # Step 0 #####
        if current_row == 2 and step == 0: # Print matrix
            focus = 1
        if current_row == 2 and step == 1:
            print_slot(stdscr, 'show')
        ## Save matrix # Step 0 ######
        if current_row == 3 and step == 0:
            focus = 1
        if current_row == 3 and step == 1:
            # Get ACTIVE SLOT ########
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[  Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            # render message
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[  Enter save slot(0-9 active): ]")
            # Get SAVE SLOT ##########
            slotID = print_slot(stdscr, 'write')
            slotID = slotID.decode("utf-8")
            # Save matrix ############
            mtrxC.saveMatrix(mtrx_all[int(to_slot)] ,int(slotID))
            pass
        ## Replace matrix # Step 0 ###
        if current_row == 4 and step == 0:
            focus = 1
        ## Replace matrix # Step 1 ###
        if current_row == 4 and step == 1:
            # Get ACTIVE SLOT ########
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ 1) Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            # Get SAVE ACT SLOT ######
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ 2) Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot1 = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot1 = to_slot1.decode("utf-8")
            # switch SLOTS ###########
            temp_mtrx =  mtrx_all[int(to_slot)]
            mtrx_all[int(to_slot)] =  mtrx_all[int(to_slot1)]
            mtrx_all[int(to_slot1)] = temp_mtrx
            # refreash
            stdscr.refresh()
            pass
    ##################################
    ## Menu 1 ########################
    if current_menu == 1: ### MENU 1 
        ## Delta # Step 0 ############
        if current_row == 0 and step == 0: # Delta
            focus = 1
        ## Delta # Step 1 ############
        if current_row == 0 and step == 1: # Delta
            # get ACTIVE SLOT ########
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            addHistory(to_slot)
            # get DELTA from func ####
            delta = mtrxC.determ(mtrx_all[int(to_slot)])
            # print message DELTA ####
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Delta:{} ]".format(delta))
            # whait for key ##########
            stdscr.getch()
        ## Minor # step 0 ############
        if current_row == 1 and step == 0: # Minor
            focus = 1
        ## Minor # step 1 ############
        if current_row == 1 and step == 1: # Minor
            # get ACTIVE SLOT ########
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            addHistory(to_slot)
            # get I ##################
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter i: ]")
            m_i = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            m_i = m_i.decode("utf-8")
            addHistory(m_i)
            # get J ##################
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter j: ]")
            m_j = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            m_j = m_j.decode("utf-8")
            addHistory(m_j)
            # get MINOR from func ####
            minor = mtrxC.minor(mtrx_all[int(to_slot)], m_i, m_j)
            # print message MINOR ####
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Minor:{} ]".format(minor))
            # refresh & whait key ####
            stdscr.refresh()
            stdscr.getch()
        ## Minor matrix # Step 0 #####
        if current_row == 2 and step == 0: # Minor matrix
            focus = 1
        ## Minor matrix # Step 1 #####
        if current_row == 2 and step == 1: # Minor matrix
            # get ACTIVE SLOT ########
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            addHistory(to_slot)
            # get I ##################
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter i: ]")
            m_i = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            m_i = m_i.decode("utf-8")
            addHistory(m_i)
            # get J ##################
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter j: ]")
            m_j = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            m_j = m_j.decode("utf-8")
            addHistory(m_j)
            # get SAVE ACT SLOT ######
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter slot(0-{} active) to save: ]".format(mtrx_all_slots-1))
            to_slot1 = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot1 = to_slot1.decode("utf-8")
            addHistory(to_slot1)
            # reasign ACTIVE SLOT ####
            mtrx_all[int(to_slot1)] = mtrxC.minorMatrix(mtrx_all[int(to_slot)], m_i, m_j)
            # refreash 
            stdscr.refresh()
        ## Cofactor # Step 0 #########
        if current_row == 3 and step == 0: # Cofactor
            focus = 1
        ## Cofactor # Step 1 #########
        if current_row == 3 and step == 1: # Cofactor
            # get ACTIVE SLOT ########
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            addHistory(to_slot)
            # get I ##################
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter i: ]")
            m_i = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            m_i = m_i.decode("utf-8")
            addHistory(m_i)
            # get J ##################
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter j: ]")
            m_j = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            m_j = m_j.decode("utf-8")
            addHistory(m_j)
            # get COFACTOR from func #
            cofac = mtrxC.cofactor(mtrx_all[int(to_slot)], m_i, m_j)
            # print message COFACTOR #
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Cofactor:{} ]".format(cofac))
            # refresh & whait key ####
            stdscr.refresh()
            stdscr.getch()
        ## Inverse # Step 0 ##########
        if current_row == 4 and step == 0: # Inverse
            focus = 1
        ## Inverse # Step 1 ##########
        if current_row == 4 and step == 1: # Inverse
            # get ACTIVE SLOT ########
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter slot(0-{} active): ]".format(mtrx_all_slots-1))
            to_slot = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot = to_slot.decode("utf-8")
            addHistory(to_slot)
            # get SAVE ACT SLOT ######
            cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ Enter slot(0-{} active) to save: ]".format(mtrx_all_slots-1))
            to_slot1 = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            to_slot1 = to_slot1.decode("utf-8")
            addHistory(to_slot1)
            # reasign ACTIVE SLOT ####
            mtrx_all[int(to_slot1)] = mtrxC.inverse(mtrx_all[int(to_slot)])
            # refreash ###############
            stdscr.refresh()
        ## Mltp by 'k' # Step 0 ######
        if current_row == 5 and step == 0: # Multiply by 'k'
            pass
    ##################################
    ## Menu 2 ########################
    if current_menu == 2: ### MENU 2
        if current_row == 0: # Mltply by mtrx
            pass
        if current_row == 1: # Sbstrct fr cur mtrx
            pass
        if current_row == 2: # Add to cur mtrx
            pass
    if current_menu == 3: ### MENU 3
        if current_row == 0: # Settings
            pass
        if current_row == 1: # Exit
            key = ord('q')
### Menu vars


def print_slot(stdscr, mode):
    height, width = stdscr.getmaxyx()
    slot_list = []
    max_len = 0
    # Func ############
    def raw_input(y, x, leng):
        curses.echo()
        input = stdscr.getstr(y, x, leng)
        return input
    # Add slots to list
    for i in range(10):
        f = open('saves/save-{:02}'.format(i))
        lines = f.readlines()
        f.close()
        if lines == []:
            slot_list.append(str("save-{:02}: [Empty]".format(i))) 
            continue
        else: slot_list.append(str("save-{:02}: {}".format(i, list(map(str.strip, lines))))) 
    ###################
    if max_len < len(max(slot_list, key=len)):
        max_len = len(max(slot_list, key=len))
    max_len += 4
    ###################
    if mode == "show":
        start_y = (height // 2) - (len(slot_list) // 2) - 1
    else: start_y = (height // 2) - (len(slot_list) // 2) - 2
    ###################
    start_x = (width // 2) - (max_len // 2) - 1
    ###################
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(start_y, start_x, "{}{}{}".format(" "*((int(max_len) // 2) - (len(" Slots: ") // 2)), " Slots: ", " "*((max_len // 2) - (len(" Slots: ") // 2) )))
    start_y += 1
    stdscr.attroff(curses.color_pair(1))
    ###################
    for i in slot_list:
        cur_len = len(i)
        stdscr.addstr(start_y, start_x, "│ {}{} │".format(str(i), " "*(max_len - cur_len - 4)))
        start_y += 1
    ###################
    if mode == 'show':
         cUI.menu_toolbar(stdscr, key, 99, 99, "[ save slots files ]")
    else: cUI.menu_toolbar(stdscr, key, 99, 99, "[ Enter save slot: ]")
    ###################
    stdscr.addstr(start_y, start_x, "└{}┘".format("─"*(max_len - 2)))
    ###################
    if mode == "write":
        stdscr.addstr(start_y, start_x, "┌{}┐".format("─"*(max_len - 2)))
        start_y += 1
        #
        stdscr.addstr(start_y, start_x, "│~:{}│".format("─"*(max_len - 4)))
        slotID = raw_input(start_y, start_x + 3, 1)
        start_y += 1
        #
        stdscr.addstr(start_y, start_x, "└{}┘".format("─"*(max_len - 2)))
        #
        stdscr.clear()
        return slotID 
    ###################
    stdscr.getch()
    stdscr.clear()

    pass
# 1 2 3 4 > 5 1 2 3 4
# 4 3 2 1
# 4 3 2 1 5
# 3 2 1 5
# 5 1 2 3
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
def draw(stdscr):
    ## Globals #############
    global menu_all
    global history, history_slots
    global mtrx_all, mtrx_all_slots
    global key, focus
    ## Vars ################
    height, width = stdscr.getmaxyx()
    current_menu, current_row = 0, 0
    start_x = 0
    start_y = 0
    ## Colors schemes ######
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLACK)
    ## Loop ################
    while (key !=ord('q')):
        ## Scan slots ######
        mtrxC.scanSlots()
        ## Refreash ########
        stdscr.clear()
        stdscr.refresh()
        height, width = stdscr.getmaxyx()
        ## ON atrb #########
        curses.curs_set(0) #Stop blinking
        ## Key binds #######
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        if key == curses.KEY_DOWN and current_row < len(menu_all[current_menu])-1:
            current_row += 1
        if key == curses.KEY_ENTER or key in [10, 13]:
            menu_chs(stdscr, start_x, start_y, menu_all, mtrx_all_slots, current_row, current_menu, 0)
        if key in [9]: #TAB
            current_row = 0
            current_menu += 1
            if current_menu >= len(menu_all):
                current_menu = 0
        ## Pre-Render ###### All off ##
        cUI.menu_list(stdscr, start_x, start_y, menu_all, current_row, current_menu, 99)
        cUI.menu_input(stdscr, start_x, start_y, history, 99)
        cUI.menu_mtrxs(stdscr, start_x, start_y, mtrx_all, mtrx_all_slots, 99 )
        ## Render ##########
        ## Render Input ####
        if focus == 1:

            menu_chs(stdscr, start_x, start_y, menu_all, mtrx_all_slots, current_row, current_menu, 1)

            # instr = cUI.menu_input(stdscr, start_x, start_y, history, focus)
            # history.pop()
            # history.insert(0, str(instr.decode("utf-8")))
            # stdscr.refresh()
            

            focus = 0
        ## Render history ##
        instr = cUI.menu_input(stdscr, start_x, start_y, history, focus)
        ## Render general ## 
        cUI.menu_list(stdscr, start_x, start_y, menu_all, current_row, current_menu, focus)
        cUI.menu_toolbar(stdscr, key, current_row, current_menu, "[ None ]")
        cUI.menu_mtrxs(stdscr, start_x, start_y, mtrx_all, mtrx_all_slots, 99 )
        # stdscr.refresh()
        # pop = cUI.menu_input(stdscr, start_x, start_y, history, focus)
        ## Whait for input #
        if key != ord('q'):
            key = stdscr.getch()
        ####################    
############################
def main():
    curses.wrapper(draw)

if __name__ == "__main__":
    main()
