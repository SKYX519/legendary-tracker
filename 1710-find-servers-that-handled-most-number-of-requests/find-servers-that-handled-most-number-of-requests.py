import heapq

class Solution:
    def busiestServers(self, k, arrival, load):

        # Segment tree
        size = 1
        while size < k:
            size *= 2

        tree = [0] * (2 * size)

        # Initially, all servers are available
        for i in range(k):
            tree[size + i] = 1

        for i in range(size - 1, 0, -1):
            tree[i] = tree[2 * i] + tree[2 * i + 1]

        # Update server availability
        def update(pos, value):
            pos += size
            tree[pos] = value

            pos //= 2

            while pos:
                tree[pos] = tree[2 * pos] + tree[2 * pos + 1]
                pos //= 2

        # Find first available server >= start
        def find(start):
            def search(node, left, right):
                if right <= start or tree[node] == 0:
                    return -1

                if right - left == 1:
                    return left

                mid = (left + right) // 2

                result = search(node * 2, left, mid)

                if result != -1:
                    return result

                return search(node * 2 + 1, mid, right)

            return search(1, 0, size)

        busy = []
        count = [0] * k

        for i in range(len(arrival)):

            # Release completed servers
            while busy and busy[0][0] <= arrival[i]:
                end_time, server = heapq.heappop(busy)
                update(server, 1)

            # All servers are busy
            if tree[1] == 0:
                continue

            # Find next available server
            server = find(i % k)

            # Wrap around if necessary
            if server == -1:
                server = find(0)

            # Assign request
            count[server] += 1
            update(server, 0)

            heapq.heappush(
                busy,
                (arrival[i] + load[i], server)
            )

        # Find busiest servers
        maximum = max(count)

        return [
            i for i in range(k)
            if count[i] == maximum
        ]