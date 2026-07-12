# UI Implementation Reference

Use this reference when a task involves UI效果图落地, Figma/FigJam screens, exported UI screenshots, HUD/menu/shop/upgrade/result screens, UI polish, UI refactors, or any complaint that the current UI effect is not good enough.

## Source Study

The UI Programmer studies [`nextlevelbuilder/ui-ux-pro-max-skill`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) for UI/UX design intelligence:

- design-system generation
- product/style matching
- color, typography, and spacing systems
- accessibility and contrast checks
- touch and interaction standards
- responsive layout behavior
- animation and motion timing
- form, feedback, navigation, and pre-delivery review rules

This is adapted for games. It does not override Art Director, UI Artist, game genre needs, engine constraints, or the project's approved UI identity.

When no project UI identity is approved, start from `references/zhanchengdashi-1930s-animal-ui-core-reference.md`. Treat its v15 pages as visual references only, then build engine-native components and project-specific information architecture.

## Default Route

Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead.

Responsibilities:

- Art Director approves the UI's identity, quality bar, and anti-copying constraints.
- UI Artist owns the style frame, icon language, typography direction, visual states, and screen readability.
- UI Programmer converts approved visuals into reusable controls, layout rules, Theme resources, input states, and motion hooks.
- Godot Specialist verifies engine structure, Control nodes, anchors, containers, signals, resources, and export behavior.
- QA Lead verifies readability, interaction, states, responsiveness, and screenshot parity.

## Required Inputs

- Figma/FigJam source URL or exported `.fig` reference.
- Exported PNG/PDF screenshots for review.
- Target platform, resolution, aspect ratio, input mode, and safe-area constraints.
- UI Artist style frame or component sheet.
- Required screens and flows.
- Text/localization requirements.
- Any existing UI kit, Theme, or component library.

If a Figma source is unavailable, make a temporary implementation spec from the screenshot, but mark missing design data as assumptions.

## Design Token Extraction

Before implementation, UI Programmer extracts or defines:

- color roles: background, panel, primary CTA, secondary action, text, muted text, border, shadow, success, warning, error, locked, rarity or reward tiers
- typography: font family, size scale, weight scale, line height, number style, fallback rules, localization tolerance
- spacing: 4/8-point rhythm or project equivalent
- radius and outline: panel radius, button radius, icon container radius, stroke widths, dark outlines
- elevation: shadows, offsets, overlays, modal dimming, focus layers
- motion: press scale, hover/selected animation, modal enter/exit, list/card reveal, transition duration, reduced-motion fallback
- icon style: filled/stroke, corner style, stroke width, color roles, size set
- safe area: top/bottom insets, notches, gesture bars, mobile thumb zones, controller focus zones

Tokens should become Theme resources, constants, style assets, or equivalent engine-level reusable definitions instead of raw per-node styling.

## Component State Matrix

Every reusable component must define the states that matter for that component:

- default
- hover
- pressed
- focused
- selected
- disabled
- locked
- loading
- success
- warning
- error
- empty
- notification/new
- affordable/unaffordable when economy is involved

Do not ship a screen that only looks correct in the default state.

## Implementation Rules

- Prefer reusable Control scenes, Theme resources, StyleBoxes, shared icons, and data-driven labels.
- Keep each UI screen as its own module with clear inputs, outputs, signals, and owned files.
- Use anchors, containers, min sizes, aspect ratios, and safe-area padding rather than absolute positioning when possible.
- Keep text inside bounds at target languages and target resolutions.
- Provide visible press/focus feedback for mouse, touch, keyboard, and controller as relevant.
- Use transform/opacity/color modulation for UI motion. Avoid layout-shifting animation.
- Make loading, empty, disabled, locked, and error states visible and recoverable.
- Use SVG/icons or approved UI assets for production UI. Emoji is for demo/prototype placeholders unless intentionally chosen as the final UI identity.
- Preserve the approved game UI identity; do not make the result look like a generic web dashboard unless that is the actual direction.

## Screenshot Parity Review

For UI效果图落地, QA should compare implementation against source screenshots or Figma exports:

- layout proportions
- text hierarchy
- component spacing
- colors and contrast
- icon size and style
- button and card states
- HUD readability over gameplay backgrounds
- animation timing and cause-effect meaning
- mobile safe areas and target breakpoints
- no text overflow, clipping, or layout jumps

Accept small engine-specific differences only when documented and approved.

## QA Checklist

- Main flow is usable with the target input modes.
- Touch targets are comfortable on mobile.
- Focus order is predictable for keyboard/controller.
- Contrast is readable for normal text and state labels.
- Buttons, tabs, cards, resource counters, and modals have clear states.
- Text wraps or scales professionally across target languages.
- Resource numbers and countdowns do not cause layout jumps.
- Loading, empty, error, locked, and unaffordable states are handled.
- Motion is responsive, interruptible, and not excessive.
- Reduced-motion or low-animation fallback exists where needed.
- The UI remains original and project-specific.
