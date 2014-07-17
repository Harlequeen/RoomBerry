"""
I guess this is on the Apache license.  Anyway it's open.  So if you have an adafruit display on a Pi,
you too can display who's in a meeting room.  (eventually)
test
"""
# A room usage display on a raspberry pi from a suggestion by Alex Watt
# Started July 2014 (too late)
# Starting with pygame library
# Probably better to go to Open GL in the end
# Can't go wrong by starting with import sys,os
# Import print function to start on Python 3 compatibility

from __future__ import print_function
import sys
import os
import logging
# Pygame for now
import pygame as pg
import pygame.font as pgfont
# Import pyexchange to connect to Exchange
import pyexchange
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
os.environ['SDL_VIDEODRIVER']="fbcon"
CAPTION = "RoomBerry Pi"
SCREEN_SIZE = (320, 240)
colour_white = (255,255,255)
colour_red = (255,0,0)
exchange_connection_info_file='exchangeconnect.txt'
exchange_folder_id='mrg:\Calendar'

class MeetingWindow(object):
  """ Currently only initiated with text.
  """
  def __init__(self,meetingText):
    self.meetingText=meetingText
    self._size = (300,80)
    self._position = (10,10)
    self.border = False
    self.border_width = 1
    self.border_colour = colour_white
    self.background_colour = colour_red
    self.text_colour = colour_white
    self.text_typeface = "no idea"
    self.backround_colour = colour_red
    self._hidden = True
    self._index=0
  def __del__():
    print('testing delete')
  def show():
    if self.hidden:
      self.hidden=False
      self.draw()
  def hide():
    if not(self.hidden):
      parent.reDraw()
  def resize(newSize):
    if not(self.hidden):
      self.hide()
    self.size=newSize
    if not(self.hidden):
      self.draw()
  def move(newPosition):
    if not(self.hidden):
      self.hide()
    self.position=newPosition
    if not(self.hidden):
      self.draw()
  def index():
    return self.index

def get_exchange_connection_info(filename):
  """ Reads the adadress, username, and password from a cleartext file
  Secure eh?
  """
  try:
    exchange_input_file=open(filename,'r')
    exchange_options=exchange_input_file.readlines()
    if len(exchange_options) < 3:
      try:
        raise IOError('Not Enough Lines in File')
      except:
        debug.error('Not enough lines in exchange options file')
    else:
      exchange_input_file.close()
      return exchange_options
  except IOError:
    debug.error('IO Error on Exchange Connection Info File')

class RoomBerry(object):
  """Sentec Meeting Room Display for Raspberry Pi
    Needs a service object and a diary folder.
  """
  def wordWrap(surf, text, font, color=(0, 0, 0)):
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
    line_spacing = font.get_sized_height() + 2
    x, y = 0, line_spacing
    space = font.get_rect(' ' * 2)  # second space given width 0
    for word in words:
      bounds = font.get_rect(word)
      if x + bounds.width + bounds.x >= width:
        x, y = 0, y + line_spacing
      if x + bounds.width + bounds.x >= width:
        raise ValueError("word too wide for the surface")
      if y + bounds.height - bounds.y >= height:
        raise ValueError("text to long for the surface")
      font.render_to(surf, (x, y), None, color)
      x += bounds.width + space.width
    return x, y

  def __init__(self,service,folder):
    logging.debug('RoomBerry __init__')
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    self.__screen = pg.display.get_surface()
    self.__screenRect = self.__screen.get_rect()
    logging.debug('Roomberry __init__ freetype init')
    pgfont.init()
    logging.debug('Roomberry __init__ freetype sysfont')
    logging.debug('Font size')
    # Wish me luck
    self.__roomFolder=service.calendar(folder)
    #logging.debug(str(font.size()))

  def main_loop(self):
    """ The main program when running
    """
    logging.debug('Roomberry mainLoop')
    self.__screen.fill(colour_red)
    self.__font=pgfont.SysFont("",14)
    self.__text=self.__font.render('This is some test text',True,(255,255,255))
    self.__screen.blit(self.__text,(10,10))
    # Attempt to get calendar entry
    #self.__appointment=self.__roomFolder.get_event(#NEEED EVENT ID#)
    self__appointments=self.__roomFolder.search_appointments("AgAA",date("17 July 2014"))
    pg.display.flip()
    pg.event.pump()
    pg.display.flip()
    pg.event.wait()
    pg.quit()

if __name__ == "__main__":
  exit_main=0
  logging.basicConfig(filename='Roomberry.log',level=logging.DEBUG)
  logging.info('Roomberry Pi Starting')
  logging.debug(pg.version.ver)
  exchange_connection_info = get_exchange_connection_info(exchange_connection_info_file)
  #I should check stuff first!!!
  #Start exchange connection
  exchange_connection = ExchangeNTLMAuthConnection(exchange_connection_info[0],exchange_connection_info[1],exchange_connection_info[2])
  #Start exchange service
  exchange_service = Exchange2010Service(exchange_connection)
  glass_meeting_room=RoomBerry(exchange_service,exchange_folder_id)
  glass_meeting_room.main_loop()
  logging.info('Roomberry Pi Exiting')


