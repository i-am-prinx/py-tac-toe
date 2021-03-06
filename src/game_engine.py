# imports
import sys
from colr import color, Colr as C
from pynput import keyboard

from player import Player
from board import Board, move_right, move_left, move_up, move_down

#************************** Needed global variable ************************** #

turns = 1               # turns which denotes which player's turn it is to play
gameFlag = True         # will be used to signify if game has started or ended


pOne = pTwo = playingPlayer = None



# ************************ Helper Method Declaration *********************** #

def note_which_player( turns ):
    '''
    helps to tell which players turn it is
    '''
    if turns == 1:
        return "playerOne"
    if turns == 2:
        return "playerTwo"



def swap_player_turn( ):
    '''
    changes turns of players to play
    '''

    # use the global turns variable
    global turns

    if turns == 1:
        turns += 1

    elif turns == 2:
        turns -= 1



def display_top_info( ):
    '''
    displays needed information at the top of game view
    '''
    its_player_turn = get_playing_player().playerName
    
    print(
        C()
        .bold().yellow(
            '\n\n\n\n\n\n\n\nxxx  PY-TAC-TOE  xxx\n' +
            '***\t\t ***\n'+
            '***\t\t ***'
        )

        (
            """\n\n 
INSTRUCTIONS:
=============
            """
        )

        .bold().magenta('\nl ')
        (':\tmove column left')
        .bold().magenta('\nr ')
        (':\tmove column right')
        .bold().magenta('\nu ')
        (':\tmove row up')
        .bold().magenta('\nd ')
        (':\tmove row down')
        .bold().magenta('\nm ')
        (':\tmark position')
        .bold().magenta('\nq ')
        (':\tquit game')
        .bold().bright().yellow('\n***\t***\t***\n')
        .bold().bright().blue(f"\n--> {its_player_turn}'s turn\n")
    )



def get_playing_player( ):
    '''
    returns the player who's currently playing
    '''
    if turns == 1:
        return pOne
    return pTwo




def check_win( board, player_obj ):
    '''
    check if there is a win. A win can occur Horizontally, Vertically, &
    Diagonally. if there is a win it returns True and the pattern in which
    game was won, else it return False and None
    @param board:
        board object
    @param player_obj:
        player object
    '''
    if board.check_win_vertically( player_obj ) == 3:
        return True, 'Vertically'

    if board.check_win_horizontally( player_obj ) == 3:
        return True, 'Horizontally'

    if board.check_win_left_to_right_diagonally( player_obj ) == 3:
        return True, 'Left to Right Diagonal'

    if board.check_win_right_to_left_diagonally( player_obj ) == 3:
        return True, 'Right to Left Diagonal'

    return False, None



def display_winner(board, player_obj, pattern):
    '''
    displays game winner and stops game play automatically
    @param board:
        represents the board object
    @param player_obj:
        represents the player object
    @param pattern:
        represents the pattern in which a player won the game
        can be 'Horizontal', 'Vertical', 'Diagonal'
    '''
    global gameFlag
    print("\n" + player_obj.playerName + f" wins the game --- { pattern }")

    gameFlag = False
    sys.exit(0)


def display_draw(  ):
    global gameFlag
    print("** ** Draw ** **")

    gameFlag = False
    sys.exit( 0 )


def compute_input_received( player_input, board_obj ):
    '''
    call appropriate method based on the input received
    '''

    # updates the current column position by moving it to the right and
    # re-display board
    if player_input.lower().startswith('r'):
        move_right(board_obj, display_top_info)

    # updates the current column position by moving it to the left and
    # re-display board
    if player_input.lower().startswith('l'):
        move_left(board_obj, display_top_info)

    # updates the current row position by moving it down and re-display board
    if player_input.lower().startswith('u'):
        move_up(board_obj, display_top_info)

    # updates the current row position by moving it down and re-display board
    if player_input.lower().startswith('d'):
        move_down(board_obj, display_top_info)

    # add player mark to current row and col position only if that position
    # has not been marked before. A user is given another chance to mark an
    # empty position in case mark was not placed

    if player_input.lower().startswith('m'):
        was_marked = False
        err_msg = ''
        playingPlayer = get_playing_player( )

        # only if a player still have move, then a player will be able to
        # mark a position
        was_marked = board_obj.mark_rNc_position(playingPlayer.playerMark)
        row_number = board_obj.get_current_row( )
        column_number = board_obj.get_current_column( )

        # only if the cell was marked then we want to reduce players
        # move count and also swap players turn
        if was_marked:
            board_obj.increment_num_of_board_marked( )

            # if there is a win
            won, winPattern = check_win(board_obj, playingPlayer)

            if won:
                display_top_info( )
                board.set_rNc_position(column_number, row_number)
                display_winner( board_obj, playingPlayer, winPattern)

            # if there is a draw
            if not won and board.get_total_marks_on_board( ) == 9:
                display_top_info( )
                board.set_rNc_position(column_number, row_number)
                display_draw( )


            # if there is no win swap players turn
            swap_player_turn( )


        display_top_info( )

        if len(err_msg) > 0:
            print(err_msg)
            board_obj.set_rNc_position(
                board_obj.get_current_column(), board_obj.get_current_row()
            )

        else:
            board_obj.set_rNc_position(column_number, row_number)
    

    if player_input.lower().startswith('q'):
        print(
            C()
            .bold().red('Game not completed, either of you might have won\n\n')
        )
        keyboard.Listener.stop      # stop listening to keyboard event
        sys.exit()





# ********************** Implementation of game engine ******************** #


# create players ( players can only be 2 )
for i in range(3):
    if i == 1:
        name = input(f"{note_which_player(i)} ---- please enter your name: ")
        pOne = Player(i, name)

    if i == 2:
        name = input(f"{note_which_player(i)} ---- please enter your name: ")
        pTwo = Player(i, name)



# display top info
display_top_info( )

# draw board
board = Board( )


# Keyboard Event Controller
def on_press(key):
    """
    Event handler that capture the key that is pressed on the keyboard.
    This method listens to keyboard event and computes game logic based
    on the input / key received from the event
    """
    # in pynput keyboard keys are of two types alphanumeric and special
    # keys. char method can be called on alphanumeric keys to return the
    # alphabet e.g ('a', 'b', 'c', 'd') while a special key are Enter or
    # Return Key, Cntrl, Up, Down e.t.c.
    try:
        # retrieve the character representation of the key that is pressed
        # and use it to compute the game logic
        compute_input_received(key.char, board)

        # receive inputs ( compute for navigation
        # `l` --- left              `r` --- right
        # `u` --- up                `d` --- down
        # `m` --- mark              `q` --- quit

    except AttributeError:
        # if the user press a special key, just ignore and keep listening
        # for event.
        pass

def on_release(key):
    """
    Event handler that listens if key pressed down is released.
    It capture the key that was pressed down which is now been released
    """
    # If false is returned, the keyboard listener is destroyed
    return True


# Activate the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

