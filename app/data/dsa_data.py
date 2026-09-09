from typing import Dict, Any, List

DSA_TOPICS: Dict[str, Any] = {
    "trees": {
        "title": "Advanced Trees & Hierarchical Structures",
        "concept": """
### Binary Tree Traversals & Depth First Search (DFS)
DFS has three primary traversals:
1. **Pre-order (Root -> Left -> Right)**: Used to clone trees, serialize structures.
2. **In-order (Left -> Root -> Right)**: Traverses Binary Search Trees (BST) in ascending order.
3. **Post-order (Left -> Right -> Root)**: Bottom-up evaluation (e.g., delete tree nodes, compute node heights).

### Lowest Common Ancestor (LCA)
The Lowest Common Ancestor of two nodes `p` and `q` in a tree is the lowest node that has both `p` and `q` as descendants.
```python
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root # Both branches returned a node, so root is LCA
    return left or right # Return the non-null branch
```

### Segment Trees & Interval Queries
A Segment Tree is a binary tree used to perform range queries (e.g., sum, min, max) and point updates in $O(\\log N)$ time.
- **Construction**: $O(N)$
- **Query**: $O(\\log N)$
- **Update**: $O(\\log N)$

### Trie (Prefix Tree)
A retrieval tree used for fast prefix matching (words, IP routing tables). Each node has character mapping edges and a boolean indicating the end of a word.
""",
        "examples": [
            {
                "title": "BST Validation",
                "code": """def isValidBST(root, low=float('-inf'), high=float('inf')) -> bool:
    if not root:
        return True
    if not (low < root.val < high):
        return False
    return isValidBST(root.left, low, root.val) and isValidBST(root.right, root.val, high)"""
            }
        ]
    },
    "graphs": {
        "title": "Shortest Paths & Connected Components",
        "concept": """
### Shortest Path Algorithms
1. **Dijkstra's Algorithm**:
   - Single source shortest path for graphs with non-negative edge weights.
   - Time Complexity: $O((V + E) \\log V)$ using a binary heap.
   - Greedy strategy: Always select the unvisited vertex with the minimum distance.

2. **Bellman-Ford Algorithm**:
   - Single source shortest path. Handles negative weights.
   - Detects negative weight cycles.
   - Time Complexity: $O(V \\cdot E)$.

3. **Floyd-Warshall Algorithm**:
   - All-pairs shortest path. Dynamic Programming approach.
   - Time Complexity: $O(V^3)$.

### Tarjan's Strongly Connected Components (SCC)
Finds maximal subgraphs where every vertex is reachable from any other vertex in the subgraph.
- Uses DFS with recursion stack.
- Assigns discovery times (`low` and `disc` links) to track back-edges.
- Runs in linear time $O(V + E)$.
""",
        "examples": [
            {
                "title": "Dijkstra Implementation",
                "code": """import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_dist > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances"""
            }
        ]
    },
    "dp": {
        "title": "Dynamic Programming & Optimization Patterns",
        "concept": """
### 0/1 Knapsack & Variances
Decide whether to include or exclude an item. The key state transition:
`dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i-1]] + val[i-1])`

### Longest Common Subsequence (LCS)
Compares two strings `s1` and `s2`:
- If `s1[i-1] == s2[j-1]`, then `dp[i][j] = 1 + dp[i-1][j-1]`
- Else, `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

### Longest Increasing Subsequence (LIS)
Can be solved in:
- $O(N^2)$ using simple state relation: `dp[i] = 1 + max(dp[j]) for j < i and arr[j] < arr[i]`
- $O(N \\log N)$ using Binary Search (patience sorting) where we maintain the active tails array.

### State Compression & Bitmask DP
When the set size is small (e.g., $N \\le 18$), we represent states as integers (bitmasks).
- Example: Travelling Salesperson Problem (TSP). State represents `(visited_mask, last_node)`.
""",
        "examples": [
            {
                "title": "LIS via Binary Search",
                "code": """import bisect

def lengthOfLIS(nums) -> int:
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)"""
            }
        ]
    }
}

DSA_PROBLEMS: List[Dict[str, Any]] = [
    {
        "id": "serialize_deserialize_tree",
        "title": "Serialize and Deserialize Binary Tree",
        "difficulty": "Hard",
        "description": """
Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Implement `Codec` class with two methods:
1. `serialize(root: TreeNode) -> str`: Serializes a tree to a single string.
2. `deserialize(data: str) -> TreeNode`: Deserializes your string data back to tree.

We use pre-order traversal representation where `'#'` represents null nodes.
""",
        "starter_code": """# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Codec:
    def serialize(self, root) -> str:
        # Write your code here
        return ""

    def deserialize(self, data: str):
        # Write your code here
        return None
""",
        "test_cases": [
            {
                "input": "[1,2,3,null,null,4,5]",
                "expected": "1,2,#,#,3,4,#,#,5,#,#",
            }
        ],
        "eval_script": """
# Predefined TreeNode class for runner
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Runner code
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.right.left = TreeNode(4)
root.right.right = TreeNode(5)

codec = Codec()
ser_data = codec.serialize(root)
new_root = codec.deserialize(ser_data)

# Test function
def check_tree(r1, r2):
    if not r1 and not r2:
        return True
    if not r1 or not r2:
        return False
    return r1.val == r2.val and check_tree(r1.left, r2.left) and check_tree(r1.right, r2.right)

passed = check_tree(root, new_root)
print("PASSED" if passed else "FAILED")
"""
    },
    {
        "id": "edit_distance",
        "title": "Edit Distance",
        "difficulty": "Hard",
        "description": """
Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.

You have the following three operations permitted on a word:
1. Insert a character
2. Delete a character
3. Replace a character

Write a function `minDistance(word1: str, word2: str) -> int`.
""",
        "starter_code": """class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        # Write your code here
        return 0
""",
        "test_cases": [
            {
                "input": 'word1 = "horse", word2 = "ros"',
                "expected": "3"
            },
            {
                "input": 'word1 = "intention", word2 = "execution"',
                "expected": "5"
            }
        ],
        "eval_script": """
sol = Solution()
t1 = sol.minDistance("horse", "ros") == 3
t2 = sol.minDistance("intention", "execution") == 5
t3 = sol.minDistance("", "") == 0
t4 = sol.minDistance("a", "b") == 1

passed = t1 and t2 and t3 and t4
print("PASSED" if passed else "FAILED")
"""
    },
    {
        "id": "merge_k_sorted_lists",
        "title": "Merge k Sorted Lists",
        "difficulty": "Hard",
        "description": """
You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

Implement `Solution.mergeKLists(lists: List[ListNode]) -> ListNode`.
""",
        "starter_code": """# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeKLists(self, lists):
        # Write your code here
        return None
""",
        "test_cases": [
            {
                "input": "[[1,4,5],[1,3,4],[2,6]]",
                "expected": "[1,1,2,3,4,4,5,6]"
            }
        ],
        "eval_script": """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_list(arr):
    dummy = ListNode()
    curr = dummy
    for x in arr:
        curr.next = ListNode(x)
        curr = curr.next
    return dummy.next

def to_arr(head):
    res = []
    curr = head
    while curr:
        res.append(curr.val)
        curr = curr.next
    return res

lists = [build_list([1,4,5]), build_list([1,3,4]), build_list([2,6])]
sol = Solution()
res_head = sol.mergeKLists(lists)
arr_res = to_arr(res_head)

passed = arr_res == [1,1,2,3,4,4,5,6]
print("PASSED" if passed else "FAILED")
"""
    }
]
