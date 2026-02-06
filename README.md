# Dados Dashboard

A modern, clean Home Assistant dashboard built with custom button cards and expander card  for a consistent UI experience.

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024-blue?style=flat&logo=home-assistant)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

## Screenshots



## Features

- 🏠 **Multi-floor overview** - Navigate through different floors and rooms with simple-tabs
- 💡 **Lighting control** - Full control over all lights with auto entities
- 🌡️ **Climate & Heating** - Vaillant heat pump integration via myPyllant
- 🪟 **Shutters & Blinds** - Control all roller shutters with custom sliders
- 🤖 **Vacuum robot** - With Roborock Integration
- 📷 **Security cameras** - Reolink cameras with Frigate integration
- 🎵 **Music** - Music Assistant with Mediocore player
- 🗑️ **Waste collection** - Schedule and reminders with Waste Collection Schedule 
- 📅 **Calendar** - Integrated calendar card with Calendar Card Pro
- 🍽️ **Dishwasher** - Home Connect Local integration
- 🚨 **Alarm system** - Alarmo integration
- 🌤️ **Weather** - Current conditions and forecastt with OpenWeatherMap

## Card Architecture

This dashboard uses a modular approach with:

- **[Button Card](https://github.com/custom-cards/button-card)** - Custom styled buttons with templates
- **[Expander Card](https://github.com/Alia5/lovelace-expander-card)** - Collapsible sections for cleaner UI
- **[Decluttering Card](https://github.com/custom-cards/decluttering-card)** - Reusable templates to reduce code duplication
- **[Bubble Card](https://github.com/Clooos/Bubble-Card)** - Beautiful popups and sub-buttons

## Installation

### Prerequisites

- Home Assistant 2024.x or newer
- [HACS](https://hacs.xyz/) installed

### Step 1: Install HACS Integrations

Install the following integrations via HACS:

| Integration | Description |
|-------------|-------------|
| [Alarmo](https://github.com/nielsfaber/alarmo) | Alarm system |
| [Browser Mod](https://github.com/thomasloven/hass-browser_mod) | Browser control & popups |
| [Frigate](https://github.com/blakeblackshear/frigate-hass-integration) | NVR integration |
| [Music Assistant](https://github.com/music-assistant/hass-music-assistant) | Music player |
| [Presence Simulation](https://github.com/slashback100/presence_simulation) | Simulate presence |
| [Waste Collection Schedule](https://github.com/mampfes/hacs_waste_collection_schedule) | Waste calendar |
| [Xiaomi Cloud Map Extractor](https://github.com/PiotrMachworker/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor) | Vacuum maps |
| [myPyllant](https://github.com/signalkraft/mypyllant-component) | Vaillant heat pump |
| [Home Connect Local](https://github.com/ekutner/home-connect-hass) | Home Connect appliances |
| [Reolink](https://github.com/fwestenberg/reolink_dev) | Reolink cameras |

### Step 2: Install HACS Frontend Cards

Install the following frontend cards via HACS:

| Card | Description |
|------|-------------|
| [Button Card](https://github.com/custom-cards/button-card) | Custom buttons |
| [Decluttering Card](https://github.com/custom-cards/decluttering-card) | Template reuse |
| [Expander Card](https://github.com/Alia5/lovelace-expander-card) | Collapsible sections |
| [Bubble Card](https://github.com/Clooos/Bubble-Card) | Popups & navigation |
| [Mini Graph Card](https://github.com/kalkih/mini-graph-card) | Graphs & charts |
| [Material Symbols](https://github.com/beecho01/material-symbols) | Icon library |

### Step 3: Copy Configuration Files

1. Clone this repository:
   ```bash
   git clone https://github.com/agrestisdavid/dados-dashboard.git
   ```

2. Copy the following folders/files to your Home Assistant `/config` directory:
   ```
   dashboards/
   themes/
   ```

3. Add the dashboard to your `configuration.yaml`:
   ```yaml
   lovelace:
     mode: storage
     dashboards:
       dados-dashboard:
         mode: yaml
         title: Dados Dashboard
         icon: mdi:view-dashboard
         show_in_sidebar: true
         filename: dashboards/dados-dashboard/main.yaml
   ```

4. Add the theme to your `configuration.yaml`:
   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```

5. Restart Home Assistant

### Step 4: Configure Templates

The decluttering templates are located in:
```
dashboards/dados-dashboard/raw/decluttering_card_templates/
```

Available templates:
- `dados_light_expander.yaml` - Light control with expander
- `dados_lights_area.yaml` - Area-based light control
- `dados_shutter_expander.yaml` - Shutter control with expander
- `dados_shutter_slider.yaml` - Shutter slider control
- `dados_shutters_open.yaml` - Open shutters overview
- `dados_climate.yaml` - Climate control
- `dados_humidity.yaml` - Humidity display
- `dados_temperature.yaml` - Temperature display
- `dados_vacuum_roboter_card.yaml` - Vacuum robot card
- `dados_vacuum_roboter_control.yaml` - Vacuum control
- `dados_oven_card.yaml` - Oven status card
- `dados_oven_control.yaml` - Oven control

## Directory Structure

```
config/
├── dashboards/
│   └── dados-dashboard/
│       ├── main.yaml
│       ├── views/
│       │   ├── home.yaml
│       │   ├── heating.yaml
│       │   ├── security.yaml
│       │   ├── music.yaml
│       │   ├── floors.yaml
│       │   ├── homelab.yaml
│       │   ├── settings.yaml
│       │   └── todo.yaml
│       └── raw/
│           ├── decluttering_card_templates/
│           ├── button_card_templates/
│           ├── kiosk/
│           └── navbar/
├── themes/
│   └── rounded/
│       └── dados-theme.yaml
└── images/
    └── (screenshots)
```

## Customization

### Button Card Templates

Button card templates are defined within the dashboard YAML files. To customize:

1. Open the relevant view file in `dashboards/dados-dashboard/views/`
2. Find the `button_card_templates:` section
3. Modify colors, icons, or layouts as needed

### Theme

The custom theme is located at `themes/rounded/dados-theme.yaml`. Adjust colors and styles there.

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License - feel free to use and modify for your own setup.

## Credits

- Inspired by various Home Assistant community dashboards
- Icons by [Material Symbols](https://github.com/beecho01/material-symbols)
