from flask import Flask, render_template,request
import csv
import pandas as pd
import heapq
import folium
app = Flask(__name__)
path=[]
@app.route('/',methods=['get','post'])
def index():
    
    city1="X"
    city2="X"
    if request.method=='POST':

        city1=request.form.get('city1')
        city2=request.form.get('city2')

        
# Class representing the graph
        class Graph:
            def __init__(self, graph_dict=None, directed=True):
                self.graph_dict = graph_dict or {}
                self.directed = directed
                if not directed:
                    self.make_undirected()

            # Method to make the graph undirected by adding reverse edges
            def make_undirected(self):
                for a in list(self.graph_dict.keys()):
                    for (b, dist) in self.graph_dict[a].items():
                        self.graph_dict.setdefault(b, {})[a] = dist

            # Method to connect two cities with a given distance
            def connect(self, A, B, distance=1):
                self.graph_dict.setdefault(A, {})[B] = distance
                if not self.directed:
                    self.graph_dict.setdefault(B, {})[A] = distance

            # Method to get neighbors of a city
            def get(self, a, b=None):
                links = self.graph_dict.setdefault(a, {})
                if b is None:
                    return links
                else:
                    return links.get(b)

        # Function to read data from CSV file
        def read_csv(filename):
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                data = [row for row in reader]
            return data

        
        def extract_graph(data):
            graph = Graph()
            for row in data:
                origin, destination, distance = row
                try:
                    graph.connect(origin, destination, float(distance))
                except ValueError:
                    continue
            return graph


        
        def heuristic(city, end_city):
            return 0

        
        def astar_search(graph, start, end):
            open_list = []  
            heapq.heappush(open_list, (0, start, []))  
            visited = set() 

            while open_list:
                cost, current_city, path = heapq.heappop(open_list)  
                if current_city == end: 
                    path.append(current_city)
                    return path, cost

                if current_city not in visited:
                    visited.add(current_city) 
                    for neighbor, distance in graph.get(current_city).items():  
                        total_cost = cost + distance + heuristic(neighbor, end)  
                        heapq.heappush(open_list, (total_cost, neighbor, path + [current_city])) 

            return None, float('inf') 
        def createMap(path1):
            data=pd.read_csv('CitiesCoordinates.csv')

            
            city_map = folium.Map(location=[data['Latitude'][0], data['Longitude'][0]], zoom_start=5)

           
            for i, row in data.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=row['CityName']
                ).add_to(city_map)

           
            for i in range(len(path)-1):
                coordinates = [
                    [data[data['CityName'] == path1[i]]['Latitude'].values[0],data[data['CityName'] == path1[i]]['Longitude'].values[0]],
                    [data[data['CityName'] == path1[i+1]]['Latitude'].values[0],data[data['CityName'] == path1[i+1]]['Longitude'].values[0]]
                ]
                folium.PolyLine(
                    locations=coordinates,
                    color='blue'
                ).add_to(city_map)

 
            city_map.save('templates/city_map_withLines.html')
                        
        def main1():
           
            data = read_csv('citieDistanceMofified.csv')
            graph = extract_graph(data)

            start_city =city1
            end_city = city2

            if start_city is None or end_city is None:
                
                print("Error: Please select both start and destination cities.")
            elif start_city == end_city:
                
                print("Error: Start and destination cities cannot be the same.")
            else:
                global path
                path=[]
                path, total_distance = astar_search(graph, start_city, end_city)
                createMap(path)
        
        main1()
    return render_template('index.html')
@app.route('/showMap')
def shMap():
    
    return render_template('city_map_withLines.html')
if __name__ == '__main__':
    app.run(debug=True)
