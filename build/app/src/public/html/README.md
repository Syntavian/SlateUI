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
```
value ? defaultValue
```
