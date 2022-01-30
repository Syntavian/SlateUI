# SlateUI

SlateUI is simple web application styling framework with the goal of speeding up development of apps with vanilla HTML, JS, & CSS.

SlateUI is built with Sass to produce a large library of prebuilt styles you can apply to your HTML, and the build tool will compile the styles you use into a minified CSS file to minimise the final app size.

## Create Optimised Build From Dev
```
python dev/slate_build_dev.py
```

### Build Mapping
```
dev......       ┌──>build
        ⁞       │       ⁞
        python──┘       app..........
        ⁞               ⁞           ⁞
        js──────────┐   ⁞       ┌──>public...
        ⁞           │   ⁞       │           ⁞
    ┌───scss        └───⁞───────│───┌──────>js
    │   ⁞               ⁞       │   │       ⁞
    └──>css─────┐       ⁞       │   │   ┌──>css
                │       ⁞       │   │   │
                │       html────┘   │   │
                │       ⁞           │   │
                │       js──────────┘   │
                │       ⁞               │
                │       css─────────────│
                │       ⁞               │
                └──────>slate_ui────────┘
```
