#!/usr/bin/env python
# coding: utf-8

# In[1]:


from random import randint, shuffle
import copy


# In[2]:


class Game:
    def __init__(self):
        # 牌 
        self.cards = [(suit,rank) for suit in ['♣', '♦', '❤️', '♠'] for rank in range(1, 14)]
        # 紀錄洗過的牌，用來 restart 
        self.shuffled_cards  = [] 
        # 用來紀錄每個牌堆的陣列
        self.rows = [[] for i in range(12)]
        # 用來記錄抽牌區最上面那張牌的位置
        self.order = 0
        #紀錄 5 ~ 11 列已翻開牌的位置
        self.open = [0, 0, 0, 0, 0, 0, 0]
        
    def demo(self):
        self.cards = [(suit,rank) for suit in ['♣', '♦', '❤️', '♠'] for rank in range(1, 14)]
        self.rows[0] = self.cards[0:13]
        self.rows[1] = self.cards[13:26]
        self.rows[2] = self.cards[26:39]
        self.rows[3] = self.cards[39:-1]
        self.rows[4] = []
        self.rows[5] = [self.cards[-1]]
        self.rows[6] = []
        self.rows[7] = []
        self.rows[8] = []
        self.rows[9] = []
        self.rows[10] = []
        self.rows[11] = []
        return self.face_to_string()
        
    def face_to_string(self):
        # 負責把每列牌轉成字串，最後回傳 layout
        
        # 處理 0 ~ 3 列的輸出
        layout = ''
        for index, suit in enumerate(['♣', '♦', '❤️', '♠']):
            layout += (suit+'('+str(index)+'):')
            for card in self.rows[index]:
                if card == (0,0): continue
                layout += (card[0]+str(card[1]) + ' ')
            layout += '\n'
        
        # 處理 4 列的輸出
        layout += '🂠(4):' 
        for card in self.rows[4]:
            if card == None: continue
            layout += (card[0]+str(card[1])+' ')

        # 處理 5 ~ 11 列的輸出    
        for row in range(5, 12):
            layout += ('\nrow'+str(row-5)+'('+str(row)+'):')
            for index, card in enumerate(self.rows[row]):
                if index <= self.open[row-5]:
                    layout += (card[0]+str(card[1]) + ' ')
                else:
                    layout += '* '

        return layout    
        
    def start(self, restart=False):
        # 開始新一局遊戲
        if restart == False:
            # 打亂牌堆
            shuffle(self.cards)
            self.shuffled_cards = copy.deepcopy(self.cards)
        else:
            # 恢復初始狀態
            self.cards = self.shuffled_cards
        
        # 分牌
        # row 0 ~ 3 放 (0,0) 是為了 move 函式判斷移動情況好寫
        self.rows[0], self.rows[1], self.rows[2], self.rows[3], self.rows[4] = [(0,0)], [(0,0)], [(0,0)], [(0,0)], []
        self.rows[5] = [self.cards[0]]
        self.rows[6] = sorted(self.cards[1:3], key = lambda r: r[1])
        self.rows[7] = sorted(self.cards[3:6], key = lambda r: r[1])
        self.rows[8] = sorted(self.cards[7:11], key = lambda r: r[1])
        self.rows[9] = sorted(self.cards[11:16], key = lambda r: r[1])
        self.rows[10] = sorted(self.cards[16:22], key = lambda r: r[1])
        self.rows[11] = sorted(self.cards[22:29], key = lambda r: r[1])
        self.order = 28

        return self.face_to_string()
    
    def move(self, from_rows, pos, to_rows):
        # 先把基本的不合法的規則先禁止，再去判斷移動到目的地排列的是否合法
        if from_rows not in range(0, 12) or to_rows not in range(0, 12):
            # 列不為合法輸入
            print('沒有此列')
            return False
        if len(self.rows[from_rows]) < pos+1:
            # 要移動的列已經沒牌的 case
            print('此列牌不夠或是為空！')
            return False
        
        if pos > self.open[from_rows-5]:
            # 移動規則一: 不能移動到覆蓋牌的 case
            print('不能移動到覆蓋的牌！')
            return False
        if from_rows in range(0, 4):
            # 不能移動答案區的牌
            print('不允許移走答案區的牌')
            return False
        
        # 移動規則四: 區分答案區與暫存區的牌堆移動後是否連續
        if to_rows in range(0,4): 
            if self.rows[from_rows][0][1] != self.rows[to_rows][-1][1] + 1:
                print('移動後無法使該列連續1！')
                return False
        else:
            if self.rows[from_rows][pos][1] + 1 != self.rows[to_rows][0][1]:
                # 暫存區的判斷
                print('移動後無法使該列連續2！')
                return False
        
        print(self.open)
        # 目的地是答案區的 case
        if to_rows in range(0,4):
            print('將牌移動至答案區')
            
            suit = self.rows[from_rows][0][0]
            if ['♣', '♦', '❤️', '♠'][to_rows] != suit:
                print('答案區只能是同花色')
                return False
            for card in self.rows[from_rows][1:pos+1]:
                if card[0] != suit:
                    # 移動到答案區的牌不同色的 case
                    print('答案區只能是同花色的牌')
                    return False
            
            self.rows[to_rows] += self.rows[from_rows][0:pos+1]
            self.rows[from_rows] = self.rows[from_rows][pos+1::]
            self.open[from_rows-5] -= (pos+1)
            self.open[from_rows-5] = max(self.open[from_rows-5], 0)
            return True
        
        # 目的地是暫存區的 case
        elif to_rows in range(5,12):
            print('將牌移動至暫放區')
            
            self.rows[to_rows] = self.rows[from_rows][0:pos+1] + self.rows[to_rows]
            self.rows[from_rows] = self.rows[from_rows][pos+1::]
            self.open[to_rows-5] += (pos+1)
            if from_rows >= 5:
                self.open[from_rows-5] -= (pos+1)
                self.open[from_rows-5] = max(self.open[from_rows-5], 0)
            return True
        
        print('移動不合法！')
        print(self.face_to_string())
        return False
        
    def draw(self,):
        #全部抽完，從剩餘牌堆中的最上面抽
        if self.order == 51:
            first = 0
            for i in range(0,12):
                if i == 4: continue
                first += len(self.rows[i])
            if first == 52:
                print('沒牌了')
                self.rows[4] = [] 
                return self.face_to_string()
            self.order = first-1
        self.order+= 1
        self.rows[4] = [self.cards[self.order]]
        return self.face_to_string()

    def check(self):
        if len(self.rows[0]) == len(self.rows[1]) == len(self.rows[2]) == len(self.rows[3]) == 13:
            print('遊戲結束')
            return True
        else:
            print('遊戲尚未結束')
            return False


# In[3]:


from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Filters, Updater, CommandHandler, MessageHandler, CallbackQueryHandler

updater = Updater(token='5053070945:AAG6BgUSQ4nN5Db6DtCH-L4WNz1jXLCpeas', use_context=True)
dispatcher = updater.dispatcher

game = Game()

def func(update, context):
    if update.callback_query.data == 'draw':
        context.bot.send_message(chat_id=update.effective_chat.id, text=game.draw(), reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(
            '翻牌', callback_data='draw'),
        InlineKeyboardButton(
            '重玩', callback_data='restart')]]))
    elif update.callback_query.data == 'restart':
        context.bot.send_message(chat_id=update.effective_chat.id, text=game.start(True), reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                '翻牌', callback_data='draw'),
            InlineKeyboardButton(
                '重玩', callback_data='restart')]]))
    

def init(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=game.start(), reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                '翻牌', callback_data='draw'),
            InlineKeyboardButton(
                '重玩', callback_data='restart')
        ]])
    )
    
def move(update, context):
    pos1, pos2, pos3 = map(int, update.message.text.split(' ')[1::])
    if game.move(pos1, pos2, pos3) == False:
        context.bot.send_message(chat_id=update.effective_chat.id, text='此移動不合法！請再次嘗試！')
    context.bot.send_message(chat_id=update.effective_chat.id, text=game.face_to_string(), reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                '翻牌', callback_data='draw'),
            InlineKeyboardButton(
                '重玩', callback_data='restart')]]))
    if game.check():
        context.bot.send_message(chat_id=update.effective_chat.id, text='遊戲成功！')
    
start_handler = CommandHandler('start', init)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CallbackQueryHandler(func))

move_handler = CommandHandler('move', move)
dispatcher.add_handler(move_handler)

updater.start_polling()


# In[ ]:




