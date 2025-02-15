import React, { useEffect, useState } from "react";

const HERE_API_KEY = "Um_xi7yD_DT5gx326WURVxpp1AFyb1dieK_mWx0MZV8";

const containerStyle = {
  width: "100%",
  height: "500px",
};

const Search = () => {
  const [location, setLocation] = useState(null);
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const userLocation = {
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        };
        setLocation(userLocation);
        fetchNearbyDoctors(userLocation);
      },
      (err) => console.error("Error getting location:", err)
    );
  }, []);

  const fetchNearbyDoctors = async (loc) => {
    try {
      const { lat, lng } = loc;
      const response = await fetch(
        `https://discover.search.hereapi.com/v1/discover?at=${lat},${lng}&q=hospital&apiKey=${HERE_API_KEY}`
      );

      const data = await response.json();

      if (data.items) {
        setDoctors(data.items);
      } else {
        console.warn("No results found.");
      }
    } catch (error) {
      console.error("Error fetching nearby doctors:", error);
    }
  };

  useEffect(() => {
    if (window.H && location) {
      const platform = new window.H.service.Platform({ apikey: HERE_API_KEY });
      const defaultLayers = platform.createDefaultLayers();

      const mapContainer = document.getElementById("mapContainer");
      if (!mapContainer) return;

      const map = new window.H.Map(
        mapContainer,
        defaultLayers.vector.normal.map,
        {
          center: { lat: location.lat, lng: location.lng },
          zoom: 14,
        }
      );

      // Enable interaction
      new window.H.mapevents.Behavior(new window.H.mapevents.MapEvents(map));
      window.H.ui.UI.createDefault(map, defaultLayers);

      // Add marker for user location
      const userMarker = new window.H.map.Marker(location);
      map.addObject(userMarker);

      // Add markers for hospitals
      doctors.forEach((place) => {
        if (place.position) {
          const marker = new window.H.map.Marker({
            lat: place.position.lat,
            lng: place.position.lng,
          });
          map.addObject(marker);
        }
      });

      return () => map.dispose();
    }
  }, [location, doctors]);

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">
        🏥 Nearby Hospitals & Doctors
      </h1>

      {/* HERE Map */}
      <div
        id="mapContainer"
        style={containerStyle}
        className="w-full max-w-4xl border border-gray-300 shadow-lg rounded-lg"
      ></div>

      {/* Nearby Doctors List */}
      <div className="bg-white shadow-md rounded-lg p-4 w-full max-w-3xl mt-6">
        {doctors.length === 0 ? (
          <p className="text-gray-600">Fetching nearby hospitals...</p>
        ) : (
          doctors.map((place, index) => (
            <div key={index} className="p-3 border-b border-gray-300">
              <h2 className="text-xl font-semibold">{place.title}</h2>
              <p className="text-gray-600">{place.address.label}</p>
              <a
                href={`https://wego.here.com/directions/mylocation/${place.position.lat},${place.position.lng}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 underline"
              >
                View on HERE Maps
              </a>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Search;
