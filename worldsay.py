import requests
import argparse
import time
import sys
import os
import re


def get_quote(api) -> str:
  req = requests.get(api)
  if req.status_code == 200:
    if req.json()['quotes'][0]['quote']:
      return re.sub('[()\[\]\'\";]', '', req.json()['quotes'][0]['quote'])
  else:
    return ''


def speak_quote(quote, accent) -> None:
  os.system('say -v ' + accent + ' ' + quote)


def get_accents(specify_accent) -> dict:
  accents = {
    "Alice": "Italian",
    "Amelie": "French",
    "Jorge": "Spanish",
    "Daniel": "English",
    "Anna": "German",
  }
  if specify_accent:
    for name, accent in accents.items():
      if specify_accent.lower() == accent.lower():
        return { name: accent }
  else:
    return accents


def parse_args() -> dict:
  parser = argparse.ArgumentParser(prog='worldsay', description='accented quotes')
  parser.add_argument('--accent', type=str, default=None, help='specify accent')
  parser.add_argument('--api', type=str, help='specifi api endpoint',
                      default='https://opinionated-quotes-api.gigalixirapp.com/v1/quotes')
  return parser.parse_args()


def main() -> None:
  arguments = parse_args()
  print(arguments.api, arguments.accent)
  accents = get_accents(arguments.accent)
  while True:
    quote = get_quote(arguments.api)
    if quote:
      print(quote)
      for accent, name in accents.items():
        print(accent, name)
        speak_quote(quote, accent)
        time.sleep(2)


if __name__ == '__main__':
  main()
