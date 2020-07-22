def merge_sort(lst, temp, left_start, right_end):
    if(left_start >= right_end):
        return 0
    middle=(left_start+right_end)//2
    merge_sort(lst, temp, left_start, middle)
    merge_sort(lst, temp, middle+1, right_end)
    merge(lst, temp, left_start, right_end)

def merge(lst, temp, left_start, right_end):
    left_end=(left_start+right_end)//2
    right_start=left_end+1

    left=left_start
    right=right_start
    idx=left_start

    while (left<=left_end and right<=right_end):
        if lst[left]<=lst[right]:
            temp[idx]=lst[left]
            left+=1
        else:
            temp[idx]=lst[right]
            right+=1
        idx+=1

        if (left>left_end):
            temp[idx:right_end+1]=lst[right:right_end+1]
        else:
            temp[idx:right_end+1]=lst[left:left_end+1]
        lst[left_start:right_end+1]=temp[left_start:right_end+1]

a = [8,6,7,2,4,51,1]
merge_sort(a, [], 0, len(a)-1)
