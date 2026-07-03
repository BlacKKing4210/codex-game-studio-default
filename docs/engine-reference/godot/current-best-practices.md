# Godot Current Best Practices

- Prefer typed GDScript for project code.
- Use scenes as reusable units.
- Use Resources for reusable data and authored content.
- Use signals for decoupled events.
- Keep autoloads limited to true global services.
- Use object pooling for frequent projectiles, pickups, damage numbers, and particles.
- Keep gameplay tuning in CSV/Resources rather than hardcoded script constants when designers need to tune it.
- Verify dense-combat scenarios early for survivorlike games.
