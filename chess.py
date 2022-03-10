import pygame
import time
from pygame import mixer
from helperfunctions import kill,change_turn,show_choice,show_target,game_over,diagonal_movement,collision_check,rook_movement,check_mate,knight_movement
#Initialization
pygame.init()
#Screen creation
screen=pygame.display.set_mode((900,600))
#background
background=pygame.image.load('chessimg.png')
#------------------------------------------------------------------------------------------------------------------------------------------
horiz_padding=120
verti_padding=20
cell_size=70
half_cellsize=35
#------------------------------------------------------------------------------------------------------------------------------------------
instruction=pygame.image.load('instructions.png')
instruction=pygame.transform.scale(instruction,(512,512))
#------------------------------------------------------------------------------------------------------------------------------------------
#Loading white colour chess piece images
pawnwhite=pygame.image.load('pawnwhite.png')
kingwhite=pygame.image.load('kingwhite.png')
rookwhite=pygame.image.load('rookwhite.png')
knightwhite=pygame.image.load('knightwhite.png')
bishopwhite=pygame.image.load('bishopwhite.png')
queenwhite=pygame.image.load('queenwhite.png')
#--------------------------------------------------------------------------------------------------------------------------------------------
#Loading black colour chess piece images
kingblack=pygame.image.load('kingblack.png')
queenblack=pygame.image.load('queenblack.png')
rookblack=pygame.image.load('rookblack.png')
bishopblack=pygame.image.load('bishopblack.png')
knightblack=pygame.image.load('knightblack.png')
pawnblack=pygame.image.load('pawnblack.png')
#-------------------------------------------------------------------------------------------------------------------------------------------
#Caption
pygame.display.set_caption('Chess Game')
#Background Colour
screen.fill((0,0,0))
#Font declaration
font=pygame.font.Font('freesansbold.ttf',32)

pawnlist_white=[]
pawnlist_black=[]
possibleMoves=[]
checkMoves=[]
killMoves=[]
rooklist_white=[]
rooklist_black=[]
knightlist_white=[]
knightlist_black=[]
bishoplist_white=[]
bishoplist_black=[]
kinglist_white=[]
kinglist_black=[]
queenlist_white=[]
queenlist_black=[]
chess=dict()
selected_item='None'
pics=dict()
turn='white'

pics['white']=[pawnwhite,rookwhite,knightwhite,bishopwhite,kingwhite,queenwhite]
pics['black']=[pawnblack,rookblack,knightblack,bishopblack,kingblack,queenblack]
#------------------------------------------------------------------------------------------------------------------------------------------------------
#board is a list containing the column wise representation of the chess Board
#Here 0-nothing,1-pawn,2-rook,3-knight,4-bishop,5-king,6-queen
board=[[2,1,0,0,0,0,1,2],[3,1,0,0,0,0,1,3],[4,1,0,0,0,0,1,4],[5,1,0,0,0,0,1,5],[6,1,0,0,0,0,1,6],[4,1,0,0,0,0,1,4],[3,1,0,0,0,0,1,3],[2,1,0,0,0,0,1,2]]
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#pawnlist_white and pawnlist_black contains the squares,where pawns are placed
i=6
for j in range(8):
    rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
    pawnlist_white.append(rect)

i=1
for j in range(8):
    rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
    pawnlist_black.append(rect)
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Similarly rooklist_white(rooklist_black),knightlist_white(knightlist_black),bishoplist_white(bishoplist_black),kinglist_white(kinglist_black),queenlist_white(queenlist_black)
#contains the squares where the rooks,knights,bishops,kings and queens are placed respectively
i=7
j=0
while j<8:
    if j==0 or j==7:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        rooklist_white.append(rect)
    elif j==1 or j==6:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        knightlist_white.append(rect)
    elif j==2 or j==5:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        bishoplist_white.append(rect)
    elif j==3:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        kinglist_white.append(rect)
    elif j==4:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        queenlist_white.append(rect)
    j+=1

i=0
j=0
while j<8:
    if j==0 or j==7:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        rooklist_black.append(rect)
    elif j==1 or j==6:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        knightlist_black.append(rect)
    elif j==2 or j==5:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        bishoplist_black.append(rect)
    elif j==3:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        kinglist_black.append(rect)
    elif j==4:
        rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
        queenlist_black.append(rect)
    j+=1
#----------------------------------------------------------------------------------------------------------------------------------------
chess['white']=[pawnlist_white,rooklist_white,knightlist_white,bishoplist_white,kinglist_white,queenlist_white]
chess['black']=[pawnlist_black,rooklist_black,knightlist_black,bishoplist_black,kinglist_black,queenlist_black]
#------------------------------------------------------------------------------------------------------------------------------------
def design_board():
    flag=0
    for i in range(8):
        for j in range(8):
            rect=pygame.Rect(horiz_padding+j*cell_size,verti_padding+i*cell_size,cell_size,cell_size)
            if flag==0:
                pygame.draw.rect(screen,(240,207,174),rect)#Desert Sand-(240,207,174)
                pygame.draw.rect(screen,(255,255,255),rect,2)
                if j<7:
                    flag+=1
            else:
                if j<7:
                    flag=0
                pygame.draw.rect(screen,(181,101,29),rect)#Light Brown-(181,101,29)
                pygame.draw.rect(screen,(255,255,255),rect,2)
#------------------------------------------------------------------------------------------------------------------------------------
def place_piece():
    for i in ['white','black']:
        for j in range(len(chess[i])):
            for k in range(len(chess[i][j])):
                Rect=pics[i][j].get_rect()
                Rect.center=chess[i][j][k].center
                screen.blit(pics[i][j],Rect)
#---------------------------------------------------------------------------------------------------------------------------------------
#Checks the pressed piece
#possibleMoves:Contains all the corners of the possible squares for a piece
#killMoves:Contains the corners of all possible squares that a piece can kill an opponent
def piece_checking(i):
    global selected_item
    selected_item='None'
    x=int((mouse[0]-horiz_padding)/cell_size)
    y=int((mouse[1]-verti_padding)/cell_size)
    #checking whether pawn is pressed
    if board[x][y]==1:
        j=0
        for k in range(len(chess[i][j])):
            if chess[i][j][k].collidepoint(mouse):
                selected_item='pawn'
                pawnx=chess[i][j][k].center[0]
                pawny=chess[i][j][k].center[1]
                px=pawnx
                py=pawny
                #num_move:number of possible moves
                num_move=0
                if i=='white':
                    #num_move is 2,for the first step of a pawn
                    if py>verti_padding+cell_size*6:
                        num_move=2
                    else:
                        num_move=1
                    while num_move!=0 and py>verti_padding+(cell_size/2):
                        py-=cell_size
                        num_move-=1
                        #Adds all possible moves
                        if collision_check(False,i,px,py,chess) and collision_check(False,change_turn(i),px,py,chess):
                            possibleMoves.append([px-half_cellsize,py-half_cellsize])
                        else:
                            break
                    px=pawnx
                    py=pawny
                    #Checks whether pawn can kill
                    if collision_check(False,'black',px+cell_size,py-cell_size,chess)==False:
                        killMoves.append([px+cell_size-half_cellsize,py-cell_size-half_cellsize])
                        possibleMoves.append([px+cell_size-half_cellsize,py-cell_size-half_cellsize])
                    if collision_check(False,'black',px-cell_size,py-cell_size,chess)==False:
                        killMoves.append([px-cell_size-half_cellsize,py-cell_size-half_cellsize])
                        possibleMoves.append([px-cell_size-half_cellsize,py-cell_size-half_cellsize])
                else:
                    if py<verti_padding+2*cell_size:
                        num_move=2
                    else:
                        num_move=1
                    while num_move!=0 and py<verti_padding+8*cell_size-half_cellsize:
                        py+=cell_size
                        num_move-=1
                        #Adds all poosible moves
                        if collision_check(False,i,px,py,chess) and collision_check(False,change_turn(i),px,py,chess):
                            possibleMoves.append([px-half_cellsize,py-half_cellsize])
                        else:
                            break
                    px=pawnx
                    py=pawny
                    #Checks whether a pawn can kill
                    if collision_check(False,'white',px+cell_size,py+cell_size,chess)==False:
                        killMoves.append([px+cell_size-half_cellsize,py+cell_size-half_cellsize])
                        possibleMoves.append([px+cell_size-half_cellsize,py+cell_size-half_cellsize])
                    if collision_check(False,'white',px-cell_size,py+cell_size,chess)==False:
                        killMoves.append([px-cell_size-half_cellsize,py+cell_size-half_cellsize])
                        possibleMoves.append([px-cell_size-half_cellsize,py+cell_size-half_cellsize])
                return x,y,i,k,selected_item
#Checking whether rook is pressed
    elif board[x][y]==2:
        j=1
        for k in range(len(chess[i][j])):
            if chess[i][j][k].collidepoint(mouse):
                selected_item='rook'
                rookx=chess[i][j][k].center[0]
                rooky=chess[i][j][k].center[1]
                rook_movement(False,i,rookx,rooky,possibleMoves,killMoves,chess)
                return x,y,i,k,selected_item
#Checking whether knight is pressed
    elif board[x][y]==3:
        j=2
        for k in range(len(chess[i][j])):
            if chess[i][j][k].collidepoint(mouse):
                selected_item='knight'
                kx=chess[i][j][k].center[0]
                ky=chess[i][j][k].center[1]
                knight_movement(False,i,kx,ky,possibleMoves,killMoves,chess)
                return x,y,i,k,selected_item
#checks whether bishop is pressed
    elif board[x][y]==4:
        j=3
        for k in range(len(chess[i][j])):
            if chess[i][j][k].collidepoint(mouse):
                selected_item='bishop'
                bishopx=chess[i][j][k].center[0]
                bishopy=chess[i][j][k].center[1]
                diagonal_movement(False,i,bishopx,bishopy,possibleMoves,killMoves,chess)
                return x,y,i,k,selected_item
#checks whether king is pressed
    elif board[x][y]==5:
        j=4
        for k in range(len(chess[i][j])):
            if chess[i][j][k].collidepoint(mouse):
                selected_item='king'
                kingx=chess[i][j][k].center[0]
                kingy=chess[i][j][k].center[1]
                for x1 in [kingx-cell_size,kingx,kingx+cell_size]:
                    for y1 in [kingy-cell_size,kingy,kingy+cell_size]:
                        #Checks for all possible moves for king
                        if check_mate(True,x1,y1,chess,i,screen,killMoves,checkMoves)==False and x1<=horiz_padding+8*cell_size-half_cellsize and x1>=horiz_padding+half_cellsize and y1<=verti_padding+8*cell_size-half_cellsize and y1>=verti_padding+half_cellsize and collision_check(False,i,x1,y1,chess):
                            possibleMoves.append([x1-half_cellsize,y1-half_cellsize])
                            #Checks for all moves that a king can kill its opponent
                            if collision_check(False,change_turn(i),x1,y1,chess)==False:
                                killMoves.append([x1-half_cellsize,y1-half_cellsize])
                return x,y,i,k,selected_item
#checks whether queen is pressed
    elif board[x][y]==6:
        j=5
        for k in range(len(chess[i][j])):
            if chess[i][j][k].collidepoint(mouse):
                selected_item='queen'
                queenx=chess[i][j][k].center[0]
                queeny=chess[i][j][k].center[1]
                diagonal_movement(False,i,queenx,queeny,possibleMoves,killMoves,chess)
                rook_movement(False,i,queenx,queeny,possibleMoves,killMoves,chess)
                return x,y,i,k,selected_item
    return 'None','None','None',-1,selected_item
#---------------------------------------------------------------------------------------------------------------------------------------
main_page=True
help_page=False
done=False
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
    if main_page:
        screen.fill((0,0,0))#Black Colour
        #Background image
        screen.blit(background,(0,0))
        #Title on the game screen
        title=font.render('CHESS GAME',True,(255,255,255))
        screen.blit(title,(300,100))
        #Play Button
        playButton=pygame.Rect(350,200,100,50)
        playText=font.render('Play',True,(0,0,0))
        playRect=playText.get_rect()
        playRect.center=playButton.center
        pygame.draw.rect(screen,(255,255,255),playButton)
        screen.blit(playText,playRect)
        #Help Button
        helpButton=pygame.Rect(350,300,100,50)
        helpText=font.render('Help',True,(0,0,0))
        helpRect=helpText.get_rect()
        helpRect.center=helpButton.center
        pygame.draw.rect(screen,(255,255,255),helpButton)
        screen.blit(helpText,helpRect)

        if pygame.mouse.get_pressed()[0]:
            mouse=pygame.mouse.get_pos()
            #Enters when play button is pressed
            if playButton.collidepoint(mouse):
                main_page=False
                help_page=False
                screen.fill((0,0,0))
                design_board()
                pygame.display.flip()
            #Enters when help button is pressed
            elif helpButton.collidepoint(mouse):
                help_page=True
                main_page=False
                screen.fill((0,0,0))
                pygame.display.flip()
        pygame.display.update()

    elif help_page:
        screen.blit(background,(0,0))
        #Back Button
        backButton=pygame.Rect(350,550,100,40)
        backText=font.render('Back',True,(0,0,0))
        backRect=backText.get_rect()
        backRect.center=backButton.center
        pygame.draw.rect(screen,(255,255,255),backButton)
        screen.blit(backText,backRect)
        #Showing instructions
        screen.blit(instruction,(150,20))

        if pygame.mouse.get_pressed()[0]:
            mouse=pygame.mouse.get_pos()
            #Enters when back button is pressed
            if backButton.collidepoint(mouse):
                help_page=False
                main_page=True
                pygame.display.flip()
        pygame.display.update()

    else:
        place_piece()
        #Exit Button
        exitButton=pygame.Rect(700,500,70,40)
        exitText=font.render('Exit',True,(0,0,0))
        exitRect=exitText.get_rect()
        exitRect.center=exitButton.center
        pygame.draw.rect(screen,(255,255,255),exitButton)
        screen.blit(exitText,exitRect)
        #Shows the turn of the player
        turnButton=pygame.Rect(780,500,100,40)
        if turn=='white':
            turnText=font.render('White',True,(0,0,0))
        else:
            turnText=font.render('Black',True,(0,0,0))
        turnRect=turnText.get_rect()
        turnRect.center=turnButton.center
        pygame.draw.rect(screen,(255,255,255),turnButton)
        screen.blit(turnText,turnRect)

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse=pygame.mouse.get_pos()
                if exitRect.collidepoint(mouse):
                    game_over(turn,font,screen)
                    done=True
                #Moves the selected piece to selected position
                elif len(possibleMoves)!=0:
                    for k in range(len(possibleMoves)):
                        rec=pygame.Rect(possibleMoves[k][0],possibleMoves[k][1],cell_size,cell_size)
                        x_value=int((mouse[0]-horiz_padding)/cell_size)
                        y_value=int((mouse[1]-verti_padding)/cell_size)
                        if rec.collidepoint(mouse):
                            board[x_prev][y_prev]=0
                            if selected_item=='pawn':
                                selected_item='None'
                                p,q,r=kill(player_id,rec.center[0],rec.center[1],chess)
                                if p!='None':
                                    chess[p][q].pop(r)
                                chess[player_id][0][x].center=rec.center
                                board[x_value][y_value]=1
                            elif selected_item=='rook':
                                selected_item='None'
                                p,q,r=kill(player_id,rec.center[0],rec.center[1],chess)
                                if p!='None':
                                    chess[p][q].pop(r)
                                chess[player_id][1][x].center=rec.center
                                board[x_value][y_value]=2
                            elif selected_item=='knight':
                                selected_item='None'
                                p,q,r=kill(player_id,rec.center[0],rec.center[1],chess)
                                if p!='None':
                                    chess[p][q].pop(r)
                                chess[player_id][2][x].center=rec.center
                                board[x_value][y_value]=3
                            elif selected_item=='bishop':
                                selected_item='None'
                                p,q,r=kill(player_id,rec.center[0],rec.center[1],chess)
                                if p!='None':
                                    chess[p][q].pop(r)
                                chess[player_id][3][x].center=rec.center
                                board[x_value][y_value]=4
                            elif selected_item=='king':
                                selected_item='None'
                                p,q,r=kill(player_id,rec.center[0],rec.center[1],chess)
                                if p!='None':
                                    chess[p][q].pop(r)
                                chess[player_id][4][x].center=rec.center
                                board[x_value][y_value]=5
                            elif selected_item=='queen':
                                selected_item='None'
                                p,q,r=kill(player_id,rec.center[0],rec.center[1],chess)
                                if p!='None':
                                    chess[p][q].pop(r)
                                chess[player_id][5][x].center=rec.center
                                board[x_value][y_value]=6
                            #Changes turn
                            turn=change_turn(player_id)
                            main_page=False
                            help_page=False
                            design_board()
                            place_piece()
                            #Adds sound
                            sound=mixer.Sound('click.wav')
                            sound.play()
                            #Checks whether king is killed
                            if q==4:
                                game_over(p,font,screen)
                                time.sleep(2)
                                done=True
                                break
                            possibleMoves.clear()
                            killMoves.clear()
                            #Buzzer sound is produced,when check move is done
                            if(check_mate(False,chess[turn][4][0].center[0],chess[turn][4][0].center[1],chess,turn,screen,killMoves,checkMoves)):
                                show_target(screen,killMoves)
                            place_piece()
                            pygame.display.update()
                            if len(killMoves)!=0:
                                #Add Buzzer sound
                                buzz=mixer.Sound('buzzer.wav')
                                buzz.play()
                                time.sleep(2)
                            break
                    main_page=False
                    help_page=False
                    checkMoves.clear()
                    killMoves.clear()
                    possibleMoves.clear()
                    design_board()
                    place_piece()
                else:
                    if turn=='white':
                        x_prev,y_prev,player_id,x,selected_item=piece_checking(turn)
                    else:
                        x_prev,y_prev,player_id,x,selected_item=piece_checking(turn)
                    if selected_item=='king' and len(possibleMoves)==0:
                        game_over(turn,font,screen)
                    show_choice(screen,possibleMoves)
                    show_target(screen,killMoves)
    pygame.display.update()
