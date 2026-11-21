class Solution:
    def findSubtreeSizes(self, parent, s):

        n = len(parent)

        # Build original tree
        children = [[] for _ in range(n)]

        for i in range(1, n):
            children[parent[i]].append(i)

        # Store nearest ancestor for each character
        last = {}

        new_parent = parent[:]

        def dfs(node):

            char = s[node]

            old_parent = last.get(char, -1)

            if old_parent != -1:
                new_parent[node] = old_parent

            last[char] = node

            for child in children[node]:
                dfs(child)

            # Restore previous ancestor
            if old_parent == -1:
                del last[char]
            else:
                last[char] = old_parent

        dfs(0)

        # Build modified tree
        new_children = [[] for _ in range(n)]

        for i in range(1, n):
            new_children[new_parent[i]].append(i)

        # Calculate subtree sizes
        answer = [1] * n

        def calculate(node):

            for child in new_children[node]:
                calculate(child)
                answer[node] += answer[child]

        calculate(0)

        return answer