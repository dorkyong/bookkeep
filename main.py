from tkinter import *
from inv import InvData
from employee import EmployeeData

inv = InvData('inventory.db')
emp = EmployeeData('employee.db')

cash = 100000
accounts_receivable = 20000
inventory = inv.sum()[0]
total_asset = cash + accounts_receivable + inventory
accounts_payable = 0
mortgage = 100000
total_liability = accounts_payable + mortgage
networth = total_asset - total_liability

sales = 0
purchase = 0
payroll = emp.sum()[0]
payroll_withholding = 0.062*payroll
bills = 4500
total_expenses = payroll + bills + purchase
tax = 0.12*(sales-total_expenses)
net_income = sales - total_expenses - tax

year = 2022
month = 1

def show_inv():
    list.delete(0, END)
    for row in inv.fetch():
        list.insert(END, row)

def show_emp():
    list.delete(0, END)
    for row in emp.fetch():
        list.insert(END, row)

def add_inv():
    # TODO if text = ''
    try:
        a = float(purchase_price_text.get())
        b = int(purchase_quantity_text.get())
        c = float(purchase_price_text.get())
        d = float(purchase_quantity_text.get())
        t = c*d
    except ValueError:
        print("price must be a FLOAT, quantity must be an INTEGER.")
    inv.insert(purchase_customer_text.get(), purchase_part_text.get(), a, b, t)
    calc()
    update()
    show_inv()

def add_emp():
    # TODO if text = ''
    emp.insert(pay_name_text.get(), pay_amount_text.get())
    calc()
    update()
    show_emp()

def select_item(event):
    try:
        global selected_item
        index = list.curselection()[0]
        selected_item = list.get(index)

        # sale_customer_entry.delete(0, END)
        # sale_customer_entry.insert(END, selected_item[1])
        sale_part_entry.delete(0, END)
        sale_part_entry.insert(END, selected_item[2])
        sale_price_entry.delete(0, END)
        sale_price_entry.insert(END, selected_item[3])
        sale_quantity_entry.delete(0, END)
        sale_quantity_entry.insert(END, selected_item[4])
    except IndexError:
        pass

def remove_inv():
    a = int(sale_quantity_text.get())
    b = int(selected_item[4])
    c = b-a
    if c < 0:
        print("not enough inventory")
    if c==0:
        inv.remove(selected_item[0])
    else:
        t = selected_item[3]*c
        inv.update(selected_item[0], selected_item[1], selected_item[2], selected_item[3], c, t)
    calc()
    show_inv()

def buy():
    global accounts_payable
    global inventory
    global purchase
    try:
        a = float(purchase_price_text.get())
        b = float(purchase_quantity_text.get())
        c = a*b
    except ValueError:
        print("Please type in a valid number.")
    add_inv()
    accounts_payable = accounts_payable + c
    purchase = purchase + c

    calc()
    update()

def pay():
    try:
        a = float(pay_amount_text.get())
    except ValueError:
        print("Please type in a valid number.")
    add_emp()
    update()

def sell():
    global accounts_receivable
    global inventory
    global sales
    try:
        a = float(sale_price_text.get())
        b = float(sale_quantity_text.get())
        ad = a*b
    except ValueError:
        print("Please type in a valid number.")
    accounts_receivable = accounts_receivable + ad
    remove_inv()
    sales = sales + ad

    calc()
    update()

def next():
    global cash
    global accounts_receivable
    global accounts_payable
    global sales
    global purchase
    global payroll
    global month
    global year
    global net_income

    cash = cash + accounts_receivable - accounts_payable

    accounts_receivable = 0
    accounts_payable = 0

    sales = 0
    purchase = 0
    payroll = emp.sum()[0]

    month = month + 1
    if month > 12:
        month = 1
        year = year + 1
    calc()
    update()


def update():
    cash_entry.config(text = str(cash))
    accounts_receivable_entry.config(text=str(accounts_receivable))
    inventory_entry.config(text=str(inventory))
    total_asset_entry.config(text=str(total_asset))
    accounts_payable_entry.config(text=str(accounts_payable))
    mortgage_entry.config(text=str(mortgage))
    total_liability_entry.config(text=str(total_liability))
    networth_entry.config(text=str(networth))

    sales_entry.config(text=str(sales))
    purchase_entry.config(text=str(purchase))
    payroll_entry.config(text=str(payroll))
    payroll_withholding_entry.config(text=str(payroll_withholding))
    bills_entry.config(text=str(bills))
    total_expenses_entry.config(text=str(total_expenses))
    tax_entry.config(text=str(tax))
    net_income_entry.config(text=str(net_income))

    date_entry.config(text = str(month) + '/1/' + str(year))

def calc():
    global cash
    global accounts_receivable
    global inventory
    global mortgage
    global payroll
    global payroll_withholding
    global sales
    global total_asset
    global total_liability
    global networth
    global payroll_withholding
    global total_expenses
    global tax
    global net_income
    global purchase
    global bills
    global accounts_payable

    accounts_receivable = sales

    inventory = inv.sum()[0]
    total_asset = cash + accounts_receivable + inventory
    total_liability = accounts_payable + mortgage
    networth = total_asset - total_liability
    payroll = emp.sum()[0]
    payroll_withholding = 0.062 * payroll
    total_expenses = payroll + bills + purchase
    accounts_payable = total_expenses
    tax = 0.12*(sales-total_expenses)
    if tax < 0:
        tax = 0
    net_income = sales - total_expenses - tax


# Interface
# Create a window
app = Tk()
calc()

app.title('TE566')
app.geometry('1400x1200')

# BalanceSheet
BS_label = Label(app, text='Balance Sheet', font=('bold',20), pady=20)
BS_label.grid(row=0, column=0, sticky=W) # sticky W aligns

# Cash
cash_label = Label(app, text='Cash', font=(16))
cash_label.grid(row=1, column=0, sticky=W) # sticky W aligns
cash_entry = Label(app, text=str(cash), font=(16))
cash_entry.grid(row=1, column=1)

# Account Receivable
accounts_receivable_label = Label(app, text='Account Receivable', font=(16))
accounts_receivable_label.grid(row=2, column=0, sticky=W) # sticky W aligns
accounts_receivable_entry = Label(app, text=str(accounts_receivable), font=(16))
accounts_receivable_entry.grid(row=2, column=1)

# Inventory
inventory_label = Label(app, text='Inventory', font=(16))
inventory_label.grid(row=3, column=0, sticky=W) # sticky W aligns
inventory_entry = Label(app, text=str(inventory), font=(16))
inventory_entry.grid(row=3, column=1)

# Total Asset
total_asset_label = Label(app, text='Total Asset', font=('bold',16))
total_asset_label.grid(row=4, column=0, sticky=W) # sticky W aligns
total_asset_entry = Label(app, text=str(total_asset), font=(16))
total_asset_entry.grid(row=4, column=1)

# Account Payable
accounts_payable_label = Label(app, text='Account Payable', font=(16))
accounts_payable_label.grid(row=5, column=0, sticky=W) # sticky W aligns
accounts_payable_entry = Label(app, text=str(accounts_payable), font=(16))
accounts_payable_entry.grid(row=5, column=1)

# Mortgage
mortgage_label = Label(app, text='Mortgage', font=(16))
mortgage_label.grid(row=6, column=0, sticky=W) # sticky W aligns
mortgage_entry = Label(app, text=str(mortgage), font=(16))
mortgage_entry.grid(row=6, column=1)

# Total Liabilities
total_liability_label = Label(app, text='Total Liabilities', font=('bold',16))
total_liability_label.grid(row=7, column=0, sticky=W) # sticky W aligns
total_liability_entry = Label(app, text=str(total_liability), font=(16))
total_liability_entry.grid(row=7, column=1)

# Net Worth
networth_label = Label(app, text='Net Worth', font=('bold', 18), pady=20)
networth_label.grid(row=8, column=0, sticky=W) # sticky W aligns
networth_entry = Label(app, text=str(networth), font=(16))
networth_entry.grid(row=8, column=1)

# Income Statement
IS_label = Label(app, text='Income Statement', font=('bold',20), pady=20)
IS_label.grid(row=0, column=2, sticky=W) # sticky W aligns

# Sales
sales_label = Label(app, text='Sales', font=(16))
sales_label.grid(row=1, column=2, sticky=W) # sticky W aligns
sales_entry = Label(app, text=str(sales), font=(16))
sales_entry.grid(row=1, column=3)

# Purchase
purchase_label = Label(app, text='Purchase', font=(16))
purchase_label.grid(row=2, column=2, sticky=W) # sticky W aligns
purchase_entry = Label(app, text=str(purchase), font=(16))
purchase_entry.grid(row=2, column=3)

# Payroll
payroll_label = Label(app, text='Payroll', font=(16))
payroll_label.grid(row=3, column=2, sticky=W) # sticky W aligns
payroll_entry = Label(app, text=str(payroll), font=(16))
payroll_entry.grid(row=3, column=3)

# Payroll withholding
payroll_withholding_label = Label(app, text='Payroll Withholding', font=(16))
payroll_withholding_label.grid(row=4, column=2, sticky=W) # sticky W aligns
payroll_withholding_entry = Label(app, text=str(payroll_withholding), font=(16))
payroll_withholding_entry.grid(row=4, column=3)

# Bills
bills_label = Label(app, text='Bills', font=(16))
bills_label.grid(row=5, column=2, sticky=W) # sticky W aligns
bills_entry = Label(app, text=str(bills), font=(16))
bills_entry.grid(row=5, column=3)

# Total Expenses
total_expenses_label = Label(app, text='Total Expenses', font=('bold', 16))
total_expenses_label.grid(row=6, column=2, sticky=W) # sticky W aligns
total_expenses_entry = Label(app, text=str(total_expenses), font=(16))
total_expenses_entry.grid(row=6, column=3)

# Taxes
tax_label = Label(app, text='Tax', font=(16))
tax_label.grid(row=7, column=2, sticky=W) # sticky W aligns
tax_entry = Label(app, text=str(tax), font=(16))
tax_entry.grid(row=7, column=3)

# Net Income
net_income_label = Label(app, text='Net Income', font=('bold', 18), pady=20)
net_income_label.grid(row=8, column=2, sticky=W) # sticky W aligns
net_income_entry = Label(app, text=str(net_income), font=(16))
net_income_entry.grid(row=8, column=3)

# Date
date_label = Label(app, text='Date: ', font=('bold', 18), pady=20)
date_label.grid(row=9, column=0, sticky=W) # sticky W aligns
date_entry = Label(app, text= str(month) + '/1/' + str(year), font=(16))
date_entry.grid(row=9, column=1)


# Purchase Order
purchase_btn = Button(app, text='Purchase Order', width=12, command=buy)
purchase_btn.grid(row=10, column=0, pady=20)
purchase_customer_text = StringVar()
purchase_customer_label = Label(app, text='Vendor: ', font=(12), pady=20)
purchase_customer_label.grid(row=10, column=1)
purchase_customer_entry = Entry(app, textvariable = purchase_customer_text)
purchase_customer_entry.grid(row=10, column=2)
purchase_part_text = StringVar()
purchase_part_label = Label(app, text='Part: ', font=(12), pady=20)
purchase_part_label.grid(row=10, column=3)
purchase_part_entry = Entry(app, textvariable = purchase_part_text)
purchase_part_entry.grid(row=10, column=4)
purchase_price_text = StringVar()
purchase_price_label = Label(app, text='Price/unit: ', font=(12), pady=20)
purchase_price_label.grid(row=10, column=5)
purchase_price_entry = Entry(app, textvariable = purchase_price_text)
purchase_price_entry.grid(row=10, column=6)
purchase_quantity_text = StringVar()
purchase_quantity_label = Label(app, text='Quantity: ', font=(12), pady=20)
purchase_quantity_label.grid(row=10, column=7)
purchase_quantity_entry = Entry(app, textvariable = purchase_quantity_text)
purchase_quantity_entry.grid(row=10, column=8)

# Create Invoice
sale_btn = Button(app, text='Create Invoice', width=12, command=sell)
sale_btn.grid(row=11, column=0, pady=20)
sale_customer_text = StringVar()
sale_customer_label = Label(app, text='Customer: ', font=(12), pady=20)
sale_customer_label.grid(row=11, column=1)
sale_customer_entry = Entry(app, textvariable = sale_customer_text)
sale_customer_entry.grid(row=11, column=2)
sale_part_text = StringVar()
sale_part_label = Label(app, text='Product: ', font=(12), pady=20)
sale_part_label.grid(row=11, column=3)
sale_part_entry = Entry(app, textvariable = sale_part_text)
sale_part_entry.grid(row=11, column=4)
sale_price_text = StringVar()
sale_price_label = Label(app, text='Price/unit: ', font=(12), pady=20)
sale_price_label.grid(row=11, column=5)
sale_price_entry = Entry(app, textvariable = sale_price_text)
sale_price_entry.grid(row=11, column=6)
sale_quantity_text = StringVar()
sale_quantity_label = Label(app, text='Quantity: ', font=(12), pady=20)
sale_quantity_label.grid(row=11, column=7)
sale_quantity_entry = Entry(app, textvariable = sale_quantity_text)
sale_quantity_entry.grid(row=11, column=8)

# Pay Employee
pay_btn = Button(app, text='Pay Employee', width=12, command=pay)
pay_btn.grid(row=12, column=0, pady=20)
pay_name_text = StringVar()
pay_name_label = Label(app, text='Name: ', font=(12), pady=20)
pay_name_label.grid(row=12, column=1)
pay_name_entry = Entry(app, textvariable = pay_name_text)
pay_name_entry.grid(row=12, column=2)
pay_amount_text = StringVar()
pay_amount_label = Label(app, text='Amount: ', font=(12), pady=20)
pay_amount_label.grid(row=12, column=3)
pay_amount_entry = Entry(app, textvariable = pay_amount_text)
pay_amount_entry.grid(row=12, column=4)

next_btn = Button(app, text='Next Cycle', width=12, command=next)
next_btn.grid(row=15, column=0, pady=20)

# List (Listbox)
list = Listbox(app, height=20, width=100, border=0)
list.grid(row=17, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=17, column=3)
# Set scroll to listbox
list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=list.yview)
# Bind select
list.bind('<<ListboxSelect>>', select_item)

inv_btn = Button(app, text='Show Inventory', width=12, command=show_inv)
inv_btn.grid(row=24, column=0, pady=20)
inv_btn = Button(app, text='Show Employees', width=12, command=show_emp)
inv_btn.grid(row=24, column=1)
#
# add_btn = Button(app, text='Next Cycle', width=12, command=next)
# add_btn.grid(row=13, column=0, pady=20)

# remove_btn = Button(app, text='Remove Part', width=12, command=remove_item)
# remove_btn.grid(row=2, column=1)
#
# update_btn = Button(app, text='Update Part', width=12, command=update_item)
# update_btn.grid(row=2, column=2)


# Start program
app.mainloop()
