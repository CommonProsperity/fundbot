import os
global csv_dict
csv_dict = None

def getCodeByName(target_name: str, relative_path='code2name/'):
    global csv_dict
    # read the dict from file 
    if not csv_dict:
        print(os.getcwd())
        print("Reading csv from storage")
        csv_dict = dict()
        try:
            with open(relative_path + "/mappings.csv", 'r') as fin:
                contents = fin.readlines()
                for line in contents:
                    line = line.replace('\n', '')
                    splitted = line.split(',')
                    code, name = splitted[0], splitted[1]
                    csv_dict[name] = code
        except Exception as e:
            print("Error occured when reading the file: ", e)
            return "Error when reading the file"
    
    # search the dict
    result = ""
    for name in csv_dict.keys():
        if name.find(target_name) != -1:
            result += name + " " + csv_dict[name] + "\n"
    if result == "":
        result = "哎呀找不到"
    return result


