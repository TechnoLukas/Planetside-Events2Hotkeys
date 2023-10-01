import asyncio
from auraxium import event, ps2
import threading
import dearpygui.dearpygui as dpg
import keycode2keyname as kc2kn
import webbrowser
import time
from os import path
import ctypes
dpg.create_context()
dpg.create_viewport(title="PlanetsideHotkeyEvents - v1.0.0",width=1000, height=1050)
dpg.setup_dearpygui()
dpg.set_global_font_scale(0.5)


hotkey={"str":"","keycodes":[]}
keyspressed=[]
hotkey_input=False
    
def hotkey_input_callback(sender, app_data):
    pass
    #print(app_data)
def hotkey_input_activated(sender, app_data):
    global hotkey, hotkey_input
    hotkey_input=app_data
    #hotkey={"str":"","keycodes":[]}
    #dpg.set_value(hotkey_input, "")
    #dpg.disable_item(hotkey_input)
    #dpg.focus_item(hotkey_input)
    #print(hotkey)

def hotkey_input_deactivated(sender, app_data):
    global hotkey_input,hotkey
    if app_data == hotkey_input:
        hotkey_input=False
        hotkey={"str":"","keycodes":[]}
        
def key_pressed(a,keycode):
    global hotkey, keyspressed
    if keycode not in keyspressed:
        keyspressed.append(keycode)
    if hotkey_input!=False and keycode not in hotkey["keycodes"]:
        if keycode == 46: #del
            hotkey={"str":"","keycodes":[]}
            dpg.set_value(hotkey_input, "")
            dpg.disable_item(hotkey_input)
            dpg.focus_item(hotkey_input)
        else:
            hotkey["keycodes"].append(keycode)
            if len(hotkey["keycodes"]) >1: hotkey["str"]+=" + "
            hotkey["str"]+=kc2kn.key(keycode) 
            dpg.configure_item(hotkey_input, user_data=hotkey)
            #print(dpg.get_item_configuration(hotkey_input)["user_data"])
            dpg.set_value(hotkey_input, dpg.get_item_configuration(hotkey_input)["user_data"]["str"])
            dpg.disable_item(hotkey_input)
            time.sleep(0.05)
            dpg.focus_item(hotkey_input)

def key_released(a,keycode):
    global keyspressed
    if keycode in keyspressed:
        keyspressed.pop(keyspressed.index(keycode))

def presshotkey(sender, app_data, user_data):
    tt=time.time()
    while time.time()-tt<0.1:
        ctypes.windll.user32.keybd_event(16, 0, 0x0002, 0)
        ctypes.windll.user32.keybd_event(17, 0, 0x0002, 0)
        for pp in dpg.get_item_configuration(user_data)["user_data"]["keycodes"]:
            ctypes.windll.user32.keybd_event(pp, 0, 0, 0)

    for pr in dpg.get_item_configuration(user_data)["user_data"]["keycodes"]:
        ctypes.windll.user32.keybd_event(pr, 0, 0x0002, 0)

with dpg.item_handler_registry(tag="hotkey_input_handler") as handler:
    dpg.add_item_activated_handler(callback=hotkey_input_activated)
    dpg.add_item_deactivated_handler(callback=hotkey_input_deactivated)
with dpg.handler_registry(tag="hotkey_handler"):
    dpg.add_key_press_handler(callback=key_pressed)
    dpg.add_key_release_handler(callback=key_released)
with dpg.font_registry():
    dpg.bind_font(dpg.add_font(path.dirname(path.realpath(__file__))+"\\data\\fonts\\SuboleyaRegular-qZeV1.ttf", 90))


with dpg.viewport_menu_bar():
    with dpg.window(label="Help",tag="help",width=300,height=300,show=False,no_collapse=True,no_resize=True):
        dpg.add_text("Version 1.0.0")
        dpg.add_separator()
        b = dpg.add_button(label="Github", callback=lambda:webbrowser.open("https://github.com/TechnoLukas/Planetside-Events2Hotkeys"))

    with dpg.window(label="Log",tag="log",width=500,height=500,show=False,no_collapse=True):
        dpg.add_text("app started...")

    dpg.add_menu_item(label="Help", callback=lambda: dpg.configure_item("help",show=not(dpg.get_item_configuration("help")["show"])))
    dpg.add_menu_item(label="Log", callback=lambda: dpg.configure_item("log",show=not(dpg.get_item_configuration("log")["show"])))
        
with dpg.window(label="",tag="main"):
    with dpg.child_window(height=180, menubar=True,pos=(5,60),tag="settings",show=False):
        with dpg.menu_bar():
            dpg.add_text("Settings")
        with dpg.table(header_row=False, borders_innerH=True, 
                    borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column()
            dpg.add_table_column()
        dpg.add_text(default_value="Note: to clear hotkey, press DEL")
        dpg.add_text(default_value="",color=(255,0,0),tag="error")
    with dpg.child_window(height=160, menubar=True,autosize_y=True,pos=(5,250),tag="hotkeys",show=False):
        with dpg.menu_bar():
            #dpg.add_menu(label="Menu Options")
            dpg.add_text("Hotkeys Setup")
        with dpg.table(header_row=False, borders_innerH=True, 
                        borders_outerH=True, borders_innerV=True, borders_outerV=True):
                
            dpg.add_table_column()
            dpg.add_table_column()
            with dpg.table_row():
                tg="test"
                dpg.add_input_text(default_value='',hint="enter hotkey",callback=hotkey_input_callback,enabled=False,tag=tg,user_data={"str":"","keycodes":[]})
                dpg.bind_item_handler_registry(dpg.last_item(), "hotkey_input_handler")
                dpg.add_button(label="test run",callback=presshotkey,user_data=tg)
            with dpg.table_row():
                dpg.add_input_text(default_value='',hint="enter hotkey",callback=hotkey_input_callback,enabled=False,tag="Player Kill",user_data={"str":"","keycodes":[]})
                dpg.bind_item_handler_registry(dpg.last_item(), "hotkey_input_handler")
                dpg.add_text("Player Kill")
            with dpg.table_row():
                dpg.add_input_text(default_value='',hint="enter hotkey",callback=hotkey_input_callback,enabled=False,tag="Player Assist Kill",user_data={"str":"","keycodes":[]})
                dpg.bind_item_handler_registry(dpg.last_item(), "hotkey_input_handler")
                dpg.add_text("Player Assist Kill")
            with dpg.table_row():
                dpg.add_input_text(default_value='',hint="enter hotkey",callback=hotkey_input_callback,enabled=False,tag="Player Death",user_data={"str":"","keycodes":[]})
                dpg.bind_item_handler_registry(dpg.last_item(), "hotkey_input_handler")
                dpg.add_text("Player Death")
            with dpg.table_row():
                dpg.add_input_text(default_value='',hint="enter hotkey",callback=hotkey_input_callback,enabled=False,tag="Player Login",user_data={"str":"","keycodes":[]})
                dpg.bind_item_handler_registry(dpg.last_item(), "hotkey_input_handler")
                dpg.add_text("Player Login")
            with dpg.table_row():
                dpg.add_input_text(default_value='',hint="enter hotkey",callback=hotkey_input_callback,enabled=False,tag="Player Logout",user_data={"str":"","keycodes":[]})
                dpg.bind_item_handler_registry(dpg.last_item(), "hotkey_input_handler")
                dpg.add_text("Player Logout")
            with dpg.table_row():
                dpg.add_text("in progress...")
                dpg.add_text("VehicleDestroy")

with dpg.window(label="Login", modal=False, show=True, tag="popup", no_title_bar=True,no_resize=True, no_move=True,pos=(5,55)):
    dpg.add_text("Enter your in game nickname.")
    with dpg.table(header_row=False, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
        dpg.add_table_column()
        dpg.add_table_column()
        with dpg.table_row():
            dpg.add_text(default_value="game nick: ")
            dpg.add_input_text(default_value="",tag="nick")

    def start():
        dpg.configure_item("settings",show=True)
        dpg.configure_item("hotkeys",show=True)
        def startasync():
            loop = asyncio.new_event_loop()
            loop.create_task(game(dpg.get_value("nick")))
            loop.run_forever()
        threading.Thread(target=startasync).start()
        dpg.configure_item("popup", show=False)

    dpg.add_button(label="DONE", callback=start)

dpg.configure_item("popup", show=True)

async def game(inp):
    client = event.EventClient(service_id='s:example') #put here your service id
    char = await client.get_by_name(ps2.Character, inp) #Selecting the player so we will listen only to events of this player.  

    try:
        print(char.id)
        dpg.add_text(char.id,parent="log")
        dpg.configure_item("error",default_value=inp+" detected.",color=(0,255,0))
    except:
        dpg.configure_item("error",default_value=inp+" is not detected.",color=(255,0,0))
        return
    
    @client.trigger(event.GainExperience,characters=[char.id])
    async def print_gainexperience(evt): #The idea is to detect the kill by detecting the xp player got https://planetside.fandom.com/wiki/Experience_Points
        exp = await client.get_by_id(ps2.Experience, evt.experience_id)
        expstr = "amount: "+str(evt.amount)+" experience_description: "+str(exp.description)+" experience_id: "+str(exp.id)
        print(expstr)
        dpg.add_text(expstr,parent="log")
        if (exp.id==1 or exp.id==278 or exp.id==279):
            tg="Player Kill"
            presshotkey(None,None,tg)
            print(tg)
            dpg.add_text(tg,parent="log")
        if (exp.id==2 or exp.id==371 or exp.id==372):
            tg="Player Assist Kill"
            presshotkey(None,None,tg)
            dpg.add_text(tg,parent="log")

        # https://planetside.fandom.com/wiki/Experience_Points

        # "Kill Assist" = Kill Assist = 2
        # "High Threat Assist" = Kill Player Priority Assist = 371
        # "Extreme Menace Kill Assist" = Kill Player High Priority Assist = 372

        # "Kill" = Kill = 1
        # "High Threat Kill" = Priority Kill = 278
        # "Extreme Menace Kill" = High Priority Kill = 279

    @client.trigger(event.Death,characters=[char.id])
    async def print_playerdeath(evt):
        if evt.character_id==char.id:
            tg="Player Death"
            presshotkey(None,None,tg)
            print(tg)
            dpg.add_text(tg,parent="log")
    @client.trigger(event.PlayerLogin,characters=[char.id])
    async def print_playerlogin(evt):
        tg="Player Login"
        presshotkey(None,None,tg)
        print(tg)
        dpg.add_text(tg,parent="log")
    @client.trigger(event.PlayerLogout,characters=[char.id])
    async def print_playerlogout(evt):
        tg="Player Logout"
        presshotkey(None,None,tg)
        print(tg)
        dpg.add_text(tg,parent="log")

dpg.set_primary_window("main", True)
dpg.show_viewport()

dpg.start_dearpygui()

dpg.destroy_context()

