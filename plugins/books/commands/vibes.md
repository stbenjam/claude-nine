---
description: Find similar books in your library based on genre, author, or themes
---

You are helping the user find books in their TBR that have similar vibes/themes to a book they specify.

## Analysis Process

Use the Calibre skill to find books with similar vibes:

### 1. Get the Reference Book

First, query for the book the user mentions (or ask them to specify one):
```bash
--fields='title,authors,series,tags,comments,*goodreads,*pages'
--search='title:"[book title]"'
```

Get all available information:
- Author(s)
- Series (if part of one)
- Tags (if any)
- Comments/description
- Goodreads rating
- Page count

### 2. Identify Similar Books

Query TBR for books with similar characteristics:

**Same Author**
```bash
--search='authors:"[author]" and #read:No and #archived:No'
```

**Same Series**
```bash
--search='series:"[series]" and #read:No and #archived:No'
```

**Similar Tags/Genres**
If the reference book has tags, search for books with those tags:
```bash
--search='tags:"[tag]" and #read:No and #archived:No'
```

**Similar Page Count** (±100 pages)
```bash
--search='#pages:">[low]" and #pages:"<[high]" and #read:No and #archived:No'
```

**Similar Rating Range**
```bash
--search='#goodreads:">[rating-0.5]" and #goodreads:"<[rating+0.5]" and #read:No and #archived:No'
```

### 3. Use Available Information

Even without formal tags, extract information from:
- Book titles (often contain genre hints: "The [Fantasy] of...")
- Series names (often thematic)
- Author names (can search for co-authors, related authors)
- Comments field (may contain descriptions with genre/theme keywords)

### 4. Search for Community Recommendations

Use WebSearch to find what other readers recommend as similar books:

**Search for Reddit recommendations:**
```
"books like [book title]" site:reddit.com
```

**Search for Goodreads lists:**
```
"similar to [book title]" site:goodreads.com
```

**General recommendation searches:**
```
"if you liked [book title]" recommendations
"books similar to [book title]"
"read alikes [book title]"
```

Extract book titles and authors from search results, then:
- Check if any are in the user's TBR (prioritize these)
- Note popular recommendations even if not in TBR (user might want to add them)

### 5. Similarity Scoring

For each book found, explain WHY it's similar:
- Same author
- Same/related series
- Shared tags/genres
- Similar length (good for pacing match)
- Similar rating (quality match)
- Similar themes (if detectable from metadata)
- **Recommended by readers** (found in search results)

## Output Format

```
# 📖 BOOKS WITH SIMILAR VIBES

Finding books similar to: **[Reference Book]** by [Author]

## About the Reference Book
- **Series**: [Series Name] or "Standalone"
- **Length**: XXX pages
- **Rating**: X.X / 5
- **Key Themes**: [Based on tags, series, title, or "Limited metadata available"]

## Similar Books in Your TBR

### By Same Author
[If any found:]
- **[Title]** ([XXX pages], rated X.X/5, added [time ago])
  Why similar: Same author, similar [length/rating/style]

### In Related Series
[If any found:]
- **[Title]** by [Author]
  Series: [Series Name]
  Why similar: [Connection to original series]

### Similar Themes/Genres
[If any found based on tags or metadata:]
- **[Title]** by [Author] ([XXX pages], rated X.X/5)
  Why similar: [Shared tags/themes/genre indicators]

### Similar Length & Quality
[Books with similar page count and rating:]
- **[Title]** by [Author] ([XXX pages], rated X.X/5)
  Why similar: Similar reading commitment and quality

### Recommended by the Community
[Books found via web search that are in your TBR:]
- **[Title]** by [Author] ([XXX pages], rated X.X/5)
  ✓ In your TBR
  Why similar: Frequently mentioned on [Reddit/Goodreads/etc.] as similar to [reference book]

## 🎯 Top Recommendations from Your TBR

Based on the similarity analysis, here are the strongest matches:

1. **[Title]** by [Author]
   Best match because: [Specific reasons]

2. **[Title]** by [Author]
   Good match because: [Specific reasons]

3. **[Title]** by [Author]
   Worth considering: [Specific reasons]

## 📚 Popular Recommendations Not in Your Library

Based on web search, these books are frequently recommended as similar but aren't in your TBR yet:

1. **[Title]** by [Author]
   Why recommended: [Based on search results - Reddit threads, Goodreads lists, etc.]
   Rating: X.X / 5 on Goodreads (if found)

2. **[Title]** by [Author]
   Why recommended: [Reason from search results]

3. **[Title]** by [Author]
   Why recommended: [Reason from search results]

---
💡 Tips:
- Want to add any of these to your library? Use Calibre to import them
- If no similar books were found in your TBR, try /books:random for a surprise pick
- Use /books:next for personalized recommendations based on reading patterns
```

## Handling Limited Metadata

If the reference book or TBR books have limited metadata:
- Focus on author and series connections (most reliable)
- Use page count for "similar reading experience"
- Use ratings for quality matching
- Look for patterns in titles
- Be transparent about limitations: "Based on available metadata..."

## User Interaction

If the user just says "/books:vibes" without specifying a book:
1. Ask them which book they want to find similar books to
2. Suggest they could use a recent read they enjoyed
3. Or ask them to name a book they loved

If they specify a book not in the library:
1. Ask if they want to find books similar to that book's:
   - Author
   - Genre/themes (ask them to describe)
   - Length/style

## Query Strategy

1. **Start broad**: Query all potential matches from library
2. **Search the web**: Use WebSearch to find community recommendations (Reddit, Goodreads, book blogs)
3. **Cross-reference**: Match web recommendations against your TBR
4. **Present both**: Show matches in TBR first, then popular recommendations not in library
5. **Score by similarity**: Books matching multiple criteria rank higher
6. **Prioritize quality**: Weight highly-rated books (>4.0) higher
7. **Prioritize community picks**: Books mentioned by other readers are strong matches
8. **Limit results**: Show top 5-10 from each category (in TBR and not in TBR)
9. **Explain reasoning**: Always say WHY books are similar
10. **Exclude archived**: Always add `#archived:No` unless user specifies otherwise
11. **Include context**: Note which platform recommended the book (Reddit, Goodreads, etc.)

## Example Scenarios

**User**: "Books like Mistborn"
- Library query: Author (Sanderson), Series (Mistborn), Tags (fantasy, magic)
- Web search: "books like Mistborn" Reddit/Goodreads
- Find in TBR: Other Sanderson books, high fantasy, magic systems
- Suggest from web: Stormlight Archive, Wheel of Time, etc.

**User**: "Something like this cozy mystery I just finished"
- Library query: By title/author, look for tags like "mystery", "cozy"
- Web search: "[title] read alikes" "similar cozy mysteries"
- Find in TBR: Similar page count, similar authors, mystery tags
- Suggest from web: Popular cozy mystery series recommendations

**User**: "Books with similar vibes to Name of the Wind"
- Library query: Author (Rothfuss), Tags (fantasy, coming-of-age)
- Web search: "books similar to Name of the Wind" site:reddit.com
- Find in TBR: Epic fantasy, similar length, highly-rated
- Suggest from web: Popular epic fantasy series often recommended together
