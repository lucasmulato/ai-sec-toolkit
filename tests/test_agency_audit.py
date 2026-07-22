import pytest
import asyncio
from core.agency_audit import ExcessiveAgencyAuditor

@pytest.fixture
def auditor():
    """Instancia o auditor de agência excessiva para os testes."""
    return ExcessiveAgencyAuditor()

@pytest.mark.asyncio
async def test_non_critical_action_allowed(auditor):
    """
    Testa uma ação comum (leitura) que não deve ser marcada como crítica
    e não deve gerar violação, mesmo sem aprovação explícita.
    """
    action = "get_user_profile"
    result = await auditor.run_audit(action, approved=False)
    
    assert result["is_critical"] is False
    assert "VIOLATION: Excessive Agency detected" not in result["audit_log"]
    assert any("Action authorized" in log for log in result["audit_log"])

@pytest.mark.asyncio
async def test_critical_delete_action_violation(auditor):
    """
    Simula uma tentativa de deleção (ferramenta crítica) sem aprovação.
    Deve disparar um log de violação.
    """
    action = "delete_all_records_from_s3"
    result = await auditor.run_audit(action, approved=False)
    
    assert result["is_critical"] is True
    assert any("VIOLATION" in log for log in result["audit_log"])

@pytest.mark.asyncio
async def test_critical_admin_action_violation(auditor):
    """
    Simula uma tentativa de acesso administrativo sem aprovação.
    """
    action = "grant_admin_privileges_to_user_123"
    result = await auditor.run_audit(action, approved=False)
    
    assert result["is_critical"] is True
    assert any("VIOLATION" in log for log in result["audit_log"])

@pytest.mark.asyncio
async def test_critical_action_approved_by_human(auditor):
    """
    Testa se uma ação crítica é permitida quando o parâmetro 
    human_approved é explicitamente True.
    """
    action = "delete_temporary_files"
    result = await auditor.run_audit(action, approved=True)
    
    assert result["is_critical"] is True
    assert not any("VIOLATION" in log for log in result["audit_log"])
    assert any("Action authorized" in log for log in result["audit_log"])

@pytest.mark.asyncio
async def test_case_insensitivity_and_keywords(auditor):
    """
    Verifica se o detector de privilégios é robusto a variações de texto.
    """
    # Teste com Mixed Case
    result_1 = await auditor.run_audit("ADMIN_shutdown", approved=False)
    # Teste com substring
    result_2 = await auditor.run_audit("soft_delete_logs", approved=False)
    
    assert result_1["is_critical"] is True
    assert result_2["is_critical"] is True

@pytest.mark.asyncio
async def test_empty_action_handling(auditor):
    """Garante que strings vazias não quebrem o fluxo do grafo."""
    result = await auditor.run_audit("", approved=False)
    assert result["is_critical"] is False
    assert "proposed_action" in result
    assert result["proposed_action"] == ""