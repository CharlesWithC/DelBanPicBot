This is a bot that remove pictures containing banned phrases in Telegram groups.
OCR powered by <b>Tesseract</b>

<hr />

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
For other coins, please PM me @won14