import tkinter as tk
from tkinter import filedialog, messagebox
from path import PlotPath

from graph import *
from test_graph import CreateGraph_1
#from airspace import AirSpace
from data_loader import load_navpoints, load_segments, load_airports
from graph import Graph, AddNode, AddSegment
from node import Node
import os
from kml_exporter import export_path_to_kml

class GraphApp:
    def __init__(self, root):
        self.airspace = None
        self.color_left_segments = None
        self.delete_segment_popup = None
        self.graph = Graph()
        self.root = root
        self.root.title("Explorador de Rutas Aéreas")
        self.create_widgets()
        self.ruta_actual= None

    def create_widgets(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Mostrar Grafo Ejemplo", command=self.load_example).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Mostrar Grafo Inventado", command=self.load_custom).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Cargar Grafo desde Archivo", command=self.load_from_file).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Guardar Grafo en Archivo", command=self.save_to_file).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Borrar Segmento", command=self.delete_segment_popup).grid(row=3, column=0, pady=5)

        tk.Label(frame, text="Nodo:").grid(row=1, column=0)
        self.node_entry = tk.Entry(frame)
        self.node_entry.grid(row=1, column=1)
        tk.Button(frame, text="Ver Vecinos", command=self.show_neighbors).grid(row=1, column=2, padx=5)


        tk.Button(frame, text="Añadir Nodo", command=self.add_node_popup).grid(row=2, column=0, pady=5)

        tk.Button(frame, text="Añadir Segmento", command=self.add_segment_popup).grid(row=2, column=1, pady=5)

        tk.Button(frame, text="Borrar Nodo", command=self.delete_node_popup).grid(row=2, column=2, pady=5)

        tk.Button(frame, text="Nuevo Grafo Vacío", command=self.new_graph).grid(row=2, column=3, pady=5)
        tk.Button(frame, text="Ver alcanzables", command=self.show_reachables).grid(row=4, column=0, pady=5)
        tk.Button(frame, text="Camino más corto", command=self.shortest_path_popup).grid(row=4, column=1, pady=5)
        tk.Button(frame, text="Cargar Airspace Catalunya", command=self.load_airspace).grid(row=5, column=0, pady=5)
        btn_google_earth = tk.Button(root, text="Mostrar en Google Earth", command=self.mostrar_en_google_earth)
        btn_google_earth.pack(pady=10)

    def load_example(self):
        plt.clf()
        self.graph = CreateGraph_1()
        Plot(self.graph)

    def load_custom(self):
        plt.clf()
        self.graph = CreateGraph_2()
        Plot(self.graph)

    def load_from_file(self):
        path = filedialog.askopenfilename(title="Selecciona archivo de grafo")
        if not path:
            return
        try:
            self.graph = LoadGraphFromFile(path)
            Plot(self.graph)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")


    def plot_airspace(self):
        """
        Dibuja el gráfico base del espacio aéreo de Catalunya.
        """
        import matplotlib.pyplot as plt
        plt.figure()

        if not self.airspace.navpoints:
            messagebox.showwarning("Advertencia", "No hay datos cargados para Catalunya.")
            return

        for nav in self.airspace.navpoints:
            plt.plot(nav.lon, nav.lat, 'o', color='blue')
            plt.text(nav.lon, nav.lat, nav.name)


        for seg in self.airspace.navsegments:
            x_vals = [seg.origin.lon, seg.destination.lon]
            y_vals = [seg.origin.lat, seg.destination.lat]
            plt.plot(x_vals, y_vals, color='gray', linestyle='-', alpha=0.7)

        plt.title("Espacio Aéreo de Catalunya")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.grid(alpha=0.3)
        plt.show()


    def mostrar_en_google_earth(self):
        global ruta_actual
        if not self.ruta_actual:
            messagebox.showinfo("Ruta no disponible", "Primero debes calcular una ruta.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".kml",
                                                filetypes=[("KML files", "*.kml")],
                                                title="Guardar archivo KML")
        if filename:
            export_path_to_kml(self.ruta_actual, filename)
            try:
                os.startfile(filename)  # Funciona en Windows
            except Exception:
                messagebox.showinfo("Archivo KML generado",
                                    f"Guardado en: {filename}\nÁbrelo manualmente si Google Earth no se abre.")



    def load_airspace(self):

        from graph import Graph, AddSegment
        from node import Node
        plt.clf()

        self.graph = Graph()
        id_to_node = {}

        try:

            navpoints = load_navpoints("Cat_nav.txt")
            for np in navpoints:
                node = Node(np['name'], np['lat'], np['lon'])
                AddNode(self.graph, node)
                id_to_node[np['id']] = node

            segments = load_segments("Cat_seg.txt")

            for seg in segments:
                origin = id_to_node.get(seg['origin_id'])
                dest = id_to_node.get(seg['dest_id'])

                if origin and dest:
                    segment_name = f"{origin.name}-{dest.name}"
                    AddSegment(self.graph, segment_name, origin.name, dest.name)


            self.plot_graph()
            messagebox.showinfo("Carga Completa", "Espacio aéreo de Cataluña cargado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def plot_graph(self):

        import matplotlib.pyplot as plt

        if not self.graph.nodes:
            messagebox.showwarning("Sin datos", "No hay datos cargados para mostrar.")
            return

        for node in self.graph.nodes:
            plt.plot(node.x, node.y, 'o', color='blue')
            plt.text(node.x, node.y, node.name)

        for segment in self.graph.segments:
            if segment.origin and segment.destination:
                x_vals = [segment.origin.x, segment.destination.x]
                y_vals = [segment.origin.y, segment.destination.y]
                plt.plot(x_vals, y_vals, color='gray', linestyle='-', alpha=0.7)

        plt.title("Espacio Aéreo de Cataluña - Todos los Segmentos Conectados")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.grid(alpha=0.3)
        plt.show()

    def save_to_file(self):
        path = filedialog.asksaveasfilename(title="Guardar grafo como", defaultextension=".txt")
        if not path:
            return
        try:
            with open(path, 'w') as f:
                f.write("[Nodes]\n")
                for n in self.graph.nodes:
                    f.write(f"{n.name} {n.x} {n.y}\n")
                f.write("[Segments]\n")
                for s in self.graph.segments:
                    f.write(f"{s.name} {s.origin.name} {s.destination.name}\n")
            messagebox.showinfo("Guardado", "Grafo guardado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    def show_neighbors(self):
        name = self.node_entry.get()
        if not PlotNode(self.graph, name):
            messagebox.showwarning("No encontrado", f"Nodo '{name}' no existe.")

    def add_node_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Añadir Nodo")
        tk.Label(win, text="Nombre").grid(row=0, column=0)
        tk.Label(win, text="X").grid(row=1, column=0)
        tk.Label(win, text="Y").grid(row=2, column=0)
        e1 = tk.Entry(win)
        e2 = tk.Entry(win)
        e3 = tk.Entry(win)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)

        def add():
            try:
                n = Node(e1.get(), float(e2.get()), float(e3.get()))
                if not AddNode(self.graph, n):
                    messagebox.showinfo("Duplicado", "Ya existe un nodo con ese nombre.")
                else:
                    messagebox.showinfo("Éxito", "Nodo añadido.")
                    win.destroy()
            except:
                messagebox.showerror("Error", "Datos inválidos.")

        tk.Button(win, text="Añadir", command=add).grid(row=3, columnspan=2)

    def add_segment_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Añadir Segmento")
        tk.Label(win, text="Nombre").grid(row=0, column=0)
        tk.Label(win, text="Origen").grid(row=1, column=0)
        tk.Label(win, text="Destino").grid(row=2, column=0)
        e1 = tk.Entry(win)
        e2 = tk.Entry(win)
        e3 = tk.Entry(win)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)

        def add():
            if not AddSegment(self.graph, e1.get(), e2.get(), e3.get()):
                messagebox.showerror("Error", "Segmento no válido. ¿Existen los nodos?")
            else:
                messagebox.showinfo("Éxito", "Segmento añadido.")
                win.destroy()

        tk.Button(win, text="Añadir", command=add).grid(row=3, columnspan=2)

    def delete_node_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Borrar Nodo")
        tk.Label(win, text="Nombre del Nodo").grid(row=0, column=0)
        e = tk.Entry(win)
        e.grid(row=0, column=1)

        def delete():
            name = e.get()
            node = next((n for n in self.graph.nodes if n.name == name), None)
            if not node:
                messagebox.showwarning("No encontrado", "Nodo no existe.")
                return
            self.graph.nodes.remove(node)
            self.graph.segments = [s for s in self.graph.segments if s.origin != node and s.destination != node]
            for n in self.graph.nodes:
                if node in n.neighbors:
                    n.neighbors.remove(node)
            messagebox.showinfo("Éxito", "Nodo y segmentos eliminados.")
            win.destroy()

        tk.Button(win, text="Eliminar", command=delete).grid(row=1, columnspan=2)

    def show_reachables(self):
        plt.clf()
        win = tk.Toplevel(self.root)
        win.title("Ver alcanzables directos")

        tk.Label(win, text="Nodo:").grid(row=0, column=0, padx=10, pady=5)
        entry_node = tk.Entry(win)
        entry_node.grid(row=0, column=1, padx=10, pady=5)

        def calculate_reachables():
            node_name = entry_node.get()


            start_node = next((n for n in self.graph.nodes if n.name == node_name), None)
            if not start_node:
                messagebox.showwarning("Nodo no encontrado", f"No se encontró el nodo '{node_name}'.")
                return

            reachable_nodes = start_node.neighbors

            import matplotlib.pyplot as plt


            for n in self.graph.nodes:
                color = "green" if n in reachable_nodes else "gray"
                plt.plot(n.x, n.y, 'o', color=color)
                plt.text(n.x, n.y, n.name)

            for s in self.graph.segments:
                x_vals = [s.origin.x, s.destination.x]
                y_vals = [s.origin.y, s.destination.y]

                color = "green" if (s.origin == start_node and s.destination in reachable_nodes) else "gray"
                plt.plot(x_vals, y_vals, color=color, linestyle='-', alpha=0.7)

            plt.title(f"Nodos directamente alcanzables desde '{node_name}'")
            plt.show()
            win.destroy()

        tk.Button(win, text="Ver alcanzables", command=calculate_reachables).grid(row=1, columnspan=2, pady=10)

    def shortest_path_popup(self):
        plt.clf()
        win = tk.Toplevel(self.root)
        win.title("Camino más corto")
        tk.Label(win, text="Origen").grid(row=0, column=0)
        tk.Label(win, text="Destino").grid(row=1, column=0)
        e1 = tk.Entry(win)
        e2 = tk.Entry(win)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        def calc():
            path = FindShortestPath(self.graph, e1.get(), e2.get())
            if path:
                self.ruta_actual = path
                PlotPath(self.graph, path)
            else:
                messagebox.showwarning("Sin camino", "No hay camino posible.")
            win.destroy()

        tk.Button(win, text="Buscar", command=calc).grid(row=2, columnspan=2)

    def new_graph(self):
        self.graph = Graph()
        messagebox.showinfo("Nuevo", "Grafo vacío creado.")


def CreateGraph_2():
    G = Graph()
    AddNode(G, Node("X", 1, 1))
    AddNode(G, Node("Y", 4, 1))
    AddNode(G, Node("Z", 2.5, 4))
    AddSegment(G, "XY", "X", "Y")
    AddSegment(G, "YZ", "Y", "Z")
    AddSegment(G, "ZX", "Z", "X")
    return G

def delete_segment_popup(self):
    win = tk.Toplevel(self.root)
    win.title("Borrar Segmento")
    tk.Label(win, text="Nombre del Segmento").grid(row=0, column=0)
    e = tk.Entry(win)
    e.grid(row=0, column=1)

    def delete():
        name = e.get()
        found = False
        for s in self.graph.segments:
            if s.name == name:
                self.graph.segments.remove(s)
                if s.destination in s.origin.neighbors:
                    s.origin.neighbors.remove(s.destination)
                found = True
                break
        if found:
            messagebox.showinfo("Eliminado", "Segmento eliminado.")
        else:
            messagebox.showwarning("No encontrado", "Segmento no existe.")
        win.destroy()

    tk.Button(win, text="Eliminar", command=delete).grid(row=1, columnspan=2)



if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
