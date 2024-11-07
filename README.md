# Simple HTML Page Parser

This is a simple parser for HTML pages without JavaScript content. Designed to fetch structured data from pages with static HTML content.

## Version 0.3

### Features:
1. **`get_urls_for_pages`**: Automatically generates a list of URLs for multiple pages based on a pattern.
2. **`analyze`**: Analyzes a given URL and identifies possible HTML tags and patterns for parsing.
3. **`return_special_chars`**: Converts HTML special characters to readable characters in parsed text.
4. **`parse`**: Parses the HTML content based on given patterns and returns structured data.

---

### Function Descriptions

#### 1. `get_urls_for_pages(url:str, start_page:int=1, pages:int=1, stop:str='', allow_repeat:bool=False) -> list | tuple`
Makes requests to an URL with multiple pages, stopping after reaching a specified limit or stop-sequence.

- **Parameters:**
  - `url (str)`: The base URL with an iterator placeholder `{page}`. If `{page}` is absent, default behavior is to append `/1`, `/2`, etc. to the URL.
  - `start_page (int, default=1)`: The starting page for iteration.
  - `pages (int, default=1)`: The number of pages to generate. Set `0` to fetch pages until `stop` or `allow_repeat=False` is met.
  - `stop (str, default='')`: A sequence that stops the iteration if matched.
  - `allow_repeat (bool, default=False)`: Whether to allow repeat pages.

- **Returns**:
  - `list`: A list of URLs or a tuple `(None, exception_message)` if an error occurs.

**Note**: Be cautious; if `allow_repeat=True` and no stop condition is set, this function could run indefinitely.

**Examples**:
```python
def get_urls_for_pages(url: str, start_page: int = 1, pages: int = 1, stop: str = '', allow_repeat: bool = False) -> list | tuple:
    # Implement the function here
    pass

get_urls_for_pages("https://example.com/{page}", 1, 3)   # returns ["https://example.com/1", "https://example.com/2", "https://example.com/3"]
get_urls_for_pages("https://example.com/{page}", pages=0, stop="not found")  # stops when "not found" appears
```
---

#### 2. `analyze(*urls: str | list) -> dict`
Analyzes the HTML structure at the given URL(s) and returns all possible tags and attributes.

- **Parameters:**
  - `urls (tuple of str | list)`: URL(s) to analyze for parsing patterns.

- **Returns**:
  - `dict`: A dictionary of tags with their associated attributes, useful for building parsing patterns.

```python
# Example usage:
result = analyze("https://example.com")
# Expected output (example structure):
# {
#     "tags": {
#         "tag1": ["attribute1", "attribute2", ...],
#         "tag2": ["attribute1", "attribute2", ...],
#         ...
#     }
# }
```
---

#### 3. `return_special_chars(text: str) -> str`
Replaces HTML special characters in a text string with their readable equivalents (e.g., `&amp;` becomes `&`).

- **Parameters:**
  - `text (str)`: Text containing HTML special characters.

- **Returns**:
  - `str`: Text with HTML entities replaced by readable characters.

**Example**:
```python
def return_special_chars(text: str) -> str:
    # Implement the function here
    pass

# Example usage:
text = "Tom &#38; Jerry are &#60;best friends&#62;."
result = return_special_chars(text)
# Output: "Tom & Jerry are <best friends>."
print(result)
```
---

#### 4. `parse(patterns_to_parse: str | dict, str_to_parse: str, alias: list[str] = [], regexp: bool = True, group_by: str = 'pattern') -> dict`
Parses a string or URL based on given patterns and returns a structured dictionary of matches.

- **Parameters:**
  - `patterns_to_parse (str | dict)`: The pattern or schema to search within the target string. Can be a single pattern (string) or a dictionary of multiple patterns.
  - `str_to_parse (str)`: The HTML content or URL to be parsed.
  - `alias (list of str)`: Optional aliases to label each pattern for easier readability in the output.
  - `regexp (bool, default=True)`: If `True`, treats each pattern as a regular expression; if `False`, uses plain string matching.
  - `group_by (str, default='pattern')`: Defines how the results are grouped in the output dictionary.
    - `'pattern'`: Groups results by each pattern.
    - `'iteration'`: Groups results by each iteration.

- **Returns**:
  - `dict`: A dictionary containing parsed content that matches each pattern. If `alias` is provided, keys in the dictionary will use aliases instead of patterns.

**Structure of the result**:
```python
{
    "1 (or alias1)": ["match1", "match2", ...],
    "2 (or alias2)": ["match1", "match2", ...],
    ...
}
```
**Example**:
```python
patterns = [
    r"<title>(.*?)</title>",
    r"<h1>(.*?)</h1>"
]
html_content = "<html><title>Example Page</title><body><h1>Welcome!</h1></body></html>"
result = parse(patterns, html_content, alias=["Title", "Header"])
output: {
#     "Title": ["Example Page"],
#     "Header": ["Welcome!"]
# }
```
---

## Additional Notes

This HTML parser is designed for educational purposes and works best with static HTML pages. It does not support JavaScript-rendered content and is intended for simpler parsing tasks where minimal dependencies are desired. For complex HTML parsing or dynamic content extraction, consider using libraries like **BeautifulSoup** or **Selenium**.

### Limitations
- **Static Content**: This parser does not process JavaScript; it only works with content available in the static HTML.
- **Regular Expressions**: The reliance on regular expressions means that complex, deeply nested HTML structures may not be parsed as reliably as with a dedicated HTML parsing library.

### Future Improvements
1. **JavaScript Support**: Integrate a solution for handling JavaScript-rendered pages, possibly by incorporating Selenium or another tool.
2. **Error Handling**: Implement more robust error handling and logging for network errors or unexpected HTML structures.
3. **Regex Optimization**: Optimize the regular expressions to improve parsing accuracy for various HTML tag structures.

### Contact and Contributions
Feel free to fork this project, suggest improvements, or report issues. Contributions are welcome, especially from those who want to improve the functionality or expand its capabilities.

---

