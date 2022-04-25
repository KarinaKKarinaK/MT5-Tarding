#importing necessary libraries
import MetaTrader5 as mt5
import sys
import time

#Connect Python to Meta Tarder 
mt5.initialize()

#Configs
TICKET = 50086766789 #replace ticket no.
MAX_DIST_SL = 0.0005 #50 pips, max distance between current price and sl, otherwise SL will update
TRAIL_AMOUNT = 0.0002 #Amount by how uch SL updates
DEFAULT_SL = 0.0005 #If position has no Sl, set a default SL

def trail_sl():
    #Get position based on teh ticket id
    position = mt5.position_get(ticket=TICKET)[0]
    if position:
        position = position[0]
    else:
        print('position does not exist.')
        sys.exit()

    #Get position data
    symbol = position.symbol
    order_type = position.type
    price_current = position.price_current
    price_open = position.price_open
    sl = position.sl


    dist_from_sl = abs(round(price_current - sl, 6))

    if dist_from_sl > MAX_DIST_SL:
        if sl != 0.0:
        #Calculating new sl
            if order_type == 0: #0 stands for BUY
                new_sl = sl + TRAIL_AMOUNT

            elif order_type == 1: #1 stands for SELL
                new_sl = sl - TRAIL_AMOUNT
        else:
            #Setting default stop loss if teher is no SL on teh symbol
            new_sl = price_open - DEFAULT_SL if order_type == 0 else price_open + DEFAULT_SL 

        request = {
            'action': mt5.TRADE_ACTION_SLTP,
            'position': TICKET,
            'sl': new_sl,
        }

        result = mt5.order_send(request)
        print(result)
        return result

if __name__ == '__main__':
    print("Starting Tariling Stoploss.")
    print(f"Position:  {str(TICKET)}")

    while True:
        result = trail_sl()
        #Wait 1 second
        time.sleep(1)
