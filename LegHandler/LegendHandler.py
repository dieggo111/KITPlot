######################
### Legend methods ###
######################


    def getLegendOrder(self):

        self.EntryPosition = []

        for Name in self.graphDetails:
            self.EntryPosition.append(Name.replace(" ","")[1])
        
        for Name in self.EntryPosition:
            if self.EntryPosition.count(Name) > 1:
                    sys.exit("Entry positions must have different values! At least two numbers are equal!")
            else:
                pass


    def changeOrder(self, counter):

        for j, number in enumerate(self.EntryPosition):
            
            if int(number) == counter:
                return int(j)
            else:
                pass

        return 0


    def setLegend(self):

        self.legend = ROOT.TLegend(self.LegendParameters[0],self.LegendParameters[1],self.LegendParameters[2],self.LegendParameters[3])
        self.legend.SetFillColor(0)

        
        if 0.02 <= self.legendTextSize <= 0.03:
            self.legend.SetTextSize(self.legendTextSize)
        else:
            sys.exit("Invalid legend text size! Need value between 0.02 and 0.03!")

        for i,graph in enumerate(self.__graphs):
            if self.legendEntry == "name":
                self.legend.AddEntry(self.__graphs[i], self.__files[i].getName(), "p")
            elif self.legendEntry == "ID" and self.__checkPID == True:
                self.legend.AddEntry(self.__graphs[i], self.__files[i].getID(), "p")
            elif self.legendEntry == "list" and self.cfg_exists == False:
                self.legend.AddEntry(self.__graphs[i], self.__files[i].getName(), "p")
            elif self.legendEntry == "list" and self.cfg_exists == True:
                self.legend.AddEntry(self.__graphs[self.changeOrder(i)], self.graphDetails[self.changeOrder(i)].replace(" ","")[3:], "p")
            else:
                print "Invalid entry! Using graph details"
                self.legend.AddEntry(self.__graphs[i], self.__files[i].getName(), "p")
                
 
        self.legend.Draw()
        self.canvas.Update()

        
    def setLegendParameters(self):
        # Evaluate Legend Position and write it into list [Lxmin, Lymin, Lxmax, Lymax]. Try top right, top left, bottom right or outside
        # Plot is arround 80% of canvas from (0.1,0.15) to (0.9,0.9). 
        
        self.LegendParameters = []
        para_height = 0
        para_width = 0
        self.TopRight = self.TopLeft = self.BottomRight = True
        
        # para_height contains the number of entries and determines the height of the legend box
        para_height = len(self.__files)

        # para_width contains the lenght of the longest entry
        for Name in self.graphDetails:
            if len(Name) > para_width:
                para_width = len(Name)
            else:
                pass

        # hold off some errors
        if para_width > 30:
                sys.exit("Legend name too long! Reduce the number of characters!")
        elif not 0.5 <= self.legendBoxPara <= 1.5:
            sys.exit("Invalid box parameter! Value must be between 0.5 and 1.5!")
        else:
            pass
        
        # magic_para .... it's magic!
        if self.legendTextSize == 0.02:
            magic_para = para_width/100.*self.legendBoxPara
        else:
            magic_para = para_width*0.0105*self.legendBoxPara
        
        
        if self.legendPosition != "auto" and self.legendPosition != "TR" and self.legendPosition != "TL" and self.legendPosition != "BR":
            sys.exit("Invalid legend position! Try 'auto', 'TR', 'TL' or 'BR'!")
        
        # Top right corner is the default/starting position for the legend box
        Lxmax = 0.98
        Lymax = 0.93
        Lxmin = Lxmax-magic_para
        Lymin = Lymax-para_height*0.04
            
            
        # Check if elements are in the top right corner. 
        for i in range(len(self.__files)):
            for j in range(len(self.__files[i].getX())):
                if abs(self.__files[i].getX()[j]/(self.xmax*(1.+self.perc)))-0.1 > Lxmin and self.legendPosition == "auto":
                    if abs(self.__files[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin:
                        self.TopRight = False
        
        if self.TopRight == False or self.legendPosition == "TL":
            Lxmin = 0.18
            Lymax = 0.88
            Lymin = Lymax-para_height*0.04
            Lxmax = Lxmin+magic_para*1.05

        # Check if elements are in the top left corner.
        for i in range(len(self.__files)):
            for j in range(len(self.__files[i].getX())):
                if Lxmin-0.1 < abs(self.__files[i].getX()[j]/(self.xmax*(1.+self.perc))) < Lxmax+0.05:
                    if abs(self.__files[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin+0.08 and self.legendPosition == "auto":
                        self.TopLeft = False
                
        if self.TopLeft == self.TopRight == False or self.legendPosition == "BR":
            Lxmax = 0.89
            Lymin = 0.18
            Lxmin = Lxmax-magic_para
            Lymax = Lymin+para_height*0.04
            
        # If the plot is too crowded, create more space on the right.
        for i in range(len(self.__files)):
            for j in range(len(self.__files[i].getX())):
                if abs(self.__files[i].getX()[j]/(self.xmax*(1.+self.perc))) > Lxmin:
                    if abs(self.__files[i].getY()[len(self.__files[i].getY())-1]/(self.ymax*(1.+self.perc))) < Lymax and self.legendPosition == "auto":
                        self.BottomRight = False
            
            
        if self.legendPosition == "TR" or self.BottomRight == self.TopLeft == self.TopRight == False:
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-magic_para
            Lymin = Lymax-para_height*0.04
            if self.BottomRight == self.TopLeft == self.TopRight == False:
                print "Couldn't find sufficient space!"
        
        self.LegendParameters.append(Lxmin)
        self.LegendParameters.append(Lymin)
        self.LegendParameters.append(Lxmax)
        self.LegendParameters.append(Lymax)
        
       
