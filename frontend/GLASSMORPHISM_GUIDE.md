# 🎨 Glassmorphism Design System

## Overview

Haniphei.ai uses a modern **glassmorphism** (frosted glass) design aesthetic to create a clean, professional, and interactive user experience. The design features:

- ✨ **Frosted glass effects** with backdrop blur
- 🎭 **Animated SVG icons** instead of static emojis
- 🌊 **Floating animated orbs** in the background
- 🎯 **Smooth transitions** and hover effects
- 🎨 **Gradient accents** for visual depth

---

## Glassmorphism Components

### `.glass` - Base Glass Effect

```jsx
<div className="glass">
  Frosted glass background with blur
</div>
```

**Properties:**
- `background: rgba(255, 255, 255, 0.7)` - Semi-transparent white
- `backdrop-filter: blur(20px)` - Frosted glass blur effect
- `border: 1px solid rgba(255, 255, 255, 0.3)` - Subtle border
- `box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15)` - Soft elevation

### `.glass-card` - Interactive Cards

```jsx
<div className="glass-card">
  <h3>Card Title</h3>
  <p>Card content with hover effects</p>
</div>
```

**Features:**
- Rounded corners (`rounded-2xl`)
- Padding (`p-6`)
- Hover lift animation (`translateY(-4px)`)
- Enhanced shadow on hover

### `.glass-input` - Form Inputs

```jsx
<input 
  type="text" 
  className="glass-input" 
  placeholder="Enter text..."
/>
```

**Features:**
- Frosted background
- Focus state with enhanced clarity
- Blue accent on focus with subtle glow

---

## Animated SVG Icons

All icons are custom-built SVGs with built-in animations. **No emojis or static icons** are used.

### Available Icons

| Icon | Component | Animation | Usage |
|------|-----------|-----------|-------|
| 📄 | `<ScanIcon />` | Scanning beam | Document scanning action |
| ☁️ | `<UploadIcon />` | Bounce arrow | File upload areas |
| 🧠 | `<AnalyzeIcon />` | Pulsing nodes | AI analysis features |
| 📊 | `<ReportIcon />` | Growing bars | Risk reports |
| 🛡️ | `<ShieldIcon />` | Pulsing ring | Risk levels |
| 📝 | `<DocumentIcon />` | Text appearing | Document display |

### Usage Examples

```jsx
import { ScanIcon, UploadIcon, ShieldIcon } from './components/icons';

// Basic usage
<ScanIcon className="w-16 h-16" />

// With custom size
<UploadIcon className="w-24 h-24 text-primary" />

// Shield with risk level
<ShieldIcon className="w-12 h-12" riskLevel="high" />
<ShieldIcon className="w-12 h-12" riskLevel="medium" />
<ShieldIcon className="w-12 h-12" riskLevel="low" />
```

### Icon Animations

Each icon has unique, purpose-built animations:

**ScanIcon:**
- Horizontal scanning beam that moves up and down
- Gradient beam with fade effects
- 2-second loop

**UploadIcon:**
- Arrow bounces up and down
- Opacity pulse effect
- 1.5-second loop

**AnalyzeIcon:**
- Network nodes pulse
- Sparkles appear randomly
- 2-second loop with delays

**ReportIcon:**
- Bar chart columns grow and shrink
- Staggered timing for each bar
- 2-second loop

**ShieldIcon:**
- Pulsing protection ring
- Risk-specific symbols (!, ⚠, ✓)
- Adaptive colors based on risk level

**DocumentIcon:**
- Text lines animate in sequentially
- Left-to-right appearance
- 1-second one-time animation

---

## Animated Background Orbs

The design includes **3 floating orbs** that create dynamic, ambient movement:

```jsx
<div className="orb orb-1"></div>
<div className="orb orb-2"></div>
<div className="orb orb-3"></div>
```

**Orb Properties:**
- **Orb 1:** Blue gradient, top-left, 400px
- **Orb 2:** Purple-cyan gradient, bottom-right, 350px
- **Orb 3:** Green-blue gradient, center, 300px

**Animation:**
- 20-second float cycle
- Staggered delays (0s, 7s, 14s)
- Moves in organic patterns
- Scale variation (0.9x - 1.1x)

---

## Button Styles

### Primary Button

```jsx
<button className="btn-primary">
  Scan Document
</button>
```

**Effects:**
- Gradient blue background
- Glass morphism overlay
- Lift on hover (`translateY(-2px)`)
- Enhanced shadow on hover
- Active press state

### Secondary Button

```jsx
<button className="btn-secondary">
  Cancel
</button>
```

**Effects:**
- Glass background
- Subtle hover lift
- Enhanced transparency on hover

---

## Risk Badges with Glass Effect

```jsx
<span className="badge-high-risk">High Risk</span>
<span className="badge-medium-risk">Medium Risk</span>
<span className="badge-low-risk">Low Risk</span>
```

All badges use glassmorphism with:
- Semi-transparent colored backgrounds
- Frosted blur effect
- Subtle colored borders
- Risk-appropriate colors

---

## Layout Structure

### Page Container

```jsx
<div className="min-h-screen relative overflow-hidden">
  {/* Background orbs */}
  <div className="orb orb-1"></div>
  <div className="orb orb-2"></div>
  <div className="orb orb-3"></div>
  
  {/* Content with z-index */}
  <div className="relative z-10">
    {/* Your content here */}
  </div>
</div>
```

**Key Points:**
- `min-h-screen` ensures full viewport height
- `relative overflow-hidden` contains orbs
- `z-10` on content keeps it above orbs
- Gradient background on `<body>`

---

## Interactive States

### Hover Effects

All interactive elements have smooth transitions:

```css
transition-all duration-300
```

**Glass Cards:**
- Background opacity increases (0.7 → 0.8)
- Lift up 4px
- Shadow enhances

**Buttons:**
- Lift up 2px
- Shadow glows with brand color
- Gradient intensifies

**Inputs:**
- Background clarifies
- Blue glow appears
- Border highlights

---

## Color Integration

Glassmorphism works seamlessly with the theme colors:

```jsx
// Glass with primary color accent
<div className="glass border-primary/30">
  Primary-accented glass
</div>

// Glass with risk colors
<div className="glass bg-danger/10 border-danger/30">
  Danger-tinted glass
</div>
```

**Opacity Levels:**
- Background: `/70` or `0.7` for glass
- Borders: `/30` or `0.3` for subtle outlines
- Color tints: `/10` or `0.1` for backgrounds
- Hover states: `/80` or `/90` for enhanced clarity

---

## Best Practices

### ✅ Do's

- **Layer glass elements** over the gradient background
- **Use animated SVGs** for all icons
- **Apply transitions** to all interactive elements
- **Maintain subtle shadows** for depth
- **Use appropriate blur levels** (blur-md to blur-xl)
- **Keep content above orbs** with z-index

### ❌ Don'ts

- **Don't use emojis** - use animated SVGs instead
- **Don't over-blur** - maintain readability
- **Don't skip hover states** - all interactive elements need feedback
- **Don't use solid backgrounds** - embrace transparency
- **Don't forget accessibility** - ensure sufficient contrast
- **Don't animate everything** - be purposeful

---

## Performance Considerations

### Backdrop Blur Support

Backdrop blur is well-supported in modern browsers:
- ✅ Chrome/Edge 76+
- ✅ Safari 9+
- ✅ Firefox 103+

**Fallback:**
```css
background: rgba(255, 255, 255, 0.9); /* Fallback */
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px); /* Safari */
```

### Optimization Tips

1. **Limit orb count** - 3 is optimal
2. **Use CSS animations** - better performance than JS
3. **Reduce blur on mobile** - if performance issues arise
4. **Lazy load complex SVGs** - for initial page load

---

## Responsive Design

Glass elements adapt to screen sizes:

```jsx
// Mobile-friendly spacing
<div className="glass-card p-4 md:p-6 lg:p-8">
  Responsive padding
</div>

// Grid layouts
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-8">
  {/* Cards */}
</div>
```

**Mobile Adjustments:**
- Reduce blur intensity if needed
- Smaller orb sizes
- Simplified animations
- Touch-friendly sizing (min 44px tap targets)

---

## Code Examples

### Complete Glass Card Component

```jsx
const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="glass-card">
    <div className="flex items-start gap-4">
      <div className="p-3 rounded-2xl bg-primary/10">
        <Icon className="w-12 h-12 text-primary" />
      </div>
      <div>
        <h4 className="text-xl font-semibold text-text-primary mb-2">
          {title}
        </h4>
        <p className="text-text-secondary">
          {description}
        </p>
      </div>
    </div>
  </div>
);
```

### Upload Zone with Glass

```jsx
<div className="glass-card">
  <div className="border-2 border-dashed border-primary/30 rounded-2xl p-12 text-center hover:border-primary/60 transition-all duration-300 glass cursor-pointer">
    <UploadIcon className="w-20 h-20 mx-auto mb-4 text-primary" />
    <p className="text-lg font-medium text-text-primary mb-2">
      Drop your document here
    </p>
  </div>
</div>
```

---

## Team Guidelines

### For Developers (Frontend Team - Yung Sreyneang)

1. **Always use glass classes** for cards and containers
2. **Import animated icons** from `components/icons`
3. **Add transitions** to all interactive elements
4. **Test hover states** for all clickable elements
5. **Ensure z-index layering** is correct

### For Designers

1. Maintain the frosted glass aesthetic
2. Use provided animated icons
3. Stick to the 3-orb background pattern
4. Ensure all interactions have smooth transitions
5. Test designs with actual blur effects

---

## Future Enhancements

- [ ] Dark mode glassmorphism variant
- [ ] More animated icon variations
- [ ] Parallax scrolling effects
- [ ] Micro-interactions on form elements
- [ ] Loading skeleton screens with glass effect
- [ ] Toast notifications with glass styling

---

For questions or suggestions about the glassmorphism design, contact:
- **Frontend Lead:** Yung Sreyneang
- **Technical Lead:** Sun Heng
