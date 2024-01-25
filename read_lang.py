import re

#moves everything after a #
def remove_comments(data : str)->str:
    return data.split("#")[0]

class ParseNode:
    def __init__(self,name):
        self.name = name
        self.rules = []
    
    def __str__(self):
        ret_val = self.name + " -> "
        for r in self.rules:
            ret_val += str(r) + " , "
        return ret_val[0:-3]


#generates a dictionary of rules based on a given .lang file
#very rudimentary, inteanded for further parsing
def get_parse_dictionary(path : str):
    continuation = re.compile("\\s+.+")

    ret_val = {}
    last_entry = ""
    with open(path,'r') as f:
        for line in f:
            line = remove_comments(line[:-1]) #strip new lines at the end
            
            if line == "" or line == "\n":
                continue

            if continuation.match(line):
                #include the seperator
                if ret_val[last_entry] != "": ret_val[last_entry]+= "|"

                ret_val[last_entry] += line.strip()
                continue
            
            split_data = line.split('=')
            
            
            if split_data[1] == "":
                add_to = split_data[1]

            ret_val[split_data[0]] = "=".join(split_data[1:]).strip()

            last_entry = split_data[0]
        else:
            print("end of the file")
        
        #clean up and create lists from the initial data
        return { key.strip():ret_val[key].split("|") for key in ret_val}


#returns true if the rule can be recursed into
def has_inner_rule(rule : str)->bool:
    reg = re.compile('<.+>')
    return re.match(reg,rule)

#returns a dictionaries of lexims from the langage
def get_lexims(data):
    return {key:data[key] 
                for key in data 
                    if not any(
                            has_inner_rule(law) for law in data[key]
                            )}

#returns a dictionaries of mappings for the language
def get_mappings(data):
    return {key:data[key] 
                for key in data 
                    if any(
                            has_inner_rule(law) for law in data[key]
                            )}

#creates a maping of lexims given a dictionary of lexims
def create_lexim_map(lexims):
    ret_val = {}
    
    for key in lexims:
        lexim_node = ParseNode(key)
        for rule in lexims[key]:
            lexim_node.rules.append(re.compile(rule))
        ret_val[key] = lexim_node
    
    return ret_val

#TODO: get the rule mappings working
#def 
#def create_rule_map(maps):
#    ret_val = {}
#    
#    for key in lexims:
#        lexim_node = ParseNode(key)
#        for rule in lexims[key]:
#            lexim_node.rules.append(rule)
#        ret_val[key] = lexim_node
#    
#    return ret_val

if __name__ == '__main__':
    print('[*] generating the parse tree')
    data = get_parse_dictionary("./example.lang")
    
    lexims = get_lexims(data)
    maps = get_mappings(data)

    lexim_nodes = create_lexim_map(lexims)
    print([str(lexim_nodes[key]) for key in lexim_nodes])

    
    print('[*] finished!')

