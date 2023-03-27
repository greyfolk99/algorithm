Add Two Numbers

[LeetCode](https://leetcode.com/problems/add-two-numbers/)


You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

![img.png](img.png)

```
Example 1:

Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # create dummy node for sum
        dummy = ListNode()
        # set current node with dummy node
        curr = dummy
        # initialize carry
        carry = 0
        # while current nodes of l1, l2, and carry are not None
        while l1 or l2 or carry:
            # set initial number with carry
            sum = carry
            # if l1 is not None move to next node
            if l1:
                sum += l1.val
                l1 = l1.next
            # if l2 is not None move to next node
            if l2:
                sum += l2.val
                l2 = l2.next
            # set carry for next node
            carry = sum // 10
            # set pointer to next node
            curr.next = ListNode(sum % 10)
            # move to next node
            curr = curr.next
        #
        return dummy.next
```
Runtime : 57 ms  
Memory : 13.8 MB

@singly-linked-list