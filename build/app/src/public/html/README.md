# Slate UI HTML Templating

## Component
```
@componentName
```

## Local variable
```
get: $localVariable
set: 
 - string: $localVariable="text"
 - component: $localVariable=@componentName
```

## Global variable
```
get: %globalVariable
set: 
 - string: %globalVariable="text"
 - component: %globalVariable=@componentName
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
