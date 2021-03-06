from .lang import LanguageService
import logging
from markdown_strings import esc_format

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[telegram_service]")

class TelegramService:
   __instance = None
   @staticmethod 
   def getInstance():
      """ Static access method. """
      if TelegramService.__instance == None:
         TelegramService()
      return TelegramService.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if TelegramService.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         TelegramService.__instance = self
         self.bot = None
         self.lang = LanguageService.getInstance()
         
   def setBot(self, bot):
      self.bot = bot
      return self
   
   def send_message(self, chatId, text, userId=None, params=None, reply_markup=None, parse_mode="Markdown"):
      if userId == None:
         userId = chatId
      escaped = []
      if params:
         for i in params:
            if type(i) == str:
               escaped.append(esc_format(i))
            else:
               escaped.append(i)
         params = tuple(escaped)

      if params and reply_markup:
         self.bot.send_message(chatId, self.lang.get_value(userId, text)%params, reply_markup=reply_markup, parse_mode=parse_mode)
      elif params:
         self.bot.send_message(chatId, self.lang.get_value(userId, text)%params, parse_mode=parse_mode)
      elif reply_markup:
         self.bot.send_message(chatId, self.lang.get_value(userId, text), reply_markup=reply_markup, parse_mode=parse_mode)
      else:
         self.bot.send_message(chatId, self.lang.get_value(userId, text), parse_mode=parse_mode)
      
   def reply_to(self, message, text):
      self.bot.reply_to(message, esc_format(self.lang.get_value(message.from_user.id, text)))
         
   def edit_message_text(self, chat_id, message_id, text, userId=None, params=None, reply_markup=None, parse_mode="Markdown"):
      try:
         if userId == None:
            userId = chat_id
         escaped = []
         if params:
            print(params)
            for i in params:
               if type(i) == str:
                  escaped.append(esc_format(i))
               else:
                  escaped.append(i)
         params = tuple(escaped)
         if params and reply_markup:
            self.bot.edit_message_text(chat_id=chat_id, 
                                       message_id=message_id, 
                                       text=self.lang.get_value(userId, text)%params, 
                                       reply_markup=reply_markup, 
                                       parse_mode=parse_mode)
         elif params:
            self.bot.edit_message_text(chat_id=chat_id, 
                                       message_id=message_id, 
                                       text=self.lang.get_value(userId, text)%params, 
                                       parse_mode=parse_mode)
         elif reply_markup:
            self.bot.edit_message_text(chat_id=chat_id, 
                                       message_id=message_id, 
                                       text=self.lang.get_value(userId, text), 
                                       reply_markup=reply_markup, parse_mode=parse_mode)
         else:
            self.bot.edit_message_text(chat_id=chat_id, 
                                       message_id=message_id, 
                                       text=self.lang.get_value(userId, text), 
                                       parse_mode=parse_mode)
      except:
         logging.error("ERROR EDITING MESSAGE: ", exc_info=True)
      
   
   def pin_chat_message(self, chatid, messageid):
      self.bot.pin_chat_message(chatid, messageid)
   
   def get_chat(self, squadid):
      return self.bot.get_chat(squadid)
   
   def export_chat_invite_link(self, squadid):
      self.bot.export_chat_invite_link(squadid)