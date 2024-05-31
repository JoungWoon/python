#start = int(input("구구단의 시작 단을 입력하세요: "))
#end = int(input("구구단의 끝 단을 입력하세요: "))

#for n in range(start, end + 1):
#   for i in range(1, 10):
#        line = f"{n} x {i} = {n * i}\n"
#        print(line)

list1 = [4,5,3,2,5]
list2 = [8,4,5,1,2,3,6,9]

def uniqarr(arr1, arr2):
    list = arr1 + arr2
    uniqlist = set(list)
    return uniqlist

result = uniqarr(list1,list2)
#print(result)

nums = [2,7,11,15]
target = 11

def two_sum(nums: int, target: int) -> list:
    num_map = {}
    for i, num in enumerate(nums):
        comp = target - num
        if(comp in num_map):
            return [num_map[comp], i]
        num_map[num] = i
    return []

print(two_sum(nums, target))

