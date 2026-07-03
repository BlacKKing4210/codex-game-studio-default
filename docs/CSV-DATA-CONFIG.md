# CSV Data Config

Codex Game Studio keeps game balance and designer-editable content in CSV by default.

## Why CSV

- Easy to open and edit.
- Friendly to designers and solo developers.
- Works well with Git diffs for simple rows.
- Avoids hardcoded gameplay tuning.

## Default Tables

Use the tables that match the project:

- `weapons.csv`
- `enemies.csv`
- `upgrades.csv`
- `waves.csv`
- `loot_tables.csv`
- `avatar_parts.csv`
- `shop_offers.csv`
- `ui_copy.csv`

## Validation Rules

Validate before gameplay starts:

- required columns
- duplicate IDs
- missing references
- empty required values
- number conversion
- boolean conversion
- enum-like fields
- semicolon list fields

## Godot Handoff

Recommended runtime path:

```text
config/csv/*.csv
src/core/csv_loader.gd
src/core/game_database.gd
```

Use one shared loader/database instead of ad hoc parsing in gameplay scripts.
