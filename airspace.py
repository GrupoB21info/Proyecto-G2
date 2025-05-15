from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

class AirSpace:
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.airports = []

    def load_navpoints(self, filename):
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 4:
                        number, name, lat, lon = parts
                        navpoint = NavPoint(number, name, lat, lon)
                        self.navpoints.append(navpoint)
        except Exception as e:
            print(f"Error loading navpoints: {e}")

    def load_segments(self, filename):
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        origin_num, dest_num, distance = parts
                        origin = next((n for n in self.navpoints if n.number == origin_num), None)
                        dest = next((n for n in self.navpoints if n.number == dest_num), None)
                        if origin and dest:
                            segment = NavSegment(origin, dest, float(distance))
                            self.navsegments.append(segment)
                            origin.neighbors.append(dest)
        except Exception as e:
            print(f"Error loading segments: {e}")

    def load_airports(self, filename):
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 1:
                        airport_name = parts[0]
                        sids = parts[1::2]
                        stars = parts[2::2]
                        airport = NavAirport(airport_name, sids, stars)
                        self.airports.append(airport)
        except Exception as e:
            print(f"Error loading airports: {e}")

    def load_all(self, nav_file, seg_file, aer_file):
        self.load_navpoints(nav_file)
        self.load_segments(seg_file)
        self.load_airports(aer_file)
