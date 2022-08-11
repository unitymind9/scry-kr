import asyncio, aiohttp
import scrython

# Windows 오류 해결
import platform
if platform.system() == 'Windows':
  from functools import wraps
  from asyncio.proactor_events import _ProactorBasePipeTransport

  def silence_event_loop_closed(func):
      @wraps(func)
      def wrapper(self, *args, **kwargs):
          try:
              return func(self, *args, **kwargs)
          except RuntimeError as e:
              if str(e) != 'Event loop is closed':
                  raise
      return wrapper

  _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

decklist = """
Deck
3 Chandra, Torch of Defiance
1 Sorin the Mirthless
4 Bloodtithe Harvester
2 Kroxa, Titan of Death's Hunger
4 Bonecrusher Giant
4 Graveyard Trespasser
2 Kalitas, Traitor of Ghet
4 Fatal Push
2 Heartless Act
4 Thoughtseize
2 Bloodchief's Thirst
4 Fable of the Mirror-Breaker
2 Mountain
1 Swamp
2 Castle Locthwain
4 Blightstep Pathway
2 Den of the Bugbear
2 Hive of the Eye Tyrant
4 Haunted Ridge
4 Blood Crypt
1 Sokenzan, Crucible of Defiance
2 Takenuma, Abandoned Mire

Sideboard
2 Chandra, Awakened Inferno
1 Kalitas, Traitor of Ghet
2 Duress
2 Anger of the Gods
3 Go Blank
1 Extinction Event
2 Unlicensed Hearse
2 Leyline of the Void
"""

async def deckE2K(i):
  if i not in ignorelist:
    if '(' in i:
      i = i[:i.find(' (')]
    cardqty, cardname = i.split(maxsplit=1)
    query = '!"' + cardname + '"' + ' lang:ko'
    try:
      card = scrython.cards.Search(q=query)
    except:
      card = scrython.cards.Search(q='!"' + cardname + '"')

    try:
      cardprintedname = card.data()[0]['card_faces'][0]['printed_name']
    except:
      try:
        cardprintedname = card.data()[0]['printed_name']
      except:
        cardprintedname = card.data()[0]['card_faces'][0]['name']
    await asyncio.sleep(0.1)
    return cardqty + cardprintedname
  else:
    await asyncio.sleep(0.1)
    return ignoredict[i]

ignorelist = ['Deck', 'Sideboard', 'Commander', 'Companion', '']
ignoredict = {'Deck' : '덱', 'Sideboard' : '사이드보드', 'Commander' : '커맨더', 'Companion' : '단짝', '' : ''}
kr_ignorelist = ['덱', '사이드보드', '커맨더', '단짝', '']
kr_ignoredict = {'덱' : 'Deck', '사이드보드' : 'Sideboard', '커맨더' : 'Commander', '단짝' : 'Companion', '' : ''}



async def main():
  global decklist
  decklist = decklist.split('\n')
  kr_decklist = await asyncio.gather(*[deckE2K(i) for i in decklist])
  print(kr_decklist)

if __name__ == "__main__":
  asyncio.run(main())

# if decklist[0] in ignorelist:
#   for i in decklist:
#     if i not in ignorelist:
#       if '(' in i:
#         i = i[:i.find(' (')]
#       cardqty, cardname = i.split(maxsplit=1)
#       query = '!"' + cardname + '"' + ' lang:ko'
#       try:
#         card = scrython.cards.Search(q=query)
#       except:
#         card = scrython.cards.Search(q='!"' + cardname + '"')

#       try:
#         cardprintedname = card.data()[0]['card_faces'][0]['printed_name']
#       except:
#         try:
#           cardprintedname = card.data()[0]['printed_name']
#         except:
#           cardprintedname = card.data()[0]['card_faces'][0]['name']
#       print(cardqty, cardprintedname)
#     else:
#       print(ignoredict[i])
# else:
#   for i in decklist:
#     print(i)