import sys,os
import curses
import numpy as np
# import random, math

def printMenuCenter( stdscr ,inputMenu, current_row ):
    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    for index, row in enumerate(inputMenu):
        menu_x = width // 2 - len(row) // 2
        menu_y = height // 2 - len(inputMenu) // 2 + index
        if index == current_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(menu_y, menu_x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(menu_y, menu_x, row)

def printMenuLeftArrow( stdscr ,inputMenu, current_row ):
    start_y = 3
    start_x = 0
    arrow = "> "
    #
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    #
    for index, menu_row in enumerate(inputMenu):
        menu_x = start_x
        menu_y = start_y + index

        if index == current_row:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(menu_y, menu_x, "{}".format(arrow))
            stdscr.attroff(curses.color_pair(2))
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(menu_y, menu_x + len(arrow), "{}".format( menu_row))
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(menu_y, menu_x, "{}{}".format(" "*len(arrow) , menu_row))

def menu_list(stdscr, start_x, start_y, menu_array, current_row, current_menu, focus):
    menuID = 0 # MENU ID
    menu_stat = "" # focus STATUS
    ## Color schemes & Focus
    if focus == menuID:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    else:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    ## Func vars
    start_x = 0
    start_y = 0
    arrow = "> "
    #
    min_row_w = 2
    max_row_w = 0
    for index in range(len(menu_array)):
         for item in menu_array[index]:
             if len(item) > max_row_w:
                 max_row_w = len(item) + 1
                 if max_row_w < min_row_w:
                     max_row_w = min_row_w
             # stdscr.addstr(20,0, str(max_row_w))
    ## Render hat
    if focus == menuID:
        menu_stat += "focused"
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(start_y, start_x, "{}".format(" "*(max_row_w + 4)))
        stdscr.addstr(start_y, start_x, "{}{}".format( " " * ((((max_row_w + 4) // 2) - (len(menu_stat) // 2))), menu_stat  ) )
        stdscr.attroff(curses.color_pair(2))
        start_y += 1
    # elif focus == 99:
    #     stdscr.addstr(start_y, start_x, "{}".format(" "*(max_row_w + 4)))
    #     start_y += 1
    else:
        menu_stat += "not focused"
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(start_x, start_y, "{}{}".format( " " * (((max_row_w + 4) // 2) - len(menu_stat) // 2), menu_stat  ) )
        stdscr.attroff(curses.color_pair(2))
        start_y += 1
        # return
    ## Render menu
    for index_menu in range(len(menu_array)):
        ## Render 0-Label
        if index_menu == 0:
            stdscr.addstr(start_y, start_x,\
            "┌─ MENU #{} {border}┐".format(index_menu, border = "─" * (max_row_w-9+1)))
        ## Render body-Labels
        else:
            start_y += 1
            stdscr.addstr(start_y, start_x,\
            "├─ MENU #{} {border}┤".format(index_menu, border = "─" * (max_row_w-9+1)))
        ## Render menu items IF current_row
        for index_row, menu_row in enumerate(menu_array[current_menu]):
            ## Break
            if index_menu != current_menu:
                break
            ## Render active and passive items
            start_y += 1
            if index_row == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(start_y, start_x, "{}".format(arrow))
                # stdscr.attroff(curses.color_pair(2))

                # stdscr.attron(curses.color_pair(1))
                stdscr.addstr(start_y, start_x + len(arrow), "{} ".format(menu_row))
                stdscr.attroff(curses.color_pair(1))
                stdscr.addstr(start_y, start_x + len(arrow) + len(menu_row) + 1, "{spaces} │".format(spaces = " " * ( max_row_w -1 -(len(menu_row)) ) ))
            else: stdscr.addstr(start_y, start_x + len(arrow), "{}{spaces} │".format(menu_row, spaces = " " * ( max_row_w -(len(menu_row)) ) ))
            if index_row == len(menu_array[current_menu]) -1:
                stdscr.addstr(start_y +1, start_x, " {}│".format(" "*(len(arrow)+max_row_w)))
                start_y += 1
    ## Render bottom cap
    # stdscr.addstr(start_y +1, start_x, "│{}│".format(" "*(len(arrow)+max_row_w)))
    stdscr.addstr(start_y +1, start_x, "└{}┘".format("─"*(len(arrow)+max_row_w)))

def menu_input(stdscr, start_x, start_y, history, focus):
    menuID = 1 # MENU ID
    menu_stat = "" # focus STATUS
    ## Func vars
    start_x = 24
    start_y = 0
    arrow = "> "
    
    ## Color schemes & Focus
    if focus == menuID:
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    else:
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    ##
    if focus == menuID:
        menu_stat += "    focused    "
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(start_y, start_x, "{}{}".format( " " * (((23) // 2) - len(menu_stat) // 2), menu_stat  ) )
        stdscr.attroff(curses.color_pair(4))
        start_y += 1
    else:
        menu_stat += "not focused"
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(start_y, start_x, "{}{}".format( " " * (((23) // 2) - len(menu_stat) // 2), menu_stat  ) )
        stdscr.attroff(curses.color_pair(4))
        start_y += 1
        # return
    ## Print Box
    stdscr.addstr(start_y, start_x, "┌─ Input ─────────────┐"); start_y += 1
    stdscr.addstr(start_y, start_x, "│~:                   │"); start_y += 1
    stdscr.addstr(start_y, start_x, "└                     ┘"); start_y += 1
    stdscr.addstr(start_y, start_x, "┌                     ┐"); start_y += 1
    for i in history:
            if len(i) >= 21:
                stdscr.addstr(start_y, start_x, "│{:18.18}...│".format(i)); start_y += 1                
            else: stdscr.addstr(start_y, start_x, "│{:21.21}│".format(i)); start_y += 1
    stdscr.addstr(start_y, start_x, "└─ Last imput ────────┘"); start_y += 1


    ##
    choice = ''
    if focus == menuID:
        def my_raw_input(r, c):
            curses.echo()
            input = stdscr.getstr(r, c, 30)
            return input  #       ^^^^  reading input at next line
        
        choice = my_raw_input(2, 27).lower()
        
        # focus = 0
        # stdscr.addstr(20, 0, choice)
        
    # stdscr.refresh()
    return choice

def menu_mtrxs(stdscr, start_x, start_y, mtrx_all, mtrx_all_slots, focus):
    start_x = 47
    start_y = 0 + 1
    height, width = stdscr.getmaxyx()
    mtrx_max_num = 0
    mtrx_max_item = 0

    g_mtrx_max_num = 0
    g_mtrx_max_item = 0
    #
    for m_m in mtrx_all:
        for m_item in m_m:
            if g_mtrx_max_num < max(m_item):
                g_mtrx_max_num = max(m_item)
            if g_mtrx_max_item < len(m_item):
                g_mtrx_max_item = len(m_item)
    #
    g_mtrx_max_num = len(str(g_mtrx_max_num))
    #
    stdscr.addstr(start_y, start_x, "┌─ Matrixes ────────┐"); start_y += 1
    stdscr.addstr(start_y, start_x, "│ Active slots: {}   │".format(mtrx_all_slots)); start_y += 1
    # stdscr.addstr(start_y, start_x, "└{} {}".format(str(len(str(mtrx_max_num))), str(mtrx_max_item)))
    stdscr.addstr(start_y, start_x, "└                   ┘"); start_y += 1
    stdscr.addstr(start_y, start_x, "┌")
    if (start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num))) < (start_x + 19):
        stdscr.addstr(start_y, start_x + 19, " ┐")
    else: stdscr.addstr(start_y, start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num)), " ┐")
    start_y += 1
    for i in range(len(mtrx_all)):
        if mtrx_all[i] == []:
            stdscr.addstr(start_y, start_x, "│{}) ║Empty║".format(i))
            if (start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num))) < (start_x + 19):
                stdscr.addstr(start_y, start_x + 19, " │")
            else: stdscr.addstr(start_y, start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num)), " │")
            start_y += 1
            stdscr.addstr(start_y, start_x, "│")
            if (start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num))) < (start_x + 19):
                stdscr.addstr(start_y, start_x + 19, " │")
            else: stdscr.addstr(start_y, start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num)), " │")
            start_y += 1
        else:
            stdscr.addstr(start_y, start_x, "│{})".format(i))#; start_y += 1
            mtrx_cur = np.array(mtrx_all[i])

            # for i1 in range(len(mtrx_cur)):
            #     if mtrx_max_num < max(mtrx_cur[i1]):
            #         mtrx_max_num = max(mtrx_cur[i1])
            # mtrx_max_num = len(str(mtrx_max_num)) + 1
            mtrx_max_num = 0

            for m_i in range(mtrx_cur.shape[0]):

                new_start_x = start_x + 4
                stdscr.addstr(start_y, start_x, "│")
                stdscr.addstr(start_y, new_start_x, "║")
                new_start_x += 1

                for m_j in range(mtrx_cur.shape[1]):
                    for cj in range(mtrx_cur.shape[0]):
                         if mtrx_cur[cj][m_j] > mtrx_max_num:
                            mtrx_max_num = mtrx_cur[cj][m_j]
                    mtrx_max_num = len(str(mtrx_max_num)) + 1


                    stdscr.addstr(start_y, new_start_x, "{:{pad}}".format(mtrx_cur[m_i][m_j], pad = mtrx_max_num))
                    new_start_x += mtrx_max_num
                    pass
                stdscr.addstr(start_y, new_start_x, " ║")
                if (start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num))) < (start_x + 19):
                    stdscr.addstr(start_y, start_x + 19, " │")
                else: stdscr.addstr(start_y, start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num)), " │")
                #
                start_y += 1
            #
            stdscr.addstr(start_y, start_x, "│")
            if (start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num))) < (start_x + 19):
                    stdscr.addstr(start_y, start_x + 19, " │")
            else: stdscr.addstr(start_y, start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num)), " │")
            start_y += 1
                # stdscr.addstr(15, 15, str(mtrx_max_num))
        # stdscr.addstr(start_y, start_x, "{}".format(str(entr.sha"║ │"); start_y += 1pe[0]))); start_y += 1
        
        pass
    if (start_x + (7 + (g_mtrx_max_item * g_mtrx_max_num))) < (start_x + 19):
        stdscr.addstr(start_y, start_x, "└───────────────────┘")

    else: stdscr.addstr(start_y, start_x, "└{}─┘".format('─' * (9 + (g_mtrx_max_item * g_mtrx_max_num))))
    # stdscr.addstr(start_y, start_x, "│"); start_y += 1
    # x = np.array([5])
    # x = np.array(5)
    # stdscr.addstr(start_y, start_x, "{}".format(str(x.shape[0]))); start_y += 1
    # data = numpy(data)



def menu_toolbar(stdscr, key, current_row, current_menu, message):
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height-2, 0, "{}".format(" "* width))
    if message != '':

        stdscr.attron(curses.color_pair(9))
        stdscr.addstr(height-2, (width // 2)-(len(message) // 2), message, curses.A_BOLD)
        stdscr.attroff(curses.color_pair(9))
    #
    statusbarstr = ' \'Tab\' | key: {:03} | row: {:03} | menu: {:03}'.format(key, current_row, current_menu)
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(height-1, 0, "{}{}{}".format(" "* (int(width//2)-int(len(statusbarstr)//2)), statusbarstr, " "* ((int(width//2) -  int(len(statusbarstr)//2))-1)      ))
    stdscr.attroff(curses.color_pair(1))
