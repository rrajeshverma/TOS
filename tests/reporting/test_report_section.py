from reporting.report_section import ReportSection


def test_section_creation():
    section = ReportSection("Summary")

    assert section.name == "Summary"


def test_section_default_content():
    section = ReportSection("Summary")

    assert section.content == ""


def test_section_custom_content():
    section = ReportSection("Summary", "Daily Performance")

    assert section.content == "Daily Performance"


def test_section_render_returns_string():
    section = ReportSection("Summary")

    assert isinstance(section.render(), str)


def test_render_contains_name():
    section = ReportSection("Summary")

    assert "Summary" in section.render()


def test_render_contains_content():
    section = ReportSection("Summary", "Performance")

    assert "Performance" in section.render()


def test_render_contains_heading():
    section = ReportSection("Summary")

    assert "<h2>" in section.render()


def test_render_contains_paragraph():
    section = ReportSection("Summary")

    assert "<p>" in section.render()


def test_render_closes_heading():
    section = ReportSection("Summary")

    assert "</h2>" in section.render()


def test_render_closes_paragraph():
    section = ReportSection("Summary")

    assert "</p>" in section.render()


def test_section_repr():
    assert "Summary" in repr(ReportSection("Summary"))


def test_section_equality():
    assert ReportSection("A") == ReportSection("A")


def test_section_slots():
    assert "__slots__" in ReportSection.__dict__


def test_empty_name_allowed():
    section = ReportSection("")

    assert section.name == ""


def test_empty_content_allowed():
    section = ReportSection("Summary", "")

    assert section.content == ""