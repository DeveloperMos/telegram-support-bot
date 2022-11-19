from telegram.ext import CommandHandler, MessageHandler, Filters

from settings import WELCOME_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID, REPLY_TO_THIS_MESSAGE, WRONG_REPLY


def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)

    user_info = update.message.from_user.to_dict()

    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
📞 Connected {user_info}.
        """,
    )


def forward_to_chat(update, context):
    forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    if forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.message.from_user.id}'
        )


def forward_to_user(update, context):
    user_id = None
    try:
        if update.message.reply_to_message.forward_from:
            user_id = update.message.reply_to_message.forward_from.id
        # elif REPLY_TO_THIS_MESSAGE in update.message.reply_to_message.text:
        #     try:
        #         user_id = int(update.message.reply_to_message.text.split('\n')[0])
        #     except ValueError:
        #         user_id = None
        if user_id:
            context.bot.copy_message(
                message_id=update.message.message_id,
                chat_id=user_id,
                from_chat_id=update.message.chat_id
            )
        else:
            if update.message.reply_to_message.from_user.is_bot:
                context.bot.send_message(
                    chat_id=TELEGRAM_SUPPORT_CHAT_ID,
                    text=WRONG_REPLY
                )
    except Exception as e:
        pass


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    return dp