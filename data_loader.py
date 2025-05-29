def load_navpoints(filename):

    navpoints = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue

            parts = line.split()
            if len(parts) >= 4:
                id_ = parts[0]
                name = parts[1]
                try:
                    lat = float(parts[2])
                    lon = float(parts[3])
                except ValueError:
                    continue
                navpoints.append({'id': id_, 'name': name, 'lat': lat, 'lon': lon})
    return navpoints

def load_segments(filename):

    segments = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():

                continue

            parts = line.split()
            if len(parts) >= 3:
                origin_id = parts[0]
                dest_id = parts[1]
                try:
                    distance = float(parts[2])
                except ValueError:
                    continue
                segments.append({'origin_id': origin_id, 'dest_id': dest_id, 'distance': distance})
    return segments

def load_airports(filename):

    airports = []
    with open(filename, 'r', encoding='utf-8') as f:
        current_airport = None
        sids = []
        stars = []

        for line in f:
            line = line.strip()
            if not line or line.startswith('·') or line.lower().startswith('airports'):
                continue

            if line.isupper() and len(line) <= 5:
                if current_airport:
                    airports.append({'name': current_airport, 'SIDs': sids, 'STARs': stars})
                current_airport = line
                sids = []
                stars = []
                continue

            if 'D' in line and '.' in line:
                sids.append(line)
            elif 'A' in line and '.' in line:
                stars.append(line)


        if current_airport:
            airports.append({'name': current_airport, 'SIDs': sids, 'STARs': stars})

    return airports



