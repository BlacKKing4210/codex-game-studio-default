# Agent Sprite Forge Reference

Adapted from `0x0funky/agent-sprite-forge` for Codex Game Studio.

## What The Sprite Forge Specialist Learned

The Sprite Forge Specialist uses agent-sprite-forge as a production pipeline for generated 2D game art. It receives approved art direction from Art Director and the relevant professional art specialist; it does not replace concept, environment, UI, visual development, 2D animation, or 2D technical-art judgment.

The key separation is:

- Image generation creates the visible artwork.
- Local deterministic tools clean, slice, align, extract, preview, validate, and package generated artwork.
- Godot integration uses metadata, frame sizes, anchors, collision notes, spawn zones, and scene import notes rather than guessing from a flattened image.
- 2D Technical Artist reviews final sprite specs, atlas/import notes, y-sort/collision requirements, and target-resolution readability before Godot integration.

## generate2dsprite

Use this for:

- player characters
- enemies and creatures
- NPCs and summons
- weapons
- projectiles
- impacts and explosions
- slash arcs and muzzle flashes
- dust and spell FX
- props and transparent object sheets
- animation GIF/PNG exports

Required prompt constraints for processable sheets:

- solid flat `#FF00FF` background
- no gradients, text, labels, UI, watermark, borders, or frame lines
- exact grid count
- same identity across frames
- same scale and bounding box across frames
- full subject inside each cell
- no part crossing cell edges
- generous magenta margin

Useful sheet defaults:

- `2x2`: simple 4-frame idle/combat/impact.
- `2x3`: 6-frame cast/attack/hurt.
- `3x3`: boss idle, larger loop, elaborate action.
- `4x4`: top-down four-direction walk.
- `1x4` or `2x2`: projectile, impact, short FX loop.

Survivor-like rule: keep bodies separate from projectiles, impacts, slash arcs, muzzle flashes, dust, and wide FX. This keeps player/enemy bodies readable and avoids oversized animation cells.

## generate2dmap

Use this for:

- survivor-like arenas
- layered raster maps
- foundation maps
- prop packs
- blockers and obstacle placement
- collision metadata
- spawn zones and spawn rings
- camera bounds
- Godot-ready map handoff

Map modes:

- `scene_mode`: foundation plus separate props. Default for Brotato-like or survivor-like arenas.
- `tile_mode`: editable tile/grid maps, Godot TileMap, Tiled, LDtk.
- `side_scroll_mode`: parallax side-scroller stages.
- `grid_mode`: rule-heavy grid scenes.
- `room_chunk_mode`: modular roguelike chunks.
- `baked_scene_mode`: fixed background only.

Playable maps should not be one flattened image unless the user explicitly asks for background-only art.

## QC Checklist

Reject or regenerate sprite output when:

- frames touch cell edges
- identity changes between frames
- scale drifts
- subject is cropped
- projectile or impact loops are unreadable
- body animation includes merged wide FX that ruins the cell size
- transparency cleanup leaves magenta fringe
- generated image contains text, UI, labels, or watermark

Reject or regenerate map output when:

- base layer includes runtime props, actors, pickups, labels, or blockers
- props are clipped or lack alpha
- collision metadata cannot parse
- spawn zones are invalid or unsafe
- blockers use full silhouette instead of gameplay footprint
- QA preview does not match camera/game scale
- a flattened reference is being used as the runtime map

## Godot Handoff Contract

Every generated asset handoff should include:

- source prompt
- raw image path
- cleaned transparent image path
- frame size and grid
- animation names, FPS, and loop mode
- origin/anchor/feet-line notes
- collision or hitbox notes
- intended Godot scene/resource path
- preview GIF or QA preview image
- known issues or regeneration notes
