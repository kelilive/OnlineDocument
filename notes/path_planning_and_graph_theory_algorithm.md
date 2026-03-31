# Path Planning & Graph Theory Algorithm Technical Manual (Universal Engineering Perspective)

---

## 1. The Unified Algorithm Comparison Matrix
This table provides a cross-dimensional comparison of 7 core algorithms regarding their search logic, design philosophy, underlying data structures, and outcome characteristics.

| Algorithm | Search Form (AI Perspective) | Design Philosophy (CS Perspective) | Core Data Structure | Goal / Result Type |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | Uninformed Search | Exhaustive Method | **Queue** | Optimal least-hops for unweighted graphs |
| **Dijkstra** | Uninformed Search | Greedy + Dynamic Programming | **Priority Queue (Min-Heap)** | Strictly optimal single-source path for weighted graphs |
| **A\* (A-Star)** | Heuristic / Informed | Branch and Bound | **Priority Queue + Hash Table** | Optimal path guided by heuristic estimation |
| **IDA\*** | Heuristic / Informed | Backtracking + Branch & Bound | **Stack / Recursion** | Optimal depth search with extreme memory efficiency |
| **Greedy BFS** | Heuristic / Informed | Greedy Algorithm | **Priority Queue (Min-Heap)** | Sub-optimal feasible solution (extremely fast) |
| **Bellman-Ford**| Uninformed Search | Dynamic Programming | **Array / Adjacency List** | Strictly optimal path supporting negative weights |
| **Floyd-Warshall**| Uninformed Search | Dynamic Programming | **2D Matrix** | All-pairs shortest paths (Multi-to-Multi matrix) |

---

## 2. Data-Centric Classification
Classification based on the underlying containers and memory characteristics the algorithms rely on during execution:

* **Heap/Priority Queue-Driven:**
    * **Algorithms:** Dijkstra, **A\***, Greedy BFS.
    * **Logic:** Dynamically maintains an "Open List," utilizing the $O(\log n)$ efficiency of a Min-Heap to extract the node with the lowest current cost. This is the industrial standard for processing weighted paths (e.g., length, pressure drop, cost).
* **Linear/Stack-Driven:**
    * **Algorithms:** BFS (Queue-based), **IDA\*** (Stack-based).
    * **Logic:** BFS memory consumption grows with search width; conversely, IDA* reduces space complexity to linear $O(d)$ via a stack structure. When dealing with massive industrial models with tens of millions of nodes, stack-driven types are critical to preventing memory overflow.
* **Array/Matrix-Driven:**
    * **Algorithms:** Bellman-Ford (Array), Floyd-Warshall (Matrix).
    * **Logic:** Utilizes contiguous memory space to store states. Floyd-Warshall specifically relies on a static $V \times V$ matrix, making it ideal for pre-calculating distances between any two points in systems with fixed node counts.

---

## 3. Complexity & Engineering Performance Parameters
| Algorithm | Time Complexity (Typical) | Space Complexity | Topological Adaptability | Memory Pressure |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | $O(V + E)$ | $O(V)$ | Sparse Graphs (Adj. List) | Medium |
| **Dijkstra** | $O(E \log V)$ | $O(V)$ | Sparse Graphs (Adj. List) | Medium |
| **A\*** | $O(b^d)$ | $O(V)$ | Sparse Graphs + Spatial Index | High |
| **IDA\*** | $O(b^d)$ | **$O(d)$** | Sparse Graphs (Extreme Depth) | **Very Low** |
| **Greedy BFS** | $O(b^d)$ | $O(V)$ | Sparse Graphs (Quick Preview) | Medium |
| **Bellman-Ford** | $O(VE)$ | $O(V)$ | Edge Lists (Supports Neg. Weights)| Low |
| **Floyd-Warshall** | $O(V^3)$ | **$O(V^2)$** | Dense Graphs (Fully Connected) | **Very High** |

---

## 4. Engineering Practice: Application Scenario Mapping

### A. System Topology & Connectivity Analysis
* **BFS:** Used for finding **logical connectivity**. Example: Counting the minimum number of fittings/valves traversed from a water source to a terminal in an MEP (Mechanical, Electrical, Plumbing) system.
* **Bellman-Ford:** Used for **logical conflict detection**. In complex energy flow analysis, identifying "negative cost cycles" that could cause algorithms to fail.
* **Floyd-Warshall:** Used for **global static indexing**. Pre-calculating a fixed distance table from all emergency exits to any room in large-scale factories or airport terminals.

### B. Automated Routing & Geometric Pathfinding (Obstacle Avoidance)
* **A\* (Standard Recommendation):** **Obstacle-avoiding pathfinding**. Generating optimal physical paths for pipes, cable trays, or conduits while considering collisions with structural components.
* **Greedy BFS:** **High-performance real-time interaction**. Providing an instantaneous (millisecond-level) preview guide line when a user drags a component, where absolute optimality is not required.

### C. Physical Performance & Extreme Scale Computation
* **Dijkstra:** **Complex weighted system analysis**. In water supply or ventilation networks, using resistance, diameter, and flow velocity costs as weights to find the most unfavorable loop with the maximum pressure drop.
* **IDA\*:** **Large-scale pathfinding in constrained environments**. Finding paths in refined point cloud data or massive BIM models containing millions of elements, leveraging its linear space advantage to avoid system crashes.