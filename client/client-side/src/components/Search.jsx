import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

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

      new window.H.mapevents.Behavior(new window.H.mapevents.MapEvents(map));
      window.H.ui.UI.createDefault(map, defaultLayers);

      const userMarker = new window.H.map.Marker(location);
      map.addObject(userMarker);

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
      <motion.h1
        className="text-3xl md:text-4xl font-bold text-blue-600 mb-4"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        🏥 Nearby Hospitals & Doctors
      </motion.h1>

      <motion.div
        id="mapContainer"
        style={containerStyle}
        className="w-full max-w-4xl border border-gray-300 shadow-lg rounded-lg"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      ></motion.div>

      <motion.div
        className="bg-white shadow-md rounded-lg p-4 w-full max-w-3xl mt-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        {doctors.length === 0 ? (
          <p className="text-gray-600 text-center animate-pulse">
            Fetching nearby hospitals...
          </p>
        ) : (
          doctors.map((place, index) => (
            <motion.div
              key={index}
              className="p-4 border border-blue-200 bg-white shadow-lg rounded-xl transition-all 
            hover:shadow-xl flex flex-col gap-2"
              whileHover={{
                scale: 1.05,
                boxShadow: "0px 10px 15px rgba(0, 0, 0, 0.1)",
              }}
            >
              <h2 className="text-xl font-semibold text-gray-800">
                {place.title}
              </h2>
              <p className="text-gray-600">{place.address.label}</p>
              <a
                href={`https://wego.here.com/directions/mylocation/${place.position.lat},${place.position.lng}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 underline hover:text-blue-700 font-medium"
              >
                View on HERE Maps
              </a>
            </motion.div>
          ))
        )}
      </motion.div>
    </div>
  );
};

export default Search;
