| Topic | Name | Device class | State class | Icon | Unit | Value template | Notes |
|---|---|---|---|---|---|---|---|
| `active_route_destination` |  |  |  |  |  |  | Not currently implemented as it does not have an obvious sensor mapping. |
| `active_route_latitude` |  |  |  |  |  |  | Not currently implemented as it does not have an obvious sensor mapping. |
| `active_route_longitude` |  |  |  |  |  |  | Not currently implemented as it does not have an obvious sensor mapping. |
| `active_route` |  |  |  |  |  |  | Not currently implemented as it does not have an obvious sensor mapping. |
| `battery_level` | `Battery` | `battery` | `measurement` |  | `%` |  |  |
| `center_display_state` | `Center Display` |  |  | `mdi:television` |  | For a Home Assistant Tesla `center_display_state` sensor, treat `vehicle_state.center_display_state` as an integer enum describing what the vehicle’s center display is currently showing or doing. Known values are: `0` means the center display is off. `2` means the display is on in standby, and may also represent Camp Mode. `3` means the display is on and showing the charging screen. `4` means the display is on in the general/default state. `5` means the display is on and showing the large charging screen. `6` means the display is on and ready to unlock. `7` means Sentry Mode. `8` means Dog Mode. `9` means Media. Value `1` is not documented in the sources I found, so preserve it as unknown rather than guessing. For future safety, any unrecognized integer should map to an unknown/unmapped state while retaining the raw value as an attribute. |  |
| `charge_current_request_max` | `Charge Current Request (Max)` | `current` | `measurement` |  | `A` | Use zero digits of precision |  |
| `charge_current_request` | `Charge Current Request` | `current` | `measurement` |  | `A` | Use zero digits of precision |  |
| `charge_energy_added` | `Energy Added` | `energy` | `total_increasing` |  | `kWh` | Use one digit of precision | |
| `charge_limit_soc` | `Charge Limit` |  | `measurement` | `mdi:battery-charging-90` | `%` | Use zero digits of precision |  |
| `charge_port_door_open` | `Charge Port` | `door` |  | `mdi:ev-plug-tesla` |  |  |  |
| `charger_actual_current` | `Charger Current` | `current` | `measurement` |  | `A` | Use zero digits of precision |  |
| `charger_phases` | `Charger Phases` |  | `measurement` | `mdi:sine-wave` | `phases` | Use zero digits of precision |  |
| `charger_power` | `Charger Power` | `power` | `measurement` |  | `kW` | Use zero digits of precision |  |
| `charger_voltage` | `Charger Voltage` | `voltage` | `measurement` |  | `V` | Use zero digits of precision |  |
| `charging_state` | `Charging State` |  |  | `mdi:ev-station` |  | Preserve the TeslaMate charging state as a human-readable string, but split camel-case words into space-separated words. For example, `NoPower` should display as `No Power`. | |
| `climate_keeper_mode` | `Climate Keeper` |  |  | `mdi:air-conditioner` |  | Preserve the TeslaMate climate keeper mode as a human-readable string, but title case the value. | |
| `display_name` | `Display Name` |  |  | `mdi:form-textbox` |  |  | Used as the Home Assistant config entry title and device name, so it is not exposed as a standalone sensor. |
| `doors_open` | `Doors` | `door` |  | `mdi:car-door` |  |  |  |
| `driver_front_door_open` | `Door (Driver Front)` | `door` |  | `mdi:car-door` |  |  |  |
| `driver_rear_door_open` | `Door (Driver Rear)` | `door` |  | `mdi:car-door` |  |  |  |
| `elevation` | `Elevation` | `distance` | `measurement` | `mdi:image-filter-hdr` | `m` | Use zero digits of precision |  |
| `est_battery_range_km` | `Range (Estimated)` | `distance` | `measurement` | `mdi:map-marker-distance` | `km` | Use zero digits of precision | |
| `exterior_color` | `Exterior Color` |  |  | `mdi:format-color-fill` |  | Preserve the TeslaMate exterior color as a human-readable string, but split camel-case words into space-separated words. For example, `DeepBlue` should display as `Deep Blue`. |  |
| `frunk_open` | `Frunk` | `door` |  | `mdi:car` |  |  |  |
| `geofence` | `Geofence` |  |  | `mdi:earth` |  |  |  |
| `heading` | `Heading` |  | `measurement` | `mdi:compass` | `°` | Use zero digits of precision |  |
| `healthy` | `Health` | `problem` |  | `mdi:heart-pulse` |  | Treat the TeslaMate healthy value as a Home Assistant problem binary sensor. Because TeslaMate publishes `true` when there are no problems and `false` when there are problems, invert the value so `true` reports off/no problem and `false` reports on/problem. |  |
| `ideal_battery_range_km` | `Range (Ideal)` | `distance` | `measurement` | `mdi:map-marker-distance` | `km` | Use zero digits of precision | |
| `inside_temp` | `Temperature (Inside)` | `temperature` | `measurement` |  | `°C` | Use one digit of precision |  |
| `is_climate_on` | `Climate` | `running` |  | `mdi:air-conditioner` |  |  |  |
| `is_preconditioning` | `Preconditioning` | `running` |  | `mdi:air-conditioner` |  |  |  |
| `is_user_present` | `Occupancy` | `occupancy` |  | `mdi:account` |  |  |  |
| `latitude` | `Latitude` |  | `measurement` | `mdi:latitude` | `°` |  | Used by the device tracker rather than exposed as a standalone sensor. |
| `location` |  |  |  | `mdi:car` |  |  | Ignored as the device tracker builds this from the latitude and longitude directly. |
| `locked` | `Lock` | `lock` |  |  |  | Treat the TeslaMate locked value as a Home Assistant lock binary sensor. Because TeslaMate publishes `true` when the car is locked and `false` when the car is unlocked, invert the value so `true` reports off/locked and `false` reports on/unlocked. |  |
| `longitude` | `Longitude` |  | `measurement` | `mdi:longitude` | `°` |  | Used by the device tracker rather than exposed as a standalone sensor. |
| `model` | `Model` |  |  | `mdi:form-textbox` |  |  | Used as the Home Assistant device name, so it is not exposed as a standalone sensor. |
| `odometer` | `Odometer` | `distance` | `total_increasing` | `mdi:counter` | `km` | Use zero digits of precision |  |
| `outside_temp` | `Temperature (Outside)` | `temperature` | `measurement` |  | `°C` | Use one digit of precision |  |
| `passenger_front_door_open` | `Door (Passenger Front)` | `door` |  | `mdi:car-door` |  |  |  |
| `passenger_rear_door_open` | `Door (Passenger Rear)` | `door` |  | `mdi:car-door` |  |  |  |
| `plugged_in` | `Plug` | `plug` |  |  |  |  |  |
| `power` | `Power` | `power` | `measurement` |  | `kW` | Use zero digits of precision |  |
| `rated_battery_range_km` | `Range (Rated)` | `distance` | `measurement` | `mdi:map-marker-distance` | `km` | Use zero digits of precision | |
| `scheduled_charging_start_time` | `Charging Start Time` | `timestamp` |  |  |  | Parse the value as a timestamp and use it as-is. |  |
| `sentry_mode` | `Sentry Mode` | `running` |  | `mdi:cctv` |  |  |  |
| `shift_state` | `Shift State` |  |  | `mdi:car-shift-pattern` |  |  |  |
| `since` | `Last Seen` | `timestamp` |  | `mdi:timer-sand` |  | Parse the value as a timestamp and use it as-is. |  |
| `speed` | `Speed` | `speed` | `measurement` | `mdi:speedometer` | `km/h` | Use zero digits of precision |  |
| `spoiler_type` | `Spoiler Type` |  |  | `mdi:weather-windy` |  | Split camel-case words into space-separated words. Append the formatted value to the Home Assistant device model as a parenthetical detail suffixed with `Spoiler`, unless the value is `none`. | Used as part of the Home Assistant device model, so it is not exposed as a standalone sensor. |
| `state` | `State` |  |  | `mdi:car-connected` |  | Preserve the TeslaMate vehicle state as a human-readable string, but title case the value. |  |
| `time_to_full_charge` | `Charging Time Remaining` | `duration` | `measurement` | `mdi:timer` | `h` |  |  |
| `tpms_pressure_fl` | `Tire Pressure (Front Left)` | `pressure` | `measurement` | `mdi:gauge` | `bar` | Use one digit of precision |  |
| `tpms_pressure_fr` | `Tire Pressure (Front Right)` | `pressure` | `measurement` | `mdi:gauge` | `bar` | Use one digit of precision |  |
| `tpms_pressure_rl` | `Tire Pressure (Rear Left)` | `pressure` | `measurement` | `mdi:gauge` | `bar` | Use one digit of precision |  |
| `tpms_pressure_rr` | `Tire Pressure (Rear Right)` | `pressure` | `measurement` | `mdi:gauge` | `bar` | Use one digit of precision |  |
| `tpms_soft_warning_fl` | `Tire Soft (Front Left)` | `problem` |  | `mdi:car-tire-alert` |  |  |  |
| `tpms_soft_warning_fr` | `Tire Soft (Front Right)` | `problem` |  | `mdi:car-tire-alert` |  |  |  |
| `tpms_soft_warning_rl` | `Tire Soft (Rear Left)` | `problem` |  | `mdi:car-tire-alert` |  |  |  |
| `tpms_soft_warning_rr` | `Tire Soft (Rear Right)` | `problem` |  | `mdi:car-tire-alert` |  |  |  |
| `trim_badging` | `Trim Badging` |  |  | `mdi:form-textbox` |  |  | Used as the Home Assistant device name, so it is not exposed as a standalone sensor. |
| `trunk_open` | `Trunk` | `door` |  | `mdi:car` |  |  |  |
| `update_available` | `Update` | `firmware` |  |  |  |  | Exposed as an update entity. |
| `update_version` | `Update` | `firmware` |  |  |  |  | Used as the latest version on the update entity. |
| `usable_battery_level` | `Usable Battery` | `battery` | `measurement` |  | `%` |  |  |
| `version` | `Version` |  |  | `mdi:numeric` |  |  | Used as the Home Assistant device software version, so it is not exposed as a standalone sensor. |
| `wheel_type` | `Wheel Type` |  |  | `mdi:tire` |  | Treat the TeslaMate wheel type as a compact string made from a camel-case wheel name followed by trailing digits for the wheel size. Split the camel-case name into space-separated words, insert a space before the size, append a double quote to the size, and append the formatted value to the Home Assistant device model as a parenthetical detail suffixed with `Wheels`. For example, `SonicCarbonTwinTurbine19` should contribute `Sonic Carbon Twin Turbine 19" Wheels`. | Used as part of the Home Assistant device model, so it is not exposed as a standalone sensor. |
| `windows_open` | `Windows` | `window` |  | `mdi:car-door` |  |  |  |
