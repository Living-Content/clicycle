# Release Notes - v2.0.0

## 🎉 Clicycle 2.0 - Component-Based CLI Revolution

We're excited to announce Clicycle 2.0, a complete reimagining of how you build beautiful command-line interfaces in Python!

### 🚀 What's New

#### Component-Based Architecture
Clicycle now treats terminal output as composable components that automatically manage their own spacing and styling. No more manual print statements or spacing calculations!

#### Simplified API
```python
import clicycle as cc

cc.header("My App", "v2.0.0")
cc.info("Starting process...")
with cc.spinner("Processing..."):
    # Your code here
cc.success("Complete!")
```

#### Interactive Components
New arrow-key navigation for user selections:
```python
choice = cc.select("Choose an option:", ["Option A", "Option B", "Option C"])
selections = cc.multi_select("Select features:", ["Feature 1", "Feature 2", "Feature 3"])
```

#### Disappearing Spinners
Spinners can now completely vanish when done, leaving a clean terminal:
```python
theme = cc.Theme(disappearing_spinners=True)
cc.configure(theme=theme)
```

### 💔 Breaking Changes

- **Python 3.11+ Required**: We've updated to Python 3.11 minimum for better type hints and performance
- **API Changes**: The main API is now function-based rather than class-based (though `Clicycle` class is still available for advanced use)

### 📦 Installation

```bash
pip install --upgrade clicycle
```

### 📚 Documentation

Check out our updated [README](https://github.com/Living-Content/clicycle) and explore the new [examples](https://github.com/Living-Content/clicycle/tree/main/examples).

### 🙏 Thanks

Thanks to all our users for your feedback that shaped this release!