import pandas as pd, os, re

        
def read():
    filename = input('Please input filename:')
    if not os.path.exists(filename):
        print('No such file')
        return read()
    data = None
    while data is None:
        records = []
        with open(filename, 'r') as f:
            kyes = ''
            for i, v in enumerate(f.readlines()):
                if i == 0:
                    keys = v.strip().split('\t')
                else:
                    values = v.strip().split('\t')
                    records.append({keys[index]: value for index, value in enumerate(values)})
        data = pd.DataFrame.from_records(records)
    return data

def process(query, data):
    query = query.lower().replace(" ", "")
    if query == 'menu':
        menu()
    elif query == 'all':
        print(data)
    elif query == 'q':
        return 0
    elif '=' in query:
        key, value = query.strip().split('=', 1)
        if key == 'year':
             if value.isdigit():
                if value == '2019' or value == '2020' or value == '2021':
                    print(data[data.GradYear == value])
                else:
                    print('Please enter a year between 2019 and 2021')                
             else:
                print('TypeError: the year must be int')
        elif key == 'lastname':
            res = re.findall(r'\w+', value)
            if res and res[0] == value:
                result = data[data.Last.str.startswith(value.capitalize())]
                if len(result) > 0:
                    print(result)
                else:
                    print('ValueError: can not match last name')
            else:
                print('ValueError: last name only allow letters, numbers and underscores')
        elif key == 'report':
            if value.isdigit():
                if value == '2019' or value == '2020' or value == '2021':
                    report_data = data[data.GradYear == value]
                    count_by_program = report_data.groupby('DegreeProgram').ID.count()
                    percentage = count_by_program / len(report_data)
                    print(pd.DataFrame({'counts': count_by_program, 'percentage': percentage}))
                else:
                    print('Please enter a year between 2019 and 2021') 
            else:
                print('TypeError: the year must be int')
    else:
        print('OptionsError: plear enter menu to show help')

def menu():
    print("""
    This is A query tool, return related data by user's input
    
    Input Options
    -------------
    all : return all data    
    year=<Year> : Display data for a certain year
    lastname=<LastName> : Display data for a certain lastname
    report=<Year> :Display a summary report of number and percent of students in
    each program, for students graduating on/after a certain year
    menu : show menu
    q : quit

    Examples
    --------
    >>> year=2019
    >>> lastname=Lee
    >>> report=2019             """)
        

if __name__ == '__main__':
    data = read()
    pd.set_option('display.max_rows', None)
    menu()
    signal = None
    while signal is None:
        query = input('What do you want to select?(enter menu to show help)')
        signal = process(query, data)
