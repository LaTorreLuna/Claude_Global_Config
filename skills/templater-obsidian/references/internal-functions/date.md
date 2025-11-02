# tp.date Module - Date Functions

**Source:** https://silentvoid13.github.io/Templater/internal-functions/internal-modules/date-module.html

All date functions use moment.js formatting. See: https://momentjs.com/docs/#/displaying/format/

## Functions

### tp.date.now()

**Signature:** `tp.date.now(format: string = "YYYY-MM-DD", offset?: number⎮string, reference?: string, reference_format?: string)`

Retrieves the current date with optional offset and reference capabilities.

**Parameters:**
- `format`: Date format (default: "YYYY-MM-DD"). Uses moment.js formatting
- `offset`: Day offset (number) or ISO 8601 duration string (e.g., "P-1M")
- `reference`: Reference date source (e.g., file title)
- `reference_format`: Format pattern for reference date

**Examples:**
```javascript
// Basic - outputs current date
<% tp.date.now() %>
// Output: 2024-01-15

// Custom format
<% tp.date.now("Do MMMM YYYY") %>
// Output: 15th January 2024

// With offset (numeric - days)
<% tp.date.now("YYYY-MM-DD", -7) %>
// Output: 2024-01-08 (last week)

<% tp.date.now("YYYY-MM-DD", 30) %>
// Output: 2024-02-14 (30 days from now)

// ISO 8601 duration offset
<% tp.date.now("YYYY-MM-DD", "P1Y") %>
// Output: 2025-01-15 (next year)

<% tp.date.now("YYYY-MM-DD", "P-1M") %>
// Output: 2023-12-15 (last month)

<% tp.date.now("YYYY-MM-DD", "P1W") %>
// Output: 2024-01-22 (next week)

// With reference date
<% tp.date.now("YYYY-MM-DD", 0, "2024-03-15", "YYYY-MM-DD") %>
// Output: 2024-03-15
```

### tp.date.tomorrow()

**Signature:** `tp.date.tomorrow(format: string = "YYYY-MM-DD")`

Returns tomorrow's date with specified formatting.

**Examples:**
```javascript
<% tp.date.tomorrow() %>
// Output: 2024-01-16

<% tp.date.tomorrow("Do MMMM YYYY") %>
// Output: 16th January 2024

<% tp.date.tomorrow("dddd") %>
// Output: Tuesday
```

### tp.date.yesterday()

**Signature:** `tp.date.yesterday(format: string = "YYYY-MM-DD")`

Returns yesterday's date with specified formatting.

**Examples:**
```javascript
<% tp.date.yesterday() %>
// Output: 2024-01-14

<% tp.date.yesterday("Do MMMM YYYY") %>
// Output: 14th January 2024
```

### tp.date.weekday()

**Signature:** `tp.date.weekday(format: string = "YYYY-MM-DD", weekday: number, reference?: string, reference_format?: string)`

Retrieves a specific weekday relative to current date or reference.

**Parameters:**
- `weekday`: Day number (0 = Monday in standard locale, -7 = previous week)
- `reference`: Optional date reference
- `reference_format`: Format for reference date

**Examples:**
```javascript
// This week's Monday (0)
<% tp.date.weekday("YYYY-MM-DD", 0) %>

// This week's Friday (4)
<% tp.date.weekday("YYYY-MM-DD", 4) %>

// Next week's Monday (7)
<% tp.date.weekday("YYYY-MM-DD", 7) %>

// Last week's Wednesday (-5)
<% tp.date.weekday("YYYY-MM-DD", -5) %>
```

## Common Format Patterns

| Pattern | Output Example |
|---------|----------------|
| `YYYY-MM-DD` | 2024-01-15 |
| `YYYY/MM/DD` | 2024/01/15 |
| `DD-MM-YYYY` | 15-01-2024 |
| `MMMM Do, YYYY` | January 15th, 2024 |
| `dddd, MMMM Do YYYY` | Monday, January 15th 2024 |
| `YYYY-MM-DD HH:mm` | 2024-01-15 14:30 |
| `YYYY-MM-DD HH:mm:ss` | 2024-01-15 14:30:45 |
| `HH:mm` | 14:30 |
| `h:mm A` | 2:30 PM |
| `dddd` | Monday |
| `MMMM` | January |
| `MMM` | Jan |
| `Do` | 15th |

## ISO 8601 Duration Strings

| Duration | Meaning |
|----------|---------|
| `P1D` | 1 day |
| `P7D` | 7 days |
| `P1W` | 1 week |
| `P1M` | 1 month |
| `P1Y` | 1 year |
| `P-1D` | -1 day (yesterday) |
| `P-1M` | -1 month |

## Advanced Usage

Access moment.js object directly for advanced manipulation:

```javascript
<%*
const date = tp.date.now();
// Use moment.js methods
%>
```

Available moment.js methods include:
- `.startOf()` - Start of period
- `.endOf()` - End of period
- `.add()` - Add duration
- `.subtract()` - Subtract duration
- `.isBefore()` - Compare dates
- `.isAfter()` - Compare dates
