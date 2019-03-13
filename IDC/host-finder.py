import time
import re
import pandas as pd

bot = telepot.Bot('[CHAT_ID]:[BOT_TOKEN]')

# message handler
def handle(msg):
# for console check
#        content_type, chat_type, chat_id = telepot.glance(msg)
#        print(content_type, chat_type, chat_id)

        if content_type == 'text':
                # if bot got message with host name pattern
                p = re.compile('[PATTERN_REGEX]')
                if p.match(msg['text']):
                        # for one excel file with multiple sheet
                        fds = []
                        xls = pd.ExcelFile('/PATH/TO/EXCEL_FILE.xlsx')
                        # in this code, the excel file has 2 sheets
                        for i in range(1, 3):
                                tmp = pd.read_excel(xls, str(i))
                                fds.append(tmp)
                        # find the host from each sheet
                        for df in fds:
                                if msg['text'] in df['HOST_NAME_COLUMN'].values:
                                        td = df.loc[df['HOST_NAME_COLUMN'] == msg['text']]
                                        res = msg['text'] + " is here: " + str(format(int(td['LOCATION_COLUMN'].values[0]), '04d')) + "-" + str(td['RACK-UNIT'].values[0])
                                        bot.sendMessage(chat_id, res)


bot.message_loop(handle)

#print ('Listening ...')
# Keep the program running.
while 1:
        time.sleep(10)
