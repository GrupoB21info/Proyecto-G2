from airspace import AirSpace

def test_airspace():
    airspace = AirSpace()
    airspace.load_navpoints("Cat_nav.txt")
    airspace.load_segments("Cat_seg.txt")
    airspace.load_airports("Cat_aer.txt")

    print(f"NavPoints: {len(airspace.navpoints)}")
    print(f"Segments: {len(airspace.navsegments)}")
    print(f"Airports: {len(airspace.airports)}")

test_airspace()
