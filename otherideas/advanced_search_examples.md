# Advanced Search Examples for Gmail, Google Drive & GitHub

## Gmail Search Examples

### Basic Operators
```
from:sender@example.com                    # Emails from specific sender
to:recipient@example.com                   # Emails to specific recipient
cc:copied@example.com                      # Emails where someone is CC'd
bcc:blindcopied@example.com               # Emails where someone is BCC'd
subject:"exact subject line"               # Exact subject line match
subject:keyword                           # Subject contains keyword
```

### Content Search
```
"exact phrase search"                     # Search for exact phrase
+required_word                           # Word must be present
-excluded_word                           # Exclude emails with this word
keyword1 OR keyword2                     # Either keyword present
keyword1 AND keyword2                    # Both keywords present
(keyword1 OR keyword2) AND keyword3      # Complex boolean logic
```

### Date and Time
```
after:2024/01/01                         # Emails after specific date
before:2024/12/31                        # Emails before specific date
older_than:30d                           # Older than 30 days
newer_than:7d                            # Newer than 7 days
older_than:1y                            # Older than 1 year
newer_than:2m                            # Newer than 2 months
```

### Status and Properties
```
is:unread                                # Unread emails
is:read                                  # Read emails
is:important                             # Important emails
is:starred                               # Starred emails
is:snoozed                               # Snoozed emails
is:muted                                 # Muted conversations
```

### Content Types and Attachments
```
has:attachment                           # Emails with attachments
has:youtube                              # Contains YouTube links
has:drive                                # Contains Google Drive links
has:document                             # Contains Google Docs
has:spreadsheet                          # Contains Google Sheets
has:presentation                         # Contains Google Slides
filename:pdf                             # PDF attachments
filename:report.xlsx                     # Specific filename
```

### Categories and Labels
```
category:primary                         # Primary inbox
category:social                          # Social category
category:promotions                      # Promotions category
category:updates                         # Updates category
category:forums                          # Forums category
label:important                          # Specific label
label:work                               # Custom label
```

### Size and Advanced
```
size:5M                                  # Emails larger than 5MB
larger:10M                               # Larger than 10MB
smaller:1M                               # Smaller than 1MB
list:mailinglist@example.com             # From mailing list
deliveredto:alias@example.com            # Delivered to specific alias
in:anywhere                              # Search everywhere including spam/trash
```

### Complex Gmail Examples
```
from:boss@company.com subject:urgent newer_than:3d
(from:client1@example.com OR from:client2@example.com) has:attachment
subject:(meeting OR call) after:2024/08/01 -is:muted
has:attachment filename:pdf larger:5M older_than:30d
```

## Google Drive Search Examples

### Basic File Properties
```
name = 'exact filename'                  # Exact filename match
name contains 'keyword'                  # Filename contains keyword
name contains 'budget' and name contains '2024'  # Multiple keywords
not name contains 'draft'                # Exclude files with 'draft'
```

### Content Search
```
fullText contains 'project alpha'        # Content contains phrase
fullText contains '"exact phrase"'       # Exact phrase in content
fullText contains 'meeting'              # Any mention of meeting
not fullText contains 'cancelled'        # Exclude specific content
```

### File Types
```
mimeType = 'application/vnd.google-apps.document'      # Google Docs only
mimeType = 'application/vnd.google-apps.spreadsheet'   # Google Sheets only
mimeType = 'application/vnd.google-apps.presentation'  # Google Slides only
mimeType = 'application/vnd.google-apps.folder'        # Folders only
mimeType = 'application/pdf'                           # PDF files only
mimeType contains 'image'                              # Any image files
```

### Date and Time
```
modifiedTime > '2024-08-01T00:00:00'     # Modified after date
modifiedTime < '2024-07-31T23:59:59'     # Modified before date
createdTime > '2024-01-01T00:00:00'      # Created after date
viewedByMeTime > '2024-07-01T00:00:00'   # Viewed by me after date
```

### Sharing and Permissions
```
'user@example.com' in owners             # Owned by specific user
'user@example.com' in writers            # User has write access
'user@example.com' in readers            # User has read access
sharedWithMe = true                      # Files shared with me
visibility = 'limited'                   # Private files only
starred = true                           # Starred files
```

### Folder and Location
```
'1ABC123XYZ' in parents                  # Files in specific folder (use folder ID)
parents in '1ABC123XYZ'                  # Alternative syntax
'1ABC123XYZ' in parents and mimeType != 'application/vnd.google-apps.folder'  # Files only, no subfolders
```

### Custom Properties
```
properties has { key='project' and value='alpha' }           # Custom property
appProperties has { key='status' and value='active' }        # App-specific property
```

### Complex Google Drive Examples
```
name contains 'report' and modifiedTime > '2024-07-01T00:00:00' and mimeType = 'application/vnd.google-apps.document'

fullText contains 'quarterly review' and 'john@company.com' in writers and starred = true

'1ABC123XYZ' in parents and mimeType = 'application/pdf' and modifiedTime > '2024-06-01T00:00:00'

sharedWithMe = true and fullText contains 'presentation' and not name contains 'old'
```

## GitHub Search Examples

### Repository Search
```
repo:username/repository-name            # Search within specific repo
org:organization-name                    # Search within organization
user:username                           # Search user's repositories
```

### Issue and PR Search
```
is:issue                                # Issues only
is:pr                                   # Pull requests only
is:open                                 # Open issues/PRs
is:closed                               # Closed issues/PRs
is:merged                               # Merged PRs
is:draft                                # Draft PRs
```

### Status and State
```
state:open                              # Open items
state:closed                            # Closed items
is:public                               # Public repositories
is:private                              # Private repositories
archived:true                           # Archived repositories
archived:false                          # Non-archived repositories
```

### People and Assignments
```
author:username                         # Created by user
assignee:username                       # Assigned to user
mentions:username                       # Mentions specific user
commenter:username                      # User commented
involves:username                       # User involved in any way
```

### Labels and Milestones
```
label:bug                               # Has bug label
label:"good first issue"                # Label with spaces
no:label                                # No labels
milestone:"v2.0"                        # Specific milestone
no:milestone                            # No milestone
```

### Date Ranges
```
created:2024-01-01..2024-12-31          # Created in date range
updated:>2024-07-01                     # Updated after date
closed:2024-08-01..2024-08-31           # Closed in August 2024
merged:>=2024-01-01                     # Merged since start of year
```

### Content and Code Search
```
"function getName"                      # Exact code phrase
language:python                         # Python files only
extension:js                            # JavaScript files
filename:package.json                   # Specific filename
path:src/components                     # Files in specific path
```

### Complex GitHub Examples
```
repo:facebook/react is:issue label:bug state:open created:>2024-01-01

org:microsoft language:typescript is:pr is:merged author:username

is:issue assignee:@me label:"good first issue" state:open

repo:username/project path:src extension:py "def test_" created:>2024-07-01
```

## Search Tips and Best Practices

### Gmail Tips
- Use parentheses for complex boolean logic
- Combine multiple operators for precise results
- Use quotes for exact phrase matching
- Remember that Gmail search is case-insensitive

### Google Drive Tips
- Always use single quotes around values
- Use folder IDs (not names) for parent searches
- Combine mimeType filters with content searches
- Use RFC 3339 format for timestamps

### GitHub Tips
- Use qualifiers to narrow down search scope
- Combine user/org with repo for targeted searches
- Use date ranges for time-based analysis
- Remember GitHub has rate limits on API searches

### General Best Practices
1. Start with broad searches and narrow down
2. Test searches incrementally
3. Use specific operators rather than generic keywords
4. Combine multiple criteria for precision
5. Save complex searches for reuse