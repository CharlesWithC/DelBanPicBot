import telepot,telepot.loop,pprint
import sqlite3
import pytesseract
from PIL import Image
from urllib.request import urlopen
import os,io,time

HELLO="""Hello!

This is a banned picture remover bot made by @won14.
It can remove pictures with banned phrases.
<b>Note: The bot is powered by tesseract OCR technology, and the accuracy is not guaranteed to be 100%. It may cannot detect all pictures with banned phrases!</b>

You can add the bot to your groups and set banned phrases for each group here.
The bot must be an admin in order to remove messages!

Commands usage:
<code>/bindgroup,/bg {group name}</code>
--<i>Bind your group with the bot so the bot will detect messages in it</i>
--Note: <b>You must add the bot to the group first and make it an admin. You also need to must be an admin of the group and the group must be a public group.</b>
--Example: <code>/bindgroup @BotDevelopment</code> (or <code>/bg @BotDevelopment</code>)
--This will bind @BotDevelopment with the bot and the bot will detect pictures in the group.

<code>/unbindgroup,/ubg {group name}</code>
--<i>Unbind a group and delete all banned phrases</i>
--Note: <b>You must be the binder of the group to execute this command.</b>
--Example: <code>/unbindgroup @BotDevelopment</code> (or <code>/ubg @BotDevelopment</code>)
--This will unbind @BotDevelopment from the bot.

<code>/banphrase,/bp {group name} {banned phrase}</code>
--<i>Remove {banned phrase} appeared in pictures in {group name}</i>
--Note: <b>The banned phrase is NOT case-sensitive. The maximum length of the phrase is 128 characters. (Longer phrase will decrease the accuracy of detection)</b>
--Note: <b>You must be either the binder or an admin of the group to execute this command!</b>
--Example: <code>/banphrase @BotDevelopment bitcoin</code> (or <code>/bp @BotDevelopment bitcoin</code>)
--This will remove <i>bitcoin, Bitcoin, BitCoin</i> etc appeared in pictures in @BotDevelopment

<code>/seebp {group name}</code>
--<i>See all banned phrases of {group name}</i>
--Note: <b>The bot must be binded to the group!</b>
--Note: <b>You must be either the binder or an admin of the group to execute this command!</b>
--Example: <code>/seebp @BotDevelopment</code>
--The bot will show all banned phrases of @BotDevelopment

<code>/delbp {group name} {banned phrase}</code>
--<i>Delete a banned phrase of {group name}</i>
--Note: <b>The bot must be binded to the group and the phrase must be banned!</b>
--Note: <b>You must be either the binder or an admin of the group to execute this command!</b>
--Example: <code>/delbp @BotDevelopment bitcoin</code>
--This command will make phrase 'bitcoin' will be no longer banned for @BotDevelopment

<code>/delallbp {group name}</code>
--<i>Delete all banned phrases of {group name}</i>
--Note: <b>The bot must be binded to the group!</b>
--Note: <b>You must be either the binder or an admin of the group to execute this command!</b>
--Example: <code>/delallbp @BotDevelopment</code>
--This command will delete all banned phrases of @BotDevelopment

Buy me a cup of coffee (Donate) (Only accept cryptocurrency):
Bitcoin: 139rwwraeZjyCRh9kgtsii45FWFt1wg5EW
For other coins, please PM me @won14"""

BIND_GROUP_COMMAND_USAGE="""Invalid command!

Command usage:
<code>/bindgroup,/bg {group name}</code>
--<i>Bind your group with the bot so the bot will detect messages in it</i>
--Note: <b>You must add the bot to the group first and make it an admin. You also need to must be an admin of the group and the group must be a public group.</b>
--Example: <code>/bindgroup @BotDevelopment</code> (or <code>/bg @BotDevelopment</code>)
--This will bind @BotDevelopment with the bot and the bot will detect pictures in the group."""

UNBIND_GROUP_COMMAND_USAGE="""Invalid command!

Command usage:
<code>/unbindgroup,/ubg {group name}</code>
--<i>Unbind a group and delete all banned phrases</i>
--Note: <b>You must be the binder of the group to execute this command.</b>
--Example: <code>/unbindgroup @BotDevelopment</code> (or <code>/ubg @BotDevelopment</code>)
--This will unbind @BotDevelopment from the bot."""

BAN_PHRASE_COMMAND_USAGE="""Invalid command!

Command usage:
<code>/banphrase,/bp {group name} {banned phrase}</code>
--<i>Remove {banned phrase} appeared in pictures in {group name}</i>
--Note: <b>The banned phrase is NOT case-sensitive. The maximum length of the phrase is 128 characters. (Longer phrase will decrease the accuracy of detection)</b>
--Note: <b>You must be either the binder or an admin of the group to execute this command!</b>
--Example: <code>/banphrase @BotDevelopment bitcoin</code> (or <code>/bp @BotDevelopment bitcoin</code>)
--This will remove <i>bitcoin, Bitcoin, BitCoin</i> etc appeared in pictures in @BotDevelopment"""

SEE_BP_COMMAND_USAGE="""Invalid command!

Command usage:
<code>/seebp {group name}</code>
--<i>See all banned phrases of {group name}</i>
--Note: <b>The bot must be binded to the group!</b>
--Note: <b>You must be either the binder or an admin of the group to execute this command!</b>
--Example: <code>/seebp @BotDevelopment</code>
--The bot will show all banned phrases of @BotDevelopment"""

DEL_BP_COMMAND_USAGE="""Invalid command!

Command usage:
<code>/delbp {group name} {banned phrase}</code>
--<i>Delete a banned phrase of {group name}</i>
--Note: <b>The bot must be binded to the group and the phrase must be banned!</b>
--Note: <b>You must be either the binder or an admin of the group to execute this command!</b>
--Example: <code>/delbp @BotDevelopment bitcoin</code>
--This command will make phrase 'bitcoin' will be no longer banned for @BotDevelopment"""

DEL_ALL_BP_COMMAND_USAGE="""Invalid command!

Command usage:
<code>/delallbp {group name}</code>
--<i>Delete all banned phrases of {group name}</i>
--Note: <b>The bot must be binded to the group!</b>
--Note: <b>You must be either the binder or an admin of the group to execute this command!</b>
--Example: <code>/delallbp @BotDevelopment</code>
--This command will delete all banned phrases of @BotDevelopment"""


db_not_exist=not os.path.exists("database.db")
conn=sqlite3.connect("database.db",check_same_thread=False)
if db_not_exist:
    cur=conn.cursor()
    cur.execute(f"CREATE TABLE groupInfo (binder INT, groupname VARCHAR(64), active INT)")
    conn.commit()
    cur.execute(f"CREATE TABLE bannedPhrase (adder INT, groupname VARCHAR(64), phrase VARCHAR(128))")
    conn.commit()

BOT_TOKEN="{TOKEN}"
BOT_ID=1351756140
bot=telepot.Bot(BOT_TOKEN)
pytesseract.pytesseract.tesseract_cmd='tesseract'

class KMP:
    def partial(self, pattern):
        ret = [0]
        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret
        
    def search(self, T, P):
        partial, ret, j = self.partial(P), [], 0
        
        for i in range(len(T)):
            while j > 0 and T[i] != P[j]:
                j = partial[j - 1]
            if T[i] == P[j]: j += 1
            if j == len(P): 
                ret.append(i - (j - 1))
                j = partial[j - 1]
            
        return ret

kmp=KMP()

def OCR(picid):
    fd=io.BytesIO()
    bot.download_file(picid,fd)
    fd.seek(0)
    image_file=io.BytesIO(fd.read())
    im=Image.open(image_file)
    text=pytesseract.image_to_string(im)
    return text

def handle(msg):
    cur=conn.cursor()
    userid=msg["from"]["id"]
    text=''
    if 'text' in msg.keys():
        text=msg["text"]
    if msg["chat"]["type"]=="private":
        if text.startswith("/start"):
            bot.sendMessage(userid,HELLO,parse_mode="html")

        elif text.lower().startswith("/bindgroup") or text.lower().startswith("/bg"):
            d=text.split(" ")
            if len(d)!=2:
                bot.sendMessage(userid,BIND_GROUP_COMMAND_USAGE,parse_mode="html")
                return
            groupName=d[1]
            if not groupName.startswith("@"):
                groupName="@"+groupName
            if not groupName[1:].isalnum():
                bot.sendMessage(userid,"Invalid group name! Group name can only contain alphabets and numbers.")
                return
                
            cur.execute(f"SELECT * FROM groupInfo WHERE groupname='{groupName.lower()}'")
            d=cur.fetchall()
            inactive=0
            if len(d)>0 and d[0][2]==1:
                bot.sendMessage(userid,f"The group {groupName}' is already binded to the bot and it's active!\nYou cannot rebind it!")
                return
            if len(d)>0 and d[0][2]==0:
                inactive=1

            chat=None
            try:
                chat=bot.getChatMember(groupName,userid)
            except:
                bot.sendMessage(userid,"It looks like we have met some issues fetching group data...\nPlease check if the group name you inputted is correct, and the bot is not kicked from the group!")
                return
            if chat is None:
                bot.sendMessage(userid,"It looks like we have met some issues fetching group data...\nPlease check if the group name you inputted is correct, and the bot is not kicked from the group!")
                return
            if not chat["status"] in ("creator","administrator"):
                bot.sendMessage(userid,f"You are not the admin of the group!\nThe group {groupName} cannot be binded to the bot!")
                return
                
            chat=None
            try:
                chat=bot.getChatMember(groupName,BOT_ID)
            except:
                bot.sendMessage(userid,"It looks like we have met some issues fetching group data...\nPlease check if the group name you inputted is correct, and the bot is not kicked from the group!")
                return
            if chat is None:
                bot.sendMessage(userid,"It looks like we have met some issues fetching group data...\nPlease check if the group name you inputted is correct, and the bot is not kicked from the group!")
                return
            if not chat["status"] in ("creator","administrator"):
                bot.sendMessage(userid,f"The bot is not an admin of the group!\nThe group {groupName} cannot be binded to the bot!")
                return
            
            if inactive:
                cur.execute(f"UPDATE groupInfo SET active=1 WHERE groupName='{groupName.lower()}'")
                conn.commit()
                bot.sendMessage(userid,f"{groupName} is reactivated! All pictures with banned phrases will be automatically removed! (You don't need to set banned phrases again)")
            else:
                cur.execute(f"INSERT INTO groupInfo VALUES ({userid},'{groupName.lower()}',1)")
                conn.commit()
                bot.sendMessage(userid,f"{groupName} is successfully binded to the bot!\nRun /banphrase to start banning phrases in pictures!")
        
        elif text.lower().startswith("/unbindgroup") or text.lower().startswith("/ubg"):
            d=text.split(" ")
            if len(d)!=2:
                bot.sendMessage(userid,UNBIND_GROUP_COMMAND_USAGE,parse_mode="html")
                return
            groupName=d[1]
            if not groupName.startswith("@"):
                groupName="@"+groupName
            if not groupName[1:].isalnum():
                bot.sendMessage(userid,"Invalid group name! Group name can only contain alphabets and numbers.")
                return

            cur.execute(f"SELECT * FROM groupInfo WHERE groupName='{groupName.lower()}'")
            dd=cur.fetchall()
            if len(dd)==0:
                bot.sendMessage(userid,f"{groupName} is not binded to the bot yet!\nUse <code>/bindgroup {groupName}</code> to bind it!",parse_mode="html")
                return
            if dd[0][2]==0:
                bot.sendMessage(userid,f"{groupName} is not active!\n/unbindgroup command is disabled!")
                return
            if dd[0][0]!=userid:
                chat=None
                try:
                    chat=bot.getChatMember(groupName,userid)
                except:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if chat is None:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if not chat["status"] in ("creator","administrator"):
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if chat["status"] in ("creator","administrator"):
                    bot.sendMessage(userid,f"You are not the binder of the group, so you cannot execute this command!\nContact the binder to execute this command! (binder account id: <a href='tg://user?id={dd[0][0]}'>{dd[0][0]}</a>)",parse_mode="html")
                    return
            
            cur.execute(f"DELETE FROM groupInfo WHERE groupName='{groupName.lower()}'")
            conn.commit()
            cur.execute(f"DELETE FROM bannedPhrase WHERE groupName='{groupName.lower()}'")
            conn.commit()
            bot.sendMessage(userid,f"Done! {groupName} is no longer binded with the bot and all banned phrases are removed! Goodbye~")

        elif text.lower().startswith("/banphrase") or text.lower().startswith("/bp"):
            d=text.split(" ")
            if len(d)<3:
                bot.sendMessage(userid,BAN_PHRASE_COMMAND_USAGE,parse_mode="html")
                return
            groupName=d[1]
            if not groupName.startswith("@"):
                groupName="@"+groupName
            if not groupName[1:].isalnum():
                bot.sendMessage(userid,"Invalid group name! Group name can only contain alphabets and numbers.")
                return

            cur.execute(f"SELECT * FROM groupInfo WHERE groupName='{groupName.lower()}'")
            dd=cur.fetchall()
            if len(dd)==0:
                bot.sendMessage(userid,f"{groupName} is not binded to the bot yet!\nUse <code>/bindgroup {groupName}</code> to bind it!",parse_mode="html")
                return
            if dd[0][2]==0:
                bot.sendMessage(userid,f"{groupName} is not active!\n/banphrase command is disabled!")
                return
            if dd[0][0]!=userid:
                chat=None
                try:
                    chat=bot.getChatMember(groupName,userid)
                except:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if chat is None:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if not chat["status"] in ("creator","administrator"):
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return

            if len(d[2])>128:
                bot.sendMessage(userid,f"Phrase too long! The phrase must be less than 128 characters in length!")
                return
            
            cur.execute(f"SELECT * FROM bannedPhrase WHERE phrase='{d[2].lower()}'")
            dd=cur.fetchall()
            if len(dd)>0:
                bot.sendMessage(userid,f"The phrase is already banned for {groupName}!")
                return
            
            cur.execute(f"INSERT INTO bannedPhrase VALUES ('{userid}','{groupName.lower()}','{d[2].lower()}')")
            conn.commit()

            bot.sendMessage(userid,f"<code>{d[2]}</code> added to banned phrases of {groupName}",parse_mode="html")
        
        elif text.lower().startswith("/seebp"):
            d=text.split(" ")
            if len(d)!=2:
                bot.sendMessage(userid,SEE_BP_COMMAND_USAGE,parse_mode="html")
                return
            groupName=d[1]
            if not groupName.startswith("@"):
                groupName="@"+groupName
            if not groupName[1:].isalnum():
                bot.sendMessage(userid,"Invalid group name! Group name can only contain alphabets and numbers.")
                return
                
            cur.execute(f"SELECT * FROM groupInfo WHERE groupName='{groupName.lower()}'")
            dd=cur.fetchall()
            if len(dd)==0:
                bot.sendMessage(userid,f"{groupName} is not binded to the bot yet!\nUse <code>/bindgroup {groupName}</code> to bind it!",parse_mode="html")
                return
            if dd[0][2]==0:
                bot.sendMessage(userid,f"{groupName} is not active!\n/seebp command is disabled!")
                return
            if dd[0][0]!=userid:
                chat=None
                try:
                    chat=bot.getChatMember(groupName,userid)
                except:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if chat is None:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if not chat["status"] in ("creator","administrator"):
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return

            cur.execute(f"SELECT phrase FROM bannedPhrase WHERE groupName='{groupName.lower()}'")
            d=cur.fetchall()
            if len(d)==0:
                bot.sendMessage(userid,f"There is no banned phrases for {groupName} yet!",parse_mode="html")
                return
            msg=f"Here are ll banned phrases for {groupName}:\n"
            for dd in d:
                msg+=f"<code>{dd[0]}</code>\n"
            bot.sendMessage(userid,msg,parse_mode="html")
        
        elif text.lower().startswith("/delbp"):
            d=text.split(" ")
            if len(d)<3:
                bot.sendMessage(userid,DEL_BP_COMMAND_USAGE,parse_mode="html")
                return
            groupName=d[1]
            if not groupName.startswith("@"):
                groupName="@"+groupName
            if not groupName[1:].isalnum():
                bot.sendMessage(userid,"Invalid group name! Group name can only contain alphabets and numbers.")
                return
                
            cur.execute(f"SELECT * FROM groupInfo WHERE groupName='{groupName.lower()}'")
            dd=cur.fetchall()
            if len(dd)==0:
                bot.sendMessage(userid,f"{groupName} is not binded to the bot yet!\nUse <code>/bindgroup {groupName}</code> to bind it!",parse_mode="html")
                return
            if dd[0][2]==0:
                bot.sendMessage(userid,f"{groupName} is not active!\n/delbp command is disabled!")
                return
            if dd[0][0]!=userid:
                chat=None
                try:
                    chat=bot.getChatMember(groupName,userid)
                except:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if chat is None:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if not chat["status"] in ("creator","administrator"):
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
            
            cur.execute(f"SELECT * FROM bannedPhrase WHERE groupName='{groupName.lower()}' AND phrase='{d[2]}'")
            dd=cur.fetchall()
            if len(dd)==0:
                bot.sendMessage(userid,f"The phrase <code>{d[2]}</code> is not banned for {groupName} yet!",parse_mode="html")
                return
            cur.execute(f"DELETE FROM bannedPhrase WHERE groupName='{groupName.lower()}' AND phrase='{d[2]}'")
            conn.commit()
            bot.sendMessage(userid,f"Done! The phrase <code>{d[2]}</code> is no longer banned in {groupName}!",parse_mode="html")
        
        elif text.lower().startswith("/delallbp"):
            d=text.split(" ")
            if len(d)!=2:
                bot.sendMessage(userid,DEL_ALL_BP_COMMAND_USAGE,parse_mode="html")
                return
            groupName=d[1]
            if not groupName.startswith("@"):
                groupName="@"+groupName
            if not groupName[1:].isalnum():
                bot.sendMessage(userid,"Invalid group name! Group name can only contain alphabets and numbers.")
                return
                
            cur.execute(f"SELECT * FROM groupInfo WHERE groupName='{groupName.lower()}'")
            dd=cur.fetchall()
            if len(dd)==0:
                bot.sendMessage(userid,f"{groupName} is not binded to the bot yet!\nUse <code>/bindgroup {groupName}</code> to bind it!",parse_mode="html")
                return
            if dd[0][2]==0:
                bot.sendMessage(userid,f"{groupName} is not active!\n/delallbp command is disabled!")
                return
            if dd[0][0]!=userid:
                chat=None
                try:
                    chat=bot.getChatMember(groupName,userid)
                except:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if chat is None:
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
                if not chat["status"] in ("creator","administrator"):
                    bot.sendMessage(userid,f"You are neither the binder nor an admin of the group, so you cannot execute this command!")
                    return
            
            cur.execute(f"SELECT * FROM bannedPhrase WHERE groupName='{groupName.lower()}'")
            dd=cur.fetchall()
            if len(dd)==0:
                bot.sendMessage(userid,f"There is no banned phrases for {groupName} yet!",parse_mode="html")
                return
            cur.execute(f"DELETE FROM bannedPhrase WHERE groupName='{groupName.lower()}'")
            conn.commit()
            bot.sendMessage(userid,f"Done! There is no phrases banned in {groupName}!",parse_mode="html")

    elif 'photo' in msg.keys():
        groupName=f"@{msg['chat']['username'].lower()}"
        fromusr=msg["from"]["first_name"]
        cur.execute(f"SELECT * FROM groupInfo WHERE groupName='{groupName}'")
        d=cur.fetchall()
        if len(d)==0:
            return
        if d[0][2]==0:
            return
        for photo in msg["photo"]:
            ocr=OCR(photo["file_id"]).lower().replace("\n"," ")
            cur.execute(f"SELECT phrase FROM bannedPhrase WHERE groupname='{groupName}'")
            d=cur.fetchall()
            for dd in d:
                if kmp.search(ocr,dd[0])!=[]:
                    bot.deleteMessage(telepot.message_identifier(msg))
                    bot.sendMessage(msg["chat"]["id"],f"A message containing picture from <b>{fromusr}</b> is removed!\nReason: <i>Picture contain banned phrase: {dd[0]}</i>",parse_mode="html")
                    break

    pprint.pprint(msg)

def checkGroupStatus():
    cur=conn.cursor()
    while 1:
        cur.execute(f"SELECT * FROM groupInfo WHERE active=1")
        groups=cur.fetchall()
        for group in groups:
            chat=None
            inactive=0
            try:
                chat=bot.getChatMember(group[1],BOT_ID)
            except:
                inactive=1
                try:
                    bot.sendMessage(group[0],f"It looks like the bot is no longer admin in (or kicked from) {group[1]} or the group is removed!\nThe group is set inactive and the bot will no longer work for it.\nYou have to run /bindgroup again to reactive.")
                except:
                    pass
            if not chat is None and not chat["status"] in ("creator","administrator"):
                inactive=1
                try:
                    bot.sendMessage(group[0],f"It looks like the bot is no longer admin in (or kicked from) {group[1]} or the group is removed!\nThe group is set inactive and the bot will no longer work for it.\nYou have to run /bindgroup again to reactive.")
                except:
                    pass
            if inactive:
                cur.execute(f"UPDATE groupInfo SET active=0 WHERE groupName='{group[1]}'")
                conn.commit()
                time.sleep(0.3)
            else:
                time.sleep(0.1)
        time.sleep(3600) # check each hour

telepot.loop.MessageLoop(bot,handle).run_as_thread()
checkGroupStatus()