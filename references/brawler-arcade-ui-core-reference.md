# Brawler Arcade UI Core Reference

Use this reference for reusable game UI, mobile-first arcade UI, lobby/menu/shop/upgrade/result screens, Brawl Stars-like broad UI direction, or 荒野乱斗 UI references.

## Default Route

Art Director -> UI Programmer -> Godot Specialist -> QA Lead.

## Shared Kit

Local kit path:

```text
C:\Users\76398\Documents\Codex\ui-kits\brawler-arcade-ui-core
```

## Visual Direction

Use:

- chunky panels
- thick dark outlines
- hard offset shadows
- saturated blue/purple bases
- yellow/orange primary CTAs
- red/green notification badges
- resource pills
- progress tracks
- card menus
- procedural pop/bounce feedback

Do not copy Brawl Stars names, logos, icons, characters, exact layouts, typography, currencies, or proprietary assets.

## Godot UI Expectations

- Use reusable Control scenes for buttons, resource pills, progress tracks, cards, tabs, and modal panels.
- Prefer Theme resources and styleboxes over per-node styling.
- Keep mobile touch targets comfortable.
- Add button press/hover/disabled states.
- Use tweened scale/position/color feedback for pop and bounce.
- Keep text inside bounds across common mobile and desktop viewports.
- Avoid cards inside cards unless the nested element is a genuine repeated item.

## QA Checklist

- All buttons have clear press state.
- Text does not overflow.
- Touch targets are usable on mobile.
- Disabled and locked states are readable.
- Resource counters update without layout shifts.
- Animation feedback does not block input.
- Screens remain original and project-specific.
