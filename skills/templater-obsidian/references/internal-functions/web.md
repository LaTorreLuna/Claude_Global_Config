# tp.web Module - Web Requests and External Data

**Source:** https://silentvoid13.github.io/Templater/internal-functions/internal-modules/web-module.html

The `tp.web` module provides functions for web interactions and fetching external content.

## Functions

### tp.web.daily_quote()

**Signature:** `tp.web.daily_quote()`

Retrieves daily quotes from a GitHub quotes database and formats them as callouts.

**Example:**
```javascript
<% await tp.web.daily_quote() %>
```

**Output:**
```
> Do the best you can until you know better. Then when you know better, do better.
> — Maya Angelou
```

**Note:** This is an **async function** - must use `await`

### tp.web.random_picture()

**Signature:** `tp.web.random_picture(size?: string, query?: string, include_size?: boolean)`

Fetches random images from Unsplash with optional parameters for dimensions and search filtering.

**Parameters:**
- `size`: Image dimensions (e.g., "200x200", "1920x1080")
- `query`: Search query for filtering images (e.g., "nature", "landscape,water")
- `include_size`: Whether to include size in markdown (default: true)

**Examples:**
```javascript
// Basic random image
<% await tp.web.random_picture() %>

// Specific size
<% await tp.web.random_picture("200x200") %>

// With search query
<% await tp.web.random_picture("1920x1080", "nature") %>

// Multiple search terms
<% await tp.web.random_picture("200x200", "landscape,water") %>

// Without size in output
<% await tp.web.random_picture("400x300", "sunset", false) %>
```

**Output:**
```markdown
![](https://source.unsplash.com/200x200/?nature)
```

**Note:** This is an **async function** - must use `await`

### tp.web.request()

**Signature:** `tp.web.request(url: string, path?: string)`

Executes HTTP requests to specified URLs with optional JSON path extraction for targeted data retrieval.

**Parameters:**
- `url`: The URL to fetch
- `path`: JSON path for extracting specific data (optional)

**Examples:**
```javascript
// Basic request - returns entire response
<% await tp.web.request("https://api.example.com/data") %>

// With JSON path extraction
<% await tp.web.request("https://jsonplaceholder.typicode.com/todos", "0.title") %>

// Access nested JSON
<% await tp.web.request("https://api.github.com/users/octocat", "name") %>

// Array access
<% await tp.web.request("https://api.example.com/items", "[0].name") %>
```

**JSON Path Examples:**

Given JSON response:
```json
{
  "user": {
    "name": "John Doe",
    "email": "john@example.com",
    "posts": [
      {"id": 1, "title": "First Post"},
      {"id": 2, "title": "Second Post"}
    ]
  }
}
```

Access patterns:
```javascript
// Get user name
<% await tp.web.request(url, "user.name") %>
// Output: John Doe

// Get user email
<% await tp.web.request(url, "user.email") %>
// Output: john@example.com

// Get first post title
<% await tp.web.request(url, "user.posts.0.title") %>
// Output: First Post

// Get all post titles (if path supports arrays)
<% await tp.web.request(url, "user.posts[*].title") %>
```

**Note:** This is an **async function** - must use `await`

## Common Workflows

### Daily Note with Quote and Image

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
---

# <% tp.date.now("dddd, MMMM Do YYYY") %>

## Daily Inspiration

<% await tp.web.daily_quote() %>

## Daily Image

<% await tp.web.random_picture("800x400", "nature,landscape") %>

## Notes

<% tp.file.cursor(1) %>
```

### Fetch API Data for Template

```javascript
<%*
// Fetch todo item from API
const todoTitle = await tp.web.request(
    "https://jsonplaceholder.typicode.com/todos/1",
    "title"
);
%>

# Task: <% todoTitle %>

**Status:** Pending
**Created:** <% tp.date.now() %>

<% tp.file.cursor(1) %>
```

### Dynamic Content from External Source

```javascript
<%*
// Fetch GitHub user info
const username = await tp.system.prompt("GitHub username");
const name = await tp.web.request(
    `https://api.github.com/users/${username}`,
    "name"
);
const bio = await tp.web.request(
    `https://api.github.com/users/${username}`,
    "bio"
);
%>

# GitHub Profile: <% name %>

**Username:** @<% username %>
**Bio:** <% bio %>
```

### Weather Data Integration (Example)

```javascript
<%*
// Note: Requires API key and proper endpoint
const city = await tp.system.prompt("City name", "London");
const weatherData = await tp.web.request(
    `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=YOUR_API_KEY`
);
// Note: This is a conceptual example - actual implementation depends on API
%>

# Weather for <% city %>

**Date:** <% tp.date.now("YYYY-MM-DD HH:mm") %>

<% tp.file.cursor(1) %>
```

### Random Image Gallery

```javascript
# Image Gallery

## Nature
<% await tp.web.random_picture("400x300", "nature") %>

## Architecture
<% await tp.web.random_picture("400x300", "architecture") %>

## Technology
<% await tp.web.random_picture("400x300", "technology") %>
```

### Quote Collection

```javascript
# Daily Quotes - <% tp.date.now("YYYY-MM-DD") %>

## Quote 1
<% await tp.web.daily_quote() %>

## Quote 2
<% await tp.web.daily_quote() %>

## Quote 3
<% await tp.web.daily_quote() %>
```

## Error Handling

Web requests can fail due to network issues, API limits, or invalid URLs. Consider error handling:

```javascript
<%*
try {
    const data = await tp.web.request("https://api.example.com/data");
    tR += `Data: ${data}`;
} catch (error) {
    tR += "Failed to fetch data";
}
%>
```

## Best Practices

1. **Always use `await`**:
   ```javascript
   // CORRECT
   <% await tp.web.daily_quote() %>

   // INCORRECT - will not work
   <% tp.web.daily_quote() %>
   ```

2. **Store results for reuse**:
   ```javascript
   <%* const quote = await tp.web.daily_quote() %>
   <% quote %>

   ---
   Share this quote: <% quote %>
   ```

3. **Use JSON paths for efficiency**:
   ```javascript
   // EFFICIENT - extract only what you need
   <% await tp.web.request(url, "user.name") %>

   // INEFFICIENT - fetches everything then manually parse
   <%* const data = JSON.parse(await tp.web.request(url)) %>
   <% data.user.name %>
   ```

4. **Combine with prompts for dynamic queries**:
   ```javascript
   <%* const query = await tp.system.prompt("Search for") %>
   <% await tp.web.random_picture("400x300", query) %>
   ```

5. **Consider rate limits**:
   - APIs may have rate limits
   - Daily quote may return the same quote on same day
   - Unsplash has usage limits

## Limitations

- Requires internet connection
- Subject to external API availability and limits
- CORS restrictions may apply to some endpoints
- JSON path syntax support may vary
- Response parsing errors can occur with malformed data

## Security Considerations

- Never expose API keys in templates that might be shared
- Validate URLs before making requests
- Be cautious with user-provided URLs
- Consider data privacy when fetching external content

## Additional Resources

- Unsplash API: https://unsplash.com/developers
- JSON Path syntax: https://goessner.net/articles/JsonPath/
- HTTP request methods: GET only (no POST, PUT, DELETE)
