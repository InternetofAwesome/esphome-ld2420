# esphome-ld2420

ESPHome LD2420 component with per-gate energy sensors added.

Extends the mainline ESPHome LD2420 component to expose `gate_energy_0` through
`gate_energy_15` as individual sensors, enabling real-time tuning of gate
thresholds directly from the Home Assistant UI.

## Usage

```yaml
external_components:
  - source:
      type: git
      url: https://github.com/InternetofAwesome/esphome-ld2420
      ref: main
    components: [ld2420]

sensor:
  - platform: ld2420
    moving_distance:
      name: Moving Distance
    gate_energy_0:
      name: Gate 0 Energy
    gate_energy_1:
      name: Gate 1 Energy
    # ... gate_energy_2 through gate_energy_15
```

All 16 gate energy sensors are optional — include only the gates you care about.
