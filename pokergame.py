#Graphic interface of a basic game of Poker on 'flet'
#by Lucas A. Oliveira

import flet as ft
import time
import pokerlogic as pkl
import importlib


#imports the values of the deck, 2 hands, table, 
#final rank of the hands and the winner

embb = pkl.embb                  #SHUFFLED DECK
maop1 = pkl.maoplayer1           #PLAYER 1 HAND
maop2 = pkl.maoplayer2           #PLAYER 2 HAND
mesa = pkl.mesa                  #TABLE
ranktotalp1 = pkl.ranktotalp1    #RANK OF P1 HAND
ranktotalp2 = pkl.ranktotalp2    #RANK OF P2 HAND
ranktotalm = pkl.ranktotalm      #RANK OF TABLE
win = pkl.vencedor               #WINNER


def main (page: ft.Page):

    page.title = 'Poker 10JQKA'
    page.window.height = 730
    page.window.width = 600

    def iniciar(e):

        """Starts the game after choosing a starting stack value"""

        saldop1.value = 0
        saldop2.value = 0        
        layout.controls[0] = telajogo
        saldop1.value = f'{insertsaldo.value}'
        saldop2.value = f'{insertsaldo.value}'
        betslider.max = int(saldop1.value)
        novarodada(e)
        betslider.disabled = False
        fold.disabled = False
        check.disabled = False
        bet.disabled = False                           
        page.update()          
        
    def voltar(e):

        """Return to menu"""

        layout.controls[0] = menuinicial 
        layout.update()       
        page.update()

    def btn_onoff(x):

        """Disable/Enable all buttons at once"""

        if x== 'on':
            fold.disabled = False
            check.disabled = False
            bet.disabled = False
            betslider.disabled = False 
        elif x == 'off':
            fold.disabled = True
            check.disabled = True
            bet.disabled = True
            betslider.disabled = True 
            

    def novarodada(e):

        """A New round, gets new values for the hands and table"""

        if saldop1.value == 0 or saldop1.value =='0':
            return
        
        global mesa
        global ranktotalp2
        global ranktotalp1
        global ranktotalm
        global win

        importlib.reload(pkl)
        cartasp1.data = pkl.maoplayer1
        if diff.value == 'Impossible Mode ON':
            cartasp2.data = [pkl.best_hand_final[-2],pkl.best_hand_final[-1]]
        else:
            cartasp2.data = pkl.maoplayer2
        cartasp1.controls = criarcarta(cartasp1.data)
        cartasp2.controls = backcard        
        mesa = pkl.mesa
        ranktotalp1 = pkl.ranktotalp1
        ranktotalp2 = pkl.ranktotalp2
        ranktotalm = pkl.ranktotalm        
        win = pkl.vencedor
        cartasmesa.data = 0
        btn_onoff('on')        

        page.update()             

    def criarcarta(maoplayer):

        """Creates the UI of a Card """

        return [ft.Container(
                height=107,
                width=80,
                border_radius= ft.border_radius.all(5),
                border= ft.border.all(width=2, color='black'),
                bgcolor="white",
                content= ft.Column(
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,              
                    controls=[         
                            numerocarta(carta),
                            naipecarta(carta)
                            ]             
                    )) for carta in maoplayer] 

    def sliderchange(e):

        slidertext.value = f'{int(e.control.value)}'
        page.update()

    def foldar(e):

        """Player 1 (you) folds"""

        global win
        win = 'PLAYER2'
        saldop2.value = int(saldop2.value) + int(pot.value)
        pot.value = '0'
        cartasmesa.data = 4                                    
        page.update()             

        fasejogo(e)

  
    def checksaldo(e):

        """Check the current stacks values, when 0 pops up to start again"""

        saldop1.value = int(saldop1.value)
        saldop2.value = int(saldop2.value)
         

        if saldop1.value == 0:            
            alerta = ft.AlertDialog(
                title=ft.Text('Vc Perdeu tudo!'),                
                actions= [
                ft.TextButton(
                    text= 'Jogar novamente', 
                    on_click= lambda e: (voltar(e),page.close(alerta))
                )               
                ]                 
            ) 
            page.open(alerta)

        elif saldop2.value == 0:
            alerta = ft.AlertDialog(
                title=ft.Text('Você eliminou Player 2'),
                content= ft.Text('Você Venceu!!'),                
                actions= [
                ft.TextButton(
                    text= 'Jogar novamente', 
                    on_click= lambda e: (voltar(e),page.close(alerta))
                )               
                ]                 
            ) 
            page.open(alerta) 

    def allin(e):

        """Begins a ALLIN sequence wherever gamephase you are currently"""  

        if cartasmesa.data == 0:

            #PRE FLOP

            cartasp2.controls = criarcarta(cartasp2.data)
            cartasmesa.data +=1            
            jogador1.data = mesa[0:3]
            cartasmesa.controls = criarmesa()            
            page.update()
            time.sleep(2)
            cartasmesa.data +=1            
            jogador1.data = mesa[0:4]
            cartasmesa.controls = criarmesa()            
            page.update()
            time.sleep(2)
            cartasmesa.data +=1            
            jogador1.data = mesa[:]
            cartasmesa.controls = criarmesa()            
            page.update()
            time.sleep(2)
            venceu = vencedor()
            mensagem.value = f'{venceu}'            
            page.update()            
            time.sleep(2)            
            cartasmesa.data = 0            
            jogador1.data = []
            cartasmesa.controls = criarmesa()
            mensagem.value = 'Nova Rodada'
            time.sleep(2)
            checksaldo(e)            
            novarodada(e)            
            page.update()
            
            
        elif cartasmesa.data == 1:

            #Already on FLOP

            cartasp2.controls = criarcarta(cartasp2.data)
            cartasmesa.data +=1            
            jogador1.data = mesa[0:4]
            cartasmesa.controls = criarmesa()            
            page.update()
            time.sleep(2)
            cartasmesa.data +=1            
            jogador1.data = mesa[:]
            cartasmesa.controls = criarmesa()            
            page.update()
            time.sleep(2)
            venceu = vencedor()
            mensagem.value = f'{venceu}'                        
            page.update()            
            time.sleep(2)                         
            cartasmesa.data = 0            
            jogador1.data = []
            cartasmesa.controls = criarmesa()
            mensagem.value = 'Nova Rodada'
            time.sleep(2)
            novarodada(e)            
            checksaldo(e)            
            page.update()
             
        
        elif cartasmesa.data == 2:

            #On Turn

            cartasp2.controls = criarcarta(cartasp2.data)
            cartasmesa.data +=1            
            jogador1.data = mesa[:]
            cartasmesa.controls = criarmesa()            
            page.update()
            time.sleep(2)
            venceu = vencedor()
            mensagem.value = f'{venceu}'            
            page.update()            
            time.sleep(2)                        
            cartasmesa.data = 0            
            jogador1.data = []
            cartasmesa.controls = criarmesa()
            mensagem.value = 'Nova Rodada'
            time.sleep(2)
            novarodada(e)                                  
            checksaldo(e)            
            page.update() 
       
        elif cartasmesa.data == 3:

            #On River

            cartasp2.controls = criarcarta(cartasp2.data)                      
            page.update()
            time.sleep(2)
            venceu = vencedor()
            mensagem.value = f'{venceu}'            
            page.update()            
            time.sleep(2)                        
            cartasmesa.data = 0            
            jogador1.data = []
            cartasmesa.controls = criarmesa()
            mensagem.value = 'Nova Rodada'
            time.sleep(2)
            novarodada(e)                                  
            checksaldo(e)            
            page.update()   
                   
        
    
    def apostar (e):

        """Does the betting sequence, and  checks for an ALLIN condition
        PLayer 2 ALWAYS CALL"""
        
        btn_onoff('off')

        page.update()
        time.sleep(1)

        bet_atual.value = int(betslider.value)   

        
        if bet_atual.value == int(saldop1.value):

            #PLAYER1 ALLIN

            saldop1.value = '0'                             
            mensagem.value = 'O Player 1 deu allin, Player 2 aceitou sua aposta!'
           
            if int(bet_atual.value) > int(saldop2.value):

                #CHECKS FOR P2 STACKS IF ITS SMALLER THAN P1 AND BETS ONLY P2 VALUE
                bet_p2.value = saldop2.value
                saldop2.value = '0'

            else:
                saldop2.value = str(int(saldop2.value) - int(bet_atual.value))
                bet_p2.value = bet_atual.value

            page.update()            
            pot.value = int(pot.value)+int(bet_p2.value)+int(bet_atual.value)
            bet_p2.value, bet_atual.value = 0, 0
            page.update()
            time.sleep(1)
            allin(e)
            btn_onoff('on')
            return              

        if int(bet_atual.value) > int(saldop2.value):
                
                #CHECKS FOR P2 STACKS IF ITS SMALLER THAN P1 AND BETS ONLY P2 VALUE
                #(NOT AN ALLIN FOR P1)

                bet_atual.value = saldop2.value 
                saldop1.value = str(int(saldop1.value) - int(bet_atual.value))            
                mensagem.value = 'O Player 2 deu all in'
                bet_p2.value = saldop2.value
                saldop2.value = '0'
                bet_atual.value = bet_p2.value
                pot.value = int(pot.value)+int(bet_p2.value)+int(bet_atual.value)
                bet_p2.value, bet_atual.value = 0, 0
                page.update()                
                time.sleep(1)
                allin(e)
                btn_onoff('on')
                return  

        else:
                #PLAYER 2 CALLS

                saldop1.value = str(int(saldop1.value) - int(bet_atual.value))                               
                time.sleep(1)
                mensagem.value = 'O Player 2 aceitou sua aposta!'
                page.update()  
                saldop2.value = str(int(saldop2.value) - int(bet_atual.value))
                bet_p2.value = bet_atual.value
            
        page.update()
        time.sleep(1)
        pot.value = int(pot.value)+int(bet_p2.value)+int(bet_atual.value)
        bet_p2.value, bet_atual.value = 0, 0            
        page.update()

        fasejogo(e)

        btn_onoff('on') 
        page.update()
             
        

    insertsaldo = ft.TextField(label="Insira o saldo de fichas: ",value='')
    btiniciar = ft.ElevatedButton(text="Iniciar",on_click=iniciar)

    def vencedor(): 

        """Gets the winner from the poker logic file and does the pot division"""       
        
        global win        
        venceu = 0
        p2hand = pkl.maop2string
        
        if diff.value == 'Impossible Mode ON':
            win = 'PLAYER2'
            p2hand = pkl.nomesdasmaos(pkl.best_rankpossb)

        if win == 'PLAYER1':
            venceu = f'Player 1 Venceu com um: {pkl.maop1string}'
            saldop1.value = int(saldop1.value) + int(pot.value)
            pot.value = '0'
        elif win == 'PLAYER2':
            venceu = f'Player 2 Venceu com um: {p2hand}'
            saldop2.value = int(saldop2.value) + int(pot.value)
            pot.value = '0'            
        elif win == 0:
            venceu = f'Empate {pkl.mesastring}'
            saldop1.value = int(saldop1.value) + int(pot.value)/2
            saldop2.value = int(saldop2.value) + int(pot.value)/2
            pot.value = '0'        
         
        return venceu


    def fasejogo(e): 

        """Phases of the game, the game already starts at preflop"""
        
        btn_onoff('off')               
        page.update()
        time.sleep(1)
        saldop1.value = int(saldop1.value)

        if cartasmesa.data == 0:
            
            #Starts the FLOP

            cartasmesa.data +=1            
            jogador1.data = mesa[0:3]
            cartasmesa.controls = criarmesa()
            mensagem.value = 'O Flop Chegou, Aposte novamente'
            betslider.max = saldop1.value
            page.update()
            
        elif cartasmesa.data == 1:

            #THE TURN

            cartasmesa.data +=1            
            jogador1.data = mesa[0:4]
            cartasmesa.controls = criarmesa()
            mensagem.value = 'O Turn Chegou, Aposte novamente'
            betslider.max = saldop1.value
            page.update()

        elif cartasmesa.data == 2:

            #THE RIVER

            cartasmesa.data +=1            
            jogador1.data = mesa[:]
            cartasmesa.controls = criarmesa()
            mensagem.value = 'O River Chegou, Aposte novamente'
            betslider.max = saldop1.value
            page.update()

        elif cartasmesa.data == 3: 

            #SHOWDOWN, reveals P2 CARDS, gets the winner, check stacks, new round

            cartasp2.controls = criarcarta(cartasp2.data)
            venceu = vencedor()
            mensagem.value = f'{venceu}'            
            page.update()            
            time.sleep(2)            
            cartasmesa.data = 0            
            jogador1.data = []
            cartasmesa.controls = criarmesa()
            mensagem.value = 'Nova Rodada'
            time.sleep(2)
            page.update()
            checksaldo(e)
            novarodada(e)                       
            page.update()
        
        elif cartasmesa.data == 4:

            #PLAYER 1 Folded, P2 auto-win, restarts everything
           
            venceu = f'{win} Venceu'            
            mensagem.value = f'{venceu}'            
            page.update()            
            time.sleep(2)            
            cartasmesa.data = 0            
            jogador1.data = []
            cartasmesa.controls = criarmesa()
            mensagem.value = 'Nova Rodada'
            time.sleep(2)
            page.update()
            checksaldo(e)
            novarodada(e)                       
            page.update()


        btn_onoff('on')
        page.update()    
 

    def naipesimb(x):

        """Hearts == 1 / Diamonds = 2 / Clubs = 3 / Spades = 4 """

        if x == 1:
            simb = '♥'
        elif x == 2:
            simb = '♦'
        elif x == 3:
            simb = '♣'
        elif x == 4:
            simb = '♠'
        return simb   
 
    def naipecores(x):

        """Colors of the Suits"""

        if x == 1:
            cor = 'Red'
        elif x == 2:
            cor = 'Red'
        elif x == 3:
            cor = 'Black'
        elif x == 4:
            cor = 'Black'
        else:
            cor = 'White'
        return cor
    
    def numerocarta(n=0):

        """Translate the numbers from poker logic file and creates UI card"""

        numeros = {
            11: 'J', 12: 'Q', 13:'K', 14: 'A',
            1: '1', 2: '2', 3: '3', 4: '4', 5: '5',
            6: '6', 7:'7', 8:'8', 9:'9', 10:'10'            
            }        
        if n == 0:
            carta = [0,0]
        else:  
            carta = divmod(n,10)
                   
        return ft.Text(        
                value= f'{numeros[carta[0]]}',
                size= 25,                
                weight= ft.FontWeight.BOLD,
                color= f'{naipecores(carta[1])}')
    
    def naipecarta(n=0):

        """Creates the UI of the Suits for the Cards, gets the colors and symbol"""

        carta = divmod(n,10)
        return ft.Text(
                value= f'{naipesimb(carta[1])}',
                size= 35,
                weight= ft.FontWeight.BOLD,
                color= f'{naipecores(carta[1])}',
                )

    
    #Buttons of the game

    fold = ft.ElevatedButton(text='FOLD', width=80, height=20, on_click=foldar)
    check = ft.ElevatedButton(text='CHECK', width=80, height=20,on_click=fasejogo)
    bet = ft.ElevatedButton(text='APOSTA', width=80, height=20,on_click=apostar)

    
    #PLAYER 1 UI Cards    
    cartasp1 = ft.Row(
        data= maop1,                    
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment= ft.CrossAxisAlignment.END,
        controls=[
            ft.Container(                                
                height=107,
                width=80,
                border_radius= ft.border_radius.all(5),
                border= ft.border.all(width=2, color='black'),
                bgcolor="white",
                content= ft.Column(
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,              
                    controls=[         
                            numerocarta(carta),
                            naipecarta(carta)
                            ]             
                    )) for carta in maop1]
    )
    

    #Hides the P2 Cards     
    backcard = [ft.Image(
        src= 'baralho.png',
        width=88,
        height=120
    ) for carta in range(2)]    

    #PLAYER 2 UI Cards
    cartasp2 = ft.Row(
        data=maop2,        
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment= ft.CrossAxisAlignment.START,
        controls= backcard
        ) 
    

    #If you want to see the P2 Cards all the time, 
    #just put this on cartasp2.controls            
    """[ft.Container(
                height=107,
                width=80,
                border_radius= ft.border_radius.all(5),
                border= ft.border.all(width=2, color='black'),
                bgcolor="white",
                content= ft.Column(
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,              
                    controls=[         
                            numerocarta(carta),
                            naipecarta(carta)
                            ]             
                    )) for carta in maop2]"""
    

    #Define the stacks, bet, pot and message initial values '0'

    saldop1 = ft.Text(value='0',size=20,weight=ft.FontWeight.BOLD)
    saldop2 = ft.Text(value='0',size=20,weight=ft.FontWeight.BOLD)
    bet_atual = ft.Text(value='0',size=20,weight=ft.FontWeight.BOLD)
    bet_p2 = ft.Text(value='0',size=20,weight=ft.FontWeight.BOLD)    
    mensagem = ft.Text(value='O jogo Começou, Faça uma aposta!', size=20, weight= ft.FontWeight.W_500)
    pot = ft.Text(value='0',size=20,weight=ft.FontWeight.BOLD)
    
    #LAYOUT of the things in the UI

    #PLayer 1 current bet, cards, stack
    jogador1 = ft.Column(
        data= [],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        controls= [
            bet_atual,
            cartasp1,
            saldop1
        ]
    )
    
    #PLayer 2 current bet, cards, stack
    jogador2 = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        controls= [
            saldop2,            
            cartasp2,
            bet_p2,
            ]
    ) #npc

    #Betslider
    slidertext = ft.Text()    
    betslider = ft.Slider(
                    min=0,
                    max=1,
                    divisions=10,                    
                    on_change=sliderchange
                    )


    def criarmesa():

        """Creates the UI of the table cards, which values are stored in
        jogador1.data (Player1)"""

        return [ft.Container(
                    height=107,
                    width=80,
                    border_radius= ft.border_radius.all(5),
                    border= ft.border.all(width=2, color='black'),
                    bgcolor="white",
                    content= ft.Column(                   
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,              
                        controls=[         
                                numerocarta(carta),
                                naipecarta(carta)
                                ]             
                            )
                        ) for carta in jogador1.data]
        

    cartasmesa = ft.Row(
        data=0,        
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment= ft.CrossAxisAlignment.END,
        controls= criarmesa()
    )  
    
    #LAYOUT of the Table: Message, Player2, pot, Table, Player1
    mesalayout = ft.Column(                
        tight=True,
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,        
        controls=[
            mensagem,jogador2,pot,cartasmesa,jogador1
        ]
    )
    
    #Buttons
    botoes = ft.Row(
        alignment= ft.MainAxisAlignment.END,
        controls=[fold,check,bet,slidertext,betslider]        
    )

    def modo(e):

        if diff.value == 'Impossible Mode ON':
            diff.value = 'Impossible Mode OFF'
        else:
            diff.value = 'Impossible Mode ON'
        page.update()

    unbeatable_btn = ft.ElevatedButton(
        text="ON/OFF",
        on_click=modo,
        color=ft.Colors.RED
        )
    unbeatable = ft.Column(
        alignment= ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,                           
        controls=[
            diff := ft.Text(
                value='Impossible Mode ON',
                size= 12,
                text_align='center',
                weight= ft.FontWeight.BOLD),
            unbeatable_btn
            ]
            )
    
    #Game layout
    telajogo = ft.Column(
        data=0,
        expand=True,
        controls=[mesalayout,botoes])

    #MENU
    menuinicial = ft.Row(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment= ft.CrossAxisAlignment.CENTER,
        controls=[
            insertsaldo,btiniciar,unbeatable
            ]         
    )


    layout = ft.Column(
        height=500,
        width=670,
        expand=True,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        alignment= ft.MainAxisAlignment.CENTER,
        controls=[menuinicial]
    )


    page.add(layout)    
    
    page.update()
    
    

if __name__ == '__main__':
    ft.app(target=main)