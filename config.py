import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bot_path_name = 'news_repost_bot'
data_base_path = os.path.join(BASE_DIR, bot_path_name, 'local_data_base.sqlite')

api_id = 17309257
api_hash = '92d3f8cf7cf27563e676c61d5929863d'


uniq_message_coef = 0.9
