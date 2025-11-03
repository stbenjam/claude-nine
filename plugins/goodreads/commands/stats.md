---
description: Show reading statistics (books per year/month, pages read, average rating, genre breakdown)
---

You are helping the user analyze their reading statistics from their Goodreads library.

## Analysis to Perform

Use the `analyze-goodreads-export` skill to gather and analyze the following statistics:

### 1. Reading Velocity

Query books read in different time periods:
- Books read this year (use `date_read.year == current_year`)
- Books read last 30 days
- Books read last 90 days
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
- Average rating given (your `my_rating` field)
- Average Goodreads rating of books read (`average_rating` field)
- Most common rating you give
- Distribution of ratings (how many 5-star, 4-star, etc.)

### 4. Author Statistics

Query all read books:
- Most read authors (count by author name)
- Total unique authors read

### 5. Series Statistics

Query all read books with series information:
- Books read that are part of series vs standalone
- Most read series
- Number of complete series finished

### 6. To-Be-Read Statistics

Query TBR list (where `is_tbr` is True):
- Total books in TBR
- Total pages in TBR
- Average Goodreads rating of TBR
- Oldest book in TBR (by date_added)
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
- Your reading pace has [increased/decreased] compared to last year
- You tend to rate books higher/lower than Goodreads average
- You're reading more/fewer series books than standalone
```

## Implementation

Write a Python script using goodreads_lib to:
1. Query all read books
2. Calculate statistics for each category
3. Format and display results with proper formatting

Use the Bash tool to run your Python script.

## Important Notes

- Use `date_read` field to determine if/when book was read
- Calculate percentages and averages from the data
- Present large numbers with thousand separators for readability
- Compare current year to all-time averages where interesting
- Handle missing data gracefully (some books may not have all fields)
- Round floating point values to 2 decimal places for readability
