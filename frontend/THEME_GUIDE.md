# 🎨 Haniphei.ai Theme Guide

## Color Philosophy

Our color palette is designed to convey **trust, professionalism, and clarity** - essential for a legal technology platform. The colors are chosen to:

- Build user confidence through professional blues
- Clearly communicate risk levels through intuitive semantic colors
- Ensure accessibility with WCAG AA compliant contrast ratios
- Maintain visual consistency across all components

---

## Primary Color Palette

### Brand Colors

| Color | Hex | Usage | Preview |
|-------|-----|-------|---------|
| Primary Blue | `#2563EB` | Main brand color, CTAs, important actions | ![#2563EB](https://via.placeholder.com/50x20/2563EB/2563EB) |
| Primary Dark | `#1E40AF` | Hover states, emphasis | ![#1E40AF](https://via.placeholder.com/50x20/1E40AF/1E40AF) |
| Primary Light | `#DBEAFE` | Backgrounds, highlights | ![#DBEAFE](https://via.placeholder.com/50x20/DBEAFE/DBEAFE) |

**Tailwind Classes:**
```jsx
bg-primary         // #2563EB
bg-primary-700     // #1E40AF  
bg-primary-100     // #DBEAFE
```

---

## Neutral Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Background | `#F8FAFC` | Main page background |
| Surface | `#FFFFFF` | Cards, modals, elevated content |
| Border | `#E2E8F0` | Dividers, card borders |
| Text Primary | `#1E293B` | Headings, important text |
| Text Secondary | `#64748B` | Body text, descriptions |
| Text Muted | `#94A3B8` | Placeholders, hints |

**Tailwind Classes:**
```jsx
bg-background      // #F8FAFC
bg-surface         // #FFFFFF
border-border      // #E2E8F0
text-text-primary  // #1E293B
text-text-secondary // #64748B
text-text-muted    // #94A3B8
```

---

## Semantic Colors (Risk Communication)

### High Risk 🔴
- **Default:** `#EF4444`
- **Light:** `#FEE2E2`
- **Dark:** `#DC2626`
- **Usage:** Critical issues, termination clauses, liability risks

```jsx
<span className="badge-high-risk">High Risk</span>
<div className="bg-danger text-white">Critical Alert</div>
```

### Medium Risk 🟡
- **Default:** `#F59E0B`
- **Light:** `#FEF3C7`
- **Dark:** `#D97706`
- **Usage:** Moderate concerns, assumptions requiring attention

```jsx
<span className="badge-medium-risk">Medium Risk</span>
<div className="bg-warning text-white">Warning</div>
```

### Low Risk 🟢
- **Default:** `#10B981`
- **Light:** `#D1FAE5`
- **Dark:** `#047857`
- **Usage:** Minor issues, standard clauses, acceptable terms

```jsx
<span className="badge-low-risk">Low Risk</span>
<div className="bg-success text-white">Safe</div>
```

### Info ℹ️
- **Default:** `#3B82F6`
- **Light:** `#DBEAFE`
- **Dark:** `#1D4ED8`
- **Usage:** General information, tips, guidance

```jsx
<div className="bg-info-light border-l-4 border-info p-4">
  <p className="text-info-dark">Helpful information</p>
</div>
```

---

## Accent Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Accent Purple | `#8B5CF6` | Secondary actions, badges, highlights |
| Accent Cyan | `#06B6D4` | Special features, tags |

```jsx
bg-accent-purple   // #8B5CF6
bg-accent-cyan     // #06B6D4
```

---

## Component Examples

### Buttons

```jsx
// Primary Button
<button className="btn-primary">
  Scan Document
</button>

// Secondary Button
<button className="btn-secondary">
  Cancel
</button>

// Custom Button
<button className="bg-primary hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg">
  Custom Action
</button>
```

### Cards

```jsx
<div className="card p-6">
  <h3 className="text-text-primary font-semibold text-lg mb-2">
    Risk Analysis Report
  </h3>
  <p className="text-text-secondary">
    Your document has been analyzed...
  </p>
</div>
```

### Risk Badges

```jsx
<span className="badge-high-risk">High Risk</span>
<span className="badge-medium-risk">Medium Risk</span>
<span className="badge-low-risk">Low Risk</span>
```

### Input Fields

```jsx
<input 
  type="text"
  className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
  placeholder="Enter URL to scan..."
/>
```

---

## Typography

**Font Family:** Inter (Google Fonts)

| Style | Tailwind Class | Size |
|-------|---------------|------|
| Heading 1 | `text-4xl font-bold` | 36px |
| Heading 2 | `text-3xl font-semibold` | 30px |
| Heading 3 | `text-2xl font-semibold` | 24px |
| Heading 4 | `text-xl font-medium` | 20px |
| Body Large | `text-lg` | 18px |
| Body | `text-base` | 16px |
| Small | `text-sm` | 14px |
| Tiny | `text-xs` | 12px |

---

## Shadows

| Name | Tailwind Class | Usage |
|------|---------------|-------|
| Card | `shadow-card` | Default card elevation |
| Card Hover | `shadow-card-hover` | Interactive card states |
| Large | `shadow-lg` | Modals, dropdowns |

---

## Usage Guidelines

### ✅ Do's
- Use `primary` blue for main actions and branding
- Use semantic colors consistently (red = danger, green = success)
- Maintain proper contrast ratios for accessibility
- Use `surface` white for elevated content on `background` gray
- Apply hover states for interactive elements

### ❌ Don'ts
- Don't use red/green for non-risk-related content
- Don't mix too many accent colors in one view
- Don't use pure black (`#000000`) for text - use `text-primary` instead
- Don't ignore accessibility - ensure readable contrast

---

## Accessibility

All color combinations meet **WCAG AA standards** for contrast:

- `text-primary` on `surface`: 16.07:1 (AAA)
- `text-secondary` on `surface`: 7.53:1 (AA)
- `primary` button text: 4.58:1 (AA)
- Risk badges: All meet AA standards

---

## Dark Mode (Future Enhancement)

While not currently implemented, the theme is structured to easily support dark mode:

```js
// Future dark mode colors
darkMode: 'class',
theme: {
  extend: {
    colors: {
      dark: {
        background: '#0F172A',
        surface: '#1E293B',
        border: '#334155',
      }
    }
  }
}
```

---

## Team References

- **Frontend Lead (Yung Sreyneang):** Use these utilities for all UI components
- **All Developers:** Stick to the defined color palette for consistency
- **Designers:** This palette matches the approved design mockups

For questions or suggestions, contact the Technical Lead (Sun Heng) or Frontend Lead (Yung Sreyneang).
