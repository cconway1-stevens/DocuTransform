
# Format Requirements for `text.txt`

To ensure that your document is processed correctly by the conversion script to generate PDF, DOCX, and Markdown (MD) files, please follow the formatting guidelines outlined below.

## General Text Formatting

- **Plain Text:** Write plain text directly without any special formatting.
- **Headings:** For headings, use the Markdown style:
  - `#` for level 1 heading
  - `##` for level 2 heading
  - `###` for level 3 heading, and so on.
- **Bold:** To bold text, wrap words with double asterisks `**`, e.g., `**bold**`.
- **Italics:** To italicize text, wrap words with single asterisks `*`, e.g., `*italics*`.

## Lists

- **Unordered Lists:** Use dashes (`-`) followed by a space for bullet points.
- **Ordered Lists:** Use numbers followed by a dot and a space for enumeration, e.g., `1. `.

## LaTeX Equations

To include mathematical equations in your document, wrap your LaTeX code with dollar signs for inline equations or double dollar signs for block equations.

- **Inline Equations:** Wrap the equation with single dollar signs `$...$`, e.g., `$x_{i} + y_{i} \leq z_{i}$`.
- **Display Equations:** Wrap the equation with double dollar signs `$$...$$` for centered equations on their own line, e.g.,
  $$
  x_{LD} + x_{LKC} + x_{LM} + x_{LS} \leq 750
  $$

## Special Characters

If you need to use special characters within your text (like Markdown syntax characters), you can escape them using a backslash (`\`), e.g., `\*not italicized\*`.

## Example Text File

Here's an example of how your `text.txt` file might look:

```
# Sample Document Title

## Subtitle

Here is some plain text. Here is **bold text** and *italic text*.

### List Example

- First item
- Second item
  - Nested item
1. First numbered item
2. Second numbered item

## Equations

Here's an inline equation $x_{i} + y_{i} \leq z_{i}$.

Here's a display equation:

$$
x_{LD} + x_{LKC} + x_{LM} + x_{LS} \leq 750
$$
```

Please follow these guidelines to ensure your document converts correctly.
