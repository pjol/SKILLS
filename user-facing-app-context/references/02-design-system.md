# Design System

## Design Posture

Build a bright, tactile consumer app that still behaves like a serious product surface. The interface should feel approachable, fast, and trustworthy: compact controls, clear hierarchy, responsive grids, real media, strong empty/loading states, and friendly error copy.

## Tailwind Tokens

Use these tokens as the starter palette:

```ts
colors: {
  ink: "#1b1240",
  grape: "#7c55f4",
  punch: "#ff4f7f",
  mint: "#5fe0c1",
  marker: "#ffd15c",
  paper: "#f7f3ff",
  locker: "#5b45d9"
},
boxShadow: {
  float: "0 18px 45px rgba(80, 55, 180, 0.16)"
}
```

Adapt names/colors for the new brand, but keep a multi-color palette: one dark text color, one primary action color, one alert color, one success/accent color, one warm marker, one soft page background, and one secondary brand color.

## Global CSS

- Body uses a soft vertical background rather than a flat white canvas.
- Inputs/selects/textareas have `min-height: 44px` and `font-size: 16px` to avoid mobile zoom.
- Use `.focus-ring` with a visible primary-color ring and page-background offset.
- Use `box-sizing: border-box`, `overflow-x: hidden`, and `touch-action: manipulation` on tappable elements.
- Provide reusable keyframes for subtle fade-up, page slide, and image skeleton shimmer.

## Layout Rules

- Use `max-w-7xl` for app-wide shells and `px-4 sm:px-6 lg:px-8`.
- Prefer mobile-first single-column layouts, then `sm`/`lg` grid expansion.
- Keep controls at `min-h-11` or `min-h-12`.
- Use full-width buttons on mobile when actions sit below forms; switch to auto width on larger screens.
- Do not nest page-section cards inside other cards. Use cards for repeated list items, forms, modals, and framed tools.
- Keep repeated cards stable with fixed aspect ratios, fixed action areas, and matching skeleton dimensions.
- Use sticky sidebars only at desktop widths.

## Type

- Use heavy weights for labels and actions: `font-black` for headings/buttons, `font-semibold` for body support text.
- Use `tracking-normal` for display headings; do not use negative letter spacing.
- Hero headings can be large (`text-4xl sm:text-6xl lg:text-7xl`), but operational panels should use compact headings.
- Uppercase eyebrow labels use small text and generous positive tracking.
- Keep line lengths readable with `max-w-xl`/`max-w-2xl`.

## Buttons and Controls

- Primary action: rounded-full, primary background, white text, strong shadow.
- Secondary action: rounded-full, white/paper background, ink text, subtle border/shadow.
- Destructive/error state: alert tint background and ink/alert text, not tiny red-only copy.
- Icon buttons should use lucide icons and `aria-label`.
- Dropdown triggers use `aria-haspopup`, `aria-expanded`, Escape close, outside click close, and route-change close.
- Segmented choices use button grids with selected state as filled primary and unselected as paper/white.

## Cards and Surfaces

- Default card radius is `rounded-lg`; avoid oversized pill cards except for buttons/chips.
- Border color is usually `border-ink/10`.
- Shadow should be subtle and consistent; the strongest named shadow is reserved for prominent floating surfaces.
- Empty states should include an icon, short heading, helpful text, and a next action.
- Admin/operator cards should be denser and quieter than public marketing cards.

## Forms

- Labels are visible, bold, and above fields.
- Inputs use rounded-md borders, ample padding, and disabled paper backgrounds.
- Form errors appear near the form as rounded alert panels.
- Password fields include a visibility toggle with icon and `aria-pressed`.
- File upload zones use dashed borders, icon, count/status, accepted type/size copy, and list selected filenames.
- Optional fields should say optional in label or placeholder; do not rely on absence of `required`.

## Responsive Navigation

- Public nav:
  - Mobile: brand left, menu button right, main CTA inside dropdown.
  - Desktop: primary links inline, overflow in "More", signed-in profile dropdown.
- Authenticated shell:
  - Sticky top header.
  - Mobile: brand + entitlement/balance + menu icon.
  - Desktop: primary nav pills, overflow "More", entitlement/balance aligned right.
- Footer:
  - Small, global, flex-wrap links.
  - Include support, order/history recovery, legal, and key informational routes.

## Image UX

- Real or generated bitmap media should carry product proof; avoid decorative gradients as substitutes.
- Use skeleton shimmer until images are fully loaded.
- Maintain layout dimensions while loading and on errors.
- Use quality based on rendered size.
- For grids, preload nearby pages/items when smooth transitions matter.

## Motion

- Keep animation small: fade up on entry, slight horizontal slide on paginated/tabbed content, opacity transition on images.
- Avoid motion that changes layout dimensions.
- Respect fast perceived performance: skeletons should appear immediately and match final card size.

## Accessibility

- Every icon-only button needs an `aria-label`.
- Active nav links use `aria-current="page"`.
- Dropdowns use `role="menu"`/`role="menuitem"` where appropriate.
- Modals should close on Escape and have clear buttons.
- Do not hide form labels in placeholders.
- Preserve keyboard focus rings.

## Copy Tone

- Short, friendly, concrete.
- Error messages should tell the user what failed and what to do next.
- Support/refund/billing copy should be clear and plain.
- Avoid exposing internal implementation details, private prompts, provider stack traces, or admin-only keywords.
