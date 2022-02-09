# Slate UI HTML Templating

## Component
```
@componentName
```

## Local variable
```
get: $localVar
set: 
 - string: $localVar="text"
 - component: $localVar=@componentName
```

## Global variable
```
get: %GlobalVar
set: 
 - string: %GlobalVar="text"
 - component: %GlobalVar=@componentName
```

## Conditionals
### Value or default value if undefined
```
value ? defaultValue
```

### Ternary operation
value must be a undefined or string where '', 'false', and '0' equate to false.
```
value ? valueTrue : valueFalse
```

## Wrappers
### Wrap all pages
```
*
```

### Wrap a page
```
*pageName
```

### Wrap a component
```
*@componentName
```

