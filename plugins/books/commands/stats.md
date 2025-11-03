---
description: Show reading statistics (books per year/month, pages read, average rating, genre breakdown)
---

You are helping the user analyze their reading statistics from their Calibre library.

## Analysis to Perform

Use the Calibre skill to gather and analyze the following statistics:

### 1. Reading Velocity

Query books read in different time periods:
- Books read this year (use `#dateread:">=YYYY-01-01"` where YYYY is current year)
- Books read last 30 days (use `#dateread:">=30daysago"`)
- Books read last 90 days (use `#dateread:">=90daysago"`)
- Break down by month for current year

Calculate:
- Books per month average (current year)
- Pages per month average
- Current reading pace vs yearly average

### 2. Page Statistics

Query all read books with page counts:
- Total pages read this year
- Total pages read all time
- Average pages per book
- Longest book read
- Shortest book read

### 3. Rating Analysis

Query all read books with ratings:
- Average rating given (your `rating` field)
- Average Goodreads rating of books read (`*goodreads` field)
- Most common rating you give
- Distribution of ratings (how many 5-star, 4-star, etc.)

### 4. Author Statistics

Query all read books:
- Most read authors (count by author name)
- Total unique authors read

### 5. Series Statistics

Query all read books with series information:
- Number of complete series finished
- Books read that are part of series vs standalone
- Most read series

### 6. To-Be-Read Statistics

Query TBR list (`#read:No and #archived:No`):
- Total books in TBR
- Total pages in TBR
- Average Goodreads rating of TBR
- Oldest book in TBR (by timestamp)
- Books added to TBR in last 30 days

## Output Format

Present statistics in a clean, organized report:

```
# READING STATISTICS

## 📊 Reading Velocity
- **This Year**: X books (Y pages)
- **Last 30 Days**: X books (Y pages)
- **Average Pace**: X books/month, Y pages/month

### Monthly Breakdown (YYYY)
Jan: X books | Feb: X books | Mar: X books | etc.

## 📖 Page Statistics
- **Total Pages Read (All Time)**: X,XXX pages
- **Total Pages Read (This Year)**: X,XXX pages
- **Average Book Length**: XXX pages
- **Longest Book**: [Title] by [Author] (XXX pages)
- **Shortest Book**: [Title] by [Author] (XXX pages)

## ⭐ Rating Analysis
- **Your Average Rating**: X.X / 5
- **Goodreads Average of Books Read**: X.X / 5
- **Most Common Rating**: X stars

### Rating Distribution
★★★★★: XX books (XX%)
★★★★☆: XX books (XX%)
★★★☆☆: XX books (XX%)
★★☆☆☆: XX books (XX%)
★☆☆☆☆: XX books (XX%)

## ✍️ Author Statistics
- **Total Authors Read**: XX unique authors
- **Most Read Authors**:
  1. [Author Name]: X books
  2. [Author Name]: X books
  3. [Author Name]: X books

## 📚 Series Statistics
- **Books in Series**: XX books (XX% of total)
- **Standalone Books**: XX books (XX% of total)
- **Most Read Series**:
  1. [Series Name]: X books
  2. [Series Name]: X books

## 📋 To-Be-Read Statistics
- **Total TBR Books**: XXX books (X,XXX pages)
- **Average TBR Rating**: X.X / 5
- **Added Recently**: XX books in last 30 days
- **Oldest Unread**: [Title] (added X years/months ago)

## 🎯 Reading Insights
[Provide 2-3 interesting insights, such as:]
- You're on track to read XX books this year
- Your reading pace has [increased/decreased] by XX% compared to last year
- You tend to rate books higher/lower than Goodreads average
- You're reading more/fewer series books than standalone
```

## Query Tips

- Use `#dateread` field with date ranges for time-based queries
- Calculate percentages and averages from the data
- Present large numbers with thousand separators for readability
- Compare current year to all-time averages where interesting
- Exclude archived books from all queries
- Handle missing data gracefully (some books may not have all custom fields set)

## Implementation Notes

**Bash/Python Pitfalls:**
- Multi-line bash for loops are tricky - use Python with heredoc instead for complex iteration
- When looping through months to count books, use Python's subprocess module rather than bash for loops
- When processing JSON data from calibredb, be careful with missing fields - always use `.get()` with defaults
- Keep Python data processing scripts simple - avoid complex inline data structures that can have KeyError issues
- Better to do multiple simple queries than one complex Python script with hard-coded data
