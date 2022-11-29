#
#   ___ _____ ___ _     _____
#  / _ \_   _|_ _| |   | ____|
# | | | || |  | || |   |  _|
# | |_| || |  | || |___| |___
#  \__\_\|_| |___|_____|_____|
#

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import qtile, layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
#from libqtile.config import EzKey
from typing import List  # noqa: F401from typing import List  # noqa: F401

#import arcobattery

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"

myTerm = "xfce4-terminal"      # My terminal of choice
myBrowser = "qutebrowser" # My terminal of choice
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [
# Most of our keybindings are in sxhkd file - except these
# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),

# SUPER + SHIFT KEYS
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

]

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
group_labels = ["", "", "", "", "", "", "", "", "", "",]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

def init_layout_theme():
    return {"margin":4,
            "border_width":2,
            "border_focus": "#5e81ac",
            "border_normal": "#4c566a"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(margin = 10, border_width = 2, border_focus="#bc94f7", border_normal="#4c566a"),
    layout.MonadWide(margin = 5, border_width = 2, border_focus="#bc94f7", border_normal="#4c566a"),
    layout.Matrix(margin = 5, border_width = 2, border_focus="#bc94f7", border_normal="#4c566a"),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(**layout_theme),
    layout.TreeTab(
    font = "Ubuntu",
         fontsize = 12,
         sections = [" FIRST", " SECOND", " THIRD", " FOURTH"],
         section_fontsize = 12,
         border_width = 2,
         bg_color = "1c1f24",
         active_bg = "4f76c7",
         active_fg = "000000",
         inactive_bg = "a9a1e1",
         inactive_fg = "1c1f24",
         padding_left = 0,
         padding_x = 0,
         padding_y = 5,
         section_top = 10,
         section_bottom = 20,
         level_shift = 8,
         vspace = 3,
         panel_width = 200
         )
]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Default
colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ffffff", "#ffffff"],
          ["#1aff1a", "#1aff1a"], # background for active groups #32cd32
          ["#50FA7B", "#50FA7B"], # center window name & cmus
          ["#ff7f7f", "#ff7f7f"]] # notification

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [

              widget.TextBox(
                       text = '',
                       fontsize = 20,
                       font = "Symbols Nerd Font",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('rofi -show drun -config ~/.config/rofi/config.rasi -display-drun \"Run: \" -drun-display-format \"{name}\"')},
                       background = colors[5],
                       width = 23
                       ),

              widget.TextBox(
                       text = '',
                       fontsize = 60,
                       width = 25,
                       background = colors[5],
                       foreground = colors[4]
                       ),

              widget.GroupBox(
                       fontsize = 14,
                       font = "Symbols Nerd Font",
                       margin_y = 4,
                       margin_x = 0,
                       padding_y = 4,
                       padding_x = 4,
                       borderwidth = 3,
                       active = colors[8],
                       inactive = colors[7],
                       highlight_color = colors[4],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       urgent_border = colors[10],
                       foreground = colors[2],
                       background = colors[4]
                       ),
              widget.TextBox(
                       text = '',
                       foreground = colors[0],
                       background = colors[4],
                       padding = 0,
                       fontsize = 60
                       ),
              widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 7,
                       foreground = colors[3],
                       background = colors[1]
                       ),
              widget.WindowName(
                       foreground = colors[9],
                       background = colors[0],
                       padding = 0
                       ),

                widget.Sep(
                       linewidth = 1,
                       padding = 10,
                       background = colors[0]
                       ),

            ############ CENTER ############

              widget.Cmus (

                background = colors[0],
                play_color = colors[9],
              ),
            ############ RIGHT ############

              widget.TextBox( #CPU
                       text = '',
                       background = colors[0],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 40
                       ),
              widget.TextBox(
                       text = '',
                       fontsize = 17,
                       font = "Symbols Nerd Font",
                       background = colors[4],
                       foreground = colors[2],
                       padding = 0
                       ),
                widget.CPU(
                        foreground = colors[2],
                        background = colors[4],
                        foreground_alert = 'ffffff',
                        update_interval= 5.0,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e bpytop')},
                        font = "SauceCodePro Nerd Font Bold",
                        fontsize = 12,
                        padding = 7,
                        format = '{load_percent}%'
                        ),

                widget.TextBox( #RAM
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = 0,
                       fontsize = 40
                       ),
                widget.TextBox(
                       text = '',
                       fontsize = 12,
                       font = "Symbols Nerd Font",
                       foreground = colors[2],
                       background = colors[5],
                       padding = 0
                       ),
                widget.Memory(
                        foreground = colors[2],
                        background = colors[5],
                        foreground_alert = 'ff0000',
                        update_interval=5.0,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e bpytop')},
                        font = "SauceCodePro Nerd Font Bold",
                        fontsize = 12,
                        padding = 0,
                        format='{MemUsed: .0f}{mm} /{MemTotal: .0f}{mm} '
                        ),

                 widget.TextBox( #Temp
                           text = '',
                           background = colors[5],
                           foreground = colors[4],
                           padding = 0,
                           fontsize = 40
                           ),

                 widget.TextBox(
                           text = '',
                           background = colors[4],
                           foreground = colors[2],
                           font = "Symbols Nerd Font",
                           fontsize = 12,
                            padding = 0
                           ),
                  widget.ThermalSensor(
                            fmt = '{} ',
                            update_interval = 10,
                            tag_sensor = 'Core 1',
                            background = colors[4],
                            foreground_alert = 'ffbb00',
                            threshold = 70,
                            font = "SauceCodePro Nerd Font Bold",
                            fontsize = 12,
                            padding = 7
                            ),

                widget.TextBox( #Vol
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = 0,
                       fontsize = 40
                       ),
               widget.TextBox(
                       text = "",
                       fontsize = 15,
                       font = "Symbols Nerd Font",
                       foreground = colors[2],
                       background = colors[5],
                       padding = 0
                       ),
              widget.Volume(
                       background = colors[5],
                       font = "SauceCodePro Nerd Font Bold",
                       fontsize = 12,
                       padding = 7
                       ),


                widget.TextBox( #Updates
                       text = '',
                       background = colors[5],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 40
                       ),
                widget.Wallpaper (
                       directory = '~/Pictures/wallpapers',
                       label = "⟳",
                       random_selection = True,
                       background = colors[4],
                       foreground = colors[2],
                       scroll_delay = 2,
                       font = "Symbols Nerd Font",
                       padding = 7,    
                       fontsize = 17
                       ),
                widget.CheckUpdates(
                       update_interval = 60,
                       distro = 'Arch',
                       fmt = '{}',
                       display_format = "{updates} Updates",
                       foreground = colors[2],
                       background = colors[4],
                       font = "SauceCodePro Nerd Font Bold",
                       fontsize = 12,
                       padding = 7,
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')}
                       ),

                widget.TextBox( #Net
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = 0,
                       fontsize = 40
                       ),
                widget.TextBox(
                       text = "",
                       foreground = colors[2],
                       background = colors[5],
                       padding = 0,
                       font = "Symbols Nerd Font",
                       fontsize = 17
                       ),
               widget.Net(
                       format = '{down} / {up} ',
                       foreground = colors[2],
                       background = colors[5],
                       update_interval= 5.0,
                       font = "SauceCodePro Nerd Font Bold",
                       fontsize = 12
                       ),

              widget.TextBox( #Windows
                       text = '',
                       background = colors[5],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 40
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       background = colors[4],
                       scale = 0.5
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[4],
                       font = "SauceCodePro Nerd Font Bold",
                       fontsize = 12,
                       padding = 7
                       ),

                widget.TextBox( #BTC
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = 0,
                       padding_x = 0,
                       fontsize = 40
                       ),
                widget.TextBox(
                       text = " ",
                       foreground = colors[2],
                       background = colors[5],
                       padding = 0,
                       font = "Symbols Nerd Font",
                       fontsize = 16
                       ),
              widget.CryptoTicker(
                       crypto = 'BTC',
                       foreground = colors[2],
                       background = colors[5],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myBrowser + ' cointop.sh')},
                       format = '{amount:.0f}',
                       font = "SauceCodePro Nerd Font Bold",
                       fontsize = 12,
                       padding = 7
                       ),

              widget.TextBox( #Date
                       text = '',
                       background = colors[5],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 40
                       ),
              widget.TextBox(
                       text = ' ',
                       background = colors[4],
                       foreground = colors[2],
                       padding = 0,
                       fontsize = 12
                       ),
              widget.Clock(
                       background = colors[4],
                       font = "SauceCodePro Nerd Font Bold",
                       fontsize = 12,
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('gsimplecal')},
                       format = '%B %d - %H:%M',
                       padding = 7
                       ),

             widget.TextBox( #System
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = 0,
                       fontsize = 40
                       ),

                widget.WidgetBox( 
                    background = colors[5],
                    text_closed = "",
                    text_open = " ",
                    fontsize = 12,                  
                    widgets=[
                      widget.Systray(background = colors[5])]                     
                    ),  

                widget.Sep(
                    background = colors[5],
                    linewidth = 0,
                    padding = 8

                    ),           
                
            ]



    return widgets_list


widgets_list = init_widgets_list()

def open_calendar(qtile):  # spawn calendar widget
    qtile.cmd_spawn('gsimplecal next_month')

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=25, opacity=0.9)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=25, opacity=0.9))]
screens = init_screens()

    

# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


dgroups_key_binder = None
dgroups_app_rules = []

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-tweak-tool.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='arcolinux-logout'),

],  

fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"