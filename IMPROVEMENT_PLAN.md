# DrawIO Roadmaps - Improvement Plan

This document outlines identified issues and proposed improvements for the DrawIO rendering functionality.

---

## Critical Issues (Runtime Errors)

### 1. LifeLine class missing `events` attribute
**File:** `drawio_roadmaps/classes/lifeline.py:24-27`
```python
def __str__(self, indent=0):
    lifeline_str = ' ' * indent + f"LifeLine: {self.name} [{self.type.metadata_drawio.color}]\n"
    for event in self.events:  # AttributeError: 'LifeLine' has no attribute 'events'
```
**Problem:** The `__init__` method never initializes `self.events`, but `__str__` tries to iterate over it.

**Fix:** Add `self.events = []` to `__init__` method.

---

### 2. LifeLine accessing non-existent `.color` attribute
**File:** `drawio_roadmaps/classes/lifeline.py:25`
```python
lifeline_str = ' ' * indent + f"LifeLine: {self.name} [{self.type.metadata_drawio.color}]\n"
```
**Problem:** `LifeLineMetadataDrawio` only has `strokeColor`, not `color`.

**File:** `drawio_roadmaps/enums/lifeline_type.py:8-10`
```python
class LifeLineMetadataDrawio:
    def __init__(self, strokeColor):
        self.strokeColor = strokeColor  # Only this exists
```

**Fix:** Change `.color` to `.strokeColor` in lifeline.py.

---

### 3. StringEventRenderer method signature mismatch
**File:** `drawio_roadmaps/renderers/event_renderer.py:19-22`
```python
class StringEventRenderer(EventRenderer):
    def render_event(self, event):  # Wrong signature!
        event_str = f"Event: {event.description} {event.event_type} {event.metadata_drawio.fillColor}\n"
```
**Problems:**
1. Missing `segment_width` and `years` parameters (doesn't match base class)
2. Accesses `event.metadata_drawio.fillColor` which doesn't exist (should be `event.event_type.render_meta.fillColor`)

**Fix:** Correct method signature and attribute access.

---

### 4. Missing `raise` statements in drawio_shapes.py
**File:** `drawio_roadmaps/drawio/drawio_shapes.py:119-121, 212-214, 281-283`
```python
except Exception as e:
    print(e)
    RuntimeError('Error creating circle')  # Missing 'raise'!
```
**Problem:** `RuntimeError` is instantiated but never raised, silently swallowing errors.

**Fix:** Add `raise` keyword before each `RuntimeError`.

---

## High Priority Issues

### 5. Duplicate `__repr__` method in Event class
**File:** `drawio_roadmaps/classes/event.py:24-26, 31-33`
```python
def __repr__(self):  # First definition (line 24)
    market = self.event_type.marker if self.event_type else '='
    return f"{market} {self.description} - {self.date.strftime('%Y-%m-%d')}"

def __repr__(self):  # Second definition (line 31) - overwrites first!
    return f"{self.event_type.marker} {self.description} [{self.date.strftime('%Y-%m-%d')} "
```
**Fix:** Remove the duplicate method. Keep the more informative version.

---

### 6. Typo: `set_roamap` instead of `set_roadmap`
**File:** `drawio_roadmaps/classes/swimlane.py:99`
```python
def set_roamap(self, roadmap):  # Typo!
    self.roadmap = roadmap
```
**Fix:** Rename to `set_roadmap`. Update all callers.

---

### 7. DrawIOEventRenderer returns placeholder instead of real XML
**File:** `drawio_roadmaps/renderers/event_renderer.py:24-27`
```python
class DrawIOEventRenderer(EventRenderer):
    def render_event(self, event, segment_width, years):
        # Simplified representation; actual implementation will generate XML
        return f"<event name='{event.name}' date='{event.date}'/>"  # Placeholder!
```
**Fix:** Implement proper XML generation using the existing `Circle` class and DrawIO utilities.

---

### 8. PowerPointEventRenderer has no actual implementation
**File:** `drawio_roadmaps/renderers/event_renderer.py:65-71`
```python
def render_event(self, event, segment_width, years):
    if not self.pptx_available:
        print("python-pptx library is not installed...")
        return
    # Placeholder implementation
    print(f"Rendering event '{event.name}' in PowerPoint format")
```
**Fix:** Implement actual PowerPoint shape rendering.

---

## Medium Priority Issues

### 9. Abstract base classes don't inherit from ABC
**Files:** Multiple renderer files
```python
class RoadmapRenderer:  # Should be: class RoadmapRenderer(ABC):
    @abstractmethod
    def render(self):
        raise NotImplementedError
```
**Affected classes:**
- `RoadmapRenderer` (`roadmap_renderer.py`)
- `SwimlaneRenderer` (`swimlane_renderer.py`)
- `EventRenderer` (`event_renderer.py`)
- `LifeLineRenderer` (`lifeline_renderer.py`)
- `RoadmapLoader` (`loaders/loaders.py`)

**Fix:** Add `from abc import ABC, abstractmethod` and inherit from `ABC`.

---

### 10. Hardcoded Windows path for DrawIO executable
**File:** `drawio_roadmaps/config.py`
```python
DRAWIO_EXECUTABLE_PATH = 'C:\\Program Files\\draw.io\\draw.io.exe'
```
**Fix:** Make platform-aware or configurable via environment variable.

---

### 11. Magic numbers scattered throughout code
**File:** `drawio_roadmaps/renderers/roadmap_renderer_drawio.py`
- Line 114: Hardcoded `9px` height offset
- Line 203: Hardcoded `36` character truncation
- Multiple hardcoded spacing calculations

**Fix:** Extract to named constants in config or class attributes.

---

## Low Priority / Code Quality

### 12. TODO comments to address
| File | Line | TODO |
|------|------|------|
| `roadmap_renderer_drawio.py` | 21 | Get years based on dates in roadmap |
| `roadmap_renderer_drawio.py` | 203 | Truncation magic should be refactored |
| `swimlane_renderer.py` | 17, 34 | Config handling and event rendering |
| `lifeline.py` | 10 | Type hints for roadmap and swimlane |
| `roadmap.py` | 11 | Refactor start_year/first_year consistency |

---

### 13. Unnecessary `pass` statements
**File:** `drawio_roadmaps/config.py:13, 19, 22`
```python
class DrawIO:
    year_length_px = 240
    pass  # Unnecessary

class PowerPoint:
    pass  # Empty class

class Text:
    pass  # Empty class
```
**Fix:** Remove unnecessary `pass` statements; consider removing empty classes.

---

### 14. Commented-out code to remove
**File:** `drawio_roadmaps/classes/roadmap.py:22-36`
Large block of commented-out property definitions for `first_year` and `last_year`.

**Fix:** Remove commented code or restore if needed.

---

### 15. Debug print statements in production code
**File:** `drawio_roadmaps/drawio/drawio_shapes.py:153-154`
```python
print(self.style)
print(self.kwargs['style'])
```
**Fix:** Remove or convert to proper logging.

---

### 16. Duplicate key in dictionary
**File:** `drawio_roadmaps/drawio/drawio_shapes.py:324, 332`
```python
self.style = {
    'strokeColor': 'none',  # First occurrence
    ...
    'strokeColor': '#000000',  # Duplicate - overwrites first
}
```
**Fix:** Remove duplicate key.

---

## Implementation Priority

### Phase 1: Critical Fixes (Must Do)
1. [ ] Fix LifeLine missing `events` attribute
2. [ ] Fix LifeLine `.color` → `.strokeColor`
3. [ ] Fix StringEventRenderer signature and attributes
4. [ ] Add missing `raise` statements in drawio_shapes.py

### Phase 2: High Priority (Should Do)
5. [ ] Remove duplicate `__repr__` in Event
6. [ ] Fix `set_roamap` typo
7. [ ] Implement DrawIOEventRenderer properly
8. [ ] Make abstract classes inherit from ABC

### Phase 3: Medium Priority (Nice to Have)
9. [ ] Extract magic numbers to constants
10. [ ] Make DrawIO executable path configurable
11. [ ] Address TODO comments

### Phase 4: Code Quality
12. [ ] Remove unnecessary pass statements
13. [ ] Remove commented-out code
14. [ ] Remove debug print statements
15. [ ] Fix duplicate dictionary keys

---

## Testing Recommendations

After fixes, test the following scenarios:
1. Create a roadmap with lifelines and verify `__str__` works
2. Render events using StringEventRenderer
3. Generate DrawIO XML and verify it's valid
4. Test error handling in shape creation functions
5. Verify all renderers have consistent method signatures
