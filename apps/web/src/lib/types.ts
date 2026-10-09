// Mirrors the API's response models in apps/api/src/sailprep_api/schemas.py.

export interface Venue {
  name: string;
  latitude: number;
  longitude: number;
  timezone: string;
}

export type BoatType = "dinghy" | "foiler" | "keelboat";

export interface BoatClass {
  key: string;
  name: string;
  type: BoatType;
  crew: number;
  min_wind_kt: number;
  max_wind_kt: number;
  heavy_air_kt: number;
  foiling_kt: number | null;
}

export interface Conditions {
  wind_mean_kt: number;
  wind_min_kt: number;
  wind_max_kt: number;
  gust_max_kt: number;
  gust_factor: number;
  direction_mean_deg: number;
  direction_label: string;
  direction_spread_deg: number;
  temp_min_c: number;
  temp_max_c: number;
  precipitation_mm: number;
}

export interface Hour {
  time: string;
  in_race_window: boolean;
  wind_speed_kt: number;
  wind_gust_kt: number;
  wind_direction_deg: number;
  direction_label: string;
  temperature_c: number;
  precipitation_mm: number;
}

export interface Brief {
  venue: Venue;
  boat: BoatClass;
  date: string;
  start: string;
  end: string;
  discipline: string;
  conditions: Conditions;
  heads_ups: string[];
  hours: Hour[];
  source: { provider: string; fetched_at: string };
}

export interface BriefQuery {
  venue: string;
  boat: string;
  date: string;
  start: string;
  end: string;
  lat?: string;
  lon?: string;
}
