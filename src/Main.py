
# On PPM and PGM formats see http://paulbourke.net/dataformats/ppm/
# On convolution operation see https://youtu.be/KiftWz544_8
# To view .pgm and .ppm files, you can use IrfanView, see https://www.irfanview.com/
# To check whether your outputs are the same as ours, you can use the same techniques as in Homework 2, or you can write your own code.
filename = input()
operation = int(input())
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()
# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
def my_img_printer(img):
    global filename
    if filename[-3:] == "pgm":
        row = len(img)
        col = len(img[0])
        for i in range(row):
            for j in range(col):
                print(img[i][j], end=" ")
                print("\t|", end=" ")
            print()
    else:
        row = len(img)
        col = len(img[0])
        cha = len(img[0][0])
        for i in range(row):
            for j in range(col):
                for k in range(cha):
                    print(img[i][j][k], end=" ")
                print("\t|", end=" ")
            print()
def read_img(f_name):
  img = list()
  fp = open(f_name)
  mode=fp.readline().strip()
  if mode=='P1':
    pass
  elif mode == "P2":
      r_c = fp.readline().split()
      n_cols, n_rows = int(r_c[0]), int(r_c[1])
      img = [[[0] for c in range(n_cols)] for r in range(n_rows)]
      res = int(fp.readline())
      rest = fp.read()
      rest_lst = rest.split()
      i = 0
      for r in range(n_rows):
          for c in range(n_cols):
                img[r][c] = int(rest_lst[i])
                i += 1
  elif mode=='P3':
    r_c = fp.readline().split()
    n_cols,n_rows = int(r_c[0]),int(r_c[1])
    img = [[[0,0,0] for c in range(n_cols)] for r in range(n_rows)]
    res = int(fp.readline().strip())
    rest = fp.read()
    rest_lst = rest.split()
    i = 0
    for r in range(n_rows):
      for c in range(n_cols):
        for ch in range(3):
          img[r][c][ch]=int(rest_lst[i])
          i+=1
  fp.close()
  return img
# op 2 functions:
def multipliers(filter_file):
    fp = open(filter_file)
    multiplier_list = fp.read().split()
    fp.close()
    for i in range(len(multiplier_list)):
        multiplier_list[i] = float(multiplier_list[i])
    return multiplier_list

def filter_size(filter_file):
    fp = open(filter_file)
    size = len(fp.readline().split())
    fp.close()
    return size
def sum_finder(r,c,multiplier_list):
    neigh_list = []
    a = int((filtersize -1) /2)
    for i in range(-a,a+1):
        for j in range(-a,a+1):
            coo = [i,j]
            neigh_list.append(coo)
    sum0,sum1,sum2 = 0,0,0
    mult_index = 0

    for neigh in neigh_list:
        sum0 += (img[r+neigh[0]][c+neigh[1]][0]) * multiplier_list[mult_index]
        sum1 += (img[r + neigh[0]][c + neigh[1]][1]) * multiplier_list[mult_index]
        sum2 += (img[r + neigh[0]][c + neigh[1]][2]) * multiplier_list[mult_index]
        mult_index += 1
    sum0 = int(sum0)
    sum1 = int(sum1)
    sum2 = int(sum2)
    list = []
    if sum0 > 255:
        sum0 = 255
    elif sum0 < 0:
        sum0 = 0
    if sum1 > 255:
        sum1 = 255
    elif sum1 < 0:
        sum1 = 0
    if sum2 > 255:
        sum2 = 255
    elif sum2 < 0:
        sum2 = 0
    list.append(sum0), list.append(sum1), list.append(sum2)
    return list
def apply_convolution(r,c):
    global conv_board,conv_index1,conv_index2
    if  r - loss < 0:
        return  apply_convolution(r+stride,c)
    if c - loss < 0:
        return apply_convolution(r,loss)
    if r + loss >= len(img):
        return conv_board
    if c + loss >= len(img[0]):
        return apply_convolution(r+stride,loss)
    sums = sum_finder(r,c,multiplier_list)
    conv_board[conv_index1][conv_index2] = sums
    if conv_index2 + 1 == len(conv_board[0]):
        conv_index1 += 1
        conv_index2 = 0
    else:
        conv_index2 += 1
    return apply_convolution(r,c+stride)
# op 1 functions:
def sum_squares(img,r,c):
    global sum, square_num
    n_rows,n_cols=len(img),len(img[0])
    if r<0 or c <0 or r>=n_rows or c>=n_cols:
        return
    if img[r][c] == 0:
        return
    if true_false_board[r][c][0] != "T":
        return
    neigh_list=[[-1,0],[+1,0],[0,-1],[0,+1]]
    sum += img[r][c]
    square_num += 1
    true_false_board[r][c] = ["W"]
    for neigh in neigh_list:
        sum_squares(img,r+neigh[0],c+neigh[1])
def apply_average_coloring(img):
    global sum, square_num
    n_rows,n_cols=len(img),len(img[0])
    for r in range(n_rows):
        for c in range(n_cols):
            if (img[r][c] != 0) and (true_false_board[r][c][0] == "T"):
                sum_squares(img,r,c)
                average = sum // square_num
                for i in range(len(true_false_board)):
                    for j in range(len(true_false_board[0])):
                        if true_false_board[i][j][0] == "W":
                            img[i][j] = average
                            true_false_board[i][j][0] = "F"
                            sum = 0
                            square_num = 0

    return img
img = read_img(filename)
if operation == 1:
    true_false_board = [[["T"] for c in range(len(img[0]))] for r in range(len(img))]
    sum = 0
    square_num = 0
    my_img_printer(apply_average_coloring(img))

else:
    filter_name = input()
    stride = int(input())
    multiplier_list = multipliers(filter_name)
    filtersize = filter_size(filter_name)
    loss = int((filtersize - 1) //2)
    conv_board = [[[0, 0, 0] for c in range(((len(img)-filtersize)//stride)+1)] for r in range(((len(img)-filtersize)//stride)+1)]
    conv_index1 = 0
    conv_index2 = 0
    img_printer(apply_convolution(loss,loss))
# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

