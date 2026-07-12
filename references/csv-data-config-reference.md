# CSV Data Config Reference

Use CSV files for designer-editable game content and balance by default.

## Default Route

Numerical Designer -> Data Config Specialist -> Technical Director -> Godot Specialist -> QA Lead.

## Table Rules

- Store tables under `config/csv/` or the project equivalent.
- Use stable unique `id` columns for every table.
- Keep one concept per table: `weapons.csv`, `enemies.csv`, `upgrades.csv`, `waves.csv`, `loot_tables.csv`, `avatar_parts.csv`.
- Use ID references between tables instead of duplicating large data.
- Keep values human-readable: plain numbers, booleans, enum-like strings, comma-free IDs, and short descriptions.
- Use semicolon-separated lists inside one cell only when a field truly needs multiple IDs.
- Keep formulas and derived values in code, but keep tuning constants in CSV.

## Starter Schemas

`weapons.csv`:

```csv
id,name,category,base_damage,cooldown_sec,range_px,projectile_id,upgrade_tags,description
spark_pistol,Spark Pistol,ranged,8,0.45,320,spark_bolt,damage;speed,Fast starter weapon
```

`enemies.csv`:

```csv
id,name,hp,move_speed,contact_damage,xp_drop,spawn_weight,tags,description
drift_grunt,Drift Grunt,18,72,4,1,100,basic;swarm,Slow pressure enemy
```

`upgrades.csv`:

```csv
id,name,target_type,target_id,stat,operation,value,max_stacks,description
spark_damage_1,Spark Coil,weapon,spark_pistol,base_damage,add,2,5,Adds flat spark damage
```

`waves.csv`:

```csv
id,start_sec,end_sec,enemy_ids,spawn_rate_per_sec,max_alive,notes
wave_001,0,45,drift_grunt,1.2,24,Intro pressure
```

## Validation

Before gameplay starts, validate:

- required columns
- duplicate IDs
- missing referenced IDs
- empty required values
- invalid numbers/booleans/enums
- list separators
- unsafe negative values
- tables referenced by systems that are absent

## Godot Loading Path

Prefer one shared CSV loader/database that:

- loads tables once at startup or project bootstrap
- exposes typed accessors or dictionaries by ID
- validates references after all tables load
- reports line numbers and table names for errors
- keeps defaults in code only as fallbacks, not as live balance source

## User-Edited CSV Rule

If the user edits a CSV table, treat the edited CSV as the source of truth. Read current CSV files before changing them, preserve existing values, and never overwrite or regenerate user-edited tables from templates without explicit approval.
