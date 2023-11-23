# Some bullshit
# Customers TAble [Customer ID, First Name, Last Name, Address, Post Code, Name on card, Card Number, CVV, Expiry Date]
import csv
import os.path
import string
from datetime import datetime
from typing import Union
from typing import Callable

import CTkMessagebox
import customtkinter as ctk
from CTkListbox import *
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
tempcust=""
chocflav = [
    "Caramel Twist", "Orange Crush", "Chocolate Bar", "Brazil Nut in Chocolate", "Cornish Fudge", "Strawberry Treat",
    "Orange Smoothie", "Toffee Bar", "Hazelnut Triangle", "Coconut Dream"
]
customersList = [[]]
customersListCMB = []


# Main Window
class Main(ctk.CTk):
    # Initialise the main window
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the title and size of the window
        self.wm_title(f"GCSE Project 2024")
        self.geometry("800x800")

        self._container = ctk.CTkFrame(self)
        self._container.pack(side="top", fill="both", expand=True)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)
        # Create a dictionary of frames
        self._frames: dict[type, ctk.CTkFrame] = {}
        for F in (MainPage, OrderCreatorPage, CustomerCreatorPage, FindDisplayPage, OrderDisplayPage):
            frame = F(self._container, self)
            self._frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    # Show frame of given function
    def show_frame(self, cont: type[ctk.CTkFrame]):
        frame = self._frames[cont]
        frame.tkraise()


# Main Page
class MainPage(ctk.CTkFrame):
    # Initialise the main page
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        # configure main page
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")
        # Create the widgets
        self.lbl = ctk.CTkLabel(self, text="Park Vale Chocolates", font=("Courier", 36))
        self.lbl.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        self.BTNordcreator = ctk.CTkButton(self, text="Order Creator",
                                           command=lambda: controller.show_frame(OrderCreatorPage))
        self.BTNordcreator.grid(row=1, column=1, pady=5)
        self.BTNcustcreator = ctk.CTkButton(self, text="Customer Creator",
                                            command=lambda: controller.show_frame(CustomerCreatorPage))
        self.BTNcustcreator.grid(row=2, column=1, pady=5)
        self.BTNfinddisplay = ctk.CTkButton(self, text="Find Customer & Display Orders",
                                            command=lambda: controller.show_frame(FindDisplayPage))
        self.BTNfinddisplay.grid(row=3, column=1, pady=5)


# Order Creator Page
class OrderCreatorPage(ctk.CTkFrame):
    # Initialise the order creator page
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        # configure order creator page
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        # Create the widgets
        self.label = ctk.CTkLabel(self, text="GCSE Project 2024", font=("Courier", 36))
        self.label.grid(column=1, row=0, columnspan=2, padx=10, pady=10)
        self.LBLid = ctk.CTkLabel(self, text="Order ID:", font=("Courier", 16))
        self.LBLid.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="e")
        self.ENTid = ctk.CTkEntry(self)
        # Read the last order ID from the file and add 1 to it and set the ID to that
        with open("lastOrderID.txt", "r") as r:
            self.ENTid.insert(0, int(r.read()) + 1)
        self.ENTid.configure(state="disabled")
        self.ENTid.grid(row=1, column=2, padx=(5, 0), pady=5, sticky="ew")
        self.LBLcustomer = ctk.CTkLabel(self, text="Customer:", font=("Courier", 16))
        self.LBLcustomer.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="e")
        # Create a list of customers and add them to a combo box
        for rowa in customersList:
            if "CustomerID" in rowa:
                continue
            print(rowa)
            customersListCMB.append(f"{rowa[0]}: {rowa[1]} {rowa[2]}")
            print(customersListCMB)
        self.CMBcustomer = ctk.CTkComboBox(self, values=customersListCMB, font=("Courier", 16))
        self.CMBcustomer.grid(row=2, column=2, padx=(5, 0), pady=5, sticky="ew")
        # Buttonto refresh the combo box
        self.BTNcmbrefresh = ctk.CTkButton(self, text="Refresh", font=("Courier", 16),
                                           command=lambda: self.CMBcustomer.configure(values=customersListCMB))
        self.BTNcmbrefresh.grid(row=2, column=3, padx=(5, 0), pady=5, sticky="w")
        # Button to create a new customer
        self.BTNcustomer = ctk.CTkButton(
            self,
            text="New Customer",
            font=("Courier", 16),
            command=lambda: controller.show_frame(CustomerCreatorPage),
        )
        self.BTNcustomer.grid(row=1, column=3, padx=(5, 0), pady=5, sticky="w")
        # Create the widgets for the chocolate flavours
        self.LBLSflavs = []
        self.SBXSflavs = []
        i = 0
        self.FRMchocflavs = ctk.CTkFrame(self)
        self.FRMchocflavs.grid_columnconfigure((0, 1), weight=1, uniform="a")
        self.LBLchocflavs = ctk.CTkLabel(self.FRMchocflavs, text="Chocolate Flavours", font=("Courier", 24))
        self.LBLchocflavs.grid(row=0, column=0, columnspan=2)
        for flav in chocflav:
            self.LBLSflavs.append(ctk.CTkLabel(self.FRMchocflavs, text=f"{flav}:", font=("Courier", 14)))
            self.LBLSflavs[i].grid(row=i + 1, column=0, padx=(0, 5), pady=5, sticky="e")
            self.SBXSflavs.append(Spinbox(self.FRMchocflavs, width=150, step_size=100))
            self.SBXSflavs[i].grid(row=i + 1, column=1, padx=(5, 10), pady=(0, 10), sticky="ew")
            i += 1
        self.FRMchocflavs.grid(row=3, column=1, columnspan=2, sticky="nsew")
        # Widgets for the message
        self.LBLmessage = ctk.CTkLabel(self, text="Message:", font=("Courier", 16))
        self.LBLmessage.grid(row=4, column=1, padx=(0, 5), pady=5, sticky="en")
        self.TBXmessage = ctk.CTkTextbox(self, height=50)
        self.TBXmessage.grid(row=4, column=2, padx=(5, 0), pady=5, sticky="ew")
        self.BTNcalcmessage = ctk.CTkButton(self, text="Calculate Prices", font=("Courier", 16), command=self.Calculate)
        self.BTNcalcmessage.grid(row=4, column=3, padx=(5, 0), pady=5, sticky="w")
        # Show the message price
        self.LBLmessagecharge = ctk.CTkLabel(self, text=f"Message Charge: £{'{:.2f}'.format(0.0)}",
                                             font=("Courier", 24))
        self.LBLmessagecharge.grid(row=5, column=1, columnspan=2, pady=(5, 0), sticky="ew")
        # Show the total price
        self.LBLtotalcharge = ctk.CTkLabel(self, text=f"Total Charge: £{'{:.2f}'.format(0.0)}", font=("Courier", 32))
        self.LBLtotalcharge.grid(row=6, column=1, columnspan=2, sticky="ew")
        self.BTNsave = ctk.CTkButton(self, text="Save", font=("Courier", 16), command=self.AddOrder)
        self.BTNsave.grid(row=7, column=2, padx=10, pady=10, sticky="nsew")
        self.BTNback = ctk.CTkButton(self, text="Back", font=("Courier", 16),
                                     command=lambda: controller.show_frame(MainPage))
        self.BTNback.grid(row=7, column=1, padx=10, pady=10, sticky="nsew")

    def Calculate(self):
        textlength = len(self.TBXmessage.get("1.0", "end-1c"))
        price = textlength * 0.10
        self.LBLmessagecharge.configure(text=f"Message Charge: £{'{:.2f}'.format(price)}")
        total = price + 9.99 + 4.99
        self.LBLtotalcharge.configure(text=f"Total Charge: £{'{:.2f}'.format(total)}")

    def AddOrder(self):
        if self.CMBcustomer.get() == "":
            CTkMessagebox.CTkMessagebox(title="Error!", message="Please select a customer", icon="cancel")
            return
        totalWeight = 0
        for i in range(10):
            totalWeight += self.SBXSflavs[i].get()
        if totalWeight != 1000:
            CTkMessagebox.CTkMessagebox(title="Error!", message="Total weight must be 1000g (1KG)", icon="cancel")
            return
        with open("lastCustomerID.txt", "w", newline='') as a:
            a.write(self.ENTid.get())
        OrderData = [
            self.ENTid.get(), self.CMBcustomer.get().split(":")[0]
        ]
        for i in range(10):
            OrderData.append(self.SBXSflavs[i].get())
        OrderData.append(self.TBXmessage.get("1.0", "end-1c"))
        OrderData.append(self.LBLmessagecharge.cget("text")[:self.LBLmessagecharge.cget("text").index("£")])
        OrderData.append(self.LBLtotalcharge.cget("text")[:self.LBLmessagecharge.cget("text").index("£")])
        OrderData.append(datetime.now().strftime("%d/%m/%Y"))
        with open("OrderData.csv", "a", newline='') as orderFile:
            orderWritera = csv.writer(orderFile, delimiter=",")
            orderWritera.writerow(OrderData)
        with open("lastOrderID.txt", "r") as r:
            self.ENTid.configure(state="normal")
            self.ENTid.delete(0, len(self.ENTid.get()) - 1)
            self.ENTid.insert(0, int(r.read()) + 1)
            self.ENTid.configure(state="disabled")
            self.CMBcustomer.set("")
            for i in range(10):
                self.SBXSflavs[i].set(0)
            self.TBXmessage.delete("1.0", "end-1c")
            self.LBLmessagecharge.configure(text=f"Message Charge: £{'{:.2f}'.format(0.0)}")
            self.LBLtotalcharge.configure(text=f"Total Charge: £{'{:.2f}'.format(0.0)}")


class CustomerCreatorPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.label = ctk.CTkLabel(self, text="Customer Creator", font=("Courier", 36))
        self.label.grid(column=1, row=0, columnspan=2, padx=10, pady=10)
        self.LBLid = ctk.CTkLabel(self, text="Customer ID:")
        self.LBLid.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="e")
        self.ENTid = ctk.CTkEntry(self)
        with open("lastCustomerID.txt", "r") as r:
            self.ENTid.insert(0, int(r.read()) + 1)
        self.ENTid.configure(state="disabled")
        self.ENTid.grid(row=1, column=2, padx=(5, 0), pady=5, sticky="ew")
        self.LBLfname = ctk.CTkLabel(self, text="First Name:")
        self.LBLfname.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="e")
        self.ENTfname = ctk.CTkEntry(self)
        self.ENTfname.grid(row=2, column=2, padx=(5, 0), pady=5, sticky="ew")
        self.LBLlname = ctk.CTkLabel(self, text="Last Name:")
        self.LBLlname.grid(row=3, column=1, padx=(0, 5), pady=5, sticky="e")
        self.ENTlname = ctk.CTkEntry(self)
        self.ENTlname.grid(row=3, column=2, padx=(5, 0), pady=5, sticky="ew")
        self.LBLSaddress = []
        self.ENTSaddress = []
        i = 1
        while i < 5:
            self.LBLSaddress.append(ctk.CTkLabel(self, text=f"Address Line {i}:"))
            self.LBLSaddress[i - 1].grid(row=i + 3, column=1, padx=(0, 5), sticky="e")
            self.ENTSaddress.append(ctk.CTkEntry(self))
            self.ENTSaddress[i - 1].grid(row=i + 3, column=2, padx=(5, 0), sticky="ew")
            i += 1
        self.LBLphonenumber = ctk.CTkLabel(self, text="Mobile Number:")
        self.LBLphonenumber.grid(row=8, column=1, padx=(0, 5), sticky="e")
        self.ENTphonenumber = ctk.CTkEntry(self)
        self.ENTphonenumber.insert(0, "07")
        self.ENTphonenumber.grid(row=8, column=2, padx=(5, 0), sticky="ew")
        self.BTNaddcustomer = ctk.CTkButton(self, text="Add Customer", command=lambda: self.addCustomer(controller))
        self.BTNaddcustomer.grid(row=10, column=2, padx=10, pady=10, sticky="nsew")
        self.BTNback = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(MainPage))
        self.BTNback.grid(row=10, column=1, padx=10, pady=10, sticky="nsew")

    def addCustomer(self, controller):
        print(self.ENTphonenumber.get()[0:2])
        print(self.ENTphonenumber.get().isdigit())
        print(len(self.ENTphonenumber.get()))
        if self.ENTphonenumber.get()[0:2] == "07" and self.ENTphonenumber.get().isdigit() and len(
                self.ENTphonenumber.get()) == 11:
            customerData = [
                self.ENTid.get(), self.ENTfname.get(), self.ENTlname.get(),
                self.ENTSaddress[0].get(),
                self.ENTSaddress[1].get(), self.ENTSaddress[2].get(), self.ENTSaddress[3].get(),
                self.ENTphonenumber.get()
            ]
            with open("lastCustomerID.txt", "w", newline='') as a:
                a.write(self.ENTid.get())
            with open("CustomerData.csv", "a", newline='') as customerFile:
                customerWriter = csv.writer(customerFile, delimiter=",")
                customerWriter.writerow(customerData)
            with open("lastCustomerID.txt", "r") as r:
                self.ENTid.configure(state="normal")
                self.ENTid.delete(0, len(self.ENTid.get()) - 1)
                self.ENTid.insert(0, int(r.read()) + 1)
                self.ENTid.configure(state="disabled")
                self.ENTfname.delete(0, len(self.ENTfname.get()) - 1)
                self.ENTlname.delete(0, len(self.ENTlname.get()) - 1)
                for i in range(4):
                    self.ENTSaddress[i].delete(0, len(self.ENTSaddress[i].get()) - 1)
                self.ENTphonenumber.delete(2, len(self.ENTphonenumber.get()) - 1)

            controller.show_frame(MainPage)
            customersList.clear()
            with open("CustomerData.csv", "r") as customerFileb:
                customerRead = csv.reader(customerFileb, delimiter=",")
                for rowb in customerRead:
                    customersList.append(rowb)
        else:
            CTkMessagebox.CTkMessagebox(title="Error!", message="Phone Number is incorrect", icon="cancel")


class FindDisplayPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.label = ctk.CTkLabel(self, text="Find Customer & Display Orders", font=("Courier", 36))
        self.label.grid(column=1, row=0, columnspan=2, padx=10, pady=10)
        self.LBXcustomers = CTkListbox(self)
        self.LBXcustomers.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.fillListBox()
        self.BTNshoworders = ctk.CTkButton(self, text="Show Orders", command=lambda: self.showOrders(controller))
        self.BTNshoworders.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        self.BTNback = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(MainPage))
        self.BTNback.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    def fillListBox(self):
        with open("CustomerData.csv", "r") as customerFile:
            customerReader = csv.reader(customerFile, delimiter=",")
            for row in customerReader:
                if "CustomerID" in row:
                    continue
                self.LBXcustomers.insert("end", f"{row[0]}: {row[1]} {row[2]}")

    def showOrders(self, controller):
        if self.LBXcustomers.get() == "":
            CTkMessagebox.CTkMessagebox(title="Error!", message="Please select a customer", icon="cancel")
            return
        with open("OrderData.csv", "r") as orderFile:
            orderReader = csv.reader(orderFile, delimiter=",")
            for row in orderReader:
                if "OrderID" in row:
                    continue
                if row[1] == self.LBXcustomers.get[:self.LBXcustomers.get().index(":")]:
                    global tempcust
                    tempcust=row[1]
                    controller.show_frame(OrderDisplayPage)

class OrderDisplayPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.label = ctk.CTkLabel(self, text=f"Display Orders for Customer {tempcust}", font=("Courier", 36))
        self.label.grid(column=1, row=0, columnspan=2, padx=10, pady=10)
        self.LBXorders = CTkListbox(self)
        self.LBXorders.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.fillListBox()
        self.BTNshowdetails = ctk.CTkButton(self, text="Show Details", command=self.showDetails)
        self.BTNback = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(FindDisplayPage))
        self.BTNback.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    def fillListBox(self):
        with open("OrderData.csv", "r") as orderFile:
            orderReader = csv.reader(orderFile, delimiter=",")
            for row in orderReader:
                if "OrderID" in row:
                    continue
                if row[1] == tempcust:
                    self.LBXorders.insert("end", f"{row[0]}: {row[15]}")

    def showDetails(self):
        if self.LBXorders.get("active") == "":
            CTkMessagebox.CTkMessagebox(title="Error!", message="Please select an order", icon="cancel")
            return
        with open("OrderData.csv", "r") as orderFile:
            orderReader = csv.reader(orderFile, delimiter=",")
            for row in orderReader:
                if "OrderID" in row:
                    continue
                if row[0] == self.LBXorders.get()[:self.LBXorders.get().index(":")]:
                    msg = CTkMessagebox.CTkMessagebox(title=f"Order {row[0]}",
                                                message=f"Customer ID: {row[1]}\nCaramel Twist: {row[2]}\nOrange Crush: {row[3]}\nChocolate Bar: {row[4]}\nBrazil Nut in Chocolate: {row[5]}\nCornish Fudge: {row[6]}\nStrawberry Treat: {row[7]}\nOrange Smoothie: {row[8]}\nToffee Bar: {row[9]}\nHazelnut Triangle: {row[10]}\nCoconut Dream: {row[11]}\nMessage: {row[12]}\nMessage Price: {row[13]}\nTotal Price: {row[14]}\nOrder Date: {row[15]}",
                                                icon="info", option_1="Generate Invoice", option_2="Back")
                    response = msg.get()
                    if response == "Generate Invoice":
                        self.generateInvoice(row)
                    elif response == "Back":
                        return


    def generateInvoice(self, row):
        return
class Spinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 start: int = 0,
                 min: int = 0,
                 max: int = 500,
                 step_size: Union[int, int] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.min = min
        self.max = max
        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                             command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0,
                                  font=("Courier", 16))
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="+", width=height - 6, height=height - 6,
                                        command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.insert(0, f"{start}g")
        self.entry.configure(state="disabled")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            if int(self.entry.get()[:-1]) < self.max:
                value = int(self.entry.get()[:-1]) + self.step_size
            else:
                value = self.entry.get()[:-1]
            self.entry.configure(state="normal")
            self.entry.delete(0, "end")
            self.entry.insert(0, f"{value}g")
            self.entry.configure(state="disabled")
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            if int(self.entry.get()[:-1]) > self.min:
                value = int(self.entry.get()[:-1]) - self.step_size
            else:
                value = self.entry.get()[:-1]
            self.entry.configure(state="normal")
            self.entry.delete(0, "end")
            self.entry.insert(0, f"{value}g")
            self.entry.configure(state="disabled")
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get()[:-1])
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.insert(0, str(f"{int(value)}g"))
        self.entry.configure(state="disabled")


if __name__ == "__main__":
    if not os.path.isfile("OrderData.csv"):
        with open("OrderData.csv", "w", newline='') as a:
            orderWriter = csv.writer(a, delimiter=",")
            orderWriter.writerow([
                "OrderID", "CustomerID", "CaramelTwist", "OrangeCrush", "ChcolateBar", "BrazilNutinChocolate",
                "CornishFudge", "StrawberryTreat", "OrangeSmoothie", "ToffeeBar", "HazelnutTriangle", "CoconutDream",
                "Message", "MessagePrice", "TotalPrice", "OrderDate"])
    if not os.path.isfile("CustomerData.csv"):
        with open("CustomerData.csv", "w", newline='') as a:
            customerWriter = csv.writer(a, delimiter=",")
            customerWriter.writerow(
                ["CustomerID", "FirstName", "LastName", "AddressLine1", "AddressLine2", "AddressLine3", "AddressLine4",
                 "PhoneNumber"])
    if not os.path.isfile("lastCustomerID.txt"):
        with open("lastCustomerID.txt", "w", newline='') as a:
            a.write("0")
    if not os.path.isfile("lastOrderID.txt"):
        with open("lastOrderID.txt", "w", newline='') as a:
            a.write("0")
    with open("CustomerData.csv", "r") as customerFilea:
        customerReader = csv.reader(customerFilea, delimiter=",")
        customersList.clear()
        for row in customerReader:
            customersList.append(row)

    root = Main()
    root.mainloop()
