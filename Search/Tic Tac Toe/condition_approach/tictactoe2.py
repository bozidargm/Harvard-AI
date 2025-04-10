from random import choice
from time import sleep

print('                  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
print('                  x                               x')
print('                  x           Tic Tac Toe         x')
print('                  x                               x')
print('                  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
print()
print('                       WELCOME TO TIC TAC TOE      ')
print()
print()

# gaming board
t = '''                               a b c
                             1 _ _ _
                             2 _ _ _              
                             3 _ _ _  '''       
d = {'a1':68,'b1':70,'c1':72,
     'a2':105,'b2':107,'c2':109,
     'a3':156,'b3':158,'c3':160}
indexes = [68,70, 72,105,107,109,156,158,160]
cells = ['a1','a2','a3','b1','b2','b3','c1','c2','c3']
winner, loser = False, False
print(t)
print()
print()

x = ''
schema = [['a1','a2','a3'],
          ['b1','b2','b3'],
          ['c1','c2','c3'],
          ['a1','b1','c1'],
          ['a2','b2','c2'],
          ['a3','b3','c3'],
          ['a1','b2','c3'],
          ['a3','b2','c1']]
me, PC, result = [], [], [0,0]
print(f'Current result is: player: {result[0]} - PC: {result[1]}')
print()
def fagain():
    """
    Function for restarting game
    """
    t = '''                               a b c
                             1 _ _ _
                             2 _ _ _              
                             3 _ _ _  '''
    print(t)
    indexes = [68,70, 72,105,107,109,156,158,160]
    cells = ['a1','a2','a3','b1','b2','b3','c1','c2','c3']
    me, PC = [], []
    return t, indexes, cells, me, PC

while cells:
    winner, loser = False, False
    print()
    x = input('Make your move: ')
    while x not in cells:
        print()
        x = input('You made incorrect move - try again: ')
    
    # List of moves made
    me.append(x)
    # Place on the board   
    i = d[x]                 
    t = t[:i] + 'X' + t[i+1:]
    indexes.remove(i)
    cells.remove(x)
    print()
    print(t)
    print()
    print()
    print(f'Current result is: player: {result[0]} - PC: {result[1]}')
    print()
    me.sort()
    if len(me) == 3 and me in schema:
        print()
        print('CONGRATULATIONS!!! You winn!')
        result[0] += 1
        winner = True
        print()
        print(f'Current result is: player: {result[0]} - PC: {result[1]}')
        print()
        again = input('Would you like to continue (y/n): ')
        if again == 'y':
            print()
            t, indexes, cells, me, PC = fagain()
        else:
            print() 
            print('See you next time.')
            break
    elif len(me) == 4:
        combinations = [me[:3], me[1:], [me[0]]+me[2:], me[:2]+[me[-1]]]
        for i in combinations:
            for j in schema:
                if j == i:
                    winner = True
        if winner:
            print()
            print('CONGRATULATIONS!!! You winn!')
            result[0] += 1
            print()
            print(f'Current result is: player: {result[0]} - PC: {result[1]}')
            print()
            again = input('Would you like to continue (y/n): ')
            if again == 'y':
                print()
                t, indexes, cells, me, PC = fagain()
            else:
                print() 
                print('See you next time.')
                break
    elif len(me) == 5:
        # Combinations of moves made
        combinations = [me[:3], me[1:4], me[2:], me[0:2]+[me[3]],\
        me[0:2]+[me[4]], me[1:3]+[me[4]], [me[0]]+me[3:],\
        [me[1]]+ me[3:],[me[0]]+[me[2]]+[me[4]], [me[0]]+me[2:4]]  
        for i in combinations:
            for j in schema:
                if j == i:
                    winner = True
        if winner:
            print()
            print('CONGRATULATIONS!!! You winn!')
            result[0] += 1
            print()
            print(f'Current result is: player: {result[0]} - PC: {result[1]}')
            print()
            again = input('Would you like to continue (y/n): ')
            if again == 'y':
                print()
                t, indexes, cells, me, PC = fagain()
            else:
                print() 
                print('See you next time.')
                break
    if winner or loser:
        pass
    else:
        if cells:
            # PC move
            y = ''              
            if not me or me == ['a1'] or me == ['a2'] or me == ['a3'] or me == ['b1']\
            or me == ['b3'] or me == ['c1'] or me == ['c2'] or me == ['c3'] and 'b2' in cells:
                y = 'b2'
            elif me == 'b2':
                y = choice(cells)
            elif (('a1' in me and 'a2' in me) or ('b3' in me and 'c3' in me) \
            or ('b2' in me and 'c1' in me)) and 'a3' in cells:
                y = 'a3'
            elif (('a2' in me and 'a3' in me) or ('b1' in me and 'c1' in me) \
            or ('b2' in me and 'c3' in me)) and 'a1' in cells:
                y = 'a1'
            elif (('a1' in me and 'b1' in me) or ('c2' in me and 'c3' in me) \
            or ('a3' in me and 'b2' in me)) and 'c1' in cells:
                y = 'c1'
            elif (('a3' in me and 'b3' in me) or ('c1' in me and 'c2' in me) \
            or ('a1' in me and 'b2' in me)) and 'c3' in cells:
                y = 'c3'
            elif (('a1' in me and 'a3' in me) or ('b2' in me and 'c2' in me)) \
            and 'a2' in cells:
                y = 'a2'
            elif (('a2' in me and 'b2' in me) or ('c1' in me and 'c3' in me)) \
            and 'c2' in cells:
                y = 'c2'
            elif (('a1' in me and 'c1' in me) or ('b2' in me and 'b3' in me)) \
            and 'b1' in cells:
                y = 'b1'
            elif (('a3' in me and 'c3' in me) or ('b1' in me and 'b2' in me)) \
            and 'b3' in cells:
                y = 'b3'
            elif (('a1' in me and 'b2' in me) or ('b1' in me and 'b2' in me)) \
            and 'b3' in cells:
                y = 'b3'
            else:
                y = choice(cells)

            PC.append(y)
            # Place on the board
            z = d[y]                  
            t = t[:z] + 'O' + t[z+1:]
            cells.remove(y)
            indexes.remove(z)
            sleep(2)
            print()
            print(t)
            print()
            PC.sort()
            if len(PC) == 3 and PC in schema:
                print()
                print('Sorry, you lost this time.')
                result[1] += 1
                loser = True
                print()
                print(f'Current result is: player: {result[0]} - PC: {result[1]}')
                print()
                again = input('Would you like to continue (y/n): ')
                if again == 'y':
                    print()
                    t, indexes, cells, me, PC = fagain()
                else:
                    print() 
                    print('See you next time.')
                    break
            elif len(PC) == 4:
                combinations = [PC[:3], PC[1:], \
                [PC[0]]+PC[2:], PC[:2]+[PC[-1]]]
                for i in combinations:
                    for j in schema:
                        if j == i:
                            loser = True
                if loser:
                    print()
                    print('Sorry, you lost this time.')
                    result[1] += 1
                    print()
                    print(f'Current result is: player: {result[0]} - PC: {result[1]}')
                    print()
                    again = input('Would you like to continue (y/n): ')
                    if again == 'y':
                        print()
                        t, indexes, cells, me, PC = fagain()
                    else:
                        print()
                        print('See you next time.')
                        break
            elif len(PC) == 5:
                # Combinations of moves made
                combinations = [PC[:3], PC[1:4], PC[2:], \
                PC[0:2]+[PC[3]], PC[0:2]+[PC[4]], \
                PC[1:3]+[PC[4]], [PC[0]]+PC[3:],\
                [PC[1]]+ PC[3:], \
                [PC[0]]+[PC[2]]+[PC[4]]]  
                for i in combinations:
                    for j in schema:
                        if j == i:
                            loser = True
                if loser:
                    print()
                    print('Sorry, you lost this time.')
                    result[1] += 1
                    print()
                    print(f'Current result is: player: {result[0]} - PC: {result[1]}')
                    print()
                    again = input('Would you like to continue (y/n): ')
                    if again == 'y':
                        print()
                        t, indexes, cells, me, PC = fagain()
                    else:
                        print()
                        print('See you next time.')
                        break
        else:
            print() 
            print("It's tied")
            print()
            print(f'Current result is: player: {result[0]} - PC: {result[1]}')
            print()
            again = input('Would you loke to try again (y/n): ')
            if again == 'y':
                print()
                t, indexes, cells, me, PC = fagain()
            else:
                print() 
                print('See you next time.')
                break