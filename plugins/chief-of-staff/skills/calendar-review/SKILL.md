---
name: calendar-review
description: Audits where someone's time goes with a time-audit script, compares it with their priorities, and proposes meetings to drop, shorten or batch and focus blocks to protect, changing only approved private blocks. Use it when someone asks where their week went, says their calendar is too full, or wants more focus time.
license: MIT
compatibility: Uses the calendar connector and runs a Python 3 script on the exported events.
---

# Calendar review

Calendars fill up by default and empty only on purpose. Show the person where their hours went compared with what they said matters, then make it easy to take time back.

## Steps

1. **Export:** fetch the period's events from the calendar connector (default: the last two weeks plus the next one). Save them as JSON with `title`, `start`, `end`, an `attendees` count, and an optional `category` when you can tell it (`1:1`, `external`, `recruiting`, `focus`, `admin`).
2. **Audit:** run `python3 scripts/time_audit.py events.json --workday <from policies, e.g. 09:00-18:00> --deep 90`. Use its numbers; never add up hours in your head.
3. **Compare with priorities:** how many hours went to each priority in `profile/priorities.md`, against the time it deserves. The gap is the finding.
4. **Propose,** ranked by hours won:
   - **Drop:** recurring meetings with no decisions or no clear owner, or where the person isn't needed. Suggest sending notes or delegating instead.
   - **Shorten:** 60 minutes to 25 or 45, a weekly to every two weeks.
   - **Batch:** cluster 1:1s and external calls on fixed days, to protect whole days.
   - **Protect:** recurring focus blocks in the largest free windows, tied to this week's one thing.
5. **Apply only what's approved.** Private focus blocks with no attendees may be created once the person agrees. Changes to meetings with other people become drafted messages or a list for the person to do themselves. Never accept, decline, move or delete those yourself.

## Output

- **The numbers:** meeting hours per day, back-to-back runs, the remaining deep-work blocks, and hours per category.
- **The gap:** time spent against the priorities, in one paragraph.
- **The proposals:** a table with the change, the hours won per week, and who acts on it.
- **The protected blocks** created, if any were approved.
