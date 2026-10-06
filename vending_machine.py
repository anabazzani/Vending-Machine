
import os 
# vending machine menu 

accepted_coins=[1,2,0.5,0.20]   #to validate input, give change


items= {'water':{'price': 1.20,'stock':5},'soda': {'price':1.50,'stock':4} ,'chocolate':{'price':2.50,'stock':10},'crisps':{'price':1.40 ,'stock':6},'sandwich':{'price':3.80,'stock':8}}

# created a dictionary to access item,price,stock 

ORDER_COUNTER_FILE= 'last_order_txt'

def load_last_order():
    if os.path.exists(ORDER_COUNTER_FILE):
        with open(ORDER_COUNTER_FILE) as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    
    return 0

def save_last_order(order_number):
    with open(ORDER_COUNTER_FILE, 'w') as f:
        f.write(str(order_number))
    

def menu_vending_machine(items):
    print('-----BU vending machine----')
    print('Accepted coins: £2, £1, £0.50, £0.20\n')
    print("------------------------------")
    for item in items:
        name= item.capitalize()
        price= items[item]['price']
        stock=items[item]['stock']
        print(f"-{name:<12} £{price:<4} ({stock} in stock)")
    print('-----------------------')
        

"""take the dict of items loop through each item and print item,price and stock"""       

def adding_coins(wallet,coins):
    if coins in accepted_coins: #check if coin is valid
        wallet= wallet + coins  #takes previous balance, add new coin, return new balance
    else:
        print('invalid coins')
    return wallet

def inserting_coins(wallet): 
    while True:  # let the costumer put as many coins as he wants
        question= input("Insert coin or type 'done' to continue: ")
        if question.lower() =='done':
            break 
        try:
            coins= float(question)
            if coins in accepted_coins:
                wallet += coins 
                print(f'balance: £{wallet:.2f}')
            else:
                print('Invalid coin. accepted coins are: 1, 2, 0.5, 0.2')
        except ValueError: 
            print("Invalid input.Please insert a valid coin or type 'done'")
            
        # because always returns a string
        #update/add the balanc #need(balance,coins)- to call the function, return new result'''
    return wallet

def costumers_choice(wallet,items):
    purchased_items=[] # save what costumers buy 
    total_spent= 0
    while True:
        print(f'\nCurrent balance: £{wallet:.2f}')
        choice= input("Choose an item by name or type 'exit' to quit: ").lower().strip()
        if choice =='exit' or choice =='done':
            break #stop the loop
        if choice not in items: #verify if item exists
            print('item not available')
            continue
        if items[choice]['stock']<=0: #inside items open stock 
            print('Out of stock')
            continue
        price= items[choice]['price'] #verify if costumer has enought balance
        if wallet< price:
            print('Not enough balance')
            continue
        wallet= wallet - price #update new balance
        items[choice]['stock']-= 1
        purchased_items.append(choice)
        total_spent += price
        
        print(f"\nPurchased {choice} for £{price:.2f}.")
        print(f"Total spent: £{total_spent:.2f} (Discount applied: 0%)")
        print(f"Remaining balance: £{wallet:.2f}\n")
        
        print("----BU Vending Machine Menu----")
        counter=1
        for item in items:
            item_name= item.capitalize()
            item_price= items[item]['price']
            item_stock= items[item]['stock']
            print(f"{counter}.{item_name}- £{item_price} ({item_stock} in stock)")
            counter +=1 
            print("------------------------------------------------")
    return wallet, purchased_items

def total_purchased(purchased_items,items):
        total=0 
        for item in purchased_items:
            total+= items [item]['price'] #sum each item, returning total + quantity
        return total, len(purchased_items) 

def discount(total, number_of_items):
    discount_percent=0
    if number_of_items>=3:
        discount_percent= max(discount_percent,5)
    if total>5:
        discount_percent= max(discount_percent,10)
    if total>7:
        discount_percent= max(discount_percent,15)
    
    final_total= total - (total* discount_percent/100)
    return final_total, discount_percent
   


def bonus(total_bonus,order_number):
    bonus_quant= 0 #no bonus yet
    if order_number % 2!=0: #cheching if its odd number
        if total_bonus >2: #spent more than 2 pounds
            bonus_quant=1
            total_bonus+=1 #new bonus
    return total_bonus,bonus_quant


def calculate_change(change):
    change_list=[] #change that the vending will return
    coins=[2,1,0.5,0.2]
    for coin in coins:
        while round(change +1e-9,2) >= coin:
            change_list.append(coin)
            change=round(change - coin,2) #reduce the change left

    return change_list

def generate_csv(order_number, purchased_items,total,discount_percent,final_total,bonus_quant,total_after_bonus,change_list):

    filename= f'order_{order_number}.csv'
    with open(filename, 'w') as file:
        file.write("=================================\n")
        file.write("=============RECEIPT=============\n")
        file.write("=================================\n\n")
        
        file.write(f"Order Number: {order_number}\n\n")
        
        file.write("items purchased:\n")
        
        for item in purchased_items:
            name= item.capitalize()
            price= items[item]['price']
            file.write(f'-{name:<15} ...... £{price:.2f}\n')
        
        file.write('\n------------------------------\n')
        file.write(f'Total before discount: £{total:.2f}\n')
        file.write(f'Discount applied: {discount_percent}%\n') 
        file.write(f'Total after discount: £{final_total:.2f}\n') 
        file.write(f'Bonus applied:{bonus_quant}\n')
        file.write(f'Total after bonus: £{total_after_bonus:.2f}\n')
        file.write(f'Change given: {change_list}\n')
        file.write('======================================\n')


def main():
    order_number= load_last_order() + 1
    purchased_items_all=[]
    wallet_total=0
    while True:
        menu_vending_machine(items)
        wallet_total= inserting_coins(wallet_total)
        
        print(f'\nYour total balance now is: £{wallet_total:.2f}\n')
        
        wallet_total,purchased_items= costumers_choice(wallet_total,items)
        purchased_items_all.extend(purchased_items)
        
        
        keep = input ('Are you still shopping? (Yes/No) ').lower().strip()
        
        if keep== 'no':   
             
            total,number_of_items= total_purchased(purchased_items_all,items)
            final_total, discount_percent= discount(total,number_of_items)
            total_after_bonus,bonus_quant= bonus(final_total, order_number)
            change=wallet_total - total_after_bonus
            change_list=calculate_change(change)
        
            generate_csv(order_number,purchased_items_all,total,discount_percent,final_total,bonus_quant,total_after_bonus,change_list)
            print('Receipt generated.Thank you for shopping!')
            save_last_order(order_number)
            break

        else:
            print('\nKeep shopping')


main()



                    
