def flatten(x): # this will convert dictionary into a list
    removed_groups = []
    for i in x:
        removed_groups.extend(x[i]) #get only from the dictionary,because dict[index] will return value only
    return removed_groups

def findminterms(a): # Combine list
    different_bit = a.count('x')
    if different_bit == 0:
        return [str(int(a,2))]
    x = [bin(i)[2:].zfill(different_bit) for i in range(pow(2,different_bit))] #change binary to original form,different bit powered by 2 
    temp = []
    for i in range(pow(2,different_bit)):
        temp2,index = a[:],-1
        for j in x[0]:
            if index != -1:
                index = index+temp2[index+1:].find('x')+1
            else:
                index = temp2[index+1:].find('x')
            temp2 = temp2[:index]+j+temp2[index+1:]
        temp.append(str(int(temp2,2)))
        x.pop(0)
    return temp

def bitcomparing(a,b): #bitcomparing and find different by 1 bit
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            nomatch_index = i
            c += 1
            if c>1:
                return (False,None)
    return (True,nomatch_index)


mt = [int(i) for i in input("Input Minterms: ").strip().split()] #input minterms here (will be input to list with separated format)
dc = [int(i) for i in input("Input dont care,if no press enter: ").strip().split()] #input dont care
bitsize = int(input("Input var : ")) #var is maximum bit size 
method = input("Input method (SOP/POS) : ".upper()) #automatically turn into uppercase to avoid input error
mt.sort() #sort the minterms list
maximum_decimal = (2**bitsize) 
if method == "SOP":
    minterms = mt+dc #add dont care into minterms
    minterms.sort() #sort combined mt and dc
    

elif method == "POS":
    temp = mt + dc
    pos_mt = [i for i in range(0,maximum_decimal) if i not in temp] 
    mt = pos_mt
    minterms = mt+dc

lengthest_bit = len(bin(minterms[-1])) - 2
groups,all_pi = {},set()

if  lengthest_bit > bitsize: #check if there are minterms greater than bitsize
    great = str(bin(minterms[-1]))
    great = great[2:]
    print("Cant count because {} bit length is {} greater than var input ({})".format(great,lengthest_bit,bitsize))
    exit()
#loop to group minterms
for minterm in minterms:
    try:
        groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(bitsize))  #count 1 from the minterms and append the value 
    except KeyError:
        groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(bitsize)]


#loop to display group 1 of convert binary from minterm
print("\n\n\n\nGroup \t\tMinterms\tBinary Form")
print("%s"%('+'*50))
for i in sorted(groups.keys()):
    print("%2d:"%i) # Prints group number
    for j in groups[i]:
        print("\t\t    %-15d%s"%(int(j,2),j)) # Prints minterm and its binary representation
    print('-'*50)


#loop to create table and find prime implicants starts
while True:
    
    tmp = groups.copy()
    groups,m,marked,stop = {},0,set(),True
    l = sorted(list(tmp.keys()))
    for i in range(len(l)-1):
        for j in tmp[l[i]]: # loop in current group
            for k in tmp[l[i+1]]: # loop to next group if still find match bit
                res = bitcomparing(j,k)#use compare function to compare different bit of j and k
                
                if res[0]: # If the minterms differ by 1 bit only (res has value)
                    try:
                        groups[m].append(j[:res[1]]+'x'+j[res[1]+1:]) if j[:res[1]]+'x'+j[res[1]+1:] not in groups[m] else None # Replace bit with x in the same bit
                        
                    except KeyError: # key error is group not created
                        groups[m] = [j[:res[1]]+'x'+j[res[1]+1:]] # if group is not created create group
                    stop = False # change stop to false,to get the loop continue
                    marked.add(j) # add element j to marked dict
                    marked.add(k) # add element k to marked dict
                    
                    
        m += 1
    
    local_unmarked = set(flatten(tmp)).difference(marked) #get item not in marked list
   
    all_pi = all_pi.union(local_unmarked) #all pi is the union or combined elements of all pi and local unmarked
     # Add prime implicants to all prime implicant list
    
    print("Prime Implicants from table :",None if len(local_unmarked)==0 else ', '.join(local_unmarked)) # Printing Prime Implicants of current table
    if stop: # If the minterms cannot combined more
        print("\n\nAll Prime Implicants: ",None if len(all_pi)==0 else ', '.join(all_pi)) # Print all prime implicants
        break #exit loop if all prime implicants already found
    # Print next group
    
    print("\n\n\n\n  Group\t\tMinterms\tBinary Form")
    print("%s"%('+'*50))
    for i in sorted(groups.keys()):
        print("%5d :"%i) # Prints group number
        for j in groups[i]:
            print("\t\t%-20s%s"%(','.join(findminterms(j)),j)) # Prints minterms and the binary of minterm
        print('-'*50)

