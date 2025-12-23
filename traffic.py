# Archipelago Project
# reads city population and road network data from text files.
# Creates graph of cities connected by highways and performs several tasks:
# 1. Create City objects
# 2. Build graph connections
# 3. Find number of islands
# 4. Find total population of each island
# 5. Find shortest path between two cities

import collections
import os
from typing import List, Dict, Tuple

# Task 1

class City:
    """
    Represents a city within the archipelago.
    Fields:
        name (str): Name of the city.
        population (int): Population of the city.
        connections (List['City']): List of connected City objects (modeling the highway).
    """

# Every city has a name, a population, and knows the other cities it is connected to
    def __init__(self, name: str, population: int):
        self.name: str = name
        self.population: int = population
        self.connections: List[City] = []
        self.visited: bool = False 
   
# Basically,if City A has an edge to City B, then City B will have an edge back to City A

    def add_connection(self, city_obj: 'City'):
        """Adds a bi-directional connection to another city object."""
        if city_obj not in self.connections:
            self.connections.append(city_obj)
# Used later to turn visited status off after traversals (DFS/BFS)

    def reset_visited(self):
        """Resets the visited flag for subsequent traversals."""
        self.visited = False
# Helpful for debugging and printing

    def __repr__(self):
        return f"City(Name='{self.name}', Pop={self.population:,})"


# Task 2

# Reads the given text file and returns its contents as a string
# If there is no such file, it prints an error messag

def read_file_content(filepath: str) -> str:
    """
    Helper function to read content from a specified file path.
    Raises FileNotFoundError if the file is missing.
    """
    print(f"Attempting to read file: {filepath}")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Required file not found: {filepath}")
        
    with open(filepath, 'r') as f:
        return f.read()
# This function creates all the City objects and connects them using the data
# from the population and road text files

def build_graph(pop_data: str, road_data: str) -> List[City]:
    """
    Reads population and road data (as strings) to construct the graph of City objects.
    Returns a list of all City objects.
    """
    # 1. Parse population and create City objects
    city_map: Dict[str, City] = {}
    # Step 1: Go through population data and make City objects

    for line in pop_data.split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            name, pop_str = line.split(' : ') 
            name = name.strip()
            population = int(pop_str.strip())
            city_map[name] = City(name, population)
        except ValueError:
            continue

    # Step 2: Go through road network and connect the cities

    for line in road_data.split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            city1_name, city2_name = line.split(' : ')
            city1_name = city1_name.strip()
            city2_name = city2_name.strip()
            
            if city1_name in city_map and city2_name in city_map:
                city1 = city_map[city1_name]
                city2 = city_map[city2_name]
                
                city1.add_connection(city2)
                city2.add_connection(city1)
                
        except ValueError:
            continue
            
    return list(city_map.values())


# Task 3 
# This function counts how many separate islands (groups of connected cities) there are.
# Basically how many connected components exist in the graph.

def number_of_islands(city_objects: List[City]) -> int:
    """
    Returns the number of islands (connected components) in the graph.
    """
    for city in city_objects:
        city.reset_visited()
        
    num_islands = 0
    # Start a DFS from this city and mark all reachable cities as visited
    for city in city_objects:
        if not city.visited:
            _depth_first_search(city)
            num_islands += 1
            
    return num_islands


# Task 4
# This function finds the population of each island (connected component).
# It runs DFS and sums up the population of all cities in each group.

def island_populations(city_objects: List[City]) -> List[int]:
    """
    Returns a list of the population of each island (connected component).
    """
    for city in city_objects:
        city.reset_visited()
    # Perform DFS to get total population of this island
    populations: List[int] = []
    for city in city_objects:
        if not city.visited:
            total_pop = _depth_first_search(city)
            populations.append(total_pop)
            
    return populations

# Helper DFS function to explore all connected cities
# Returns total population for that island

def _depth_first_search(start_city: City) -> int:
    """
    Private helper: DFS to mark visited and sum population of component.
    """
    if start_city.visited:
        return 0
    
    stack: List[City] = [start_city]
    start_city.visited = True
    island_population = start_city.population
    # Use a stack for DFS (iterative version)
    while stack:
    # Visit all neighbors of the current city
        city = stack.pop()
        for neighbor in city.connections:
            if not neighbor.visited:
                neighbor.visited = True
                island_population += neighbor.population
                stack.append(neighbor)
                
    return island_population


# Task 5
# This function finds the minimum number of highways needed to go
# from one city to another using Breadth First Search (BFS).
# Returns -1 if there's no route.

def min_highways(start_city: City, end_city: City) -> int:
    """
    Returns the minimum number of unique highways between two cities using BFS.
    Returns -1 if not reachable.
    """
    if start_city == end_city:
        return 0
# Use a queue for BFS traversal
    queue: collections.deque[Tuple[City, int]] = collections.deque([(start_city, 0)])
    visited: set[City] = {start_city} 
    while queue:
    # Check all directly connected cities (neighbors)
        current_city, distance = queue.popleft()
        # If we reach the destination city, return distance + 1
        for neighbor in current_city.connections:
            if neighbor == end_city:
                return distance + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
                
    return -1




POPULATION_FILE = 'city_population.txt'
ROAD_NETWORK_FILE = 'road_network-1.txt' 

# Main part of the program
# Reads data files, builds the graph, and prints out all results for each task

if __name__ == '__main__':
    print("--- Archipelago Graph Analysis Start ---")
    # Try reading both text files, exit if not found.
    try:
        pop_content = read_file_content(POPULATION_FILE)
        road_content = read_file_content(ROAD_NETWORK_FILE)
        
    except FileNotFoundError as e:
        print(f"\nFATAL ERROR: {e}. Please ensure the files exist in the current directory.")
        exit(1)
 
    # Task 2 

    city_list = build_graph(pop_content, road_content)
    print(f"\nTask 2 Result: Graph built with {len(city_list)} cities.")
    
    # Task 3 

    num_islands = number_of_islands(city_list)
    print(f"\nTask 3 Result: The Archipelago has {num_islands} islands (connected components).")
    
    # Task 4 

    islands_pop = island_populations(city_list)
    print("\nTask 4 Result: Population of Each Island (Sorted by Size):")
    for i, pop in enumerate(sorted(islands_pop, reverse=True)):
        print(f"  Island {i+1}: {pop:,} (Total population of the component)")

    # Task 5 

    print("\n--- Task 5: Shortest Path Examples ---")
    
    city_map: Dict[str, City] = {city.name: city for city in city_list}
    
    start1, end1 = "Washington", "Detroit" 
    if start1 in city_map and end1 in city_map:
        distance1 = min_highways(city_map[start1], city_map[end1])
        print(f"Min highways from {start1} to {end1} is: {distance1}")
    
    start2, end2 = "Los Angeles", "San Diego"
    if start2 in city_map and end2 in city_map:
        distance2 = min_highways(city_map[start2], city_map[end2])
        print(f"Min highways from {start2} to {end2} is: {distance2}")
    
    start3, end3 = "New York", "Oro Valley"
    if start3 in city_map and end3 in city_map:
        distance3 = min_highways(city_map[start3], city_map[end3])
        print(f"Min highways from {start3} to {end3} is: {distance3}")
    
    print("\n--- Archipelago Graph Analysis Complete ---")
    # End of the program
