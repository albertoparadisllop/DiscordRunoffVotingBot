import sys, os


def main(token):
    from bot import botClient
    botClient.run_bot(token)


if __name__ == '__main__':
    bot_token = ""
    if len(sys.argv)==2 and "TOKEN" in os.environ:
        # Try to get it from env
        print("Token from command line")
        bot_token = sys.argv[1]
    else:
        print("Token from env var")
        bot_token = os.getenv("TOKEN")
    main(bot_token)
