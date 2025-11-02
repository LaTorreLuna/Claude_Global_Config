---
name: obsidian-iconize
description: Use when working with Obsidian Iconize plugin for adding custom icons to folders, files, and notes in Obsidian vault
---

# Obsidian-Iconize Skill

Comprehensive assistance with obsidian-iconize development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with obsidian-iconize
- Asking about obsidian-iconize features or APIs
- Implementing obsidian-iconize solutions
- Debugging obsidian-iconize code
- Learning obsidian-iconize best practices

## Quick Reference

### Common Patterns

**Adding Icons to Files/Folders**
```
Right-click file/folder → Change Icon (Ctrl/Cmd-Shift-J) → Select icon
```

**Using Frontmatter (Programmatic Method)**
```yaml
---
icon: IbBell
---
```
⚠️ Must enable "Properties" in Iconize settings first!

**Icons in Note Content**
```markdown
Type :iconname: to insert icons inline
Example: :smile: or :IbHome:
```
Works in both edit and preview mode.

**Custom Rules (Default Icons)**
```
Settings → Custom Rules → Input: . → Select default icon
```
Applies to all files/folders without specific icons.

**Icon above Title (Notion-style)**
```
Enable in settings: "Icon above title"
Icon is inherited from file icon
```

**Individual Icon Colors**
```
Right-click icon → Change color of icon → Select/reset color
```

**Icon in Tabs**
```
Enable in settings: "Icons in tabs"
Tabs automatically show file icons
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **frontmatter_guide.md** - ⭐ Complete guide to frontmatter icon usage (NEW)
- **api_reference.md** - ⭐ Developer API documentation and workarounds (NEW)
- **getting_started.md** - Installation and basic setup
- **files_and_folders.md** - File and folder icon management
- **notes.md** - Icons in note content and above titles
- **other.md** - Additional features and settings

Use `view` to read specific reference files when detailed information is needed.

### Priority Reading Order

1. **New users:** Start with `getting_started.md`
2. **Programmatic usage:** Read `frontmatter_guide.md`
3. **Plugin developers:** Check `api_reference.md`
4. **Advanced features:** Explore `files_and_folders.md` and `notes.md`

## Key Features

### Icon Assignment Methods

1. **Manual Assignment** - Right-click context menu (highest priority for specific files)
2. **Frontmatter Properties** - Programmatic via YAML (highest priority, overrides all)
3. **Custom Rules** - Vault-wide default patterns (lowest priority)

### Display Locations

- File explorer (before filename)
- Tabs (requires setting enabled)
- Above note title (Notion-style, requires setting)
- Within note content (`:iconname:` syntax)
- Search results and backlinks

### Customization Options

- Individual icon colors per file/folder
- Icon packs from community or custom SVG
- CSS styling for title icons
- Enable/disable features selectively

## Working with This Skill

### For Beginners
Start with `getting_started.md` for installation, then use the Quick Reference above for common tasks.

### For Frontmatter Users
Read `frontmatter_guide.md` for comprehensive programmatic icon management including:
- Setup requirements (enable Properties setting!)
- Syntax and examples
- Integration with templating plugins
- Troubleshooting common issues

### For Plugin Developers
Check `api_reference.md` for:
- Current API status (coming soon)
- Interim workarounds using frontmatter
- Obsidian metadata cache integration
- Event listeners and plugin compatibility

### For Advanced Features
Explore `files_and_folders.md` and `notes.md` for:
- Custom rules for default icons
- Icon color customization
- Icons in note content
- Title icons (Notion-style)

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

### Skill Enhancements (October 2025)

This skill has been **enhanced** with comprehensive documentation:

✅ **New Content Added:**
- Complete frontmatter usage guide with troubleshooting
- Developer API reference with interim workarounds
- Enhanced quick reference patterns for common tasks
- Priority reading order for different user types
- Integration examples with Templater and Dataview

✅ **Documentation Sources:**
- Official documentation site scraped
- WebFetch analysis of key pages
- Code examples extracted and annotated
- Best practices consolidated

### Original Features Preserved

- Automatically generated from official documentation
- Reference files preserve structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples

### Troubleshooting

**Frontmatter icons not working?**
→ Read `frontmatter_guide.md` section "Troubleshooting"

**Need programmatic control?**
→ Check `api_reference.md` for current workarounds

**General usage questions?**
→ Start with Quick Reference above, then read relevant reference file

## Updating

To refresh this skill with updated documentation:
1. Re-run Skill Seeker with obsidian-iconize documentation URL
2. Or manually add new reference files to `references/`
3. Update SKILL.md with new quick reference patterns

**Last Enhanced:** October 25, 2025
**Documentation Source:** https://florianwoelki.github.io/obsidian-iconize/
