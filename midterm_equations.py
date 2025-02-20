

def main():
    question_type_list = []
    question_type = fix_inp("1: Opportunity Cost   2: Surplus  3: Elasticity\n")
    while question_type != None and question_type != 'r':
        if not question_type.isdigit():
            question_type_list = convert_to_list(question_type)
        if question_type == '1' or "opportunity" in question_type_list:
            calc_opp_cost()
        elif question_type == '2' or "surplus" in question_type_list:
            surplus = calc_surplus()
            if surplus != None:
                print(surplus)
        elif question_type == '3' or "elasticity" in question_type_list:
            elasticity()
        else:
            print("Invalid input")
        print('_____________________________________________________________________________________')
        question_type = fix_inp("1: Opportunity Cost   2: Surplus  3: elasticity\n")

def convert_to_list(answer): #converts input to list of words
    import re
    answer = answer.strip().lower()
    answer = re.split(r'\W+', answer)
    return answer

def fix_inp(prompt): #lowers and strips an input, returns none if answer is empty and exits if EOFERROR or answer is 'q'
    import sys
    while True:
        try:
            answer = input(prompt)
        except EOFError:
            print('\n')
            return sys.exit()
        if answer == 'r' or answer == '':
            return 'r'
        if answer == 'q' or answer == 'quit':
            print('\n')
            return
        return answer.strip().lower()

def fix_inp_int(prompt): #returns an int or float, repeats prompt until an int or float is entered
    while True:
        x = fix_inp(prompt)
        if x == None:
            return
        elif x == "r":
            return x
        try:
            x = int(x)
        except ValueError:
            try: 
                x = float(x)
            except ValueError:
                print(f'"{x}" is not a valid value!')
                continue
        if x <= 0:
            print(f'"{x}" is not a valid value!')
            continue
        return x

def fix_inp_int_all(prompt): #returns an int or float, repeats prompt until an int or float is entered
    while True:
        x = fix_inp(prompt)
        if x == None:
            return
        if x == 'r':
            return x
        try:
            x = int(x)
        except ValueError:
            try: 
                x = float(x)
            except ValueError:
                print(f'"{x}" is not a valid value!')
                continue
        return x

def isfloat(a):
    try:
        a = str(a)
        a = int(a)
        return False
    except ValueError: 
        try:
            a = float(a)
            return True
        except ValueError:
            return False

def find_frac(num1,num2): #finds a simplified fraction
    from fractions import Fraction
    frac = Fraction(num1,num2)
    return f'{frac}'

def isretry_quit(variable): #Checks if answer is empty (needs to retry) and prints retry if true
    if variable == 'r':
        print("\n___retry___")
        return True
    if variable == None:
        return True

def isworker(): #Checks if the amount is measured in workers/amount of time (changes opp cost)
    while True:
        answer = convert_to_list(fix_inp("Are the amounts measured in either workers or time? "))
        if answers_yes(answer):
            return True
        elif answers_no(answer):
            return False
        else:
            print("Please enter a valid answer")
            continue

def get_country_info(item1 = '', item2 = ''):
    if item1 != '' and item2 != '':
        country_input = [
                    "Producer: ",
                    f"Item: {item1}\nAmount: ",
                    f"Item: {item2}\nAmount: "
        ]
    else:
        country_input = [
            "Producer: ",
            "Item: ",
            "Amount: ",
            "Item: ",
            "Amount: "
        ]
    country_info = []
    info = ''
    for i in range(len(country_input)):
        while info != None and info != 'r':
            if country_input[i] == "Amount: " or country_input[i] == f"Item: {item1}\nAmount: " or country_input[i] == f"Item: {item2}\nAmount: ":
                info = fix_inp_int(country_input[i])
                if isretry_quit(info):
                    continue
                country_info.append(info)
            else:
                info = fix_inp(country_input[i])
                if isretry_quit(info):
                    continue
                elif len(info) >= 10:
                    print('\n___Text must be 10 chr or less, please retry___')
                    info = 'r'
                    continue
                country_info.append(info)
            break
        if info == None:
            return
        elif info == 'r':
            return 'r'
    return country_info

def calc_opp_cost(): #finds opp cost of two contries and two items
    country1_info = []
    country2_info = []
    while country1_info != None and country2_info != None:
        while True:
            country1_info = get_country_info()
            if country1_info == 'r':
                continue
            break
        if country1_info == None:
            continue
        else:
            country_1, item1, amount11, item2, amount12 = country1_info
        print()
        while True:
            country2_info = get_country_info(item1 = item1, item2 = item2)
            if country2_info == 'r':
                continue
            break
        if country2_info == None:
            continue
        else:
            country_2, amount21, amount22 = country2_info

        country_1 = country_1.upper()
        country_2 = country_2.upper()
        amounts = [amount11, amount12, amount21, amount22]
        if not isworker():
            for i in range(len(amounts)):
                if isfloat(amounts[i]):
                    has_float = True
                    break
                else:
                    has_float = False
                
            if has_float:
                opp_costs = [
                    amounts[1]/amounts[0],
                    amounts[0]/amounts[1],
                    amounts[3]/amounts[2],
                    amounts[2]/amounts[3]
                ]
            
            else:
                opp_costs = [
                    find_frac(amounts[1],amounts[0]),
                    find_frac(amounts[0],amounts[1]), 
                    find_frac(amounts[3],amounts[2]), 
                    find_frac(amounts[2],amounts[3])
                ]
            all_country_info = [item1,item2,country_1,country_2,opp_costs[0],opp_costs[1],opp_costs[2],opp_costs[3]]
            
            opp_cost_graph(*all_country_info) #maybe replace with *opp_costs

            print(f'\nCOMPARITIVE ADVANTAGE')
            if amount12/amount11 == amount22/amount21:
                print(f'Niether {country_1} not {country_2} has a comparative advantage')
            if amount12/amount11 < amount22/amount21:
                print(f'{country_1} has a comparative advantage in {item1}\n{country_2} has a comparative advantage in {item2}')
            else:
                print(f'{country_2} has a comparative advantage in {item1}\n{country_1} has a comparative advantage in {item2}')
            print(f'\nABSOLUTE ADVANTAGE')
            if amount11 > amount21 and amount12 > amount22:
                print(f'{country_1} has absolute advantage in both {item1} and {item2}')
            elif amount11 < amount21 and amount12 < amount22:
                print(f'{country_2} has absolute advantage in both {item1} and {item2}')
            elif amount11 == amount21 and amount12 == amount22:
                print(f'Neither {country_1} nor {country_2} have absulute advantage')
            else:
                if amount11 > amount21:
                    print(f'{country_1} has absolute advantage in {item1}')
                elif amount11 == amount21:
                    print(f'Neither {country_1} nor {country_2} has absolute advantage in {item1}')
                else:
                    print(f'{country_2} has absolute advantage in {item1}')
                if amount12 > amount22:
                    print(f'{country_1} has absolute advantage in {item2}')
                elif amount12 == amount22:
                    print(f'Neither {country_1} nor {country_2} has absolute advantage in {item2}')
                else:
                    print(f'{country_2} has absolute advantage in {item2}')
        else:
            for i in range(len(amounts)):
                if isfloat(amounts[i]):
                    has_float = True
                    break
                else:
                    has_float = False
                
            if has_float:
                opp_costs = [
                    amounts[0]/amounts[1],
                    amounts[1]/amounts[0],
                    amounts[2]/amounts[3],
                    amounts[3]/amounts[2]
                ]
            else:
                opp_costs = [
                    find_frac(amounts[0],amounts[1]),
                    find_frac(amounts[1],amounts[0]), 
                    find_frac(amounts[2],amounts[3]), 
                    find_frac(amounts[3],amounts[2])
                ]
            opp_cost_graph(item1,item2,country_1,country_2,opp_costs[0],opp_costs[1],opp_costs[2],opp_costs[3])
            print(f'\nCOMPARITIVE ADVANTAGE')
            if amount12/amount11 == amount22/amount21:
                print(f'Niether {country_1} not {country_2} has a comparative advantage')
            elif amount12/amount11 > amount22/amount21:
                print(f'{country_1} has a comparative advantage in {item1}\n{country_2} has a comparative advantage in {item2}')
            else:
                print(f'{country_2} has a comparative advantage in {item1}\n{country_1} has a comparative advantage in {item2}')
            print(f'\nABSOLUTE ADVANTAGE')
            if amount11 < amount21 and amount12 < amount22:
                print(f'{country_1} has absolute advantage in both {item1} and {item2}')
            elif amount11 > amount21 and amount12 > amount22:
                print(f'{country_2} has absolute advantage in both {item1} and {item2}')
            elif amount11 == amount21 and amount12 == amount22:
                print(f'Neither {country_1} nor {country_2} have absulute advantage')
            else:
                if amount11 < amount21:
                    print(f'{country_1} has absolute advantage in {item1}')
                elif amount11 == amount21:
                    print(f'Neither {country_1} nor {country_2} has absolute advantage in {item1}')
                else:
                    print(f'{country_2} has absolute advantage in {item1}')
                if amount12 < amount22:
                    print(f'{country_1} has absolute advantage in {item2}')
                elif amount12 == amount22:
                    print(f'Neither {country_1} nor {country_2} has absolute advantage in {item2}')
                else:
                    print(f'{country_2} has absolute advantage in {item2}')
        return 'Done!'
    print('--exited--')

def sci_note(value):
    digits = []
    fraction = []
    if '.' in str(value):
        digits = str(value).split('.')
    elif '/' in str(value):
        fraction = value.split('/')
    else:
        digits.append(str(value))
    try:
        int(digits[0])
    except ValueError:
        return value
    except IndexError:
        pass
    try:
        int(fraction[0])
    except ValueError:
        return value
    except IndexError:
        pass
    if value == 0:
        return value
    if len(digits) >= 1:
        if len(digits[0]) > 3: #If dealing with even bigger numbers, can change to take into account pythons auto sci notation.
            e_value = (len(digits[0])-1)
            value = f'{(float(digits[0])/(10**e_value)):.2f}*10^{e_value}'
            return value
    
    if len(fraction) > 1:
        value1, value2 = fraction
        if len(fraction[0]) > 3:
            e_value = (len(fraction[0])-1)
            value1 = f'{(float(fraction[0])/(10**e_value)):.2f}*10^{e_value}'
        if len(fraction[1]) > 3:
            e_value = (len(fraction[1])-1)
            value2 = f'{(float(fraction[1])/(10**e_value)):.2f}*10^{e_value}'
        return f'{value1}/{value2}'
    
    elif len(digits) > 1:
        if len(digits[1]) > 4 and float(value) > 1e-4 and int(digits[0]) == 0:
            count = 0
            for num in digits[1]:
                count += 1
                if num != '0':
                    e_value = (count)
                    break
            if count > 3:
                value = f'{(float(value)*(10**e_value)):.2f}*10^-{e_value}'
        elif float(value) < 1e-4 and float(value) > 0 or 0 > float(value) > -1e-4:
            value = float(value)
            value = str(value).split('e')
            value[1] = value[1].replace('-','')
            digit = round(float(value[0]),2)
            e_value = int(value[1])
            value = f'{digit}*10^-{e_value}'
    if isfloat(value):
        value = round(value,3)
    
    return value

def opp_cost_graph(*all_info): #prints opp_cost_graph

    item1, item2, country_1, country_2, opp_cost11, opp_cost12, opp_cost21, opp_cost22 = all_info

    opp_costs = [opp_cost11,opp_cost12,opp_cost21,opp_cost22]
    
    for i in range(len(opp_costs)):
        opp_costs[i] = sci_note(opp_costs[i])

    print(f'\n{"":10}{"OPPORTUNITY COST":^26}')
    print(f'{"":10}{item1:^13}{item2:^13}')
    print(f'{country_1:>10}{opp_costs[0]:^13}{opp_costs[1]:^13}')
    print(f'{country_2:>10}{opp_costs[2]:^13}{opp_costs[3]:^13}')

def calc_surplus():
    type = ''
    while type != None:
        type = fix_inp('Do you want to calculate consumer or producer surplus, or a change in consumer or producer surplus? \n')
        if isretry_quit(type):
            continue
        type = convert_to_list(type)
        quant_o, price_o, highest_price_o, price_f, quant_f, highest_price_f = [0,0,0,0,0,0]
        while quant_o != None and price_o != None and highest_price_o != None and quant_f != None and price_f != None and highest_price_f != None:
            if 'consumer' in type and 'change' in type:
                quant_o = fix_inp_int('Initial QD: ')
                if isretry_quit(quant_o):
                    continue
                price_o = fix_inp_int('Initial PD: ')
                if isretry_quit(price_o):
                    continue
                highest_price_o = fix_inp_int('Initial Top Price: ')
                if isretry_quit(highest_price_o):
                    continue
                quant_f = fix_inp_int('Final QD: ')
                if isretry_quit(quant_f):
                    continue
                price_f = fix_inp_int('Final PD: ')
                if isretry_quit(price_f):
                    continue
                highest_price_f = fix_inp_int('Final Top Price: ')
                if isretry_quit(highest_price_f):
                    continue
                change_price_o = highest_price_o - price_o
                change_price_f = highest_price_f - price_f
                change_surplus = 1/2 * (change_price_f * quant_f - change_price_o * quant_o)
                return f'Total Change in Consumer Surplus: {sci_note(change_surplus)}'
            elif 'consumer' in type:
                quant_o = fix_inp_int('QD: ')
                if isretry_quit(quant_o):
                    continue
                price_o = fix_inp_int('PD: ')
                if isretry_quit(price_o):
                    continue
                highest_price_o = fix_inp_int('Top Price: ')
                if isretry_quit(highest_price_o):
                    continue
                change_price_o = highest_price_o - price_o
                surplus = 1/2 * change_price_o * quant_o
                return f'Consumer Surplus: {sci_note(surplus)}'
            if 'producer' in type and 'change' in type:
                quant_o = fix_inp_int('Initial QS: ')
                if isretry_quit(quant_o):
                    continue
                price_o = fix_inp_int('Initial PS: ')
                if isretry_quit(price_o):
                    continue
                quant_f = fix_inp_int('Final QD: ')
                if isretry_quit(quant_f):
                    continue
                price_f = fix_inp_int('Final PS: ')
                if isretry_quit(price_f):
                    continue
                change_surplus = 1/2 * (price_f * quant_f - price_f * quant_o)
                return f'Total Change in Producer Surplus: {sci_note(change_surplus)}'
    
            elif 'producer' in type:
                quant_o = fix_inp_int('QS: ')
                if isretry_quit(quant_o):
                    continue
                price_o = fix_inp_int('PS: ')
                if isretry_quit(price_o):
                    continue
                surplus = 1/2 * price_o * quant_o
                return f'Total Producer Surplus: {sci_note(surplus)}'
            print('\n____Unreconizable Input____')
            break
    return '--exited--'

def answers_yes(answer):    #checks if a answer is in a list of yes variations
    yes_variations = ["yes","ya","yuh","yep","sure","yeah", "ye", 'y']
    for x in range(0,len(answer)):
        if answer[x] in yes_variations:
            return True
    return False

def answers_no(answer):     #checks if a answer is in a list of no variations
    no_variations = ["no","nah","na","nope",'n']
    for x in range(0,len(answer)):
        if answer[x] in no_variations:
            return True
    return False

def calc_elasticity():
    type, type_2, type_3 = ['','','',]
    while type_2 != None and type != None and type_3 != None:
        type = fix_inp("Is this income elasticity, demand elasticity, supply elasticity, cross_price, or percent change in price? ")
        if isretry_quit(type):
            continue
        else:
            type = convert_to_list(type)
        if 'demand' in type or 'supply' in type or 'cross' in type or 'cross-price' in type or 'income' in type:
            if 'income' in type:
                type = 1
            elif 'demand' in type:
                type = 2
            elif 'supply' in type:
                type = 3
            elif 'cross' in type or 'cross-price' in type:
                type = 4
            type_2 = ''
            while type_2 != None and type_2 != 'r':
                type_2 = fix_inp("Is the question giving percent changes? ")
                if isretry_quit(type_2):
                    continue
                else:
                    type_2 = convert_to_list(type_2)
                if not answers_yes(type_2) and not answers_no(type_2):
                    print("___Please Enter a Valid Response___")
                    continue
                break
            if type_2 == 'r':
                continue
            perc_change_in_quant, perc_change_in_price, quant_o, quant_f, price_o, price_f = ['','','','','','']
            while perc_change_in_quant != None and perc_change_in_price != None and quant_o != None and quant_f != None and price_o != None and price_f != None and type_2 != None:
                if answers_yes(type_2):
                    if type == 1:
                        perc_change_in_quant = fix_inp_int_all("Percent Change in Quantity: ")
                        if isretry_quit(perc_change_in_quant):
                            continue
                        perc_change_in_price = fix_inp_int_all("Percent Change in Income: ")
                        if isretry_quit(perc_change_in_price):
                            continue
                    elif type != 1:
                        perc_change_in_quant = fix_inp_int_all("Percent Change in Quantity: ")
                        if isretry_quit(perc_change_in_quant):
                            continue
                        perc_change_in_price = fix_inp_int_all("Percent Change in Price: ")
                        if isretry_quit(perc_change_in_price):
                            continue
                    
                    elasticity = perc_change_in_quant/perc_change_in_price
            
                elif answers_no(type_2):
                    if type == 1:
                        quant_o = fix_inp_int("Initial Quantity: ")
                        if isretry_quit(quant_o):
                            continue
                        quant_f = fix_inp_int("Final Quantity: ")
                        if isretry_quit(quant_f):
                            continue
                        price_o = fix_inp_int("Initial Income: ")
                        if isretry_quit(price_o):
                            continue
                        price_f = fix_inp_int("Final Income: ")
                        if isretry_quit(price_f):
                            continue
                    elif type != 1:
                        quant_o = fix_inp_int("Initial Quantity: ")
                        if isretry_quit(quant_o):
                            continue
                        quant_f = fix_inp_int("Final Quantity: ")
                        if isretry_quit(quant_f):
                            continue
                        price_o = fix_inp_int("Initial Price: ")
                        if isretry_quit(price_o):
                            continue
                        price_f = fix_inp_int("Final Price: ")
                        if isretry_quit(price_f):
                            continue
                    elasticity = ((quant_o - quant_f)/(1/2*(quant_o + quant_f)))/((price_o - price_f)/(1/2*(price_o + price_f)))
                
                return [sci_note(elasticity),type]
        
        elif 'percent' in type or 'price' in type or 'chang' in type:
            type = 5
            elas_dem, elas_supply, perc, type_3 = ['','','','']
            while elas_dem != None and elas_supply != None and perc != None and type_3 != None:
                elas_dem = fix_inp_int_all('Elasticity of demand: ')
                if isretry_quit(elas_dem):
                    continue
                elas_dem = abs(elas_dem)
                elas_supply = fix_inp_int('Elasticity of Supply: ')
                if isretry_quit(elas_supply):
                    continue
                perc = fix_inp_int_all('Percent Change: ')
                if isretry_quit(perc):
                    continue
                perc_change_in_price = perc / (elas_dem + elas_supply)
                perc_change_in_price = sci_note(perc_change_in_price)
                type_3 = ''
                while type_3 != None and type_3 != 'r':
                    type_3 = fix_inp("Is the percent change in supply or demand? ")
                    if isretry_quit(type_3):
                        continue
                    else:
                        type_3 = convert_to_list(type_3)
                        if not 'demand' and not answers_yes(type_3):
                            print("___Please Enter a Valid Response___")
                            continue
                        if 'demand' in type_3:
                            perc_change_in_price = perc_change_in_price
                        elif 'supply' in type_3:
                            perc_change_in_price = -perc_change_in_price
                        return [perc_change_in_price,type]
        else:
            print("___Please Enter a Valid Type___")
            continue
    return [None,None]

def elasticity():
    value, type = calc_elasticity()
    while type != None and value != None:
        if type == 2:
            elas = abs(value)
            if elas > 1:
                print('\nELASTIC')
            elif elas < 1:
                print('\nINELASTIC')
            else:
                print('\nUNITARY')
            print(f'\nDemand Elasticity: {elas}')
        elif type == 3:
            elas = abs(value)
            print(f'\nSupply Elasticity: {elas}')

        elif type == 4:
            elas = value
            print(f'\nCross-price Elasticity: {elas}')
            print(f'\nTYPE:')
            if '-' in str(value):
                print('The two products are compliments\n')
            else:
                print('The two products are substitutes\n')
        
        elif type == 1:
            elas = value
            print(f'\nIncome Elasticity: {elas}')
            print('\nTYPE OF GOOD:')
            if '-' in str(elas):
                print('Inferior good\n')
            else:
                print('Normal good\n')
        elif type == 5:
            print("\nPERCENT CHANGE:")
            if value < 0:
                print(f'{abs(value)} percent decrease in price!')
            elif value == 0:
                print('No change in price')
            else:
                print(f'{value} percent increase in price!')
        return 'Done'
    print('--exited--')

if __name__ == '__main__':
    main()