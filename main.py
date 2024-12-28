import sys, os


def main(token):
    from bot import botClient
    botClient.run_bot(token)


if __name__ == '__main__':
    bot_token = ""
    if len(sys.argv)==2:
        # Try to get it from env
        print("Token from command line")
        bot_token = sys.argv[1]
    elif "TOKEN" in os.environ:
        print("Token from env var")
        bot_token = os.getenv("TOKEN")
    else:
        print("No bot token provided")
        raise Exception("")
    main(bot_token)
