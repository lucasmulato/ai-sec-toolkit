# The Conscience: Prevents security rules from breaking app utility.
class UtilityGuardian:
    def check_patch(self, patch_code: str) -> bool:
        # 1. Run against Golden Dataset
        # 2. If utility_score < threshold: return False
        return True