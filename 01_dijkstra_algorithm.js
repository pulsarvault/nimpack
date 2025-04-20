// Rohit: Dijkstra Algorithm for Path Finding

// First create a simulated min-heap priority queue
class PriorityQueue {
  constructor() {
    this.queue = [];
  }

  enqueue(node, priority) {
    this.queue.push({ node, priority });
    this.queue.sort((a, b) => a.priority - b.priority);
  }

  dequeue() {
    return this.queue.shift()?.node;
  }

  isEmpty() {
    return this.queue.length === 0;
  }
}

// Graph class with adjacency list using Map
class Graph {
  constructor() {
    this.adjacencyList = new Map();
  }

  addVertex(vertex) {
    if (!this.adjacencyList.has(vertex)) {
      this.adjacencyList.set(vertex, new Map());
    }
  }

  addEdge(source, target, weight) {
    this.addVertex(source);
    this.addVertex(target);
    this.adjacencyList.get(source).set(target, weight);
    this.adjacencyList.get(target).set(source, weight); // Undirected graph both ways connected
  }

  dijkstra(start, end) {
    const distances = new Map();
    const previous = new Map();
    const pq = new PriorityQueue();

    // Initialize distances
    for (const vertex of this.adjacencyList.keys()) {
      distances.set(vertex, Infinity);
      previous.set(vertex, null);
    }
    distances.set(start, 0);
    pq.enqueue(start, 0);

    while (!pq.isEmpty()) {
      const current = pq.dequeue();

      if (current === end) break;

      for (const [neighbor, weight] of this.adjacencyList.get(current)) {
        const alt = distances.get(current) + weight;
        
        if (alt < distances.get(neighbor)) {
          distances.set(neighbor, alt);
          previous.set(neighbor, current);
          pq.enqueue(neighbor, alt);
        }
      }
    }

    return {
      distance: distances.get(end),
      path: this.#reconstructPath(previous, end)
    };
  }

// this is a private method hence hash
  #reconstructPath(previous, end) {
    const path = [];
    let current = end;
    
    while (current !== null) {
      path.unshift(current);
      current = previous.get(current);
    }
    
    return path.length === 1 ? [] : path;
  }
}
