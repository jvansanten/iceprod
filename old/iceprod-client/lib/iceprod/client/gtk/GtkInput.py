#!/bin/env python
#   copyright  (c) 2005
#   the icecube collaboration
#   $Id: $
#
#   @version $Revision: $
#   @date $Date: $
#   @author Juan Carlos Diaz Velez <juancarlos@icecube.wisc.edu>
#	@brief icetray connections frame for GtkIcetraConfig application
#########################################################################

import pygtk
import threading
pygtk.require('2.0')
import gtk
import re
import time
from gtkcal import Cal
import iceprod
from iceprod.core import dataclasses
from iceprod.core.dataclasses import *
from iceprod.core import metadata
from iceprod.core import lex
from GtkAddSimCat import GtkAddSimCat 
from iceprod.client.soaptrayclient import i3SOAPClient


class GtkInput:

    def __init__(self,parent,test=False):

        self.parent  = parent
        self.ticket  = 0
        self.maxjobs = 0
        self.descriptionstr = iceprod.client.descriptionstr
        self.description = ""
        self.descmap = {}
        self.difplus   = metadata.DIF_Plus()
        self.dif    = self.difplus.GetDIF()
        self.plus   = self.difplus.GetPlus()
        self.vbox = gtk.VBox(False,0)
        self.tv = gtk.TextView()
        if test: 
        	buff = self.tv.get_buffer()
        	buff.insert(buff.get_end_iter(),'Test...')
        self.sw = gtk.ScrolledWindow()

        self.frame = gtk.Frame()
        self.frame.set_border_width(20)

        self.sumframe = gtk.Frame("Summary")
        self.sumframe.set_border_width(10)
        self.sumframe.show()
        self.sumframe.add(self.sw)

        self.b0 = gtk.Button('Submit',stock=gtk.STOCK_EXECUTE)
        self.b0.connect('clicked', self.submit)

        self.hbbox = gtk.HButtonBox()
        self.hbbox.pack_start(self.b0, False, False, 1)

        gridbox = gtk.HBox()
        # Grid(s)
        self.grid_entry = gtk.Entry()
        self.grid_entry.set_max_length(300)
        self.grid_entry.connect("activate", self.submit)
        self.gridframe = gtk.Frame("Grid(s) to use")
        self.gridframe.add(self.grid_entry)
        gridbox.pack_start(self.gridframe,False,False,1)

        # Maxjobs
        self.maxjobs_entry = gtk.Entry()
        self.maxjobs_entry.set_max_length(10)
        self.maxjobs_entry.connect("activate", self.submit)
        self.maxjobs_entry.set_text(str(self.maxjobs))
        self.maxjobsframe = gtk.Frame("Number of jobs in dataset")
        self.maxjobsframe.add(self.maxjobs_entry)
        gridbox.pack_start(self.maxjobsframe,False,False,1)

        self.vbox.pack_start(gridbox,False,False,1)

        # Title Text field
        #self.title_entry = gtk.Entry()
        if test:
        	self.dif.SetEntryTitle('test')
        #	self.title_entry.set_text('test')

        #self.title_entry.set_max_length(80)
        #self.title_entry.connect("activate", self.submit)
        #self.entryframe = gtk.Frame("DIF Entry Title")
        #self.entryframe.add(self.title_entry)

        hbox = gtk.HBox()
        #hbox.pack_start(self.entryframe,False,False,1)

        # DIF Sensor menu
        hbbox = gtk.HButtonBox()
        sensor_menu = gtk.combo_box_new_text()
        sensor_menu.connect('changed', self.set_dif_sensor)
        self.dif.SetSensorName("ICECUBE")
        if test:
			item = sensor_menu.append_text("ICECUBE")
			sensor_menu.set_active(0)
        else: 
			for s in self.dif.GetValidSensorNames(): 
			       item = sensor_menu.append_text(s)
			sensorIndex = self.dif.GetValidSensorNames().keys().index('ICECUBE')
			sensor_menu.set_active(sensorIndex)

        self.sensorframe = gtk.Frame("Sensor")
        self.sensorframe.add(sensor_menu)

        hbbox.pack_start(self.sensorframe,False,False,1)
        hbox.pack_start(hbbox,False,False,1)

        #initialize descripton
        inputdataset = self.parent.GetSteering().GetParameter('inputdataset')
        if inputdataset:
           self.descriptionstr += "input dataset %s. " % inputdataset.GetValue()
        

        # Simprod Ticket No.
        self.ticket_entry = gtk.Entry()

        self.ticket_entry.set_max_length(6)
        self.ticket_entry.connect("activate", self.submit)
        self.ticket_entry.set_text('0')
        self.ticketframe = gtk.Frame("SimProd Ticket No.")
        self.ticketframe.add(self.ticket_entry)

        hbox.pack_start(self.ticketframe,False,False,1)


        # Parent dataset
        parentId = self.parent.GetSteering().GetParentId()
        self.pid_entry =  gtk.Label()
        self.pid_entry.set_markup(
            "<span foreground='red'><b>%d</b></span>" % parentId)
        self.pidframe = gtk.Frame("Parent ID")
        self.pidframe.add(self.pid_entry)
        hbox.pack_start(self.pidframe,False,False,1)
        self.vbox.pack_start(hbox,False,False,1)


        # Plus Category menu
        category_menu = gtk.combo_box_new_text()
        category_menu.connect('changed', self.set_plus_category)
        if test:
			self.plus.SetCategory('unclassified')
			item = category_menu.append_text(self.plus.GetCategory())
			for cat in self.plus.GetValidCategories(): 
				if cat != 'unclassified':
				   item = category_menu.append_text(cat)
        else:
			item = category_menu.append_text("[Select Category]")
			for cat in self.plus.GetValidCategories(): 
				item = category_menu.append_text(cat)
        category_menu.set_active(0)

        self.catframe = gtk.Frame("Category")
        self.catframe.add(category_menu)
        hbox = gtk.HBox()

        hbox.pack_start(self.catframe,False,False,1)


        # Plus Subcategory Text entry
        self.subcat_entry =  gtk.Label()
        subcat_txt="Sub-category will be automatically filled by server"
        self.subcat_entry.set_markup("<span foreground='red'>%s</span>" % subcat_txt)

        self.subcatframe = gtk.Frame("Subcategory")
        self.subcatframe.add(self.subcat_entry)
        hbox.pack_start(self.subcatframe,False,False,1)


        # DIF SOURCE menu
        hbbox = gtk.HButtonBox()
        source_menu = gtk.combo_box_new_text()
        source_menu.connect('changed', self.set_dif_source)
        if test:
			item = source_menu.append_text("SIMULATION")
			self.dif.SetSourceName("SIMULATION")
			source_menu.set_active(0)
        else: 
			for s in self.dif.GetValidSourceNames(): 
			    item = source_menu.append_text(s)
			source_menu.set_active(1)

        self.sourceframe = gtk.Frame("Source")
        self.sourceframe.add(source_menu)

        hbbox.pack_start(self.sourceframe,False,False,1)
        hbox.pack_start(hbbox,False,False,1)
        self.vbox.pack_start(hbox,False,False,1)

        # Plus Subcategory Text entry

        # DIF Parameters menu
        #dif_parameters_menu = gtk.combo_box_new_text()
        #dif_parameters_menu.connect('changed', self.set_dif_param)
        #if test:
        #	self.dif.SetParameters(self.dif.GetValidParameters()[0])
        #	item = dif_parameters_menu.append_text(self.dif.GetValidParameters()[0])
        #else:
        #	item = self.make_menu_item ("[Select Parameters]", self.set_dif_param, None) 
        #	for param in self.dif.GetValidParameters(): 
		#		item = self.make_menu_item (param, self.set_dif_param, param) 
		#		item = dif_parameters_menu.append_text(param)
        #dif_parameters_menu.set_active(0)

        #self.difparamframe = gtk.Frame("DIF Parameters")
        #self.difparamframe.add(dif_parameters_menu)

        #hbox = gtk.HButtonBox()
        #hbox.pack_start(self.difparamframe,False,False,1)
        #self.vbox.pack_start(hbox,False,False,1)
        self.dif.SetParameters(self.dif.GetValidParameters()[0])



        # Date entries
        current_year = time.strftime('%Y',time.localtime())
        self.scalframe = gtk.Frame("Start Date")
        self.startdate_entry = gtk.Entry()
        self.startdate_entry.set_text('%s-01-01T00:00:01' % current_year)
        self.c0 = gtk.Button('#')
        self.c0.connect('clicked', self.cal,self.startdate_entry)
        hbox = gtk.HBox()
        hbox.pack_start(self.startdate_entry,False,False,1)
        hbox.pack_start(self.c0,False,False,1)
        self.scalframe.add(hbox)

        self.ecalframe = gtk.Frame("End Date")
        self.enddate_entry = gtk.Entry()
        self.enddate_entry.set_text('%s-12-31T00:00:00' % current_year)
        self.c1 = gtk.Button('#')
        self.c1.connect('clicked', self.cal,self.enddate_entry)
        hbox = gtk.HBox()
        hbox.pack_start(self.enddate_entry,False,False,1)
        hbox.pack_start(self.c1,False,False,1)
        self.ecalframe.add(hbox)

        hbox = gtk.HBox()
        hbox.pack_start(self.scalframe,False,False,1)
        hbox.add(self.ecalframe)
        self.vbox.pack_start(hbox,False,False,1)

        # Simulation Category menu
        self.simulation_category_menu =  gtk.combo_box_new_text()
        self.simulation_category_menu.connect('changed', self.set_simulation_category)
        if test:
        	item = self.simulation_category_menu.append_text("Test")
        	self.parent.GetSteering().SetCategory("Test")
        else:
        	item = self.simulation_category_menu.append_text("[Select Category]")

        #for cat in dataclasses.SimulationCategories: 
        client = i3SOAPClient(geturl=self.parent.geturl)
        client.SetPrinter(self.parent.PrintText)
        if not test:
           for cat in client.GetSimCategories():
               item = self.simulation_category_menu.append_text(cat)
        self.simulation_category_menu.set_active(0)
        self.simulation_category_menu.append_text('Add category...')

        self.simcatframe = gtk.Frame("SimProd Category")
        self.simcatframe.add(self.simulation_category_menu)
        self.simcathbox = gtk.HBox()
        self.simcathbox.pack_start(self.simcatframe,False,False,1)

        # Dataset Type menu
        self.dataset_type_menu =  gtk.combo_box_new_text()
        self.dataset_type_menu.connect('changed', self.set_dataset_type)
        if test:
        	item = self.dataset_type_menu.append_text("TEST")
        	self.parent.GetSteering().SetDatasetType("TEST")
        else:
        	item = self.dataset_type_menu.append_text("[Select Dataset Type]")
        for cat in dataclasses.DatasetTypes: 
        	item = self.dataset_type_menu.append_text(cat)
        self.dataset_type_menu.set_active(0)

        self.datasettypeframe = gtk.Frame("Dataset Type")
        self.datasettypeframe.add(self.dataset_type_menu)
        self.simcathbox.pack_start(self.datasettypeframe,False,False,1)

        self.vbox.pack_start(self.simcathbox,False,False,1)



        # Pack Summary TextView
        self.vbox.pack_start(self.sumframe)
        self.vbox.pack_start(self.hbbox, False)
        self.sw.add(self.tv)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_MOUSE)
        self.window.set_border_width(10)
        self.frame.add(self.vbox)
        self.window.add(self.frame)
        self.window.set_resizable(True)
        self.window.show()

        self.window.set_size_request(700, 500)
        self.window.set_title("Run Description")
        self.frame.show_all()

        self.descmap['category'] = '%(category)s'
        self.descmap['inputdataset'] = '%(inputdataset)s'
        self.descmap['geometry'] = '%(geometry)s'
        self.descmap['simcat'] = '%(simcat)s'
        self.descmap['composition'] = '%(composition)s'
        self.descmap['weighted'] = '%(weighted)s'
        self.descmap['spectrum'] = '%(spectrum)s'
        self.descmap['icemodel'] = '%(icemodel)s'
        self.descmap['angularrange'] = '%(angularrange)s'
        self.descmap['energyrange'] = '%(energyrange)s'

        steering = self.parent.GetSteering()
        expparser = lex.ExpParser( {
                    'extern':0,
                    'procnum':0,
                    'tray':0,
                    'iter':0,
                    'dataset':0,
                    'nproc': 0,
                    },
                    steering)
        for p in steering.GetParameters():
            try:
               self.descmap[p.GetName()] = expparser.parse(p.GetValue())
            except Exception,e: pass

        self.description = self.descriptionstr % self.descmap
        buff = self.tv.get_buffer()
        buff.set_text(self.description)
        if test:
            self.descmap['simcat']   = 'Test'
            self.descmap['category'] = 'unclassified'
            self.description = self.descriptionstr % self.descmap
            buff.set_text('Test: '+ self.description )
            if time.localtime()[1:3] == (4,1):
               buff.set_text(''.join(map(chr,iceprod.apr1))*4)
        
    def cal(self,widget,text_field):
        cal = Cal(text_field)
	

    def submit(self,widget):
        buff = self.tv.get_buffer()
        bounds = buff.get_bounds()
        dtext = buff.get_text(bounds[0],bounds[1])
        self.dif.SetSummary(dtext)
        #self.dif.SetEntryTitle(self.title_entry.get_text())
        self.dif.SetEntryTitle(dtext[0:min(len(dtext)-1,100)])
        self.plus.SetStartDatetime(self.startdate_entry.get_text())
        self.plus.SetEndDatetime(self.enddate_entry.get_text())

        self.grids = self.grid_entry.get_text()
        if not self.grids:
			self.fail_submit("You must specify at least one grid!")
			return

        try: 
            self.maxjobs = int(self.maxjobs_entry.get_text())
        except: 
			self.fail_submit("No. of jobs must be an integer!")
			return

        try: 
            self.ticket = int(self.ticket_entry.get_text())
        except: 
			self.fail_submit("SimProd ticket No. must be an integer!")
			return

        if not self.dif.GetEntryTitle(): 
			self.fail_submit("You must enter a DIF entry title before submitting")
			return

        if not self.dif.GetParameters(): 
			self.fail_submit("You must select DIF Parameters before submitting")
			return

        if not self.plus.GetCategory(): 
			self.fail_submit("You must select a Category before submitting")
			return

        if not len(dtext): 
			self.fail_submit("You must enter a summary before submitting")
			return

        date_regex = r'^[0-9]{4,4}(-[0-9]{2,2}){2,2}T([0-9]{2,2}:){2,2}[0-9]{2,2}'

        startdate = self.startdate_entry.get_text()
        if not startdate:
			self.fail_submit("You must enter a start date")
			return

        match = re.match(date_regex, startdate)
        if not match:
			self.fail_submit("There is a problem with your start date")
			return

        enddate = self.enddate_entry.get_text()
        if not enddate:
			self.fail_submit("You must enter an end date")
			return

        match = re.match(date_regex, enddate)
        if not match:
			self.fail_submit("There is a problem with your end date")
			return

        if self.parent.GetSteering().GetCategory() == None:
			self.fail_submit("You need to select a simulation category")
			return

        self.parent.GetSteering().SetDescription(dtext)
        self.window.destroy()

        # Add projects from any included metaprojects to DIFPlus
        for metaproject in self.parent.GetIceTrayConfig().GetMetaProjectList():
        	for project in metaproject.GetProjectList():
				self.plus.AddProject(project)

        # Add projects not included in any metaprojects to DIFPlus
        for project in self.parent.GetIceTrayConfig().GetProjectList():
			self.plus.AddProject(project)

        self.parent.GetSteering().AddExtra("Grid",self.grids)
        self.parent.GetSteering().AddExtra("Metadata",self.difplus)
        self.parent.GetSteering().AddExtra("Ticket",self.ticket)
        self.parent.GetSteering().AddExtra("Maxjobs",self.maxjobs)
        self.parent.GetSteering().AddExtra("DatasetParams",self.descmap)
        self.parent.PrintText("preparing submission...")
        self.parent.submit_auth(self.parent.submit)

    def fail_submit(self,msg):
        self.parent.PrintText(msg)

    def make_menu_item(self,name, callback, data=None):
		item = gtk.MenuItem(name)
		item.connect("activate", callback, data)
		item.show()
		return item

    def set_plus_category(self,combobox): 
		model = combobox.get_model()
		index = combobox.get_active()
		if index: 
			cat = model[index][0]
			if not cat == "[Select Category]" :
				self.plus.SetCategory(cat)
				self.set_description('category',cat)


    def set_dif_source(self,combobox): 
		model = combobox.get_model()
		index = combobox.get_active()
		if index: 
			src = model[index][0]
			self.dif.SetSourceName(src)

    def set_description(self,key=None,value=None): 
        buff = self.tv.get_buffer()
        bounds = buff.get_bounds()
        txt = buff.get_text(bounds[0],bounds[1])
        for k,v in self.descmap.items():
            txt = txt.replace(v,'%('+k+')s')
        if key:
            self.descmap[key] = value
        self.description = txt % self.descmap 
        buff.set_text(self.description)

    def set_dif_sensor(self,combobox): 
		model = combobox.get_model()
		index = combobox.get_active()
		if index: 
			src = model[index][0]
			self.dif.SetSensorName(src)
			self.set_description('sensor',src.strip())

    def set_simulation_category(self,combobox): 
		model = combobox.get_model()
		index = combobox.get_active()
		if index: 
			cat = model[index][0]
			if cat.startswith('Add category'):
				self.make_simulation_category(cat)
			elif not cat == "[Select Category]":
				self.parent.GetSteering().SetCategory(cat)
				self.set_description('simcat',cat)

    def set_dataset_type(self,combobox): 
		model = combobox.get_model()
		index = combobox.get_active()
		if index: 
			dtype = model[index][0]
			if not dtype == "[Select Dataset Type]":
				self.parent.GetSteering().SetDatasetType(dtype)
				self.set_description('datasetType',dtype)

    def add_simulation_category(self, cat): 
		self.simulation_category_menu.insert_text(1,cat)
		self.simulation_category_menu.set_active(1)

    def make_simulation_category(self,cat): 
        addsimcatwindow = GtkAddSimCat(self)


    def set_dif_param(self,combobox): 
		model = combobox.get_model()
		index = combobox.get_active()
		if index: 
			self.dif.SetParameters(model[index][0])
