## 42. Trapping Rain Water:

[LeetCode](https://leetcode.com/problems/trapping-rain-water/)

Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example 1:
> ![img.png](img.png)  
> Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]  
> Output: 6  
> Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1].   
> In this case, 6 units of rain water (blue section) are being trapped.

Example 2:
> Input: height = [4,2,0,3,2,5]  
> Output: 9


Constraints:

- n == height.length
- 1 <= n <= 2 * 104
- 0 <= height[i] <= 105



## Solution:

**First Try**

Created two arrays to record the highest height to the right and left of each bar to solve
```python
class Solution:
    def trap(self, height: List[int]) -> int:
        output = 0
        max_x = len(height)

        to_right = [0 for _ in range(max_x)]
        to_left = [0 for _ in range(max_x)]

        to_right[0] = height[0]
        to_left[max_x-1] = height[max_x-1]

        for x in range(1, max_x):
            to_right[x] = max([height[x], to_right[x-1]])
            to_left[(max_x-1)-x] = max([height[(max_x-1)-x], to_left[(max_x-1)-x+1]])

        for x in range(max_x):
            output += min(to_left[x], to_right[x]) - height[x]

        return output
```

**Second Try**  

However this solution was not optimal when I searched other answers. I found that I could solve this problem with two pointers with only one loop.
```python
class Solution:
    def trap(self, height: List[int]) -> int:
        max_x = len(height)
        lmax = 0
        rmax = 0
        left_index = 0
        right_index = max_x - 1
        output = 0
        while left_index <= right_index:
            if height[left_index] <= height[right_index]:
                lmax = max(height[left_index], lmax)
                output += (lmax - height[left_index])
                left_index += 1
            else:
                rmax = max(height[right_index], rmax)
                output += (rmax - height[right_index])
                right_index -= 1
        return output
```

@Two-Pointers @Dynamic-Programming