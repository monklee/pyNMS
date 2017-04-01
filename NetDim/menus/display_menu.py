# NetDim
# Copyright (C) 2017 Antoine Fourmy (contact@netdim.fr)

import tkinter as tk
from os.path import join
from objects.objects import *
from tkinter import ttk
from PIL import ImageTk
from pythonic_tkinter.preconfigured_widgets import *
from collections import OrderedDict
from graph_generation.network_dimension import NetworkDimension

class DisplayMenu(ScrolledFrame):
    
    def __init__(self, notebook, master):
        super().__init__(notebook, width=200, height=600, borderwidth=1, relief='solid')
        self.ms = master
        font = ('Helvetica', 8, 'bold')
        
        # label frame for multi-layer display
        lf_multilayer_display = Labelframe(self.infr)
        lf_multilayer_display.text = 'Multi-layer display'
        lf_multilayer_display.grid(0, 0, sticky='nsew')
        
        # label frame to manage sites
        lf_site_display = Labelframe(self.infr)
        lf_site_display.text = 'Per-site display'
        lf_site_display.grid(1, 0, sticky='nsew')
        
        # label frame to control the display per subtype
        lf_object_display = Labelframe(self.infr)
        lf_object_display.text = 'Per-object display'
        lf_object_display.grid(2, 0, sticky='nsew')
        
        self.dict_image = {}
        
        self.dict_size_image = {
        'netdim': (75, 75), 
        'motion': (75, 75), 
        'multi-layer': (150, 150),
        'site': (50, 50),
        'ethernet link': (85, 15),
        'optical link': (85, 15),
        'optical channel': (85, 15),
        'etherchannel': (85, 15),
        'pseudowire': (85, 15),
        'BGP peering': (85, 15),
        'routed traffic': (85, 15),
        'static traffic': (85, 15),
        'ring': (50, 40), 
        'tree': (50, 30), 
        'star': (50, 50), 
        'full-mesh': (50, 45)
        }
        
        for image_type, image_size in self.dict_size_image.items():
            x, y = image_size
            img_path = join(self.ms.path_icon, image_type + '.png')
            img_pil = ImageTk.Image.open(img_path).resize(image_size)
            img = ImageTk.PhotoImage(img_pil)
            self.dict_image[image_type] = img
        
        self.type_to_button = {}
                
        # multi-layer button
        ml_button = TKButton(self.infr)
        ml_button.config(image=self.dict_image['multi-layer'])
        ml_button.command = self.ml_display_mode
        ml_button.config(width=150, height=150)
        ml_button.grid(0, 0, 2, 2, padx=40, in_=lf_multilayer_display)
        self.type_to_button['multi-layer'] = ml_button
                
        self.layer_boolean = []
        for layer in range(1, 5):
            layer_bool = tk.BooleanVar()
            layer_bool.set(True)
            self.layer_boolean.append(layer_bool)
            button_limit = Checkbutton(self.infr, variable = layer_bool)
            button_limit.text = 'L' + str(layer)
            button_limit.command = self.update_display
            row, col = layer > 2, 2 + (layer + 1)%2
            button_limit.grid(row, col, in_=lf_multilayer_display)
            
        for obj_type in object_properties:
            if obj_type not in ('l2vc', 'l3vc'):
                cmd = lambda o=obj_type: self.invert_display(o)
                button = TKButton(self.infr, relief=tk.SUNKEN, command=cmd)
                if obj_type in link_class:
                    button.configure(text={
                                       'ethernet link': 'Ethernet link',
                                       'optical link': 'Optical link',
                                       'optical channel': 'Optical channel',
                                       'etherchannel': 'Etherchannel',
                                       'pseudowire': 'Pseudowire',
                                       'BGP peering': 'BGP peering',
                                       'routed traffic': 'Routed traffic',
                                       'static traffic': 'Static traffic' 
                                }[obj_type], compound='top', font=font)
                    button.config(image=self.dict_image[obj_type])
                    button.config(width=160, height=40)
                else:
                    button.config(image=self.ms.dict_image['default'][obj_type])
                    button.config(width=75, height=75)
                self.type_to_button[obj_type] = button
        
        # creation mode: type of node or link
        self.type_to_button['router'].grid(0, 0, padx=2, in_=lf_object_display)
        self.type_to_button['switch'].grid(0, 1, padx=2, in_=lf_object_display)
        self.type_to_button['oxc'].grid(0, 2, padx=2, in_=lf_object_display)
        self.type_to_button['host'].grid(0, 3, padx=2, in_=lf_object_display)
        self.type_to_button['regenerator'].grid(1, 0, padx=2, in_=lf_object_display)
        self.type_to_button['splitter'].grid(1, 1, padx=2, in_=lf_object_display)
        self.type_to_button['antenna'].grid(1, 2, padx=2, in_=lf_object_display)
        self.type_to_button['cloud'].grid(1, 3, padx=2, in_=lf_object_display)
        
        sep = Separator(self.infr)
        sep.grid(2, 0, 1, 4, in_=lf_object_display)
        
        self.type_to_button['ethernet link'].grid(3, 0, 1, 2, in_=lf_object_display)
        self.type_to_button['optical link'].grid(3, 2, 1, 2, in_=lf_object_display)
                                                
        self.type_to_button['optical channel'].grid(4, 0, 1, 2, in_=lf_object_display)
        self.type_to_button['etherchannel'].grid(4, 2, 1, 2, in_=lf_object_display)
        self.type_to_button['pseudowire'].grid(5, 0, 1, 2, in_=lf_object_display)
        self.type_to_button['BGP peering'].grid(5, 2, 1, 2, in_=lf_object_display)
        
        self.type_to_button['routed traffic'].grid(6, 0, 1, 2, in_=lf_object_display)
        self.type_to_button['static traffic'].grid(6, 2, 1, 2, in_=lf_object_display)
        
    def ml_display_mode(self):
        value = self.ms.cs.switch_display_mode()
        relief = 'sunken' if value else 'raised'
        self.type_to_button['multi-layer'].config(relief=relief)

    def update_display(self):
        display_settings = [0] + list(map(lambda x: x.get(), self.layer_boolean))
        self.ms.cs.display_layer = display_settings
        self.ms.cs.draw_all(False)
        
    def invert_display(self, obj_type):
        value = self.ms.cs.show_hide(obj_type)
        relief = 'sunken' if value else 'raised'
        self.type_to_button[obj_type].config(relief=relief)
         