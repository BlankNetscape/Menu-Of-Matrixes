# pip install numpy
# pip install colorama
# pip install getch
import numpy as np
import os
# import time
# from colorama import init
# ^ MODULES
global slots
slots={}
# curMtrx = []
# tempMtrx_1 = []
# tempMtrx_2 = []
# np.blankMtrx = [""]
# answ = ""
# global pop
# pop = 0

# ^ GLOBAL VARS

def toMatrix( R, C, string ):
    entries = list(map(int, string))
    np.mtrx = np.array(entries).reshape(R, C)
    return np.mtrx
# return np.mtrx

def scanSlots():
    # Scan 10 slot files
    script_dir = os.path.dirname(__file__)
    rel_path = "saves/save"
    for i in range(10):
    # Read lines from each file 
        f = open('{path}-{num:02}'.format(path = os.path.join(script_dir, rel_path), num = i))
        lines = f.readlines()
        f.close()
    # If lines Empty >> fill:
        if lines == []:
            slots["r-slot{}".format(i)] = 0
            slots["c-slot{}".format(i)] = 0
            slots["slot{}".format(i)] = lines
    # Split lines 
        else:
            rows = (list(map(str.strip, lines))[0].split())[1]
            rows = int(rows)
            cols = (list(map(str.strip, lines))[1].split())[1]
            cols = int(cols)
            entries = list(lines)[2].split()
            entries = list(map(int, entries))
    # Add to slot dictionary
            slots["r-slot{}".format(i)] = rows
            slots["c-slot{}".format(i)] = cols
            slots["slot{}".format(i)] = entries

def genMatrix( rows, cols, entries ):
    tmpMtrx = []
    # Vars
    rows = int(rows)
    cols = int(cols)
    entries = list(map(int, entries.split()))
    # to matrix
    tmpMtrx = toMatrix(rows, cols, entries)
    # return
    return tmpMtrx
# return tmpMtrx

def loadMatrix( slot ):
    row = slots["r-slot{}".format(slot)]
    # print(":" ,row, type(row))
    col = slots["c-slot{}".format(slot)]
    # print(":" ,col, type(col))
    entries = slots["slot{}".format(slot)]
    # print(":" ,entries, type(entries))
    return toMatrix(row, col, entries)
    # result = []
    # # load from dictionary by 'slot' >> from scanSlots
    # result.append(slots["r-slot{}".format(slot)])   # ROW
    # result.append(slots["c-slot{}".format(slot)])   # COL
    # result.append(slots["slot{}".format(slot)])     # ENTR
    # return result
# return result

def saveMatrix( mtrx, slot ):
    # Break if 1,1
    if mtrx.size < 1:
        #????????????????????
        print("fck too smol")
        return
    # init ROWS $ COLS
    R = mtrx.shape[0]
    C = mtrx.shape[1]
    str = ""
    # write mtrx to str
    for i in range(0, R):
        for j in range(0, C):
            str += "{} ".format(mtrx[i][j])
        pass
    # open save file
    f = open("saves/save-{:02}".format(slot), "w+")
    f = open("saves/save-{:02}".format(slot), "a+")
    # write to save file
    f.write("row: {0}\ncol: {1}\n".format(R, C))
    f.write(str)
    f.close()
    # return
    # return

def printSlots():
    for i in range(10):
        # open&close saves files in loop
        f = open('saves/save-{:02}'.format(i))
        lines = f.readlines()
        f.close()
        # if file empty >>
        if lines == []:
            print("save-{:02}: [Empty]".format(i))
            continue
        # else
        else: print("save-{:02}: {}".format(i, list(map(str.strip, lines))))

def minorMatrix( mtrx, m_i, m_j ):
    m_i = int(m_i) - 1 # for array
    m_j = int(m_j) - 1 # for array
    newR = mtrx.shape[0]
    newC = mtrx.shape[1]
    # create minor matrix shape
    np.minorMatrix = np.arange((newR - 1) * (newC - 1)).reshape((newR - 1), (newC - 1))
    # arr to matrix without m_i row & m_j items in rows
    row = 0
    for ir in range(newR):
        if ir == m_i:
            continue
        col = 0
        for ic in range(newC):
            if ic == m_j:
                continue
            np.minorMatrix[row][col] = mtrx[ir][ic]
            col+= 1
        row+= 1
    # result
    return np.minorMatrix
# return np.minorMatrix

def minor( mtrx, m_i, m_j ):
    result = determ(minorMatrix(mtrx, m_i, m_j))
    return result
# return result

def cofactor( mtrx, m_i, m_j ):
    result = int((  (-1)**( int(m_i) + int(m_j) )  ) * int(minor( mtrx, m_i, m_j )))
    return result
# return result

def inverse( mtrx ):
    # step 1
    i = int(mtrx.shape[0])
    j = int(mtrx.shape[1])
    inverseMtrx = np.arange(i*j).reshape(i, j)
    for ir in range(i):
        for ic in range(j):
            inverseMtrx[ir][ic] = cofactor(mtrx, (ir + 1), (ic + 1))
    # step 2
    i = int(mtrx.shape[0])
    j = int(mtrx.shape[1])
    inverseMtrx_changed = np.arange(i*j).reshape(i, j)
    for ir in range(i):
        for ic in range(j):
            inverseMtrx_changed[ir][ic] = inverseMtrx[ic][ir]
    # result
    return inverseMtrx_changed
# return inverseMtrx_changed

def determ( mtrx ):
    i = mtrx.shape[0]
    j = mtrx.shape[1]
    if i == 1 and j == 1:
        result = mtrx[0][0]
        return result
    if i == 2 and j == 2:
        result = (mtrx[0][0] * mtrx[1][1]) - (mtrx[0][1] * mtrx[1][0])
        return result
    if R == 3 and C == 3:
        result = (mtrx[0][0] * mtrx[1][1] * mtrx[2][2]) +\
                 (mtrx[1][0] * mtrx[2][1] * mtrx[0][2]) +\
                 (mtrx[0][1] * mtrx[1][2] * mtrx[2][0]) -\
                 (mtrx[0][2] * mtrx[1][1] * mtrx[2][0]) -\
                 (mtrx[0][1] * mtrx[1][0] * mtrx[2][2]) -\
                 (mtrx[1][2] * mtrx[2][1] * mtrx[0][0])
        return result
# return result