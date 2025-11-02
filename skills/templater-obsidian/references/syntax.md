# Templater Syntax Documentation

**Source:** https://silentvoid13.github.io/Templater/syntax.html

## Core Command Structure

Commands require opening `<%` and closing `%>` tags. A complete example: `<% tp.date.now() %>`

## Function Hierarchy

All Templater functions exist under the `tp` object using dot notation. Functions are invoked by appending parentheses: `tp.date.now()`

## Argument Passing

Arguments go between parentheses in correct order:
```javascript
tp.date.now(arg1_value, arg2_value, arg3_value, ...)
```

### Argument Types

- **String**: Use single or double quotes (`"value"` or `'value'`)
- **Number**: Integer values (`15`, `-5`)
- **Boolean**: Lowercase `true` or `false` only

## Documentation Syntax

Function signatures use this pattern:
```
tp.<function>(arg1: type, arg2?: type, arg3: type = <default>, arg4: type1|type2)
```

Where:
- `?` indicates optional arguments
- `=` shows default values
- `|` indicates multiple accepted types

**Critical note:** "this syntax is for documentation purposes only" — don't include argument names, types, or defaults in actual function calls.

## Valid vs. Invalid Examples

### Valid invocations:
```javascript
<% tp.date.now() %>
<% tp.date.now("YYYY-MM-DD", 7) %>
<% tp.date.now("dddd, MMMM Do YYYY", 0, tp.file.title, "YYYY-MM-DD") %>
```

### Invalid invocations:
```javascript
// DON'T DO THIS - includes type annotations
tp.date.now(format: string = "YYYY-MM-DD")

// DON'T DO THIS - includes optional markers and defaults
tp.date.now(format: string = "YYYY-MM-DD", offset?: 0)
```

## Best Practices

1. **Always omit types** - Use values only: `tp.date.now("YYYY-MM-DD")`
2. **Respect argument order** - Parameters must be in documented order
3. **Quote strings properly** - Use quotes for string arguments
4. **Use correct boolean syntax** - Always lowercase: `true`, `false`
