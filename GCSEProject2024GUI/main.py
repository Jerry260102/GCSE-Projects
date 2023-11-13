# Some bullshit
# Customers TAble [Customer ID, First Name, Last Name, Address, Post Code, Name on card, Card Number, CVV, Expiry Date]
import csv
import os.path
from typing import Union
from typing import Callable

import CTkMessagebox
import customtkinter as ctk

chocflav = [
    "Caramel Twist", "Orange Crush", "Chocolate Bar", "Brazil Nut in Chocolate", "Cornish Fudge", "Strawberry Treat",
    "Orange Smoothie", "Toffee Bar", "Hazelnut Triangle", "Coconut Dream"
]
customersList = ["test"]


class Main(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wm_title(f"GCSE Project 2024")
        self.geometry("800x800")

        self._container = ctk.CTkFrame(self)
        self._container.pack(side="top", fill="both", expand=True)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        self._frames: dict[type, ctk.CTkFrame] = {}
        for F in (MainPage, OrderCreatorPage, CustomerCreatorPage):
            frame = F(self._container, self)
            self._frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont: type[ctk.CTkFrame]):
        frame = self._frames[cont]
        frame.tkraise()


class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.lbl = ctk.CTkLabel(self, text="Park Vale Chocolates", font=("Courier", 36))
        self.lbl.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        self.BTNordcreator = ctk.CTkButton(self, text="Order Creator",
                                           command=lambda: controller.show_frame(OrderCreatorPage))
        self.BTNordcreator.grid(row=1, column=1, pady=5)
        self.BTNcustcreator = ctk.CTkButton(self, text="Customer Creator",
                                            command=lambda: controller.show_frame(CustomerCreatorPage))
        self.BTNcustcreator.grid(row=2, column=1, pady=5)


class OrderCreatorPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        lastordid = 0
        msgcharge = "1.00"
        totalcharge = "20.00"
        self.label = ctk.CTkLabel(self, text="GCSE Project 2024", font=("Courier", 36))
        self.label.grid(column=1, row=0, columnspan=2, padx=10, pady=10)
        self.LBLid = ctk.CTkLabel(self, text="Order ID:", font=("Courier", 16))
        self.LBLid.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="e")
        self.ENTid = ctk.CTkEntry(self, placeholder_text=str(lastordid + 1))
        self.ENTid.configure(state="disabled")
        self.ENTid.grid(row=1, column=2, padx=(5, 0), pady=5, sticky="ew")
        self.LBLcustomer = ctk.CTkLabel(self, text="Customer:", font=("Courier", 16))
        self.LBLcustomer.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="e")
        self.CMBcustomer = ctk.CTkComboBox(self, values=customersList, font=("Courier", 16))
        self.CMBcustomer.grid(row=2, column=2, padx=(5, 0), pady=5, sticky="ew")
        self.BTNcustomer = ctk.CTkButton(
            self,
            text="New Customer",
            font=("Courier", 16),
            command=lambda: controller.show_frame(CustomerCreatorPage),
        )
        self.BTNcustomer.grid(row=2, column=3, padx=(5, 0), pady=5, sticky="w")
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
        self.LBLmessage = ctk.CTkLabel(self, text="Message:", font=("Courier", 16))
        self.LBLmessage.grid(row=4, column=1, padx=(0, 5), pady=5, sticky="en")
        self.TBXmessage = ctk.CTkTextbox(self, height=50)
        self.TBXmessage.grid(row=4, column=2, padx=(5, 0), pady=5, sticky="ew")
        self.LBLmessagecharge = ctk.CTkLabel(self, text=f"Message Charge: £{msgcharge}", font=("Courier", 24))
        self.LBLmessagecharge.grid(row=5, column=1, columnspan=2, pady=(5, 0), sticky="ew")
        self.LBLtotalcharge = ctk.CTkLabel(self, text=f"Total Charge: £{totalcharge}", font=("Courier", 32))
        self.LBLtotalcharge.grid(row=6, column=1, columnspan=2, sticky="ew")
        self.BTNsave = ctk.CTkButton(self, text="Save", font=("Courier", 16))
        self.BTNsave.grid(row=7, column=1, columnspan=2)


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
            self.ENTid.insert(0, int(r.read())+1)
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
        self.BTNaddcustomer.grid(row=10, column=1, columnspan=2)

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
                self.ENTid.delete(0,len(self.ENTid.get())-1)
                self.ENTid.insert(0, int(r.read()) + 1)
                self.ENTid.configure(state="disabled")
                self.ENTfname.delete(0,len(self.ENTfname.get())-1)
                self.ENTlname.delete(0,len(self.ENTlname.get())-1)
                for i in range(4):
                    self.ENTSaddress[i].delete(0,len(self.ENTSaddress[i].get())-1)
                self.ENTphonenumber.delete(2,len(self.ENTphonenumber.get())-1)

            controller.show_frame(MainPage)
        else:
            CTkMessagebox.CTkMessagebox(title="Error!", message="Phone Number is incorrect", icon="cancel")


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
                "Message"])
    if not os.path.isfile("CustomerData.csv"):
        with open("CustomerData.csv", "w", newline='') as a:
            customerWriter = csv.writer(a, delimiter=",")
            customerWriter.writerow(
                ["CustomerID", "FirstName", "LastName", "AddressLine1", "AddressLine2", "AddressLine3", "AddressLine4",
                 "PhoneNumber"])
    if not os.path.isfile("lastCustomerID.txt"):
        with open("lastCustomerID.txt", "w", newline='') as a:
            a.write("0")
    root = Main()
    root.mainloop()
