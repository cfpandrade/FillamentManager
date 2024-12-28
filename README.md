# Home Assistant Filament Manager

Addon for Home Assistant to manage 3D printer filament inventory.

## Features
- API to add, update, and list filaments.
- Persistent storage using SQLite.
- Integration with Home Assistant via REST sensors.

## Usage
1. Place the addon in the `/addons/local/filament_manager` directory of Home Assistant.
2. Install and start the addon from the Supervisor interface.
3. Use the API endpoints to manage filaments.

## API Endpoints
- `GET /filamentos`: List all filaments.
- `POST /filamentos`: Add a new filament.

## Docker Build Instructions
```bash
docker build -t filament_manager .
docker run -p 5000:5000 -v $(pwd)/data:/data filament_manager
