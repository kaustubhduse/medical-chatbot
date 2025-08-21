import React, { useEffect, useState, useRef } from "react";
import { motion } from "framer-motion";
import { FiMapPin, FiNavigation } from "react-icons/fi";

// IMPORTANT: In a real-world app, store your API key in a .env file
// Example: const HERE_API_KEY = import.meta.env.VITE_HERE_API_KEY;
const HERE_API_KEY = "Um_xi7yD_DT5gx326WURVxpp1AFyb1dieK_mWx0MZV8";

// --- Skeleton Loader Component for a better loading experience ---
const SkeletonCard = () => (
    <div className="p-4 bg-white/5 rounded-xl animate-pulse">
        <div className="h-6 bg-slate-700 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-slate-700 rounded w-full"></div>
    </div>
);

const Search = () => {
    const [location, setLocation] = useState(null);
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(true);

    // Use a ref to hold the map instance to avoid re-renders
    const mapRef = useRef(null);
    const mapContainerRef = useRef(null);

    // --- Fetch user location and nearby hospitals on component mount ---
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
            (err) => {
                console.error("Error getting location:", err);
                setLoading(false);
                // You could also set a default location here
            }
        );
    }, []);

    const fetchNearbyDoctors = async (loc) => {
        setLoading(true);
        try {
            const { lat, lng } = loc;
            const response = await fetch(
                `https://discover.search.hereapi.com/v1/discover?at=${lat},${lng}&q=hospital&apiKey=${HERE_API_KEY}`
            );
            const data = await response.json();
            if (data.items) {
                setDoctors(data.items);
            }
        } catch (error) {
            console.error("Error fetching nearby doctors:", error);
        } finally {
            setLoading(false);
        }
    };

    // --- Initialize and update the HERE Map ---
    useEffect(() => {
        // Ensure the HERE Maps scripts are loaded and we have a location
        if (!window.H || !location || !mapContainerRef.current) {
            return;
        }

        const platform = new window.H.service.Platform({ apikey: HERE_API_KEY });
        const defaultLayers = platform.createDefaultLayers({
            // Use a dark map style to match the theme
            ppi: window.devicePixelRatio > 1 ? 320 : 72
        });

        // Initialize the map only once
        if (!mapRef.current) {
            const map = new window.H.Map(
                mapContainerRef.current,
                defaultLayers.vector.normal.map,
                {
                    center: location,
                    zoom: 14,
                    pixelRatio: window.devicePixelRatio || 1
                }
            );
            // Add map events and default UI
            new window.H.mapevents.Behavior(new window.H.mapevents.MapEvents(map));
            const ui = window.H.ui.UI.createDefault(map, defaultLayers);
            // Store the map instance in the ref
            mapRef.current = map;
        }

        const map = mapRef.current;
        // Clear previous markers before adding new ones
        map.removeObjects(map.getObjects());

        // --- Custom SVG Markers for a better look ---
        const userSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#4a90e2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>`;
        const hospitalSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="#f472b6" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`;

        const userIcon = new window.H.map.Icon(userSvg);
        const hospitalIcon = new window.H.map.Icon(hospitalSvg);

        // Add user marker
        const userMarker = new window.H.map.Marker(location, { icon: userIcon });
        map.addObject(userMarker);

        // Add hospital markers
        doctors.forEach((place) => {
            if (place.position) {
                const marker = new window.H.map.Marker(place.position, { icon: hospitalIcon });
                map.addObject(marker);
            }
        });

        // Set map center and zoom
        map.setCenter(location);
        map.setZoom(14);

        // Cleanup function to dispose of the map when the component unmounts
        return () => {
            if (mapRef.current) {
                mapRef.current.dispose();
                mapRef.current = null;
            }
        };
    }, [location, doctors]);

    return (
        <div className="relative min-h-screen flex flex-col items-center bg-slate-900 p-6 overflow-hidden">
            {/* Animated background shapes */}
            <div className="absolute top-0 -left-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-lighten filter blur-xl opacity-70 animate-blob"></div>
            <div className="absolute top-0 -right-4 w-72 h-72 bg-purple-500 rounded-full mix-blend-lighten filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>

            <motion.h1
                className="text-4xl md:text-5xl font-extrabold text-white mb-6 z-10"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                🏥 Nearby Hospitals
            </motion.h1>

            {/* Glassmorphism Map Container */}
            <motion.div
                ref={mapContainerRef}
                style={{ height: "40vh", width: "100%" }}
                className="w-full max-w-5xl bg-white/5 border border-white/20 shadow-2xl rounded-2xl z-10"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
            ></motion.div>

            <div className="w-full max-w-5xl mt-6 z-10">
                {loading ? (
                    <div className="space-y-4">
                        <SkeletonCard />
                        <SkeletonCard />
                        <SkeletonCard />
                    </div>
                ) : (
                    <motion.div
                        className="space-y-4"
                        initial="hidden"
                        animate="visible"
                        variants={{
                            visible: { transition: { staggerChildren: 0.1 } },
                        }}
                    >
                        {doctors.map((place, index) => (
                            <motion.div
                                key={index}
                                className="p-4 bg-white/5 border border-white/20 rounded-xl transition-all hover:border-pink-400 cursor-pointer"
                                variants={{
                                    hidden: { y: 20, opacity: 0 },
                                    visible: { y: 0, opacity: 1 },
                                }}
                            >
                                <h2 className="text-xl font-semibold text-white">{place.title}</h2>
                                <p className="text-gray-400 text-sm">{place.address.label}</p>
                                <a
                                    href={`https://wego.here.com/directions/mylocation/${place.position.lat},${place.position.lng}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-pink-400 hover:text-pink-300 font-medium inline-flex items-center gap-2 mt-2"
                                >
                                    <FiNavigation size={16} /> Get Directions
                                </a>
                            </motion.div>
                        ))}
                    </motion.div>
                )}
            </div>
        </div>
    );
};

export default Search;
