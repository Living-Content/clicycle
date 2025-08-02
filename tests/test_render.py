"""Unit tests for clicycle.render module."""

from unittest.mock import MagicMock

from clicycle.render import (
    Block,
    Code,
    Confirm,
    Header,
    List,
    ProgressBar,
    Prompt,
    RenderStream,
    Section,
    Spinner,
    Summary,
    Table,
    Text,
)
from clicycle.theme import ComponentIndentation, Theme


class TestComponent:
    """Test the base Component class."""

    def test_spacing_before_no_previous(self):
        """Test spacing calculation with no previous component."""
        theme = Theme()
        comp = Text(theme, "test", "info")
        assert comp.spacing_before(None) == 0

    def test_spacing_before_with_rules(self):
        """Test spacing calculation with defined rules."""
        theme = Theme()
        theme.spacing.info = {"error": 2}

        prev_comp = Text(theme, "error", "error")
        comp = Text(theme, "info", "info")

        assert comp.spacing_before(prev_comp) == 2

    def test_spacing_before_default(self):
        """Test default spacing when no rule defined."""
        theme = Theme()
        prev_comp = Text(theme, "test", "custom")
        comp = Text(theme, "info", "info")

        assert comp.spacing_before(prev_comp) == 1


class TestHeader:
    """Test the Header component."""

    def test_init(self):
        """Test Header initialization."""
        theme = Theme()
        header = Header(theme, "Title", "Subtitle", "App")

        assert header.title == "Title"
        assert header.subtitle == "Subtitle"
        assert header.app_name == "App"
        assert header.component_type == "header"

    def test_render_with_app_name(self):
        """Test Header rendering with app name."""
        theme = Theme()
        console = MagicMock()
        header = Header(theme, "Title", "Subtitle", "App")

        header.render(console)

        calls = console.print.call_args_list
        assert len(calls) >= 1  # At least title
        # Check that app name and title appear in the output
        all_output = str(calls)
        assert "TITLE" in all_output  # Transformed to upper
        if len(calls) > 1:
            assert "Subtitle" in all_output

    def test_render_without_app_name(self):
        """Test Header rendering without app name."""
        theme = Theme()
        console = MagicMock()
        header = Header(theme, "Title", "Subtitle")

        header.render(console)

        calls = console.print.call_args_list
        assert len(calls) >= 1
        all_output = str(calls)
        assert "TITLE" in all_output  # Transformed to upper

    def test_render_no_subtitle(self):
        """Test Header rendering without subtitle."""
        theme = Theme()
        console = MagicMock()
        header = Header(theme, "Title")

        header.render(console)

        assert console.print.call_count == 1


class TestSection:
    """Test the Section component."""

    def test_init(self):
        """Test Section initialization."""
        theme = Theme()
        section = Section(theme, "Section Title")

        assert section.title == "Section Title"
        assert section.component_type == "section"

    def test_render(self):
        """Test Section rendering."""
        theme = Theme()
        console = MagicMock()
        section = Section(theme, "Test Section")

        section.render(console)

        console.rule.assert_called_once()
        args = console.rule.call_args
        assert "TEST SECTION" in args[0][0]  # Transformed to upper


class TestText:
    """Test the Text component."""

    def test_init(self):
        """Test Text initialization."""
        theme = Theme()
        text = Text(theme, "Message", "info")

        assert text.text == "Message"
        assert text.text_type == "info"
        assert text.component_type == "info"

    def test_render_info(self):
        """Test Text rendering for info type."""
        theme = Theme()
        console = MagicMock()
        text = Text(theme, "Info message", "info")

        text.render(console)

        console.print.assert_called_once()
        args = console.print.call_args
        assert "Info message" in args[0][0]
        assert theme.icons.info in args[0][0]

    def test_render_list(self):
        """Test Text rendering for list type."""
        theme = Theme()
        console = MagicMock()
        text = Text(theme, "List item", "list")

        text.render(console)

        console.print.assert_called_once()
        args = console.print.call_args
        assert "List item" in args[0][0]
        assert theme.icons.bullet in args[0][0]

    def test_render_with_indentation(self):
        """Test Text rendering with indentation."""
        theme = Theme()
        theme.indentation = ComponentIndentation(info=4)
        console = MagicMock()
        text = Text(theme, "Indented", "info")

        text.render(console)

        args = console.print.call_args
        assert "    " in args[0][0]  # 4 spaces
        assert "Indented" in args[0][0]


class TestTable:
    """Test the Table component."""

    def test_init(self):
        """Test Table initialization."""
        theme = Theme()
        data = [{"col1": "val1"}]
        table = Table(theme, data, "Title")

        assert table.data == data
        assert table.title == "Title"
        assert table.component_type == "table"

    def test_render_empty_data(self):
        """Test Table rendering with empty data."""
        theme = Theme()
        console = MagicMock()
        table = Table(theme, [], "Title")

        table.render(console)

        console.print.assert_called_once()
        args = console.print.call_args
        assert "No data to display" in args[0][0]

    def test_render_with_data(self):
        """Test Table rendering with data."""
        theme = Theme()
        console = MagicMock()
        data = [
            {"Name": "Test", "Value": 123},
            {"Name": "Test2", "Value": 456}
        ]
        table = Table(theme, data, "Test Table")

        table.render(console)

        console.print.assert_called_once()

    def test_create_base_table(self):
        """Test base table creation."""
        theme = Theme()
        data = [{"col": "val"}]
        table = Table(theme, data)

        rich_table = table._create_base_table()

        assert rich_table.box == theme.layout.table_box
        assert rich_table.border_style == theme.layout.table_border_style

    def test_add_columns_special_headers(self):
        """Test column addition with special header names."""
        theme = Theme()
        data = [{
            "ID": 1,
            "Status": "OK",
            "Name": "Test",
            "Message": "Msg",
            "Check": "Health",
            "Frontend URL": "http://example.com",
            "Environment": "prod",
            "Cluster": "main"
        }]
        table = Table(theme, data)

        rich_table = table._create_base_table()
        headers = list(data[0].keys())
        table._add_columns(rich_table, headers)

        # Should have 8 columns
        assert len(rich_table.columns) == 8

    def test_add_rows(self):
        """Test row addition."""
        theme = Theme()
        data = [
            {"col1": "val1", "col2": 123},
            {"col1": "val2", "col2": 456}
        ]
        table = Table(theme, data)

        rich_table = table._create_base_table()
        headers = list(data[0].keys())
        table._add_columns(rich_table, headers)
        table._add_rows(rich_table)

        # Check rows were added
        assert len(rich_table.rows) == 2


class TestCode:
    """Test the Code component."""

    def test_init(self):
        """Test Code initialization."""
        theme = Theme()
        code = Code(theme, "print('hello')", "python", "Example", True)

        assert code.code == "print('hello')"
        assert code.language == "python"
        assert code.title == "Example"
        assert code.line_numbers is True
        assert code.component_type == "code"

    def test_render_with_title(self):
        """Test Code rendering with title."""
        theme = Theme()
        console = MagicMock()
        code = Code(theme, "code", "python", "Title")

        code.render(console)

        # Should print title and code
        assert console.print.call_count == 2

    def test_render_without_title(self):
        """Test Code rendering without title."""
        theme = Theme()
        console = MagicMock()
        code = Code(theme, "code", "python")

        code.render(console)

        # Should only print code
        assert console.print.call_count == 1

    def test_render_without_line_numbers(self):
        """Test Code rendering without line numbers."""
        theme = Theme()
        console = MagicMock()
        code = Code(theme, "line1\nline2\nline3", "python", line_numbers=False)

        code.render(console)

        # Check that padding is calculated for alignment
        assert console.print.call_count == 1


class TestSummary:
    """Test the Summary component."""

    def test_init(self):
        """Test Summary initialization."""
        theme = Theme()
        data = [{"label": "Name", "value": "Test"}]
        summary = Summary(theme, data)

        assert summary.data == data
        assert summary.component_type == "summary"

    def test_render(self):
        """Test Summary rendering."""
        theme = Theme()
        console = MagicMock()
        data = [
            {"label": "Name", "value": "Test"},
            {"label": "Count", "value": 42}
        ]
        summary = Summary(theme, data)

        summary.render(console)

        assert console.print.call_count == 2
        calls = console.print.call_args_list
        assert "Name" in str(calls[0])
        assert "Test" in str(calls[0])
        assert "Count" in str(calls[1])
        assert "42" in str(calls[1])


class TestBlock:
    """Test the Block component."""

    def test_init(self):
        """Test Block initialization."""
        theme = Theme()
        components = [Text(theme, "text", "info")]
        block = Block(theme, components)

        assert block.components == components
        assert block.component_type == "block"

    def test_render_without_nested_blocks(self):
        """Test Block rendering without nested blocks."""
        theme = Theme()
        console = MagicMock()
        text1 = MagicMock()
        text2 = MagicMock()
        block = Block(theme, [text1, text2])

        block.render(console)

        text1.render.assert_called_once_with(console)
        text2.render.assert_called_once_with(console)

    def test_render_with_nested_blocks(self):
        """Test Block rendering with nested blocks."""
        theme = Theme()
        console = MagicMock()
        text = MagicMock()
        text.spacing_before = MagicMock(return_value=0)
        nested_block = Block(theme, [])
        block = Block(theme, [text, nested_block])

        block.render(console)

        # Should create temporary stream for nested blocks
        text.render.assert_called()


class TestSpinner:
    """Test the Spinner component."""

    def test_init(self):
        """Test Spinner initialization."""
        theme = Theme()
        spinner = Spinner(theme, "Loading...")

        assert spinner.message == "Loading..."
        assert spinner.component_type == "spinner"

    def test_render(self):
        """Test Spinner rendering."""
        theme = Theme()
        console = MagicMock()
        spinner = Spinner(theme, "Processing")

        spinner.render(console)

        console.print.assert_called_once()
        args = console.print.call_args
        assert "Processing" in args[0][0]
        assert theme.icons.running in args[0][0]


class TestProgressBar:
    """Test the ProgressBar component."""

    def test_init(self):
        """Test ProgressBar initialization."""
        theme = Theme()
        progress = ProgressBar(theme, "Processing")

        assert progress.description == "Processing"
        assert progress.component_type == "progress"

    def test_render(self):
        """Test ProgressBar rendering."""
        theme = Theme()
        console = MagicMock()
        progress = ProgressBar(theme, "Loading")

        progress.render(console)

        console.print.assert_called_once()
        args = console.print.call_args
        assert "Loading" in args[0][0]


class TestPrompt:
    """Test the Prompt component."""

    def test_init(self):
        """Test Prompt initialization."""
        theme = Theme()
        prompt = Prompt(theme, "Enter value:", default="test")

        assert prompt.text == "Enter value:"
        assert prompt.kwargs == {"default": "test"}
        assert prompt.component_type == "prompt"

    def test_render(self):
        """Test Prompt rendering (no-op for spacing only)."""
        theme = Theme()
        console = MagicMock()
        prompt = Prompt(theme, "Test")

        prompt.render(console)

        # Prompt render is a no-op (spacing only)
        console.print.assert_not_called()


class TestConfirm:
    """Test the Confirm component."""

    def test_init(self):
        """Test Confirm initialization."""
        theme = Theme()
        confirm = Confirm(theme, "Are you sure?", abort=True)

        assert confirm.text == "Are you sure?"
        assert confirm.kwargs == {"abort": True}
        assert confirm.component_type == "confirm"

    def test_render(self):
        """Test Confirm rendering (no-op for spacing only)."""
        theme = Theme()
        console = MagicMock()
        confirm = Confirm(theme, "Test")

        confirm.render(console)

        # Confirm render is a no-op (spacing only)
        console.print.assert_not_called()


class TestList:
    """Test the List component."""

    def test_init(self):
        """Test List initialization."""
        theme = Theme()
        items = ["Item 1", "Item 2"]
        list_comp = List(theme, items)

        assert list_comp.items == items
        assert list_comp.component_type == "list"

    def test_render(self):
        """Test List rendering."""
        theme = Theme()
        console = MagicMock()
        items = ["First", "Second", "Third"]
        list_comp = List(theme, items)

        list_comp.render(console)

        assert console.print.call_count == 3
        calls = console.print.call_args_list
        for i, call in enumerate(calls):
            assert items[i] in str(call)
            assert theme.icons.bullet in str(call)

    def test_render_with_indentation(self):
        """Test List rendering with indentation."""
        theme = Theme()
        theme.indentation = ComponentIndentation(list=4)
        console = MagicMock()
        list_comp = List(theme, ["Item"])

        list_comp.render(console)

        args = console.print.call_args
        assert "    " in args[0][0]  # 4 spaces


class TestRenderStream:
    """Test the RenderStream class."""

    def test_init(self):
        """Test RenderStream initialization."""
        console = MagicMock()
        stream = RenderStream(console)

        assert stream.console is console
        assert stream.history == []

    def test_render_first_component(self):
        """Test rendering the first component."""
        console = MagicMock()
        stream = RenderStream(console)
        component = MagicMock()
        component.spacing_before.return_value = 0

        stream.render(component)

        component.spacing_before.assert_called_once_with(None)
        component.render.assert_called_once_with(console)
        assert stream.history == [component]

    def test_render_with_spacing(self):
        """Test rendering with spacing."""
        console = MagicMock()
        stream = RenderStream(console)

        comp1 = MagicMock()
        comp1.spacing_before.return_value = 0
        comp2 = MagicMock()
        comp2.spacing_before.return_value = 2

        stream.render(comp1)
        stream.render(comp2)

        # Should print 2 newlines for spacing
        calls = console.print.call_args_list
        assert len(calls) == 1
        assert calls[0][0][0] == "\n\n"

    def test_last_component(self):
        """Test last_component property."""
        console = MagicMock()
        stream = RenderStream(console)

        assert stream.last_component is None

        comp = MagicMock()
        comp.spacing_before.return_value = 0
        stream.render(comp)

        assert stream.last_component is comp

    def test_clear_history(self):
        """Test clear_history method."""
        console = MagicMock()
        stream = RenderStream(console)

        comp = MagicMock()
        comp.spacing_before.return_value = 0
        stream.render(comp)

        assert len(stream.history) == 1

        stream.clear_history()

        assert stream.history == []
        assert stream.last_component is None
