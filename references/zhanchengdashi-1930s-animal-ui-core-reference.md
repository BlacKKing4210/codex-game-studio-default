# Zhanchengdashi 1930s Animal UI Core Reference

Use this reference for the default game UI starting point, unspecified game UI direction, mobile lobby/menu/shop/deck/battle/result screens, reusable animal-card UI, or adoption of the shared animal and procedural-motion assets.

## Route

Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead.

## Shared kit

```text
C:\Users\76398\Documents\Codex\ui-kits\zhanchengdashi-1930s-animal-ui-core
```

Read the kit's `README.md`, `STYLE_GUIDE.md`, `GODOT_IMPLEMENTATION.md`, `ASSET_PROVENANCE.md`, token files, catalog, and source snapshot before adoption.

## Default visual language

- Warm paper and deep ink.
- Hand-painted 1930s fairground framing.
- Red/gold primary actions and teal secondary actions.
- Stable resource and numeric slots.
- Readable animal cards with white sticker-like silhouettes.
- One dominant CTA per screen or modal.
- At least two cues for selected, disabled, locked, loading, completed, error, and unaffordable states.

The 720 x 1280 v15 pages are visual and screenshot-parity targets only. Never ship a whole page PNG as the interactive layer. Extract or redraw text-free, nine-slice-safe components and keep text, icons, values, navigation, state, and input engine-native.

## Animal default

Use the 60 animal PNGs only when the project has no specified character art and the theme fits. Copy selected images into the project, preserve filenames and catalog/provenance entries, and never silently replace existing project-owned art. Treat public redistribution as rights-review gated.

Default display scale by rarity is common 1.0, rare 1.2, epic 1.5, and legendary 1.8 unless project readability or balance requires another mapping.

## Motion default

Start with:

- `godot/scripts/unit_motion_feedback.gd` for idle/move, attack, hit, stat gain, power-up, and death feedback.
- `godot/scripts/zhanchengdashi_ui_motion.gd` for lobby animal idle, deck-slot breathing, gacha flip/open/particles, detail pulse, and toast fade.

Apply poses to a visual child so logical position, collision, focus, layout, and touch bounds remain stable. Center pivots, cancel and reset previous tweens before replay, stop loops when hidden/exiting, and honor reduced-motion. Upgrade to drawn frames only when silhouette, direction, anticipation/recovery, hero/boss quality, or gameplay readability requires them.

## Precedence and alternate

This is a default visual/component starting point, not a fixed information architecture. Project `AGENTS.md`, approved UI/UE, platform conventions, aspect ratio, accessibility, existing art direction, and explicit user choices take precedence.

Use `brawler-arcade-ui-core` only when a saturated modern arcade/brawler direction is explicitly requested.

## QA

- Verify native target resolution, 50% visual scale, target aspect ratios, and safe areas.
- Verify long localized text and one-to-three-digit values without layout shift.
- Verify mouse, touch, keyboard, and controller states as applicable.
- Verify all motion can be interrupted and returns to base state.
- Verify reduced-motion behavior and stable hit/focus/collision areas.
- Verify adopted animals and UI assets remain traceable to their source manifest.
