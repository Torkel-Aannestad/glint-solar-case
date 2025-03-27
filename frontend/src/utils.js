import { API_URL_DEV } from "./constants";
export async function getLocationData({ latitude, longitude }) {
  const response = await fetch(`${API_URL_DEV}/location-data`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      lat: latitude,
      lng: longitude,
    }),
  });

  if (!response.ok) {
    return null;
  }

  const data = await response.json();
  return data;
}
