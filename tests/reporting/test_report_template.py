from reporting.report_template import ReportTemplate


def test_template_creation():
    template = ReportTemplate(name="default")

    assert template.name == "default"


def test_template_default_title():
    template = ReportTemplate(name="default")

    assert template.title == ""


def test_template_default_version():
    template = ReportTemplate(name="default")

    assert template.version == "1.0"


def test_template_default_author():
    template = ReportTemplate(name="default")

    assert template.author == ""


def test_template_default_description():
    template = ReportTemplate(name="default")

    assert template.description == ""


def test_template_custom_values():
    template = ReportTemplate(
        name="daily",
        title="Daily Report",
        version="2.0",
        author="Rajesh",
        description="Trading report",
    )

    assert template.title == "Daily Report"
    assert template.version == "2.0"
    assert template.author == "Rajesh"
    assert template.description == "Trading report"


def test_validate_returns_true():
    template = ReportTemplate(name="default")

    assert template.validate() is True


def test_render_returns_string():
    template = ReportTemplate(name="default")

    html = template.render({})

    assert isinstance(html, str)


def test_render_empty_context():
    template = ReportTemplate(name="default")

    assert template.render({}) == ""


def test_render_with_context():
    template = ReportTemplate(name="default")

    result = template.render({"title": "ABC"})

    assert isinstance(result, str)


def test_templates_are_equal():
    first = ReportTemplate(name="default")
    second = ReportTemplate(name="default")

    assert first == second


def test_repr_contains_name():
    template = ReportTemplate(name="default")

    assert "default" in repr(template)


def test_template_has_slots():
    assert "__slots__" in ReportTemplate.__dict__


def test_name_is_preserved():
    template = ReportTemplate(name="performance")

    assert template.name == "performance"


def test_version_is_string():
    template = ReportTemplate(name="default")

    assert isinstance(template.version, str)