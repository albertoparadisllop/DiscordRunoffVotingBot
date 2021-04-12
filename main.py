import sys

def main(token):
	import botClient
	botClient.run_bot(token)

if __name__ == '__main__':
	print(sys.argv[1]) 
	main(sys.argv[1])