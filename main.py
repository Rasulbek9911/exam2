import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Salom qidirayotgan narsangizni yozing {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def asaxiy(update: Update, context: CallbackContext) -> None:
    URL = f"https://asaxiy.uz/product?key={update.message.text}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    element = soup.find_all("div", class_="col-6 col-xl-3 col-md-4")[:10]
    for i in element:
        image = i.find("div", class_="product__item d-flex flex-column justify-content-between").find("div",
                                                                                                      class_="product__item-img").find(
            "img", class_="img-fluid lazyload")["data-src"]
        title = i.find("div", class_="product__item d-flex flex-column justify-content-between").find("div",
                                                                                                      class_="product__item-info").find(
            "a").text

        content = i.find("div", class_="product__item d-flex flex-column justify-content-between").find("div",
                                                                                                        class_="product__item-info").find(
            "div", class_="product__item-info--prices").find("div", class_="produrct__item-prices--wrapper").find(
            "span", class_="product__item-price").text

        context.bot.send_message(update.message.chat_id, f"{image}{title}{content}")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1996578306:AAFp5cUKvjDoYldUjgQ-3sYG416CLLcnfj0")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, asaxiy))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
