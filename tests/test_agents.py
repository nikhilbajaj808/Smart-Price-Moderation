import sys, os

# ✅ Add project root to sys.path so Python can find "agents"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.price_agent import PriceAgent
from agents.moderation_agent import ModerationAgent


def test_price_agent_basic():
    pa = PriceAgent()
    res = pa.suggest_price({
        'category': 'mobile',
        'brand': 'Apple',
        'condition': 'Good',
        'age_months': 24,
        'asking_price': 20000
    })
    assert 'suggested_min' in res and 'suggested_max' in res
    assert res['suggested_min'] <= res['suggested_max']


def test_moderation_phone_and_abuse():
    ma = ModerationAgent()
    r1 = ma.moderate({'message': 'Call me +91 9610608060'})
    assert r1['contains_mobile'] is True

    r2 = ma.moderate({'message': 'You are an idiot'})
    assert 'abusive_language' in r2['flags'] or r2['status'] == 'Abusive'


# ✅ This allows direct run with "python tests/test_agents.py"
if __name__ == "__main__":
    test_price_agent_basic()
    test_moderation_phone_and_abuse()
    print("✅ All tests passed!")
