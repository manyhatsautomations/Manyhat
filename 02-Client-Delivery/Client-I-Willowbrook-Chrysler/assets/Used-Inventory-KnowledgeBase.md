# Willowbrook Chrysler - Used Vehicle Inventory (Optimized for AI)

## Inventory Metadata
- **Total Units**: 207 vehicles
- **Price Policy**: All units listed as "Call for pricing"
- **Location**: Langley, Surrey (All vehicles)
- **Last Updated**: 2026-03-06

## Make Distribution (Top 10)
- **Jeep**: 42 units (Avg: 49,112km, Years: 2000-2026
- **RAM**: 41 units (Avg: 53,484km, Years: 2018-2024
- **Dodge**: 27 units (Avg: 40,228km, Years: 2007-2025
- **Hyundai**: 18 units (Avg: 55,796km, Years: 2016-2025
- **Ford**: 15 units (Avg: 50,781km, Years: 2017-2024
- **Nissan**: 14 units (Avg: 49,812km, Years: 2016-2025
- **Kia**: 11 units (Avg: 60,009km, Years: 2016-2025
- **Chevrolet**: 7 units (Avg: 43,635km, Years: 2019-2024
- **Toyota**: 5 units (Avg: 63,948km, Years: 2019-2025
- **GMC**: 4 units (Avg: 33,983km, Years: 2021-2023

## Vehicle Record Schema
Each vehicle record contains:
- **id**: Stock number (e.g., "23J338B")
- **vin**: Full VIN
- **vehicle**: Year, Make, Model, Trim, Age
- **specs**: Mileage (km), Category, Transmission, Colors
- **availability**: Status, Tags (e.g., "New arrivals"), Image availability
- **pricing**: Always "Call for pricing"

## Sample Records (First 5):
| stock_number   |   year | make   | model    | trim       | mileage_km   | exterior_color   | tags   |
|:---------------|-------:|:-------|:---------|:-----------|:-------------|:-----------------|:-------|
| 23J338B        |   2020 | MINI   | 5 door   | Cooper     | 34,422       | Not specified    | -      |
| 25UP578A       |   2021 | Jeep   | Cherokee | Sport      | 83,622       | Not specified    | -      |
| 25UP727        |   2019 | Nissan | Rogue    | Awd Sv     | 46,200       | White            | -      |
| 25UP734A       |   2020 | Honda  | HR-V     | Lx Awd Cvt | 67,428       | Not specified    | -      |
| 25R192A        |   2022 | Kia    | Seltos   | Ex         | 102,563      | Blue             | -      |

## Usage Instructions for AI:
1. **Searching by Make**: Filter JSON objects by `vehicle.make`
2. **Mileage Ranges**: Use `specs.mileage_category` (Low/Medium/High/Very High)
3. **New Arrivals**: Check `availability.tags` array for "New arrivals"
4. **Age Filter**: Use `vehicle.age_years` or `vehicle.year`
5. **Color Search**: Check `specs.exterior_color` (may be "Not specified")

## Data Quality Notes:
- 1 vehicle removed due to missing mileage data
- 19 vehicles missing trim data (marked as empty string in JSON)
- Images available for approximately 8% of inventory (17 unique URLs)
- Transmission: 99% Auto, 1% Manual (approximate)
