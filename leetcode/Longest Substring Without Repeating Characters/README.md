Longest Substring Without Repeating Characters

[LeetCode](https://leetcode.com/problems/longest-substring-without-repeating-characters/)


Given a string s, find the length of the longest 
substring
 without repeating characters.

```
Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
```

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0
        
        max_len = 1
        start = 0
        checked = set()

        for end in range(n):
            while s[end] in checked:
                checked.remove(s[start])
                start += 1
            
            checked.add(s[end])
            # compare max_len
            max_len = max(max_len, end - start + 1)

        return max_len
```
Runtime : 61 ms  
Memory : 14.1 MB

@sliding-window