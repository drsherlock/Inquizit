import sys

from aiohttp import web

from app import main

if __name__ == '__main__':
	main(sys.argv[1:])
