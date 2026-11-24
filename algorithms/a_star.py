
import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0

        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            goal_index = tile - 1

            current_row, current_col = divmod(index, 3)
            goal_row, goal_col = divmod(goal_index, 3)

            distance += abs(current_row - goal_row) + abs(current_col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        frontier = []
        heapq.heappush(frontier, (self.heuristic(initial), initial))

        visited = {}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, current = heapq.heappop(frontier)

            if current.tiles in visited and visited[current.tiles] <= current.cost:
                continue

            visited[current.tiles] = current.cost

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current.actions())
                )

            nodes_expanded += 1

            for neighbor in current.neighbors():
                if neighbor.tiles not in visited or neighbor.cost < visited[neighbor.tiles]:
                    priority = neighbor.cost + self.heuristic(neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size
        )
