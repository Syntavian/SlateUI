# SlateUI

SlateUI is simple web application styling framework with the goal of speeding up development of apps with vanilla HTML, JS, & CSS.

SlateUI is built with Sass to produce a large library of prebuilt styles you can apply to your HTML, and the build tool will compile the styles you use into a minified CSS file to minimise the final app size.

## Create Optimised Build From Dev
```
python dev/slate_build_dev.py
```

### Build Mapping
```
dev......                   build....
        ⁞                           ⁞       
        slate_dev.py────────┐       app......
        ⁞                   │               ⁞
        python/*.py─────────│               slate........
        ⁞                   │               ⁞           ⁞
    ┌───scss/*.scss         └───────────────⁞──────────>slate.py
    │   ⁞                                   ⁞           ⁞
    └──>css/*.css───────────────────────────⁞──────────>slate.css───┐
        ⁞                                   ⁞                       │
        js.......                           public..................│....................
                ⁞                           ⁞                       │                   ⁞
            ┌───src/*.js                    ⁞                       │                   css..........
            │   ⁞                           ⁞                       │                   ⁞           ⁞
            └──>lib/*.js────────────────────⁞───────────────────┐   └───────────────────⁞──────────>slate.css
                                            ⁞                   │                       ⁞           ⁞
                                            ⁞                   │           ┌───────────⁞──────────>*.css
                                            ⁞                   │           │           ⁞
                                            ⁞                   │           │           js...........
                                            ⁞                   │           │           ⁞           ⁞
                                            ⁞                   └───────────│───────────⁞──────────>slate.js
                                            ⁞                               │           ⁞           ⁞
                                            ⁞                               │   ┌───────⁞──────────>*.js
                                            ⁞                               │   │       ⁞
                                            ⁞                               │   │   ┌──>*/*.html
                                            ⁞                               │   │   │ 
                                            src..........                   │   │   │               
                                            ⁞           ⁞                   │   │   │
                                            ⁞           public...           │   │   │
                                            ⁞           ⁞       ⁞           │   │   │
                                            ⁞           ⁞       css/*.css───┘   │   │  
                                            ⁞           ⁞       ⁞               │   │ 
                                            ⁞           ⁞       js/*.js─────────┘   │ 
                                            ⁞           ⁞       ⁞                   │
                                            ⁞           ⁞       html/*/*.html───────┘
                                            ⁞           ⁞
                                        ┌───⁞───────────*.js
                                        │   ⁞           
                                        └──>lib/*.js
```