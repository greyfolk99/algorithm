## Generate Parentheses

[LeetCode](https://leetcode.com/problems/generate-parentheses)  


Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.  

Example 1:
```
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
```
Example 2:
```
Input: n = 1
Output: ["()"]
```
Constraints:
1 <= n <= 8

```python
class Solution:
  def generateParenthesis(self, n: int) -> List[str]:
    result = []
    def dfs(left, right, s):
      if len(s) == n * 2:
        result.append(s)
        return 

      if left < n:
        dfs(left + 1, right, s + '(')

      if right < left:
        dfs(left, right + 1, s + ')')
	dfs(0, 0, '')
	return result
```

'(' 로 닫히는 경우의 수를 전부 찾는 다면 깊이 탐색 사용


@DFS
