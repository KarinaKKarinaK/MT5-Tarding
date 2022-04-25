#Code from: https://stackoverflow.com/questions/61552973/getting-signals-from-telegram-channel-and-placing-them-in-mt4-using-python
import MetaTrader5 as mt5
from pyrogram import Client, filters
import re
from time import sleep

# Problems:
# - API key has to be inputtedf into the code 
# api_id: 9871990
# api_hash: 3b5e9dbccbcb96c9e0e8c491051ab51f
# App title: Signals


channels = {
    -1001416233252: {'type': 'channel', 'trading': 'str_long', 'url': 'test'},  #
    -1001445377985: {'type': 'channel', 'trading': 'str_long', 'url': '@americanforexspecialist'},  #
    -1001349935562: {'type': 'channel', 'trading': 'gold',     'url': '@bestForexSignalsPips'},  #
    -1001246538371: {'type': 'channel', 'trading': 'scalping', 'url': '@bestforextradinggroup'},  #
    -1001291056071: {'type': 'channel', 'trading': 'scalping', 'url': '@fXReaperFreeForexSignals'},  #
    -1001383532475: {'type': 'channel', 'trading': 'scalping', 'url': '@forexMoneyNLFree'},  #
    -1001411820913: {'type': 'channel', 'trading': 'scalping', 'url': '@forexPipsFactory2'},  #
    -1001480924116: {'type': 'channel', 'trading': 'scalping', 'url': '@forex_Signals_PIPs_Signal_Fx'},  #
    -1001270204996: {'type': 'channel', 'trading': 'scalping', 'url': '@forex_xlab1'},  #
    -1001126668980: {'type': 'group',   'trading': 'scalping', 'url': '@forexgreenpips958'},  #
    -1001414424977: {'type': 'group',   'trading': 'scalping', 'url': '@forexgroup1111'},  #
    -1001414424977: {'type': 'group',   'trading': 'scalping', 'url': '@Forexgroup112'},  #
    -1001414424977: {'type': 'group',   'trading': 'scalping', 'url': '@Forexkiller1123'},  #
    -1001311844342: {'type': 'channel', 'trading': 'scalping', 'url': '@forexsignalfactory'},  #
    -1001491035512: {'type': 'channel', 'trading': 'scalping', 'url': '@forexsignalsolutions'},  #
    -1001316056319: {'type': 'channel', 'trading': 'scalping', 'url': '@forexsignalsstreet'},  #
    -1001470291934: {'type': 'channel', 'trading': 'scalping', 'url': '@forexsignalvalue'},  #
    -1001420572107: {'type': 'channel', 'trading': 'scalping', 'url': '@forexsignalzz'},  #
    -1001062012353: {'type': 'group',   'trading': 'str_long', 'url': '@FxGlobal5'},  #
    -1001341052202: {'type': 'channel', 'trading': 'scalping', 'url': '@fxSignals_Gold'},  #
    -1001298489655: {'type': 'channel', 'trading': 'scalping', 'url': '@fxpipsaction1'},  #
    -1001399543862: {'type': 'channel', 'trading': 'scalping', 'url': '@fxpipsfactory'},  #
    -1001399543862: {'type': 'group',   'trading': 'scalping', 'url': '@fx_globaltrades'},  #
    -1001157841207: {'type': 'channel', 'trading': 'scalping', 'url': '@greenpipsforex'},  #
    -1001203106845: {'type': 'channel', 'trading': 'scalping', 'url': 'https://t.me/joinchat/AAAAAEe19B0ZIeRRXNOpAg'},
    -1001355784993: {'type': 'channel', 'trading': 'scalping', 'url': 'https://t.me/joinchat/AAAAAFDPoyF6DXvyQDYpDw'},
    -1001302273796: {'type': 'channel', 'trading': 'scalping', 'url': '@m5MacDScalpers'},  #
    -1001449789431: {'type': 'channel', 'trading': 'scalping', 'url': '@mADIFOREX_SIGNAL_MASTAR'},  #
    -1001299535263: {'type': 'channel', 'trading': 'scalping', 'url': '@metatrader4Signals0'},  #
    -1001494412791: {'type': 'channel', 'trading': 'scalping', 'url': '@metatrader5signal1'},  #
    -1001171155421: {'type': 'channel', 'trading': 'scalping', 'url': '@octaFxsignalx'},  #
    -1001148641286: {'type': 'channel', 'trading': 'scalping', 'url': '@pipstowin'},  #
    -1001392466168: {'type': 'channel', 'trading': 'scalping', 'url': '@proFxSecretStrategy'},  #
    -1001473518645: {'type': 'channel', 'trading': 'scalping', 'url': '@professoroff'},  #
    -1001391473841: {'type': 'channel', 'trading': 'scalping', 'url': '@ronaldpatrick'},  #
    -1001141061818: {'type': 'channel', 'trading': 'scalping', 'url': '@signal4000'},  #
    -1001409206299: {'type': 'channel', 'trading': 'scalping', 'url': '@signalfxoption'},  #
    -1001471162189: {'type': 'group',   'trading': 'scalping', 'url': '@signalsscalping12'},  #
    -1001127289760: {'type': 'channel', 'trading': 'scalping', 'url': '@sureshotforex'},  #
    -1001331117752: {'type': 'channel', 'trading': 'scalping', 'url': '@taarget_plus'},  #
    -1001296877896: {'type': 'channel', 'trading': 'scalping', 'url': '@trendFriend12'},  #
    -1001188607041: {'type': 'channel', 'trading': 'scalping', 'url': '@vipCoinexhangePump'},  #
    -1001398995940: {'type': 'channel', 'trading': 'str_long', 'url': '@voltforex'},
}

symbols = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'GBPAUD', 'GBPCAD',
           'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD',
           'EURUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDCNH', 'USDJPY', 'XAUUSD']


bot = Client("signal", api_id="9871990", api_hash="3b5e9dbccbcb96c9e0e8c491051ab51f")


def sltp(chat_id, text, Sl, Tp):
    try:
        if chat_id == -1001416233252:  # test
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001445377985:  # @americanforexspecialist
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001349935562:  # @bestForexSignalsPips
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001246538371:  # @bestforextradinggroup
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001291056071:  # @fXReaperFreeForexSignals
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001383532475:  # @forexMoneyNLFree
            try:
                PRICE = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if 'enter' in i][0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[0])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001411820913:  # @forexPipsFactory2
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001480924116:  # @forex_Signals_PIPs_Signal_Fx
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[2]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001270204996:  # @forex_xlab1
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001126668980:  # @forexgreenpips958
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001414424977:  # @Forexkiller1123
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001311844342:  # @forexsignalfactory
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001491035512:  # @forexsignalsolutions
            try:
                PRICE = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if '@' in i][0]))[-1])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001316056319:  # @forexsignalsstreet
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[4]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001470291934:  # @forexsignalvalue
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001420572107:  # @forexsignalzz
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[2]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if 'stop loss' in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if 'take profit' in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001062012353:  # @FxGlobal5
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001341052202:  # @fxSignals_Gold
            try:
                PRICE = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if 'entry' in i]))[-1])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001298489655:  # @fxpipsaction1
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001399543862:  # @fx_globaltrades
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[1]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001157841207:  # @greenpipsforex
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001203106845:  # https://t.me/joinchat/AAAAAEe19B0ZIeRRXNOpAg Exclusive
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001355784993:  # https://t.me/joinchat/AAAAAFDPoyF6DXvyQDYpDw 💲Horizon
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001302273796:  # @m5MacDScalpers
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001449789431:  # @mADIFOREX_SIGNAL_MASTAR
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001299535263:  # @metatrader4Signals0
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001494412791:  # @metatrader5signal1
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001171155421:  # @octaFxsignalx
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001148641286:  # @pipstowin
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001392466168:  # @proFxSecretStrategy
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[2]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001473518645:  # @professoroff
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[2]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001391473841:  # @ronaldpatrick
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                if ('loss' in text):
                    SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if 'stop loss' in i]))[-1])
                    TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if 'take profit' in i][-1]))[-1])
                else:
                    SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                    TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001141061818:  # @signal4000
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001409206299:  # @signalfxoption
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001471162189:  # @signalsscalping12
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001127289760:  # @sureshotforex
            try:
                if not ('order' in text):
                    PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                    SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                    TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                    print(PRICE, SL, TP)
            except:
                return False
        elif chat_id == -1001331117752:  # @taarget_plus
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[1]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001296877896:  # @trendFriend12
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001188607041:  # @vipCoinexhangePump
            try:
                PRICE = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if '  #' in i]))[-1])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
        elif chat_id == -1001398995940:  # @voltforex
            try:
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if 'stop loss' in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if 'take profit' in i][-1]))[-1])
                return [PRICE, SL, TP]
            except:
                return False
    except Exception as ex:
        bot.send_message(-1001247941772, f"sltp.{str(chat_id)}: {ex}")


def OrderSend(Symbol, Lot, Type, PRICE, Sl, Tp, Magic):
    selected = mt5.symbol_select(Symbol, True)
    if not selected:
        bot.send_message(-1001247941772, f"OrderSend.symbol_select: {str(mt5.last_error())}")
        mt5.shutdown()
    symbol_info = mt5.symbol_info(Symbol)
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Symbol,
        "volume": Lot,
        "type": Type,
        "price": PRICE,
        "sl": Sl,
        "tp": Tp,
        "deviation": 3,
        "magic": Magic,
        "comment": "Order ochish",
        "type_time": mt5.ORDER_TIME_GTC,
        #"type_filling": mt5.ORDER_FILLING_    return,
    }
    result = mt5.order_send(request)
    # bot.send_message(-1001247941772, f"OrderSend.last_error: {str(mt5.last_error())}")
    mt5.shutdown()
    #quit()


@bot.on_message(filters.channel)
# @bot.on_message((filters.photo | filters.text) & (filters.channel | filters.chat))
def my_handler(client, message):
    Type = 2
    NOW_PRICE = 0
    Lot = 0.01
    chat_id = message.chat.id
    text = str(message.text).lower()
    if message.photo:
        if message.caption:
            text = message.caption
    if chat_id < 0:
        if 0 < len(text):
            if not ('limit' in text) and not ('sell stop' in text) and not ('buy stop' in text):
                if ('sl' in text and 'tp' in text) or ('stop loss' in text and 'take profit' in text):
                    for Symbol in symbols:
                        if Symbol.lower() in text:
                            print(Symbol)
                            if 'buy' in text:
                                Type = 0
                            if 'sell' in text:
                                Type = 1
                            st = sltp(chat_id, text, 'sl', 'tp')
                            print(st)
                            if st is not False and Type != 2:
                                for i in range(20):
                                    if mt5.initialize(login=68025724, server="RoboForex-DemoPro",
                                                      password="Metatrader5"):
                                        if abs(st[0] - NOW_PRICE) < 200 * mt5.symbol_info(Symbol).point:
                                            if Type == 0:
                                                NOW_PRICE = mt5.symbol_info_tick(Symbol).ask
                                            if Type == 1:
                                                NOW_PRICE = mt5.symbol_info_tick(Symbol).bid
                                            if mt5.symbol_info(Symbol) is not None:

                                                OrderSend(Symbol.upper(), Lot, Type, NOW_PRICE, st[1], st[2],
                                                          int(str(chat_id)[-10:]))
                                                break
                                            else:
                                                bot.send_message(-1001247941772,
                                                                 f"{str(mt5.last_error())}")
                                                OrderSend(Symbol.upper(), Lot, Type, NOW_PRICE, st[1], st[2],
                                                          int(str(chat_id)[-10:]))
                                                mt5.shutdown()
                                        else:
                                            mt5.shutdown()
                                            break
                                    sleep(5)

if __name__ == "__main__":
    bot.run()