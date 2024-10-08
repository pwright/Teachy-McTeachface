---
template: page
icon:
  type: uil:layer-group
  color: Salmon
order: 20  
---

- Logseq cheatsheet
- Sourced from [My own Cheatsheet - Customization / Look what I built - Logseq]( https://discuss.logseq.com/t/my-own-cheatsheet/23795 )
- Page properties
	- To set properties for a page, you MUST use the first block
	- properties name must be without spaces. e.g. `Hebrew Name::` is bad, but `Hebrew-name::` is fine
	- `icon::` for setting a page icon
	- `alias::` is a way to call the same thing with different names.
	- `page-type::` to inherit icon e.g. [[locations]] and should be used a general type.
		- e.g. Mcdonalds is `page-type:: [[Locations]]` but it's `type:: [[Restaurant]]`
		- page-type is always pages (with [[]]) while type doesn't have (but still can).
	- `type::` is "like a subset" of `page-type::` it can also be set to a block. and it's "more detailed version of" page-type
	- `tags::` is a way to tag a block/page.
		- should I use `#` with tags? how does this work?
	- you can link property value with ``[[]]``, e.g. `birthday::[[10.06.1995]]`
- Use # for statuses and people
	- `#delayed` tasks
	- `#[[Or Gaist]]`
- TODO:
	- use `/TODO` to make a new task
	- you can add `/scheduled` or `/deadline`
	  :LOGBOOK:
	  CLOCK: [2023-11-17 Fri 20:57:34]--[2023-11-17 Fri 20:57:35] =>  00:00:01
	  CLOCK: [2023-11-17 Fri 20:57:35]
	  :END:
	- Add a progress bar with `{{renderer :todomaster}}` or `/todo master`
		- {{renderer :todomaster}}
- Kanban:
	- `/kanban`
	- [ReadMe](https://github.com/sethyuan/logseq-plugin-kanban-board/blob/master/README.en.md)
- namespaces
	- use `/` at the name of the file to use it as folder structure.
	  e.g. `[[Germany/Berlin]]`
- Syntax examples
	- [Style Guide](https://www.logseqtemplates.com/t/candide/Style%20Guide)
	- ### my_checklist_title
	  * [ ] point 1
	  * [X] point 2 
	  * [ ] point 3
- Icon selector
	- [NerdFonts](https://www.nerdfonts.com/cheat-sheet)
	- 🪟WinKey + .
- Plugins
  lastUpdate:: [[18.12.2023]]
	- Show weekday and week-number
	  id:: logseq-plugin-show-weekday-and-week-number
	  Version:: 1.44.0
	  Description:: Show weekday and week number beside journal titles. etc.. mini-calendar for daily page.
	  Author:: YU000jp
	  PluginID:: logseq-plugin-show-weekday-and-week-number
	- Kanban Board
	  version:: 1.17.10
	  description:: Draggable, editable Kanban view.
	  author:: sethyuan
	  pluginId:: logseq-kanban-board
	- Awesome UI
	  version:: 2.4.0
	  description:: Reworked, simplified, fixed and pumped-up Logseq layout.
	  author:: yoyurec
	  pluginId:: logseq-awesome-ui
	- Logseq Calendars
	  version:: 2.2.2
	  description:: Sync your logseq daily note with your google, icloud or outlook calendar
	  author:: Aryan Sawhney
	  pluginId:: logseq-calendars-plugin
		- [Documentation](https://github.com/sawhney17/logseq-calendars-plugin)
	- Logseq Find and Replace
	  version:: 1.1.1
	  description:: Find and Replace across your entire database
	  author:: Aryan Sawhney
	  pluginId:: logseq-find-and-replace
	- Todo list
	  version:: 1.20.0
	  description:: Show your all TODO items and easy to add new items on your today's journal page
	  author:: ahonn
	  pluginId:: logseq-todo-plugin
	- Journals calendar
	  version:: 0.10.10
	  description:: A simple journals calendar plugin for Logseq.
	  author:: xyhp915
	  pluginId:: logseq-journals-calendar
	- Markdown Table Editor
	  version:: 1.8.0
	  description:: Markdown Table Editor
	  author:: haydenull
	  pluginId:: logseq-markdown-table
	- Copy Code
	  version:: 1.2.0
	  description:: Copy code from code blocks to your clipboard
	  author:: vyleung
	  pluginId:: logseq-copy-code-plugin
	- Bullet Threading
	  version:: 1.1.4
	  description:: Add bullet threading to your active blocks in Logseq.
	  author:: pengx17
	  pluginId:: logseq-bullet-threading
	- Recurrence
	  version:: 1.0.7 
	  description:: This plugin allows you to quickly add recurring blocks based on your desired recurrence. It also allows you to delete inserted recurring blocks as well!
	  author:: hkgnp
	  pluginId:: logseq-recurrence-plugin
	- Ordered Lists
	  version:: 0.6.1
	  description:: Ordered lists, flat or nested, multiple formats ordered lists.
	  author:: sethyuan
	  pluginId:: logseq-ol
	- Awesome Links
	  version:: 1.15.16
	  description:: Favicons for external links, page icons for internal
	  author:: yoyurec
	  pluginId:: logseq-awesome-links
	- ToDo Master
	  version:: 1.10.3
	  description:: Render a progress bar to gether the overall progress of the current block or page.
	  author:: pengx17
	  pluginId:: logseq-todo-master
	- Tabs
	  version:: 1.19.3
	  description:: Open pages or blocks in tabs like working in the browser
	  author:: pengx17
	  pluginId:: logseq-tabs
	- Tags
	  version:: 0.1.2
	  description:: A plugin that lets you find and search all of your tags.
	  author:: Gidong Kwon
	  pluginId:: logseq-tags
	- Tabler picker
	  version:: 1.4.0
	  description:: Tabler icon picker plugin for Logseq
	  author:: yoyurec
	  pluginId:: logseq-tabler-picker
	- Habit Tracker
	  version:: 0.4.3
	  description:: Track habits on daily journal pages.
	  author:: c6p
	  pluginId:: logseq-habit-tracker
	- SmartBlocks
	  version:: 3.51
	  description:: A port of the roam SmartBlocks extension with a dash of Notion
	  author:: Aryan Sawhney
	  pluginId:: logseq-smartblocks
		- [Documentation](https://github.com/sawhney17/logseq-smartblocks)
		- [Youtube](https://www.youtube.com/watch?v=55s-K1uAUc0)
	- Awesome Content
	  version:: 1.2.1
	  description:: Enhanced content blocks (tasks, quotes, flashcards, headers, queries, diagrams, etc...)
	  author:: yoyurec
	  pluginId:: logseq-awesome-content
	- Flow Nord theme
	  version:: 0.10.7
	  description:: A minimalist theme that focuses on a clean and sleek interface with various color palette options.
	  author:: nmartin84 and henices
	  pluginId:: logseq-flow-nord-theme