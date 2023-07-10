## Asteroid Collision

[LeetCode](https://leetcode.com/problems/asteroid-collision/)


We are given an array asteroids of integers representing asteroids in a row.

For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.

Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.

```
Example 1:

Input: asteroids = [5,10,-5]
Output: [5,10]
Explanation: The 10 and -5 collide resulting in 10. The 5 and 10 never collide.
```

```python
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        for asteroid in asteroids:
            # if loop breaks, else. if loop escaped with while condition, ignore else
            # loop if stack is not empty and last asteroid is positive and current asteroid is negative
            while stack and stack[-1] > 0 > asteroid:
                if abs(asteroid) > stack[-1]:
                    stack.pop()
                    continue
                elif abs(asteroid) == stack[-1]:
                    stack.pop()
                break
            # if while loop is escaped, append asteroid. if break, ignore
            else:
                stack.append(asteroid)
        return stack
```
Runtime : 94 ms / Beats 85.64%  
Memory : 15.1 MB / Beats 61.75%


tags: @stack
