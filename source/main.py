# LICENSED ON GPL v3
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.app import App
from webbrowser import open as open_url
from kivy.core.window import Window
from kivy.clock import mainthread
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.progressbar import ProgressBar
from toast import toast
from threading import Thread
import re
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from sys import exit
from time import sleep, time
from kivy.loader import Loader
from functools import partial
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.carousel import Carousel
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from socket import socket, AF_INET, SOCK_DGRAM
from kivy.uix.image import AsyncImage
from urllib import urlopen, quote, urlencode
from kivy.utils import platform
from kivy.core.window import Window
__version__="1.1"
Builder.load_string("""
<MainLayout>:
   size_hint_y: None
   cols: 2
   spacing: 1
<CvarLabel>:
   background_color: .7, .7, .7, 1
   size_hint_y: None
   height: 50
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size

<MapnameLabel>:
   background_color: .7, .7, .7, 1
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: (self.pos[0], self.pos[1]+1)
         size: (self.size[0], self.size[1]-2)
<VarLabel>:
   background_color: 1, 1, 1, 1
   size_hint_y: None
   height: 50
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<HostnameButton>:
   color: 1, 1, 1, 1
   background_color: .7, .7, .7, 1
   size_hint_y: None
   height: 70
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<ClientsButton>:
   color: 1, 1, 1, 1
   background_color: 1, 1, 1, 1
   size_hint_y: None
   height: 90
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<RedTeam>:
   background_color: 1, 0, 0, 1
   size_hint_y: None
   markup: True
   height: 50
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<BlueTeam>:
   background_color: 0, 0, 1, 1
   size_hint_y: None
   height: 50
   markup: True
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<PurpleTeam>:
   background_color: .5, 0, .5, 1
   size_hint_y: None
   height: 50
   markup: True
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<YellowTeam>:
   background_color: 1, 1, 0, 1
   size_hint_y: None
   height: 50
   markup: True
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<Observer>:
   background_color: 1, 1, 1, 1
   size_hint_y: None
   height: 50
   markup: True
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<Connecting>:
   background_color: .3, .3, .3, 1
   size_hint_y: None
   height: 50
   markup: True
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<NetworkError>:
   background_color: 0, 0, 0, 1
   size_hint_y: None
   size_hint_x: None
   markup: True
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
<Black>:
   background_color: .7, .7, .7, 1
   size_hint_y: None
   markup: True
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size

<PlDesc>
   background_color: 1, 1, 1, 1
   size_hint_y: 1
   size_hint_x: 1
   canvas.before:
      Color:
         rgba: self.background_color
      Rectangle:
         pos: self.pos
         size: self.size
""")
class Check(): 
   def __init__(self):
      self.response=None
      self.size=None

class PlDesc(Label):
   pass

class NetworkError(Label):
   pass

class MainLayout(GridLayout):
   pass

class RedTeam(ButtonBehavior, Label):
   pass

class BlueTeam(ButtonBehavior, Label):
   pass

class YellowTeam(ButtonBehavior, Label):
   pass

class PurpleTeam(ButtonBehavior, Label):
   pass

class Observer(ButtonBehavior, Label):
   pass

class Connecting(ButtonBehavior, Label):
   pass

class MapnameLabel(Label):
   pass

class CvarLabel(Label):
   pass

class VarLabel(Label):
   pass

class HostnameButton(ButtonBehavior, Label):
   pass

class ClientsButton(ButtonBehavior, Label):
   pass

class Black(Label):
   pass

class ServerBrowser(App):
   #-----------------------------------------------
   # build
   #-----------------------------------------------
   def build(self):
      self.popup_layout=GridLayout(cols=1,
                                   rows=2,
                                   size_hint_x=1,
                                   size_hint_y=1)
      self.popup_label=Label(text='New Version: 1.1\nFeatures:\n -new look\n  -hello\n -bug fixes\n\n\nDo you wish to update?',
                             size_hint_y=1,
                             halign='center',
                             size_hint_x=1)
      self.popup_layout.add_widget(self.popup_label)
      gl=GridLayout(cols=2,
                    rows=1,
                    size_hint_x=1,
                    size_hint_y=None,
                    height=70)
      self.yes=Button(text='Yes')
      gl.add_widget(self.yes)
      no=Button(text='No')
      gl.add_widget(no)
      self.popup_layout.add_widget(gl)
      self.popup = Popup(title='A new version is available!',
                         content=self.popup_layout,
                         auto_dismiss=False)
      no.bind(on_press=self.popup.dismiss)
      self.enable_playerlist_overscroll=False
      self.loaded_servers_id = 0
      self.serverinfo = None
      self.loading_serverlist=False
      self.screen_height = Window.size[0]
      Window.bind(size = self.update_height)
      App.use_kivy_settings = False
      self.bind(on_start = self.post_build_init) #Bind the 'back' key on startup
      self.serverlist_cache = {}
      self.sm=ScreenManager(transition=NoTransition())
      #Create the loading_screen
      self.loading_screen=Screen(name='loading_screen')
      anchor_layout=AnchorLayout(anchor_x='center', anchor_y='center')
      box_layout=BoxLayout(orientation='vertical',
                           size_hint_y=None,
                           height=100,
                           size_hint_x=.9)
      self.loading_label=Label(text='Pinging servers, please wait...',
                               size_hint_y=None,
                               height=40)
      box_layout.add_widget(self.loading_label)
      self.progress_bar = ProgressBar(max=100)
      box_layout.add_widget(self.progress_bar)
      self.hostname = Label(text='0.0.0.0:00000')
      box_layout.add_widget(self.hostname)
      anchor_layout.add_widget(box_layout)
      self.loading_screen.add_widget(anchor_layout)
      #create the server info screen
      self.server_info = Screen(name='server_info')
      #create the server list screen
      self.server_list = Screen(name='server_list')
      self.slist_scroll = ScrollView()
      #create the player info screen
      self.player_info=Screen(name='player_info')
      self.player_description=PlDesc(markup=True, 
                                     size=(Window.size[0], Window.size[1]),
                                     text_size=(Window.size[0]*0.8, Window.size[1]*0.8),
                                     text='', 
                                     halign='left', 
                                     strip=True,
                                     valign='middle')
      self.player_info.add_widget(self.player_description)
      #add the screens to the screen manager
      self.sm.add_widget(self.loading_screen)
      self.sm.add_widget(self.server_info)
      self.sm.add_widget(self.server_list)
      self.sm.add_widget(self.player_info)
      return self.sm
   #-----------------------------------------------
   # latest (check for updates)
   #-----------------------------------------------
   def tomaster(self):
      sock = socket(AF_INET, SOCK_DGRAM)
      sock.connect(("91.239.67.195", 5123))
      sock.settimeout(1)
      sock.send('sb')
      try:
         response = sock.recv(2048)
      except:
         return
      response=response.split('\t')
      res={}
      res['version']=response[0]
      res['url']=response[1]
      res['features']=response[2]
      if __version__!=res['version']:
         self.yes.bind(on_press=partial(open_url, res['url']))
         self.popup_label.text='Version: %s\n\nFeatures:\n%s\n\nDo you wish to update?\n' % (res['version'], res['features'])
         self.popup.open()
         return
      return


   #-----------------------------------------------
   # on_pause
   #-----------------------------------------------
   def on_pause(self): #Don't close the application when user's pauses it (by clicking the home button, for example)
      return True

   #-----------------------------------------------
   # on_resume
   #-----------------------------------------------
   def on_resume(self): #Don't do anything on resume.
      pass

   #-----------------------------------------------
   # my_key_handler
   #-----------------------------------------------
   def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
      if keycode1 in [27, 1001]:
         if self.sm.current == 'server_info':
            self.sm.current = 'server_list'
            return True
         if self.sm.current == 'loading_screen' and self.ls_terminate == False:
            self.ls_terminate = True
            return True
         if self.sm.current == 'server_list':
            self.stop()
            return True
         if self.sm.current=='player_info':
            self.sm.current='server_info'
            return True
         return True
      return False

   #-----------------------------------------------
   # post_build_init
   #-----------------------------------------------
   def post_build_init(self, *args):
      #load the serverlist on startup
      Thread(target=self.load_serverlist).start()
      Thread(target=self.tomaster).start()
      #bind the back button
      if platform() == 'android':
         import android
         android.map_key(android.KEYCODE_BACK, 1001)
      win = Window
      win.bind(on_keyboard=self.my_key_handler)

   #-----------------------------------------------
   # load_player
   #-----------------------------------------------
   def load_player(self, name, args=None):
      info = GetPlayerInfo(name)
      if info=='canceled':
         return
      self.sm.current='player_info'
      if not info:
         self.player_description.halign='center'
         if info!=False:
            self.player_description.text="[size=30][color=#000000]No profile for %s[/color][/size]" % name
         else:
            self.player_description.text="[size=30][color=#000000]Couldn't connect to DPLogin.com[/color][/size]"
         return
      else:
         self.player_description.halign='left'
      string = '[size=30][color=#000000][b]Profile for %s[/b][/color][/size]\n\n' % name
      tab = [ 'DPLogin ID:',
            'Names Registered:',
            'Active Clan:',
            'Former Clans:'
         ]
      for i in range(len(tab)):
         if info[i]!='':
            string=string+'[color=#000000][b]%s [/b][/color][color=#555555]%s[/color]\n' % (tab[i], info[i])
      self.player_description.text=string

   #-----------------------------------------------
   # thread_load_server
   #-----------------------------------------------
   def thread_load_server(self, server, b=None):
      self.c_server=server
      Thread(target=self.load_server, args=(server,)).start()

   #-----------------------------------------------
   # thread_update_server
   #-----------------------------------------------
   def thread_update_server(self, server, b=None):
      self.c_server=server
      Thread(target=self.update_server, args=(server,)).start()

   #-----------------------------------------------
   # load_server
   #-----------------------------------------------
   def load_server(self, server, b=None):
      self.loaded_servers_id += 1 #This is for the mapshot loader.
      self.server_info.clear_widgets()
      self.row_list = {} #The list of objets in the cvars table.
      self.page_root = GridLayout(cols=1,
                                  size_hint_y=1,
                                  size_hint_x=1)
      self.main_layout = MainLayout()
      self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
      status_response = self.serverlist_cache[server] #load the cached status response
      status_response_keys = status_response.keys() #get keys of the dict
      status_response_keys.sort() #sort them
      for i in status_response_keys: #adding rows to the cvars table, check add_row to understand it
         if i == 'players': continue
         self.add_row(i, status_response[i])

      self.carousel=Carousel(scroll_timeout=100,
                             size_hint_y=.5)
      self.cvarlist=BoxLayout(size_hint_x=1, size_hint_y=1)
      self.scroll_view = ScrollView()
      self.scroll_view.effect_y.bind(overscroll=self.on_playerlist_overscroll)
      self.addwidget(self.scroll_view, self.main_layout)
      self.addwidget(self.cvarlist, self.scroll_view)
      
      self.mapname_label = MapnameLabel(text=status_response['mapname'],
                                        size_hint_y=.05)

      self.carousel.add_widget(self.cvarlist)
      self.playerlist_root_layout = BoxLayout(size_hint_x=1, size_hint_y=1)
      self.playerlist_layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
      self.playerlist_layout.bind(minimum_height=self.playerlist_layout.setter('height'))
      self.coloured_playerlist(status_response)
      self.playerlist = ScrollView(do_scroll_y=True)
      self.playerlist.effect_y.bind(overscroll=self.on_playerlist_overscroll)
      self.addwidget(self.playerlist, self.playerlist_layout)
      self.addwidget(self.playerlist_root_layout, self.playerlist)
      self.carousel.add_widget(self.playerlist_root_layout)
      self.img=AsyncImage(source='loading_mapshot.png',
                     allow_stretch=True,
                     size_hint_y=.45,
                     nocache=True)
      mpname = status_response['mapname'].split('/')[-1] #get the mapname for loading mapshot
      src = 'http://91.239.67.195/mapshots/mapshots/%s.jpg' % mpname #create the link
      #add the widgets in the main thread
      self.addwidget(self.page_root, self.img)
      self.addwidget(self.page_root, self.mapname_label)
      self.addwidget(self.page_root, self.carousel)
      self.addwidget(self.server_info, self.page_root)
      self.sm.current = 'server_info'
      Thread(target=self.load_mapshot, args=(src, self.img,)).start()
   #-----------------------------------------------
   # update_server
   #-----------------------------------------------
   hx=0
   def update_server(self, server):
      self.hx+=1
      #self.sm.current='loading_screen'
      msg="Server Refreshed"
      #self.clearwidgets(
      #)
      try:
         status=Status(server)
      except:
         status=self.serverlist_cache[server]
         msg="UDP Timeout"
      #---
      if status['mapname']!=self.serverlist_cache[server]['mapname']:
         self.mapname_label.text=status['mapname']
         self.img.source='loading_mapshot.png'
         mpname = status['mapname'].split('/')[-1] #get the mapname for loading mapshot
         src = 'http://91.239.67.195/mapshots/mapshots/%s.jpg' % mpname #create the link
         Thread(target=self.load_mapshot, args=(src, self.img,)).start()
      #---
      self.refresh_cvarlist(status)
      self.refresh_playerlist(status)
      self.enable_playerlist_overscroll = False
      if msg=="Server Refreshed":
         self.serverlist_cache[server]=status
      sleep(0.5); self.tst(msg)

   @mainthread
   def refresh_playerlist(self, status):
      self.playerlist.effect_y.unbind(overscroll=self.on_playerlist_overscroll)
      self.playerlist_layout.unbind(minimum_height=self.playerlist_layout.setter('height'))
      self.playerlist_root_layout.remove_widget(self.playerlist)
      del self.playerlist
      del self.playerlist_layout
      self.playerlist_layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
      self.coloured_playerlist(status)
      self.playerlist = ScrollView(do_scroll_y=True)
      self.playerlist_layout.bind(minimum_height=self.playerlist_layout.setter('height'))
      self.playerlist.effect_y.bind(overscroll=self.on_playerlist_overscroll)
      self.playerlist.add_widget(self.playerlist_layout)
      self.playerlist_root_layout.add_widget(self.playerlist)

   @mainthread
   def refresh_cvarlist(self, status):
      self.scroll_view.effect_y.unbind(overscroll=self.on_playerlist_overscroll)
      self.main_layout.unbind(minimum_height=self.main_layout.setter('height'))
      self.cvarlist.remove_widget(self.scroll_view)
      del self.scroll_view
      del self.main_layout
      self.main_layout = MainLayout()
      status_keys = status.keys() #get keys of the dict
      status_keys.sort() #sort them
      for i in status_keys: #adding rows to the cvars table, check add_row to understand it
         if i == 'players': continue
         self.add_row(i, status[i], False)

      self.scroll_view = ScrollView()
      self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
      self.scroll_view.effect_y.bind(overscroll=self.on_playerlist_overscroll)
      self.scroll_view.add_widget(self.main_layout)
      self.cvarlist.add_widget(self.scroll_view)

   @mainthread
   def tst(self, msg):
      toast(msg)
   @mainthread
   def load_plist(self):
      self.carousel.load_slide(self.playerlist)
      self.sm.current='server_info'

   @mainthread
   def b_ind(self):
      self.playerlist_layout.bind(minimum_height=self.playerlist_layout.setter('height'))
      self.playerlist.effect_y.bind(overscroll=self.on_playerlist_overscroll)

   @mainthread
   def un_bind(self):
      self.playerlist.effect_y.unbind(overscroll=self.on_playerlist_overscroll)
      self.playerlist_layout.unbind(minimum_height=self.playerlist_layout.setter('height'))
      self.playerlist_root_layout.remove_widget(self.playerlist)
      del self.playerlist
      del self.playerlist_layout
      self.playerlist_layout = GridLayout(cols=1, spacing=1, size_hint_y=None)

   #-----------------------------------------------
   # load_mapshot
   #-----------------------------------------------
   def load_mapshot(self, src, img): #threaded mapshot loading
      loaded_servers_id = self.loaded_servers_id
      sleep(0.6) #Wait for the main layout to load-don't lag it.
      with open('mapshot.jpg', 'w+') as mapshot:
         try:
            if self.loaded_servers_id != loaded_servers_id:
               return #Don't put the picture if the a new server has been loaded.
            string=urlopen(src).read()
            if string[:9]=="<!DOCTYPE":
               raise('404')
            if self.loaded_servers_id != loaded_servers_id:
               return #Don't put the picture if the a new server has been loaded.
            mapshot.write(string)
         except:
            if self.loaded_servers_id != loaded_servers_id:
               return #Don't put the picture if the a new server has been loaded.
            self.set_mapshot('no_mapshot.png', img)
            return
      self.set_mapshot('mapshot.jpg', img) #Change the mapshot in the main thread

   #-----------------------------------------------
   # set_mapshot
   #-----------------------------------------------
   @mainthread
   def set_mapshot(self, src, img):
      img.source = src
      img.reload()

   def coloured_playerlist(self, serverinfo):
      if serverinfo['clients'] == 0:
         size=((Window.size[1]*0.5)-50*serverinfo['clients']+1) #Grey box's size (playerlist)
         if size<0:
            size=0
         self.serverinfo=serverinfo
         self.spacer=Black(size_hint_y=None, height=size, text='Server is empty') #Creating the grey box
         self.playerlist_layout.add_widget(self.spacer) #adding it
         return
      #get information about teams
      pr=[]; pb=[]; py=[]; pp=[]; po=[]
      for i in ['pr', 'pb', 'py', 'pp', 'po']:
         if i in serverinfo:
            if i=='pr': pr = serverinfo[i].split('!')[1:]
            if i=='pb': pb = serverinfo[i].split('!')[1:]
            if i=='py': py = serverinfo[i].split('!')[1:]
            if i=='pp': pp = serverinfo[i].split('!')[1:]
            if i=='po': po = serverinfo[i].split('!')[1:]
      j=-1
      for i in serverinfo['players']: #Yeah, this might be shorter, but it's not really important since it isn't that heavy ;) You can do it for me if you want ;D
         j+=1
         wgt=None
         if str(j) in pr: #LABEL FOR THE RED TEAM
            wgt=GridLayout(size_hint_y=None,
                           height=50,
                           cols=3,
                           spacing=1) #Row's layout

            pn=RedTeam(text='[color=#FFFFFF]%s[/color]' % i['name'], 
                       size_hint_x=1) #Player's name

            scr=RedTeam(size_hint_x=None, 
                        width=70,
                        text='[color=#FFFFFF]%s[/color]' % i['score']) #Player's score

            png=RedTeam(size_hint_x=None,
                        width=70,
                        text='[color=#FFFFFF]%s[/color]' % i['ping']) #Player's ping

            wgt.add_widget(pn); wgt.add_widget(scr); wgt.add_widget(png) #Add to the row.

         if str(j) in pb:
            wgt=GridLayout(size_hint_y=None,
                           height=50,
                           cols=3,
                           spacing=1)

            pn=BlueTeam(text='[color=#FFFFFF]%s[/color]' % i['name'],
                        size_hint_x=1)

            scr=BlueTeam(size_hint_x=None,
                         width=70,
                         text='[color=#FFFFFF]%s[/color]' % i['score'])

            png=BlueTeam(size_hint_x=None,
                         width=70,
                         text='[color=#FFFFFF]%s[/color]' % i['ping'])

            wgt.add_widget(pn); wgt.add_widget(scr); wgt.add_widget(png)

         if str(j) in py:
            wgt=GridLayout(size_hint_y=None,
                           height=50,
                           cols=3,
                           spacing=1)

            pn=YellowTeam(text='[color=#000000]%s[/color]' % i['name'],
                          size_hint_x=1)

            scr=YellowTeam(size_hint_x=None,
                           width=70,
                           text='[color=#000000]%s[/color]' % i['score'])

            png=YellowTeam(size_hint_x=None,
                           width=70,
                           text='[color=#000000]%s[/color]' % i['ping'])

            wgt.add_widget(pn); wgt.add_widget(scr); wgt.add_widget(png)

         if str(j) in pp:
            wgt=GridLayout(size_hint_y=None,
                           height=50,
                           cols=3,
                           spacing=1)

            pn=PurpleTeam(text='[color=#FFFFFF]%s[/color]' % i['name'],
                          size_hint_x=1)

            scr=PurpleTeam(size_hint_x=None,
                           width=70,
                           text='[color=#FFFFFF]%s[/color]' % i['score'])

            png=PurpleTeam(size_hint_x=None,
                           width=70,
                           text='[color=#FFFFFF]%s[/color]' % i['ping'])

            wgt.add_widget(pn); wgt.add_widget(scr); wgt.add_widget(png)

         if str(j) in po:
            wgt=GridLayout(size_hint_y=None,
                           height=50,
                           cols=3,
                           spacing=1)

            pn=Observer(text='[color=#000000]%s[/color]' % i['name'],
                        size_hint_x=1)

            scr=Observer(size_hint_x=None,
                        width=70,
                        text='[color=#000000]%s[/color]' % i['score']);

            png=Observer(size_hint_x=None,
                        width=70,
                        text='[color=#000000]%s[/color]' % i['ping']);

            wgt.add_widget(pn); wgt.add_widget(scr); wgt.add_widget(png)

         if not wgt:
            wgt=GridLayout(size_hint_y=None,
                           height=50,
                           cols=3,
                           spacing=1)

            pn=Connecting(text='[color=#000000]%s[/color]' % i['name'],
                          size_hint_x=1)

            scr=Connecting(size_hint_x=None,
                           width=70,
                           text='[color=#000000]%s[/color]' % i['score'])

            png=Connecting(size_hint_x=None,
                           width=70,
                           text='[color=#000000]%s[/color]' % i['ping'])

            wgt.add_widget(pn); wgt.add_widget(scr); wgt.add_widget(png)
         pn.bind(on_press=partial(self.thread_load_player, i['name']))
         scr.bind(on_press=partial(self.thread_load_player, i['name']))
         png.bind(on_press=partial(self.thread_load_player, i['name']))
         self.playerlist_layout.add_widget(wgt) #adding a row to the playerlist table
      size=((Window.size[1]*0.5)-50*serverinfo['clients']+1) #Grey box's size (playerlist)
      if size<0:
         size=0
      self.serverinfo=serverinfo
      self.spacer=Black(size_hint_y=None, height=size) #Creating the grey box
      self.playerlist_layout.add_widget(self.spacer) #adding it
   #-----------------------------------------------
   #thread_load_player
   #-----------------------------------------------
   def thread_load_player(self, name, arg=None):
      Thread(target=self.load_player, args=(name, )).start()
   #-----------------------------------------------
   # load_webpage
   #-----------------------------------------------
   def load_webpage(self, url, desc=None, post=None):
      if desc==None:
         desc='Downloading %s' % url
      self.loading_label.text=desc
      self.ls_terminate=False
      self.progress_bar.value=0
      self.hostname.text = "[0%]"
      chk=Check()
      Thread(target=self.threaded_urlopen, args=(chk, url, post)).start() #Thread loading headers
      t1 = time()
      limit=2
      if post:
         limit=4
      while (chk.size==None) and time()-t1<limit: #Wait for the HTTP response.
         if self.ls_terminate:
            return 'canceled'
         pass
      if not chk.response or chk.size==False: #If there's no response after more than 2 seconds
         return False
      myfile=''
      bytes_loaded = 0
      try:
         while not self.ls_terminate: #no loading when self.total_size is not known.
            chunk = chk.response.read(64)
            if not chunk: break #break the loop when the file has been just loaded.
            myfile=myfile+chunk
            percent = (bytes_loaded*100)/(chk.size)
            self.progress_bar.value=percent
            self.hostname.text = "[%s%%]"%percent
            bytes_loaded += len(chunk)
         if self.ls_terminate:
            return 'canceled'
      except:
         return False
      return myfile

   #-----------------------------------------------
   #threaded_urlopen
   #-----------------------------------------------
   def threaded_urlopen(self, chk, url, post):
      try:
         if post:
            chk.response = urlopen(url, urlencode(post.items()))
         else:
            chk.response = urlopen(url)
         try:
            chk.size = chk.response.info().getheader('Content-Length').strip()
            chk.size = int(chk.size)
         except AttributeError:
            chk.size=9999999
      except:
         chk.size = False

   #-----------------------------------------------
   # update_height
   #-----------------------------------------------
   def update_height(self, a=None, b=None): #Update some widgets on screen resize.
      try:
         if self.ne:
            self.ne.size=(Window.size[0], Window.size[1]+1)
            self.ne.text_size=self.ne.size
         self.screen_height=Window.size[0]
         if self.serverinfo:
            self.spacer.height=((Window.size[1]*0.5)-50*self.serverinfo['clients']+1)
         self.player_description.size=(Window.size[0], Window.size[1])
         self.player_description.text_size=(Window.size[0]*0.8, Window.size[1]*0.8)
      except:
         pass

   def popup_open(self, obj):
      self.popup_label.text_size=self.popup_label.size

   #-----------------------------------------------
   # on_ne
   #-----------------------------------------------
   def on_ne(self, first): #On network error while loading serverlist
      self.nerun = 1 #Mark the network error event as done
      self.ne.text_size = self.ne.size #change text size for the NetworkError label to it's size
      self.clearwidgets(self.server_list_layout) #Clearing widgets
      self.clearwidgets(self.slist_scroll)
      self.server_list_layout.bind(minimum_height=self.server_list_layout.setter('height')) #Enable scrolling event for refreshing after error
      self.addwidget(self.server_list_layout, self.ne)
      self.addwidget(self.slist_scroll, self.server_list_layout)
      if first: #If it's the first refresh
         self.slist_scroll.effect_y.bind(overscroll=self.thread_overscroll)
         self.addwidget(self.server_list, self.slist_scroll)

   #-----------------------------------------------
   # threaded_webload
   #-----------------------------------------------
   def threaded_webload(self): #this function is called from a thread to handle network problems. It's self-explainable.
      self.res = urlopen('http://70.85.9.178/serverlist.php')
      self.total_size = self.res.info().getheader('Content-Length').strip()
      self.total_size = int(self.total_size)

   #-----------------------------------------------
   # load_serverlist
   #-----------------------------------------------
   def load_serverlist(self, first=True):
      self.loading_serverlist=True
      self.nerun = 0 #set on_ne as 'haven't been run yet'
      self.sm.current = 'loading_screen' #switch to the loading_screen
      if first: #Do if it's the first run
         self.loading_label.text = "Downloading serverlist.php..."
         self.progress_bar.value = 0
         self.hostname.text = "[0%]"

      self.ls_terminate = False #Mark the loading process as not canceled
      self.ne = NetworkError(text='[color=#FFFFFF]No servers found or no internet connection.\nSwipe down to refresh.[/color]',
                     halign='center',
                     valign='top',
                     size=(Window.size[0], Window.size[1]+1)) #The label displayed on network errors.
      if first: #Do if it's the first run
         self.server_list_layout=GridLayout(cols=2,
                                    spacing=1,
                                    size_hint_y=None)
      addresses = []
      if first:
         sleep(0.6)
      serverlist=self.load_webpage('http://70.85.9.178/serverlist.php', 'Downloading serverlist.php...')
      if self.ls_terminate or not serverlist or serverlist.find('LatestClientBuild')==-1: #kill the function if it has been canceled by clicking the 'back' button / connection error.
         if not self.nerun: #Call the on_ne event on first run - no servers have been loaded yet OFC.
            self.on_ne(first)
         self.sm.current = 'server_list'
         self.enable_overscroll = False
         self.loading_serverlist = False
         return
      self.progress_bar.value = 100
      serverlist = serverlist.split('\r\n')
      self.loading_label.text = "Pinging servers..."
      self.progress_bar.value = 0
      for server in serverlist:
         if server == 'X': break #read http://dplogin.com/serverlist.php to understand it
         addresses.append(server)
      i = 0 #just for the progress bar
      serverlist_cache_backup = self.serverlist_cache
      l = len(addresses)
      for address in addresses: #ping the servers
         if self.ls_terminate: #run if the function has been canceled by user
            if first and not self.nerun: #if the on_ne function hasn't been run yet and it's the first serverlist refresh.
               self.on_ne(first)
            self.serverlist_cache=serverlist_cache_backup
            self.sm.current='server_list'
            self.enable_overscroll=False
            self.loading_serverlist = False
            return
         progress=(i*100)/l
         self.hostname.text = '%20.20s   [%d%%]' % (address, progress)
         self.progress_bar.value = progress
         try:
            self.serverlist_cache[address] = Status(address)
         except:
            self.serverlist_cache[address] = None
         i += 1

      queue = sort_dicts(self.serverlist_cache, 'clients') #sort the serverlist
      queue.reverse() #move the used servers from bottom to top
      self.hostname.text = "Done."
      self.progress_bar.value = 100

      self.loading_label.text = "Creating the table..."
      self.progress_bar.value = 0
      self.hostname.text = "[0%]"
      l = l*2
      dn = 0 #done servers count :D
      #Yeah, this might look crappy, but it's a safe solution
      if first:
         self.server_list_layout = GridLayout(cols=2,
                                    spacing=1,
                                    size_hint_y=None)
      self.clearwidgets(self.server_list_layout)
      self.clearwidgets(self.slist_scroll)
      if not first:
         self.server_list_layout = GridLayout(cols=2,
                                    spacing=1,
                                    size_hint_y=None)
      if len(queue) == 0: #If the serverlist is empty 
            self.addwidget(self.server_list_layout, NetworkError(text='No servers found.\nSwipe up to refresh.'))
            self.addwidget(self.slist_scroll, self.server_list_layout)
            self.sm.current = 'server_list'
            self.enable_overscroll = False
            self.loading_serverlist = False
            return
      for address in queue: #Appending to the table
         if not self.serverlist_cache[address]: continue #skip server if the UDP status package has timed out.
         h=self.serverlist_cache[address]['hostname'] #load the hostname
         btn=HostnameButton(markup=True,
                        size_hint_x=1,
                        text='[color=#000000][b]%s[/b][/color]' % h)
         btn.bind(on_press=partial(self.thread_load_server, address)) #Make the button load the detailed information on_press
         self.addwidget(self.server_list_layout, btn)
         dn+=1
         percent = (dn*100)/l
         self.progress_bar.value = percent
         self.hostname.text = "%s [%s%%]" % (h, percent) #h is the hostname ;)
         btn=ClientsButton(markup=True,
                     size_hint_x=None,
                     width=90,
                     text='[color=#000000][b]%s/%s[/b][/color]'%(len(self.serverlist_cache[address]['players']),
                                                      self.serverlist_cache[address]['maxclients']))
         btn.bind(on_press=partial(self.thread_load_server, i)) #Make the button load the detailed information on_press
         self.addwidget(self.server_list_layout, btn) 
      self.progress_bar.value = 100
      self.server_list_layout.bind(minimum_height=self.server_list_layout.setter('height'))
      self.addwidget(self.slist_scroll, self.server_list_layout)
      if first: #Enable overscrolls
         self.slist_scroll.unbind()
         self.slist_scroll.effect_y.bind(overscroll=self.thread_overscroll)
         self.addwidget(self.server_list, self.slist_scroll)
      self.sm.current = 'server_list'
      self.ls_terminate = True
      self.enable_overscroll = False #make the overscroll event active

   #-----------------------------------------------
   # addwidget
   #-----------------------------------------------
   @mainthread
   def addwidget(self, parent, child): #Adds a widget in the main thread
      parent.add_widget(child)

   #-----------------------------------------------
   # delwidget
   #-----------------------------------------------
   @mainthread
   def delwidget(self, parent, child): #Adds a widget in the main thread
      parent.remove_widget(child)

   #-----------------------------------------------
   # clearwidgets
   #-----------------------------------------------
   @mainthread
   def clearwidgets(self, obj): #Clears widgets in the main thread
      obj.clear_widgets()

   #-----------------------------------------------
   # thread_overscroll
   #-----------------------------------------------
   def thread_overscroll(self, obj, pos): #thread the overscroll event
      if not self.enable_overscroll and pos<-self.screen_height/4: #run if overscroll has not been disabled and it's long enough.
         self.loading_label.text = "Downloading serverlist.php..."
         self.progress_bar.value = 0
         self.hostname.text = "[0%]"
         self.sm.current = 'loading_screen'
         self.enable_overscroll = True   
         Thread(target=self.load_serverlist, args=(False,)).start() #thread it
         return
      if self.enable_overscroll == True and pos == 0:
         self.enable_overscroll = False #Enable the overscroll event again when pos is 0

   #-----------------------------------------------
   # on_playerlist_overscroll
   #-----------------------------------------------
   def on_playerlist_overscroll(self, obj, pos): #called when the playerlist has been overscrolled. Not used yet
      if not self.enable_playerlist_overscroll and pos<-75:
         self.enable_playerlist_overscroll = True
         self.playerlist_layout.clear_widgets()
         self.main_layout.clear_widgets()
         self.thread_update_server(self.c_server) 
         #self.load_serverlist(False)
         return
      if self.enable_playerlist_overscroll == True and pos == 0:
         self.enable_playerlist_overscroll = False
      return

   def add_row(self, cvar, cvar_value, in_thread=True): #Add a row to the cvars list
      cvar_label = CvarLabel(text=("[color=#000000][b]%s[/b][/color]" % cvar),
                        markup=True,
                        size_hint_x=.3) #header label
      var_label = VarLabel(size_hint_y=None,
                     size_hint_x=.7,
                     height=34,
                     text=("[color=#000000]%s[/color]" % cvar_value),
                     markup=True)
      if in_thread:
         self.addwidget(self.main_layout, cvar_label)
         self.addwidget(self.main_layout, var_label)
      else:
         self.main_layout.add_widget(cvar_label)
         self.main_layout.add_widget(var_label)
      self.row_list[cvar] = [cvar_label, var_label]#add to the list of rows


char_tab = ['\0','-', '-', '-', '_', '*', 't', '.', 'N', '-', '\n','#', '.', '>', '*', '*',
            '[', ']', '@', '@', '@', '@', '@', '@', '<', '>', '.', '-', '*', '-', '-', '-',
            ' ', '!', '\"','#', '$', '%', '&', '\'','(', ')', '*', '+', ',', '-', '.', '/', 
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
            '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\',']', '^', '_',
            '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '<',
            '(', '=', ')', '^', '!', 'O', 'U', 'I', 'C', 'C', 'R', '#', '?', '>', '*', '*',
            '[', ']', '@', '@', '@', '@', '@', '@', '<', '>', '*', 'X', '*', '-', '-', '-',
            ' ', '!', '\"','#', '$', '%', '&', '\'','(', ')', '*', '+', ',', '-', '.', '/',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
            '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\',']', '^', '_',
            '`', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '{', '|', '}', '~', '<']
#-----------------------------------------------
# rcon
#-----------------------------------------------
def rcon(hostname, port): #a basic status function
      sock = socket(AF_INET, SOCK_DGRAM)
      sock.connect((hostname, port))
      sock.settimeout(1)
      sock.send("\xFF\xFF\xFF\xFFstatus\0")
      try:
         response = sock.recv(2048)
      except:
         raise Exception('UDP Connection timed out')
      if response == '\xff\xff\xff\xffprint\nBad rcon_password.\n':
         raise Exception('Bad rcon password.')
      return response[:-1]

#-----------------------------------------------
# sort_dicts
#-----------------------------------------------
def sort_dicts(l, key): #sorts a list of dicts by a key
      pom=[]
      ret_list = []
      for j in l:
         i = l[j]
         if i:
            pom.append([i[key], j])
      pom.sort()
      for i in pom:
         ret_list.append(i[1])
      return ret_list

#-----------------------------------------------
# CleanSpecialChars
#-----------------------------------------------
def CleanSpecialChars(text): #Removes the garbage from player's nick (colors, symbols etc.)
   cleaned_text = ""
   skip_next = False
   for i in text:
      char_ascii=ord(i)
      #134-underline, 135-italic, 136-color
      if char_ascii==134 or char_ascii==135 or char_ascii==136 or skip_next: # Remove underline, italic symbols                           
         if char_ascii==136:
            skip_next = True
         else:
            skip_next = False
      else:
         cleaned_text = cleaned_text+char_tab[char_ascii]
         skip_next = False
   return cleaned_text

#-----------------------------------------------
# GetPlayerInfo
#-----------------------------------------------
def GetPlayerInfo(nameorid):
   server_browser.sm.current='loading_screen'
   #Check if there's at least one alphanumeric character in the name.
   cont=False
   for character in nameorid.lower():
      if character in 'abcdefghijklmnopqrstuvwxyz1234567890':
         cont=True; break
   if not cont:
      server_browser.sm.current='player_info'
      return None
   #--------
   res=None
   nicks = []
   post={'username': nameorid, 'pwhash': '', 'action': 'weblogin1'}
   response = server_browser.load_webpage('http://70.85.9.178/index.php', 'Getting the ID of %s' % nameorid, post=post)
   if not response:
      server_browser.sm.current='player_info'
      return False
   if response=='canceled':
      server_browser.sm.current='server_info'
      return 'canceled'
   matches = re.findall("<br>User ID: (\d+)<br>", response)
   for i in matches:
      response = server_browser.load_webpage('http://70.85.9.178/index.php?action=viewmember&playerid={id}'.format(id=i), 'Downloading the profile of %s' % i)
      if response=='canceled':
         server_browser.sm.current='server_info'
         return 'canceled'
      if not response:
         return False
      names = re.findall('\\<tr\\>\\<td\\>\\<b\\ class\\=\\"faqtitle\\"\\>Names?\\ registered\\:\\<\\/b\\>\\<\\/td\\>\\<td\\>(.*?)\\<\\/td\\>\\<\\/tr\\>', response)[0].split(', ')
      dp_id=str(i)
      res=response
   if not res:
      server_browser.sm.current='player_info'
      return None
   clan=re.findall('\\Active\\ (?:Clans)|(?:Clan)\\:\\<\\/b\\>\\<\\/td\\>\\<td\\>.*?\\<\\/td\\>\\<\\/tr\\>', res)
   for i in clan: #len(clan) is 0 or 1 propably
      clan=re.findall('\\<a\\ href\\=\\"\\/index.php\\?action\\=viewclan\\&clanid\\=\d+\\"\\>(.*?)\\<\\/a\\>', i)
   
   old_clan=re.findall('\\<b\\ class\\=\\"faqtitle\\"\\>\\Former\\ Clans?\\:\\<\\/b\\>\\<\\/td\\>\\<td\\>.*?\\<\\/td\\>\\<\\/tr\\>', res, re.DOTALL)
   for i in old_clan: #len(clan) is 0 or 1 propably
      old_clan=re.findall('\\<a\\ href\\=\\"\\/index.php\\?action\\=viewclan\\&clanid\\=\d+\\"\\>(.*?)\\<\\/a\\>', i)
   server_browser.sm.current='player_info'
   return [dp_id, ', '.join(names), ', '.join(clan), ', '.join(old_clan)]

#-----------------------------------------------
# Status
#-----------------------------------------------
def Status(host): #a simple status function
      ip=host.split(':')[0]
      port=int(host.split(':')[1])
      dictionary = {}
      players = []
      response = rcon(ip, port).split('\n')[1:]
      players_ = (response[1:])
      variables = response[0]
      for i in players_:
         temp_dict = {}
         cleaned_name = CleanSpecialChars(i)
         separated = cleaned_name.split(' ')
         temp_dict['score'] = separated[0]
         temp_dict['ping'] = separated[1]
         temp_dict['name'] = cleaned_name.split("%s %s " % (separated[0], separated[1]))[1][1:-1]
         players.append(temp_dict)
      dictionary['players'] = players
      dictionary['clients'] = len(players)
      variables=variables.split('\\')[1:]
      for i in range(0, len(variables), 2):
         dictionary[variables[i]] = variables[i+1]
      return dictionary
if __name__ == '__main__':
   server_browser=ServerBrowser()
   server_browser.run()
    
