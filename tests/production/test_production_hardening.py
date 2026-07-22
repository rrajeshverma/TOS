from production.deployment_checker import DeploymentChecker
from production.failover_validator import FailoverValidator
from production.health_auditor import HealthAuditor
from production.runtime_validator import RuntimeValidator


# -------------------------
# Deployment Checker
# -------------------------


def test_deployment_initial_state():

    checker = DeploymentChecker()

    assert checker is not None


def test_deployment_add_component():

    checker = DeploymentChecker()

    checker.add_component("broker")

    assert checker.has_component("broker")


def test_deployment_ready():

    checker = DeploymentChecker()

    checker.add_component("broker")

    assert checker.is_ready()


def test_deployment_missing_component():

    checker = DeploymentChecker()

    assert not checker.is_ready()


def test_deployment_summary():

    checker = DeploymentChecker()

    result = checker.summary()

    assert "components" in result


# -------------------------
# Failover Validator
# -------------------------


def test_failover_initial():

    validator = FailoverValidator()

    assert validator is not None


def test_failover_register():

    validator = FailoverValidator()

    validator.register("broker")

    assert validator.has_service("broker")


def test_failover_available():

    validator = FailoverValidator()

    validator.register("broker")

    assert validator.validate("broker")


def test_failover_failure():

    validator = FailoverValidator()

    validator.register("broker")
    validator.fail("broker")

    assert not validator.validate("broker")


def test_failover_summary():

    result = FailoverValidator().summary()

    assert "services" in result


# -------------------------
# Health Auditor
# -------------------------


def test_health_register():

    auditor = HealthAuditor()

    auditor.register("database")

    assert auditor.has_component("database")


def test_health_ok():

    auditor = HealthAuditor()

    auditor.register("database")

    assert auditor.is_healthy()


def test_health_failure():

    auditor = HealthAuditor()

    auditor.register("database")
    auditor.mark_failed("database")

    assert not auditor.is_healthy()


def test_health_report():

    report = HealthAuditor().report()

    assert "health" in report


# -------------------------
# Runtime Validator
# -------------------------


def test_runtime_initial():

    validator = RuntimeValidator()

    assert validator is not None


def test_runtime_set():

    validator = RuntimeValidator()

    validator.set("python", "3.12")

    assert validator.get("python") == "3.12"


def test_runtime_validate():

    validator = RuntimeValidator()

    validator.set("mode", "production")

    assert validator.validate()


def test_runtime_invalid():

    validator = RuntimeValidator()

    assert not validator.validate()


def test_runtime_summary():

    result = RuntimeValidator().summary()

    assert "runtime" in result