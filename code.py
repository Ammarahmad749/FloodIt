str="aaabbccdffghijjk"
count=1
for i in range(0,len(str)):
    j=i+1
    if j < len(str):
        if str[i]==str[j]:
            count=count+1
            continue;
        elif str[i]!=str[j] and count > 1:
            print(str[i],count)
            count=1
        elif str[i]!=str[j] and count == 1:
            print(str[i])
            count=1
print("\n")


