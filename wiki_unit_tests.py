import pytest
from wiki_classes import WikiArticle

MOCK_HTML = """
<html>
    <body>
        <div class="mw-parser-output">
            <p>A Creeper is a common hostile mob that will silently approach players and explode.</p>
            <p>This is a second paragraph about history that should be ignored by the summary.</p>
            
            <a href="/w/Gunpowder">Gunpowder</a>
            <a href="https://minecraft.net">Official Site</a>
            <a href="/w/Charged_Creeper">Charged Creeper</a>
            
            <table>
                <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                </tr>
                <tr>
                    <td>Gunpowder</td>
                    <td>0-2</td>
                </tr>
            </table>
        </div>
    </body>
</html>
"""

def test_get_summary_extracts_first_paragraph():
    """
    Verifies that get_summary correctly extracts text from the first <p> tag.
    """
    article = WikiArticle("Creeper", MOCK_HTML)
    summary = article.get_summary()
    assert summary == "A Creeper is a common hostile mob that will silently approach players and explode."

def test_get_summary_returns_message_on_missing_content():
    """
    Verifies that the method returns a safe error message instead of crashing
    when the HTML structure is invalid.
    """
    bad_html = "<html><body><h1>Steve</h1></body></html>"
    article = WikiArticle("Empty Page", bad_html)
    
    assert article.get_summary() == "Content not found"

def test_get_links_filters_internal_wiki_links():
    """
    Verifies that get_links only returns links starting with '/w/' 
    and correctly formats them (removing prefix and underscores).
    """
    article = WikiArticle("Links Test", MOCK_HTML)
    links = article.get_links()
    
    # Should contain "Gunpowder" and "Charged Creeper"
    assert "Gunpowder" in links
    assert "Charged Creeper" in links
    # Should NOT contain external links
    assert "minecraft.net" not in links
    # Should have exactly 2 valid links
    assert len(links) == 2

@pytest.mark.parametrize("html_snippet, expected_word, expected_count", [
    ("Block block BLOCK", "block", 3),      # Case insensitivity check
    ("Crafting, crafting!", "crafting", 2), # Punctuation removal check
    ("Redstone 15", "15", 0),               # Digit ignoring check (isalpha)
    ("End-City", "city", 1),                # Hyphen handling check
])
def test_word_count_logic(html_snippet, expected_word, expected_count):
    """
    Tests various word counting scenarios using pytest parametrization.
    """
    full_html = f'<div class="mw-parser-output">{html_snippet}</div>'
    article = WikiArticle("Word Count Test", full_html)
    
    counts = article.get_word_count()
    assert counts[expected_word] == expected_count

def test_get_table_raises_error_when_index_out_of_range():
    """
    Verifies that asking for a non-existent table raises an IndexError.
    """
    article = WikiArticle("Table Test", MOCK_HTML)
    
    # MOCK_HTML has only 1 table, so asking for #2 should fail
    with pytest.raises(IndexError):
        article.get_table(number=2, row_header=False)

def test_get_word_count_raises_error_on_empty_html():
    """
    Verifies that get_word_count raises ValueError when content is missing.
    """
    bad_html = "<html><body>No content here</body></html>"
    article = WikiArticle("Bad Article", bad_html)
    
    with pytest.raises(ValueError, match="Article content not found"):
        article.get_word_count()
