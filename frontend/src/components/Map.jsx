"use client";
import { useState } from "react";
import "../App.css";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { getLocationData } from "../utils";

export function Map() {
  const [position, setPosition] = useState([0.0, 0.0]);
  const [locationData, setLocationData] = useState(null);

  async function handleMapClick(e) {
    const { lat, lng } = e.latlng;
    setPosition([lat, lng]);
    const data = await getLocationData({ latitude: lat, longitude: lng });

    setLocationData({
      maxWaveHeight: data.max_wave_height,
      nearestLatitude: data.nearest_latitude,
      nearestLongitude: data.nearest_longitude,
    });
  }

  function MapEventsHandler({ position, handleMapClick }) {
    useMapEvents({
      click: (e) => handleMapClick(e),
    });
    return <Marker position={position}></Marker>;
  }

  return (
    <div className="container">
      <div className="header">
        {locationData ? (
          <p>{`Max wave height: ${locationData.maxWaveHeight} for location: (${locationData.nearestLatitude}, ${locationData.nearestLongitude})`}</p>
        ) : (
          <p>No location data available</p>
        )}
      </div>
      <div className="map-container">
        <MapContainer
          className="full-size"
          center={position}
          zoom={6}
          scrollWheelZoom={true}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapEventsHandler
            locationData={position}
            handleMapClick={handleMapClick}
          />
        </MapContainer>
      </div>
    </div>
  );
}
