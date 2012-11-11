
Vocab_gold ='po'
Vocab_level_a = 'lvl'
Vocab_mp_a = 'MP'
Vocab_hp_a = 'HP'
Vocab_agi = 'agi'
Vocab_atk = 'atk'
Vocab_spi = 'spi'
Vocab_def = 'def'

class WindowBase(Window):
  #--------------------------------------------------------------------------
  # * Constants
  #--------------------------------------------------------------------------
  
  #--------------------------------------------------------------------------
  # * Object Initialization
  #     x      : window x-coordinate
  #     y      : window y-coordinate
  #     width  : window width
  #     height : window height
  #--------------------------------------------------------------------------
  def initialize(x, y, width, height):
    super().__init__(self, x, y, width, height)
    self.windowskin = Cache.load_windowskin("Window")
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.z = 100
    self.back_opacity = 200
    self.openness = 255
    self.create_contents()
    self._opening = false
    self._closing = false
    
##  #--------------------------------------------------------------------------
##  # * Dispose
##  #--------------------------------------------------------------------------
##  def dispose
##    self.contents.dispose
##    #super

  #--------------------------------------------------------------------------
  # * Create Window Contents
  #--------------------------------------------------------------------------
  def create_contents(self):
    self.contents = Contents((self.width - 32, self.height - 32))
  
  #--------------------------------------------------------------------------
  # * Frame Update
  #--------------------------------------------------------------------------
  def update():
    super().update()
    if self._opening:
      self.openness += 48
      if self.openness == 255:
          self._opening = False 
    elif self._closing:
      self.openness -= 48
      if self.openness == 0:
         self._closing = False
          
  #--------------------------------------------------------------------------
  # * Open Window
  #--------------------------------------------------------------------------
  def open(self):
    if self.openness < 255:
        self._opening = True 
    self._closing = False

  #--------------------------------------------------------------------------
  # * Close Window
  #--------------------------------------------------------------------------
  def close(self):
    if self.openness > 0:
        self._closing = True
    self._opening = False
    
  #--------------------------------------------------------------------------
  # * Get Text Color
  #     n : Text color number  (0-31)
  #--------------------------------------------------------------------------
  def text_color(self, n):
    x = 64 + (n % 8) * 8
    y = 96 + (n / 8) * 8
    return self.windowskin.get_at(x, y)
  
  #--------------------------------------------------------------------------
  # * Get Normal Text Color
  #--------------------------------------------------------------------------
  def normal_color(self):
    return self.text_color(0)
  
  #--------------------------------------------------------------------------
  # * Get System Text Color
  #--------------------------------------------------------------------------
  def system_color(self):
    return self.text_color(16)

  #--------------------------------------------------------------------------
  # * Get Crisis Text Color
  #--------------------------------------------------------------------------
  def crisis_color(self):
    return self.text_color(17)
  
  #--------------------------------------------------------------------------
  # * Get Knockout Text Color
  #--------------------------------------------------------------------------
  def knockout_color(self):
    return self.text_color(18)

  #--------------------------------------------------------------------------
  # * Get Gauge Background Color
  #--------------------------------------------------------------------------
  def gauge_back_color(self):
    return self.text_color(19)
  
  #--------------------------------------------------------------------------
  # * Get HP Gauge Color 1
  #--------------------------------------------------------------------------
  def hp_gauge_color1(self):
    return self.text_color(20)
  
  #--------------------------------------------------------------------------
  # * Get HP Gauge Color 2
  #--------------------------------------------------------------------------
  def hp_gauge_color2(self):
    return self.text_color(21)
  
  #--------------------------------------------------------------------------
  # * Get MP Gauge Color 1
  #--------------------------------------------------------------------------
  def mp_gauge_color1(self):
    return self.text_color(22)
  
  #--------------------------------------------------------------------------
  # * Get MP Gauge Color 2
  #--------------------------------------------------------------------------
  def mp_gauge_color2(self):
    return self.text_color(23)
  
  #--------------------------------------------------------------------------
  # * Get Equip Screen Power Up Color
  #--------------------------------------------------------------------------
  def power_up_color(self):
    return self.text_color(24)
  
  #--------------------------------------------------------------------------
  # * Get Equip Screen Power Down Color
  #--------------------------------------------------------------------------
  def power_down_color(self):
    return self.text_color(25)
  
  #--------------------------------------------------------------------------
  # * Draw Icon
  #     icon_index : Icon number
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     enabled    : Enabled flag. When false, draw semi-transparently.
  #--------------------------------------------------------------------------
  def draw_icon(self, icon_index, x, y, enabled=True):
    bitmap = Cache.iconset()
    rect = Rect(icon_index % 16 * 24, icon_index / 16 * 24, 24, 24)
    #enabled ? 255 : 128
    self.contents.blit(bitmap, (x, y), rect)
  
  #--------------------------------------------------------------------------
  # * Draw Face Graphic
  #     face_name  : Face graphic filename
  #     face_index : Face graphic index
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     size       : Display size
  #--------------------------------------------------------------------------
  def draw_face(self, face_name, face_index, x, y, size = 96):
    bitmap = Cache.face(face_name)
    rect = Rect.new(0, 0, 0, 0)
    rect.x = face_index % 4 * 96 + (96 - size) / 2
    rect.y = face_index / 4 * 96 + (96 - size) / 2
    rect.width = size
    rect.height = size
    self.contents.blit(bitmap, (x,y), rect)
    
  #--------------------------------------------------------------------------
  # * Draw Character Graphic
  #     character_name  : Character graphic filename
  #     character_index : Character graphic index
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #--------------------------------------------------------------------------
  def draw_character(self, character_name, character_index, x, y):
    if character_name == None: return
    bitmap = Cache.character(character_name)
    sign = character_name[0:2]#[/^[\!\$].]
    if ('$' in sign):
      cw = bitmap.width / 3
      ch = bitmap.height / 4
    else:
      cw = bitmap.width / 12
      ch = bitmap.height / 8
    
    n = character_index
    src_rect = Rect((n%4*3+1)*cw, (n/4*4)*ch, cw, ch)
    self.contents.blit(bitmap, (x - cw / 2, y - ch), src_rect)
  
  #--------------------------------------------------------------------------
  # * Get HP Text Color
  #     actor : actor
  #--------------------------------------------------------------------------
  def hp_color(self, actor):
    if actor.hp == 0: return self.knockout_color()
    if actor.hp < actor.maxhp / 4:return self.crisis_color()
    return self.normal_color()
  
  #--------------------------------------------------------------------------
  # * Get MP Text Color
  #     actor : actor
  #--------------------------------------------------------------------------
  def mp_color(self, actor):
    if actor.mp < actor.maxmp / 4:return self.crisis_color()
    return self.normal_color()

  #--------------------------------------------------------------------------
  # * Draw Actor Walking Graphic
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #--------------------------------------------------------------------------
  def draw_actor_graphic(self, actor, x, y):
    self.draw_character(actor.character_name, actor.character_index, x, y)
  
  #--------------------------------------------------------------------------
  # * Draw Actor Face Graphic
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     size  : Display size
  #--------------------------------------------------------------------------
  def draw_actor_face(self, actor, x, y, size=96):
    self.draw_face(actor.face_name, actor.face_index, x, y, size)
  
  #--------------------------------------------------------------------------
  # * Draw Name
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #--------------------------------------------------------------------------
  def draw_actor_name(self, actor, x, y):
    self.font.color = hp_color(actor)
    self.draw_text(x, y, 108, WLH, actor.name)
  
  #--------------------------------------------------------------------------
  # * Draw Class
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #--------------------------------------------------------------------------
  def draw_actor_class(self, actor, x, y):
    self.font.color = normal_color
    self.draw_text(x, y, actor.class_name)
  
  #--------------------------------------------------------------------------
  # * Draw Level
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #--------------------------------------------------------------------------
  def draw_actor_level(self, actor, x, y):
    self.font_color = self.system_color()
    self.draw_text(x, y, 32, WLH, Vocab_level_a)
    self.font_color = self.normal_color()
    self.draw_text(x + 32, y, 24, WLH, actor.level, 2)
  
  #--------------------------------------------------------------------------
  # * Draw State
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     width : draw spot width
  #--------------------------------------------------------------------------
  def draw_actor_state(actor, x, y, width = 96):
    count = 0
    for state in actor.states:
      draw_icon(state.icon_index, x + 24 * count, y)
      count += 1
      if (24 * count > width - 24):break 
    
  
  #--------------------------------------------------------------------------
  # * Draw HP
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     width : Width
  #--------------------------------------------------------------------------
  def draw_actor_hp(actor, x, y, width = 120):
    self.draw_actor_hp_gauge(actor, x, y, width)
    self.font_color = system_color
    self.draw_text(x, y, 30, WLH, Vocab_hp_a)
    self.font_color = hp_color(actor)
    last_font_size = self.font.get_ascent()
    xr = x + width
    if width < 120:
      self.draw_text(xr - 44, y, 44, WLH, actor.hp, 2)
    else:
      self.draw_text(xr - 99, y, 44, WLH, actor.hp, 2)
      self.font.color = normal_color
      self.draw_text(xr - 55, y, 11, WLH, "/", 2)
      self.draw_text(xr - 44, y, 44, WLH, actor.maxhp, 2)
    
  
  #--------------------------------------------------------------------------
  # * Draw HP gauge
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     width : Width
  #--------------------------------------------------------------------------
  def draw_actor_hp_gauge(self, actor, x, y, width = 120):
    gw = width * actor.hp / actor.maxhp
    gc1 = self.hp_gauge_color1()
    gc2 = self.hp_gauge_color2()
    self.contents.fill(gauge_back_color, Rect(x, y + WLH - 8, width, 6))
    #self.contents.gradient_fill_rect(x, y + WLH - 8, gw, 6, gc1, gc2)
  
  #--------------------------------------------------------------------------
  # * Draw MP
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     width : Width
  #--------------------------------------------------------------------------
  def draw_actor_mp(self, actor, x, y, width=120):
    self.draw_actor_mp_gauge(actor, x, y, width)
    self.font_color = self.system_color()
    self.draw_text(x, y, Vocab_mp_a)
    self.font_color = self.mp_color(actor)
    last_font_size = self.font.get_ascent()
    xr = x + width
    if width < 120:
      self.draw_text(xr - 44, y, actor.mp)
    else:
      self.draw_text(xr - 99, y, actor.mp)
      self.font_color = self.normal_color()
      self.draw_text(xr - 55, y, "/")
      self.draw_text(xr - 44, y, actor.maxmp)
    

  #--------------------------------------------------------------------------
  # * Draw MP Gauge
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     width : Width
  #--------------------------------------------------------------------------
  def draw_actor_mp_gauge(self, actor, x, y, width = 120):
    gw = width * actor.mp / max(actor.maxmp, 1)
    gc1 = self.mp_gauge_color1()
    gc2 = self.mp_gauge_color2()
    self.contents.fill(self.gauge_back_color(), Rect(x, y + WLH - 8, width, 6))
    #self.contents.gradient_fill_rect(x, y + WLH - 8, gw, 6, gc1, gc2)
  
  #--------------------------------------------------------------------------
  # * Draw Parameters
  #     actor : actor
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     type  : Type of parameters (0-3)
  #--------------------------------------------------------------------------
  def draw_actor_parameter(self, actor, x, y, type):
    if type == 0:
      parameter_name = Vocab_atk
      parameter_value = actor.atk
    elif type == 1:
      parameter_name = Vocab_def
      parameter_value = actor.defense
    elif type == 2:
        parameter_name = Vocab_spi
        parameter_value = actor.spi
    elif type == 3:
      parameter_name = Vocab_agi
      parameter_value = actor.agi
    self.font_color = self.system_color
    self.draw_text(x, y, parameter_name)
    self.font_color = normal_color
    self.draw_text(x + 120, y, parameter_value)
  
  #--------------------------------------------------------------------------
  # * Draw Item Name
  #     item    : Item (skill, weapon, armor are also possible)
  #     x       : draw spot x-coordinate
  #     y       : draw spot y-coordinate
  #     enabled : Enabled flag. When false, draw semi-transparently.
  #--------------------------------------------------------------------------
  def draw_item_name(self, item, x, y, enabled = True):
    if item != None:
      self.draw_icon(item.icon_index, x, y, enabled)
      self.font_color = self.normal_color()
      #enabled ? 255 : 128
      self.font_color.alpha = 255
      self.draw_text(x + 24, y, item.name)
    

  #--------------------------------------------------------------------------
  # * Draw number with currency unit
  #     value : Number (gold, etc)
  #     x     : draw spot x-coordinate
  #     y     : draw spot y-coordinate
  #     width : Width
  #--------------------------------------------------------------------------
  def draw_currency_value(self, value, x, y, width):
    self.font_color = self.normal_color()
    self.draw_text(x, y, value)
    self.font_color = self.system_color()
    self.draw_text(x, y, Vocab_gold)
    

