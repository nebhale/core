| Topic | Name | Device class | State class | Icon | Unit | Value template | Payload on | Payload off | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `active_route_destination` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `active_route_latitude` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `active_route_longitude` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `active_route` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `battery_level` | `Battery` | `battery` | `measurement` |  | `%` |  |  |  |  |
| `center_display_state` | `Center Display` |  |  | `mdi:television` |  | For a Home Assistant Tesla `center_display_state` sensor, treat `vehicle_state.center_display_state` as an integer enum describing what the vehicle’s center display is currently showing or doing. Known values are: `0` means the center display is off. `2` means the display is on in standby, and may also represent Camp Mode. `3` means the display is on and showing the charging screen. `4` means the display is on in the general/default state. `5` means the display is on and showing the large charging screen. `6` means the display is on and ready to unlock. `7` means Sentry Mode. `8` means Dog Mode. `9` means Media. Value `1` is not documented in the sources I found, so preserve it as unknown rather than guessing. For future safety, any unrecognized integer should map to an unknown/unmapped state while retaining the raw value as an attribute. |  |  |  |
| `charge_current_request_max` | `Charge Current Request (Max)` | `current` | `measurement` |  | `A` |  |  |  |  |
| `charge_current_request` | `Charge Current Request` | `current` | `measurement` |  | `A` |  |  |  |  |
| `charge_energy_added` | `Energy Added` | `energy` | `total_increasing` |  | `kWh` | Use one digit of precision |  |  | `Session total; expected to reset between charges.` |
| `charge_limit_soc` | `Limit` |  | `measurement` | `mdi:battery-charging-90` | `%` |  |  |  |  |
| `charge_port_door_open` | `Charge Port` | `door` |  | `mdi:ev-plug-tesla` |  |  | `true` | `false` |  |
| `charger_actual_current` | `Charger Current` | `current` | `measurement` |  | `A` |  |  |  |  |
| `charger_phases` | `Charger Phases` |  |  | `mdi:sine-wave` |  |  |  |  |  |
| `charger_power` | `Charger Power` | `power` | `measurement` |  | `kW` |  |  |  |  |
| `charger_voltage` | `Charger Voltage` | `voltage` | `measurement` |  | `V` |  |  |  |  |
| `charging_state` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `climate_keeper_mode` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `display_name` | `Display Name` |  |  | `mdi:form-textbox` |  |  |  |  |  |
| `doors_open` | `Doors` | `door` |  | `mdi:car-door` |  |  | `true` | `false` |  |
| `driver_front_door_open` | `Door (Driver Front)` | `door` |  | `mdi:car` |  |  | `true` | `false` |  |
| `driver_rear_door_open` | `Door (Driver Rear)` | `door` |  | `mdi:car` |  |  | `true` | `false` |  |
| `elevation` | `Elevation` |  | `measurement` | `mdi:image-filter-hdr` | `unitsCfg.Distance.DistanceShortUnits()` | `unitsCfg.Distance.DistanceShortValueTemplate()` |  |  |  |
| `est_battery_range_km` | `Range` |  | `measurement` | `mdi:map-marker-distance` | `unitsCfg.Distance.DistanceLongUnits()` | `unitsCfg.Distance.DistanceLongValueTemplate()` |  |  | `Conditional: Go uses fmt.Sprintf("%s_battery_range_km", unitsCfg.RangeType.Prefix()).` |
| `exterior_color` | `Exterior Color` |  |  | `mdi:format-color-fill` |  |  |  |  |  |
| `frunk_open` | `Frunk` | `door` |  | `mdi:car` |  |  | `true` | `false` |  |
| `geofence` | `Geofence` |  |  | `mdi:earth` |  |  |  |  |  |
| `heading` | `Heading` |  |  | `mdi:compass` | `°` |  |  |  |  |
| `healthy` | `Health` | `problem` |  | `mdi:heart-pulse` |  |  | `false` | `true` | `Payloads are inverted: healthy=false maps to ON/problem.` |
| `ideal_battery_range_km` | `Range` |  | `measurement` | `mdi:map-marker-distance` | `unitsCfg.Distance.DistanceLongUnits()` | `unitsCfg.Distance.DistanceLongValueTemplate()` |  |  | `Conditional: Go uses fmt.Sprintf("%s_battery_range_km", unitsCfg.RangeType.Prefix()).` |
| `inside_temp` | `Inside Temp` | `temperature` | `measurement` |  | `°C` | Use one digit of precision |  |  |  |
| `is_climate_on` | `Climate` | `running` |  | `mdi:fan` |  |  | `true` | `false` |  |
| `is_preconditioning` | `Preconditioning` | `running` |  | `mdi:fan` |  |  | `true` | `false` |  |
| `is_user_present` | `Occupied` | `occupancy` |  | `mdi:account` |  |  | `true` | `false` |  |
| `latitude` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `location` |  |  |  | `mdi:car` |  | `home/not_home geofence template` |  |  | `Uses location as both state topic and JSON attributes topic.` |
| `locked` | `Locked` | `lock` |  |  |  |  | `false` | `true` | `Payloads are inverted for lock class.` |
| `longitude` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `model` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `odometer` | `Odometer` |  | `total_increasing` | `mdi:counter` | `unitsCfg.Distance.DistanceLongUnits()` | `unitsCfg.Distance.DistanceLongValueTemplate()` |  |  |  |
| `outside_temp` | `Outside Temp` | `temperature` | `measurement` |  | `°C` | Use one digit of precision |  |  |  |
| `passenger_front_door_open` | `Door (Passenger Front)` | `door` |  | `mdi:car` |  |  | `true` | `false` |  |
| `passenger_rear_door_open` | `Door (Passenger Rear)` | `door` |  | `mdi:car` |  |  | `true` | `false` |  |
| `plugged_in` | `Plug` | `plug` |  |  |  |  | `true` | `false` |  |
| `power` | `Power` | `power` | `measurement` |  | `kW` |  |  |  |  |
| `rated_battery_range_km` | `Range` |  | `measurement` | `mdi:map-marker-distance` | `unitsCfg.Distance.DistanceLongUnits()` | `unitsCfg.Distance.DistanceLongValueTemplate()` |  |  | `Conditional: Go uses fmt.Sprintf("%s_battery_range_km", unitsCfg.RangeType.Prefix()).` |
| `scheduled_charging_start_time` | `Scheduled Start Time` | `timestamp` |  |  |  |  |  |  |  |
| `sentry_mode` | `Sentry Mode` |  |  | `mdi:cctv` |  |  | `true` | `false` |  |
| `shift_state` | `Shift State` |  |  | `mdi:car-shift-pattern` |  |  |  |  |  |
| `since` | `Last Seen` |  |  | `mdi:timer-sand` |  |  |  |  |  |
| `speed` | `Speed` |  | `measurement` | `mdi:speedometer` | `unitsCfg.Distance.SpeedUnits()` | `unitsCfg.Distance.SpeedValueTemplate()` |  |  |  |
| `spoiler_type` | `Spoiler Type` |  |  | `mdi:weather-windy` |  |  |  |  |  |
| `state` | `Charging` | `battery_charging` |  |  |  | ``{{ "ON" if value == "charging" else "OFF" }}`` |  |  | `Also published raw state topic; discovery uses it as Charging binary sensor.` |
| `time_to_full_charge` | `Time to Charged` | `duration` | `measurement` | `mdi:timer` | `h` |  |  |  |  |
| `tpms_pressure_fl` | `Tire Pressure (Front Left)` | `pressure` | `measurement` | `mdi:gauge` | `unitsCfg.Pressure.PressureUnits()` | `unitsCfg.Pressure.PressureValueTemplate()` |  |  |  |
| `tpms_pressure_fr` | `Tire Pressure (Front Right)` | `pressure` | `measurement` | `mdi:gauge` | `unitsCfg.Pressure.PressureUnits()` | `unitsCfg.Pressure.PressureValueTemplate()` |  |  |  |
| `tpms_pressure_rl` | `Tire Pressure (Rear Left)` | `pressure` | `measurement` | `mdi:gauge` | `unitsCfg.Pressure.PressureUnits()` | `unitsCfg.Pressure.PressureValueTemplate()` |  |  |  |
| `tpms_pressure_rr` | `Tire Pressure (Rear Right)` | `pressure` | `measurement` | `mdi:gauge` | `unitsCfg.Pressure.PressureUnits()` | `unitsCfg.Pressure.PressureValueTemplate()` |  |  |  |
| `tpms_soft_warning_fl` | `Tire Soft (Front Left)` | `problem` |  | `mdi:car-tire-alert` |  |  | `true` | `false` |  |
| `tpms_soft_warning_fr` | `Tire Soft (Front Right)` | `problem` |  | `mdi:car-tire-alert` |  |  | `true` | `false` |  |
| `tpms_soft_warning_rl` | `Tire Soft (Rear Left)` | `problem` |  | `mdi:car-tire-alert` |  |  | `true` | `false` |  |
| `tpms_soft_warning_rr` | `Tire Soft (Rear Right)` | `problem` |  | `mdi:car-tire-alert` |  |  | `true` | `false` |  |
| `trim_badging` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `trunk_open` | `Trunk` | `door` |  | `mdi:car` |  |  | `true` | `false` |  |
| `update_available` | `Update` | `update` |  |  |  |  | `true` | `false` |  |
| `update_version` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `usable_battery_level` | `Usable Battery` | `battery` | `measurement` |  | `%` |  |  |  |  |
| `version` | `Version` |  |  | `mdi:numeric` |  |  |  |  |  |
| `wheel_type` |  |  |  |  |  |  |  |  | `Missing in publish_discovery.go` |
| `windows_open` | `Windows` | `window` |  | `mdi:car-door` |  |  | `true` | `false` |  |
