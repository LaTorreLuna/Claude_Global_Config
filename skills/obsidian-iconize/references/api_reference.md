# Obsidian Iconize - API Reference

**Developer documentation for programmatic interaction with Obsidian Iconize**

---

## Current Status

⚠️ **Official API documentation is coming soon.**

The Obsidian Iconize plugin is actively developing its public API. This document provides available information and workarounds for developers.

## What's Possible

While official API documentation is pending, developers can interact with Iconize through:

### 1. Frontmatter Properties

The most stable programmatic interface is the frontmatter `icon` property:

```yaml
---
icon: IbBell
---
```

This method is:
- ✅ Documented and stable
- ✅ Works across plugin updates
- ✅ Programmable via templating and scripting plugins

### 2. Plugin Compatibility

Iconize maintains compatibility with other plugins. Documented integrations include:

**Metadatamenu Plugin**
- Icons can be integrated with metadata menu workflows
- See compatibility documentation for implementation details

### 3. Custom CSS Integration

Developers can target Iconize elements via CSS classes:

```css
/* Title icon customization */
.iconize-title-icon {
    width: 1.5em;
    height: 1.5em;
}
```

**Available CSS Classes:**
- `.iconize-title-icon` - Icons above note titles
- Additional classes TBD in official API docs

## Workarounds for Common Tasks

### Programmatic Icon Assignment

Until the official API is available, use these approaches:

**Method 1: Template-Based (Recommended)**

Use Templater or similar plugins to programmatically set frontmatter:

```javascript
<%*
const folder = tp.file.folder(true);
let iconName = "IbFile"; // default

// Assign icons based on folder
if (folder.includes("Projects")) iconName = "IbFolder";
if (folder.includes("Archive")) iconName = "IbArchive";

tR += `icon: ${iconName}`;
%>
```

**Method 2: Dataview Integration**

Create scripts that query files and suggest icon assignments based on properties.

**Method 3: Manual Bulk Operations**

Right-click multiple files while holding Ctrl/Cmd to batch-assign icons (UI-based, not API).

### Reading Current Icons

Currently, there's no documented API method to query which icon is assigned to a file. Workarounds:

1. Read frontmatter `icon` property if using frontmatter method
2. Use Obsidian's metadata cache to check frontmatter
3. Await official API for programmatic icon queries

### Event Listeners

No documented event listeners currently available. Expected in future API:
- `on-icon-changed` - When file/folder icon changes
- `on-icon-pack-loaded` - When icon pack is installed/loaded

## Plugin Development Resources

### GitHub Repository

The [official GitHub repository](https://github.com/FlorianWoelki/obsidian-iconize) provides:
- Source code for understanding implementation
- Issue tracker for API feature requests
- Community discussions about programmatic usage

### Contributing

Iconize is open-source (MIT license). Developers can:
- Submit PRs for API features
- Request specific API endpoints via GitHub issues
- Contribute documentation improvements

## Planned API Features

Based on community discussions and plugin architecture, the API will likely include:

### Expected Methods (Unconfirmed)

```typescript
// These are SPECULATIVE - await official docs
interface IconizeAPI {
  setIcon(file: TFile, iconId: string): Promise<void>;
  getIcon(file: TFile): string | null;
  removeIcon(file: TFile): Promise<void>;
  getAvailableIcons(): string[];
  registerIconPack(pack: IconPack): void;
}
```

**⚠️ Do not implement based on these speculative interfaces - wait for official release.**

## Current Best Practices

### For Plugin Developers

1. **Use frontmatter method** for icon assignment compatibility
2. **Check for Iconize availability** before assuming it's installed:

```typescript
// Check if Iconize is available
const iconizePlugin = this.app.plugins.getPlugin('obsidian-iconize');
if (iconizePlugin) {
  // Plugin is installed and enabled
}
```

3. **Await official API** before building tight integrations
4. **Monitor GitHub** for API release announcements

### For Script Developers

1. Manipulate frontmatter directly for reliable icon control
2. Use Obsidian's metadata cache API to read frontmatter:

```javascript
const metadata = app.metadataCache.getFileCache(file);
const icon = metadata?.frontmatter?.icon;
```

3. Set frontmatter via file processing:

```javascript
await app.fileManager.processFrontMatter(file, (frontmatter) => {
  frontmatter.icon = "IbBell";
});
```

## Requesting API Features

To request specific API functionality:

1. Visit [GitHub Issues](https://github.com/FlorianWoelki/obsidian-iconize/issues)
2. Search for existing API requests
3. Open a new issue with:
   - Use case description
   - Proposed API signature
   - Example implementation

## Stay Updated

**Documentation Updates:**
- Official docs site: https://florianwoelki.github.io/obsidian-iconize/
- GitHub releases: https://github.com/FlorianWoelki/obsidian-iconize/releases
- Community forum discussions

**When Official API Launches:**
- This reference will be updated with complete API documentation
- Breaking changes will be noted
- Migration guides will be provided

---

## Interim Solutions

### QuickAdd Integration

Use QuickAdd macros to assign icons during note creation:

```javascript
module.exports = async (params) => {
  const { app, quickAddApi } = params;

  // Add icon to frontmatter
  await quickAddApi.inputPrompt("Icon ID:");
  // Process and add to frontmatter
};
```

### Templater Integration

Template with dynamic icon selection:

```javascript
<%*
const iconMap = {
  "meeting": "IbCalendar",
  "task": "IbCheckSquare",
  "note": "IbFileText"
};

const type = await tp.system.prompt("Note type?");
tR += `icon: ${iconMap[type] || "IbFile"}`;
%>
```

---

**Last Updated:** October 2025
**API Status:** Coming Soon
**Stable Programmatic Method:** Frontmatter properties

Check back regularly for official API documentation updates.
