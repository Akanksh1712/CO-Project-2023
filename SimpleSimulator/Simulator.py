import sys

#ALL THE GLOBAL VARIABLES
global  register_file
global mem
global PC
global flag_val 

PC="0"*7
flag_val=-1
result = []
br=0 # used in halt inst to break the loop

register_file={"000":0,
"001":0,
"010":0,
"011":0,
"100":0,
"101":0,
"110":0,
"111":"0"*16 } #111=flag

mem={}

PC= "0"*16

for i in range(256):
    mem[i]="0"*16


# binary to decimal
def btd(s):
    p=0
    w=len(s)

    for i in s:
        
        p+=(2**(w-1))*int(i)
        w-=1
    

    #print(p)

    return p

#decimal to binary
def dtb(val):
    bi=bin(val)[2:]
    s=16-len(bi)
    bi='0'*s+bi
    return bi

#float to binary
def ftb(y):
    x= bin(int(y))[2:]#integer

    f=y-int(y) #mantissa


    b=x+"."


    while(1):
        if(len(b)<8):
            f=f*2
            if(f//1==1):
                b+='1'
                f-=1
            else:
                b+='0'

        else:    
            break


    #print(b)
    temp=0

    for i in range(len(b)):
        
        if(b[i]=='.'):
            

            #print(i)
            b=b[(1):i]+b[(i+1):]
            temp=i-1
            break
        
        

    exp=bin(3+temp)[2:]
    exp=(3-len(exp))*'0'+exp
    num=exp+b[0:5]
    #print(num)
    num=(16-len(num))*'0'+num
    return num


# binary to float
def btf(y):
    x=y[0:3]
    x=btd(x)-3

    y=y[3:]

    f=y[x:]
    y='1'+y[0:x]

    num=btd(y)
    for i in range(len(f)):
        num+=(2**(-i-1))*int(f[i])
        
    return num
# to keep track of number of entries of mem dictionary
q=0

#with open ("test1",'r') as f:
f = sys.stdin.readlines()

for line in f:
    mem[q]=line.strip()
    q+=1
    # print (line,end='')

# loop over mem dictionary
l=0
while (l<q):
#for i in range(q) :
    s=mem[l]
    PC=dtb(l)[9:]
    l+=1
    opc=s[0:5]

    rds=""
    rs1=""
    rs2="" #can be an immediate

    # writing all the functions

    # opcodes with 3 address format
    # unused bits = 2
    #add operation
    if(opc=="00000"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]
        #performing operation
        value= register_file[rs1]+register_file[rs2]

        
        if(value>2**16):
            flag_val=3
            temp=register_file["111"]
            register_file["111"]=temp[0:12]+"1"+temp[13:]

            # store the value in rds
            register_file[rds]=0

        else:
            # store the value in rds
            register_file[rds]=value


    
    # subtract
    elif(opc=="00001"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]
        #performing operation
        value= register_file[rs1]-register_file[rs2]

        
        if(value<0):
            flag_val=3
            temp=register_file["111"]
            register_file["111"]=temp[0:12]+"1"+temp[13:]

             # store the value in rds
            register_file[rds]=0

        else:
            # store the value in rds
            register_file[rds]=value



    #multiplication
    elif(opc=="00110"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]
        #performing operation
        value= register_file[rs1]*register_file[rs2]

        
        if(value>2**16):
            flag_val=3
            temp=register_file["111"]
            register_file["111"]=temp[0:12]+"1"+temp[13:]

             # store the value in rds
            register_file[rds]=0

        else:
            # store the value in rds
            register_file[rds]=value

    #division
    elif(opc=="00001"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]
        #performing operation
        value= register_file[rs1]//register_file[rs2]

        
        
        if(value>2**16):
            flag_val=3
            temp=register_file["111"]
            register_file["111"]=temp[0:12]+"1"+temp[13:]

             # store the value in rds
            register_file[rds]=0

        else:
            # store the value in rds
            register_file[rds]=value

    #F_ADDITION
    elif(opc=="10000"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]
        #performing operation
        value= register_file[rs1]+register_file[rs2]

        

      
        
        if(value>7.96875):
            flag_val=3
            temp=register_file["111"]
            register_file["111"]=temp[0:12]+"1"+temp[13:]

             # store the value in rds
            register_file[rds]=0

        else:
            # store the value in rds
            register_file[rds]=value
    
    #F_SUBTRACTION
    elif(opc=="10001"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]
        #performing operation
        value= register_file[rs1]-register_file[rs2]

       
        
        if(value<0):
            flag_val=3
            temp=register_file["111"]
            register_file["111"]=temp[0:12]+"1"+temp[13:]

             # store the value in rds
            register_file[rds]=0
            
        else:
            # store the value in rds
            register_file[rds]=value


#*********** 2 address format************

    # move immediate
    #unsused bit =1
    elif(opc=="00010"):
        rds = s[6:9]
        
        rs2 = s[9:16]#rs2 = immediate

        #performing operation
        value= btd(rs2)

        # store the value in rds
        register_file[rds]=value

    # move F_immediate
    #unsused bit =0
    elif(opc=="10010"):
        rds = s[5:8]
        
        rs2 = s[8:16]#rs2 = floating immediate

        #performing operation
        value= btf(rs2)

        # store the value in rds
        register_file[rds]=value
        
    # move register
    #unsused bit = 5
    elif(opc=="00011"):
        rds = s[10:13]
        
        rs2 = s[13:16]

        
        value=0
        if(rs2!='111'):
        #performing operation
            value=  register_file[rs2]
        else:
            value=btd( register_file[rs2])
            register_file[rs2]=16*'0'


        # store the value in rds
        register_file[rds]=value


    #load
    #unsused bit = 1
    elif(opc=="00100"):
        rds = s[6:9]
        
        rs2 = s[9:16]#memory address

        #performing operation
        value=  btd(mem[btd(rs2)])

        # store the value in rds
        register_file[rds]=value

    #store
    #unsused bit = 1
    elif(opc=="00101"):
        rds = s[6:9]
        
        rs2 = s[9:16]#memory address

        #performing operation
        value= register_file[rds] 

        # store the value in rds
        mem[btd(rs2)]=dtb(value)
    

    #right shift
    #unsused bit = 1
    elif(opc=="01000"):
        print("yes")
        rds = s[6:9]
        
        rs2 = s[9:16]#immediate

        #performing operation
        value= btd(rs2)
        value= register_file[rds]  >>value

        # store the value in rds
        register_file[rds]=value
    
    #left shift
    #unsused bit = 1
    elif(opc=="01001"):
        rds = s[6:9]
        
        rs2 = s[9:16]#immediate

        #performing operation
        value= btd(rs2)
        value= register_file[rds]  <<value

        # store the value in rds
        register_file[rds]=value

    #exclusive or
    #unsused bit = 2
    elif(opc=="01010"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]

        #performing operation
        
        value= register_file[rs1] ^ register_file[rs2]

        # store the value in rds
        register_file[rds]=value
    
    #And
    #unsused bit = 2
    elif(opc=="01100"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]

        #performing operation
        
        value= register_file[rs1] & register_file[rs2]

        # store the value in rds
        register_file[rds]=value

    #or
    #unsused bit = 2
    elif(opc=="01011"):
        rds = s[7:10]
        rs1 = s[10:13]
        rs2 = s[13:16]

        #performing operation
        
        value= register_file[rs1] | register_file[rs2]

        # store the value in rds
        register_file[rds]=value

    #invert
    #unsused bit = 5
    elif(opc=="01101"):
        rds = s[10:13]
        
        rs2 = s[13:16]

        #performing operation
        
        st= bin(register_file[rs2])[2:]
        

        p=0
        w=len(st)

        for i in st:
            if(i=='1'):
                i='0'
            else:
                i="1"
            
            p+=(2**(w-1))*int(i)
            w-=1
        

        # store the value in rds
        register_file[rds]=p

    #compare
    #unsused bit = 5
    elif(opc=="01110"):
        rds = s[10:13]
        
        rs2 = s[13:16]

        #performing operation
        val1 = register_file[rds]
        val2 = register_file[rs2]

        #print("**",val1,val2,rds)

        if(val1>val2):
            temp=register_file["111"]
            register_file["111"]=temp[0:13]+"010"
        
        elif(val1==val2):
            temp=register_file["111"]
            register_file["111"]=temp[0:13]+"001"
        else:
            temp=register_file["111"]
            register_file["111"]=temp[0:13]+"100"
        
    # uncoditional jump
    #unused bit = 4
    elif(opc=="01111"):
        
        
        rs2 = s[9:16]#memory address of the label first instruction
        l=btd(rs2)

    # coditional(less than) jump
    #unused bit = 4
    elif(opc=="11100"):
        
        
        rs2 = s[9:16]#memory address of the label first instruction

        value=register_file["111"]
        if(value[13]=='1'):
            l=btd(rs2)
        register_file["111"]='0' *16

    # coditional(greater than) jump
    #unused bit = 4
    elif(opc=="11101"):

        rs2 = s[9:16]#memory address of the label first instruction

        value=register_file["111"]

        if(value[14]=='1'):
            l=btd(rs2)
        register_file["111"]='0' *16
    
    # coditional(equal) jump
    #unused bit = 4
    elif(opc=="11111"):

        rs2 = s[9:16]#memory address of the label first instruction

        value=register_file["111"]

        if(value[15]=='1'):
            l=btd(rs2)
        register_file["111"]='0' *16
        

    # halt 
    elif(opc=="11010"):
        br=1

    #pc has been printed
    #print(PC,end='')
    result.append(PC)
    result.append(" "*7)

    np = 0 #use for not printing

    #values of all register has been printed
    for i in register_file.values():
        if(register_file["111"]!=i):
            #print(" "*8, dtb(i),end='')
            if(i//1==i):
                result.append(" "*1)
                result.append(dtb(i))
            else:
                result.append(" "*1)
                result.append(ftb(i))
            
		
		
		
	
        else:
            #print(" "*8, i,end='')
            result.append(" "*1)
            result.append(i)
    #print()
    result.append("\n")
    
     # resetted the value of stack over flow
    if(flag_val==3):
        register_file["111"]=temp[0:12]+"0"+temp[13:]
    if(br==1):
        break
    
#print 128 lines of memory
for i in range(128):
    result.append(mem[i])
    result.append("\n")

#************output*******
for i in result:
    sys.stdout.write(i)
    
    #if(rds!=''):
    #    print(PC,dtb(register_file[rds]))
        
'''for i in range(0,q+1):
    print(mem[i])'''

'''temp=register_file["111"]
register_file["111"]=temp[0:12]+"1"+temp[13:]
print(register_file["111"])'''

    
