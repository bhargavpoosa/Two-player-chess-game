import pygame
#--------------------------------------------------------------------------------------------------------------------------------
horiz_padding=120
verti_padding=20
cell_size=70
half_cellsize=35
#--------------------------------------------------------------------------------------------------------------------------------
#returns the position of opponent
def kill(player,x,y,chess):
    z=change_turn(player)
    for j in range(len(chess[z])):
        for k in range(len(chess[z][j])):
            if chess[z][j][k].center[0]==x and chess[z][j][k].center[1]==y:
                return z,j,k
    return 'None',-1,-1
#--------------------------------------------------------------------------------------------------------------------------------
#returns true,when king is under threat of capture
def check_mate(king_check,kingx,kingy,chess,turn,screen,killMoves,checkMoves):
    turn=change_turn(turn)
    for j in range(len(chess[turn])):
        for k in range(len(chess[turn][j])):
            x=chess[turn][j][k].center[0]
            y=chess[turn][j][k].center[1]
            if j==0:
                px=x
                py=y
                if turn=='white':
                    for px in [px+cell_size,px-cell_size]:
                        if px==kingx and py-cell_size==kingy and king_check==False:
                            checkMoves.append([kingx-half_cellsize,kingy-half_cellsize])
                            killMoves.append([kingx-half_cellsize,kingy-half_cellsize])
                else:
                    px=x
                    py=y
                    for px in [px+cell_size,px-cell_size]:
                        if px==kingx and py+cell_size==kingy and king_check==False:
                            checkMoves.append([kingx-half_cellsize,kingy-half_cellsize])
                            killMoves.append([kingx-half_cellsize,kingy-half_cellsize])
            elif j==1:
                rook_movement(True,turn,x,y,checkMoves,killMoves,chess)
            elif j==2:
                knight_movement(True,turn,x,y,checkMoves,killMoves,chess)
            elif j==3:
                diagonal_movement(True,turn,x,y,checkMoves,killMoves,chess)
            elif j==5:
                rook_movement(True,turn,x,y,checkMoves,killMoves,chess)
                diagonal_movement(True,turn,x,y,checkMoves,killMoves,chess)
            for p in range(len(checkMoves)):
                if checkMoves[p][0]+half_cellsize==kingx and checkMoves[p][1]+half_cellsize==kingy:
                    if king_check==False:
                        killMoves.append([kingx-half_cellsize,kingy-half_cellsize])
                    checkMoves.clear()
                    return True
    return False
#---------------------------------------------------------------------------------------------------------------------------------
#Changes Turn
def change_turn(turn):
    if turn=='white':
        turn='black'
    else:
        turn='white'
    return turn
#--------------------------------------------------------------------------------------------------------------------------------
#Shows all possible choices for a particular piece
def show_choice(screen,possibleMoves):
    for j in range(len(possibleMoves)):
        pygame.draw.rect(screen,(255,255,153),[possibleMoves[j][0],possibleMoves[j][1],cell_size,cell_size])
        pygame.draw.rect(screen,(0,0,0),[possibleMoves[j][0],possibleMoves[j][1],cell_size,cell_size],2)
        pygame.display.update()
#--------------------------------------------------------------------------------------------------------------------------------
#Shows the possible choice for killing the opponent's pieces
def show_target(screen,killMoves):
    for j in range(len(killMoves)):
        pygame.draw.rect(screen,(255,0,0),[killMoves[j][0],killMoves[j][1],cell_size,cell_size])
        pygame.draw.rect(screen,(0,0,0),[killMoves[j][0],killMoves[j][1],cell_size,cell_size],2)
        pygame.display.update()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def knight_movement(check,i,kx,ky,possibleMoves,killMoves,chess):
    if kx+2*cell_size<=horiz_padding+8*cell_size-half_cellsize and kx+2*cell_size>=horiz_padding+half_cellsize and ky-cell_size>=verti_padding+half_cellsize and ky-cell_size<=verti_padding+8*cell_size-half_cellsize and collision_check(False,i,kx+2*cell_size,ky-cell_size,chess):
        possibleMoves.append([kx+2*cell_size-half_cellsize,ky-cell_size-half_cellsize])
        if check==False and collision_check(check,change_turn(i),kx+2*cell_size,ky-cell_size,chess)==False:
            killMoves.append([kx+2*cell_size-half_cellsize,ky-cell_size-half_cellsize])
    if kx-2*cell_size<=horiz_padding+8*cell_size-half_cellsize and kx-2*cell_size>=horiz_padding+half_cellsize and ky-cell_size>=verti_padding+half_cellsize and ky-cell_size<=verti_padding+8*cell_size-half_cellsize and collision_check(False,i,kx-2*cell_size,ky-cell_size,chess):
        possibleMoves.append([kx-2*cell_size-half_cellsize,ky-cell_size-half_cellsize])
        if check==False and collision_check(check,change_turn(i),kx-2*cell_size,ky-cell_size,chess)==False:
            killMoves.append([kx-2*cell_size-half_cellsize,ky-cell_size-half_cellsize])
    if kx+cell_size<=horiz_padding+8*cell_size-half_cellsize and kx+cell_size>=horiz_padding+half_cellsize and ky-2*cell_size<=verti_padding+8*cell_size-half_cellsize and ky-2*cell_size>=verti_padding+half_cellsize and collision_check(False,i,kx+cell_size,ky-2*cell_size,chess):
        possibleMoves.append([kx+cell_size-half_cellsize,ky-2*cell_size-half_cellsize])
        if check==False and collision_check(check,change_turn(i),kx+cell_size,ky-2*cell_size,chess)==False:
            killMoves.append([kx+cell_size-half_cellsize,ky-2*cell_size-half_cellsize])
    if kx-cell_size<=horiz_padding+8*cell_size-half_cellsize and kx-cell_size>=horiz_padding+half_cellsize and ky-2*cell_size<=verti_padding+8*cell_size-half_cellsize and ky-2*cell_size>=verti_padding+half_cellsize and collision_check(False,i,kx-cell_size,ky-2*cell_size,chess):
        possibleMoves.append([kx-cell_size-half_cellsize,ky-2*cell_size-half_cellsize])
        if check==False and collision_check(check,change_turn(i),kx-cell_size,ky-2*cell_size,chess)==False:
            killMoves.append([kx-cell_size-half_cellsize,ky-2*cell_size-half_cellsize])
    if kx+2*cell_size>=horiz_padding+half_cellsize and kx+2*cell_size<=horiz_padding+8*cell_size-half_cellsize and ky+cell_size>=verti_padding+half_cellsize and ky+cell_size<=verti_padding+8*cell_size-half_cellsize and collision_check(False,i,kx+2*cell_size,ky+cell_size,chess):
        possibleMoves.append([kx+2*cell_size-half_cellsize,ky+cell_size-half_cellsize])
        if check==False and collision_check(check,change_turn(i),kx+2*cell_size,ky+cell_size,chess)==False:
            killMoves.append([kx+2*cell_size-half_cellsize,ky+cell_size-half_cellsize])
    if kx-2*cell_size<=horiz_padding+8*cell_size-half_cellsize and kx-2*cell_size>=horiz_padding+half_cellsize and ky+cell_size>=verti_padding+half_cellsize and ky+cell_size<=verti_padding+8*cell_size-half_cellsize and collision_check(False,i,kx-2*cell_size,ky+cell_size,chess):
        possibleMoves.append([kx-2*cell_size-half_cellsize,ky+cell_size-half_cellsize])
        if check==False and collision_check(check,change_turn(i),kx-2*cell_size,ky+cell_size,chess)==False:
            killMoves.append([kx-2*cell_size-half_cellsize,ky+cell_size-half_cellsize])
    if kx+cell_size<=horiz_padding+8*cell_size-half_cellsize and kx+cell_size>=horiz_padding+half_cellsize and ky+2*cell_size<=verti_padding+8*cell_size-half_cellsize and ky+2*cell_size>=verti_padding+half_cellsize and collision_check(False,i,kx+cell_size,ky+2*cell_size,chess):
        possibleMoves.append([kx+cell_size-half_cellsize,ky+2*cell_size-half_cellsize])
        if check==False and collision_check(check,change_turn(i),kx+cell_size,ky+2*cell_size,chess)==False:
            killMoves.append([kx+cell_size-half_cellsize,ky+2*cell_size-half_cellsize])
    if kx-cell_size<=horiz_padding+8*cell_size-half_cellsize and kx-cell_size>=horiz_padding+half_cellsize and ky+2*cell_size<=verti_padding+8*cell_size-half_cellsize and ky+2*cell_size>=verti_padding+half_cellsize and collision_check(False,i,kx-cell_size,ky+2*cell_size,chess):
        possibleMoves.append([kx-cell_size-half_cellsize,ky+2*cell_size-half_cellsize])
        if check==False and collision_check(check,change_turn(i),kx-cell_size,ky+2*cell_size,chess)==False:
            killMoves.append([kx-cell_size-half_cellsize,ky+2*cell_size-half_cellsize])
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def game_over(turn,font,screen):
    if turn=='white':
        drawText=font.render('BLACK COLOR WINS',True,(0,0,0))
    else:
        drawText=font.render('WHITE COLOR WINS',True,(0,0,0))
    screen.blit(drawText,(250,250))
    pygame.display.update()
#-----------------------------------------------------------------------------------------------------------------------------------
def diagonal_movement(check,i,x,y,possibleMoves,killMoves,chess):
    bx=x
    by=y
    while bx<horiz_padding+8*cell_size-half_cellsize and by>verti_padding+half_cellsize:
        bx+=cell_size
        by-=cell_size
        if collision_check(check,change_turn(i),bx,by,chess)==False:
            if check==False:
                killMoves.append([bx-half_cellsize,by-half_cellsize])
            possibleMoves.append([bx-half_cellsize,by-half_cellsize])
            break
        if collision_check(False,i,bx,by,chess):
            possibleMoves.append([bx-half_cellsize,by-half_cellsize])
        else:
            break
    bx=x
    by=y
    while bx>horiz_padding+half_cellsize and by<verti_padding+8*cell_size-half_cellsize:
        bx-=cell_size
        by+=cell_size
        if collision_check(check,change_turn(i),bx,by,chess)==False:
            if check==False:
                killMoves.append([bx-half_cellsize,by-half_cellsize])
            possibleMoves.append([bx-half_cellsize,by-half_cellsize])
            break
        if collision_check(False,i,bx,by,chess):
            possibleMoves.append([bx-half_cellsize,by-half_cellsize])
        else:
            break
    bx=x
    by=y
    while bx>horiz_padding+half_cellsize and by>verti_padding+half_cellsize:
        bx-=cell_size
        by-=cell_size
        if collision_check(check,change_turn(i),bx,by,chess)==False:
            if check==False:
                killMoves.append([bx-half_cellsize,by-half_cellsize])
            possibleMoves.append([bx-half_cellsize,by-half_cellsize])
            break
        if collision_check(False,i,bx,by,chess):
            possibleMoves.append([bx-half_cellsize,by-half_cellsize])
        else:
            break
    bx=x
    by=y
    while bx<horiz_padding+8*cell_size-half_cellsize and by<verti_padding+8*cell_size-half_cellsize:
        bx+=cell_size
        by+=cell_size
        if collision_check(check,change_turn(i),bx,by,chess)==False:
            if check==False:
                killMoves.append([bx-half_cellsize,by-half_cellsize])
            possibleMoves.append([bx-half_cellsize,by-half_cellsize])
            break
        if collision_check(False,i,bx,by,chess):
            possibleMoves.append([bx-half_cellsize,by-half_cellsize])
        else:
            break
#----------------------------------------------------------------------------------------------------------------------------------------
def collision_check(check,i,x,y,chess):
    for j in range(len(chess[i])):
        for k in range(len(chess[i][j])):
            if check==True and j!=4:
                if chess[i][j][k].center[0]==x and chess[i][j][k].center[1]==y:
                    return False
            elif check==False:
                if chess[i][j][k].center[0]==x and chess[i][j][k].center[1]==y:
                    return False
    return True
#------------------------------------------------------------------------------------------------------------------------------------------
def rook_movement(check,i,x,y,possibleMoves,killMoves,chess):
    ry=y
    while ry>verti_padding+half_cellsize:
        ry-=cell_size
        if collision_check(check,change_turn(i),x,ry,chess)==False:
            if check==False:
                killMoves.append([x-half_cellsize,ry-half_cellsize])
            possibleMoves.append([x-half_cellsize,ry-half_cellsize])
            break
        if collision_check(False,i,x,ry,chess):
            possibleMoves.append([x-half_cellsize,ry-half_cellsize])
        else:
            break
    ry=y
    while ry<verti_padding+8*cell_size-half_cellsize:
        ry+=cell_size
        if collision_check(check,change_turn(i),x,ry,chess)==False:
            if check==False:
                killMoves.append([x-half_cellsize,ry-half_cellsize])
            possibleMoves.append([x-half_cellsize,ry-half_cellsize])
            break
        if collision_check(False,i,x,ry,chess):
            possibleMoves.append([x-half_cellsize,ry-half_cellsize])
        else:
            break
    rx=x
    while rx>horiz_padding+half_cellsize:
        rx-=cell_size
        if collision_check(check,change_turn(i),rx,y,chess)==False:
            if check==False:
                killMoves.append([rx-half_cellsize,y-half_cellsize])
            possibleMoves.append([rx-half_cellsize,y-half_cellsize])
            break
        if collision_check(False,i,rx,y,chess):
            possibleMoves.append([rx-half_cellsize,y-half_cellsize])
        else:
            break
    rx=x
    while rx<horiz_padding+8*cell_size-half_cellsize:
        rx+=cell_size
        if collision_check(check,change_turn(i),rx,y,chess)==False:
            if check==False:
                killMoves.append([rx-half_cellsize,y-half_cellsize])
            possibleMoves.append([rx-half_cellsize,y-half_cellsize])
            break
        if collision_check(False,i,rx,y,chess):
            possibleMoves.append([rx-half_cellsize,y-half_cellsize])
        else:
            break
