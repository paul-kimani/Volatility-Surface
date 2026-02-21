from volsurface.bs import bs_price
from volsurface.implied_vol import implied_vol_bisect

def test_implied_vol_inverts_bs():
    S, K, T, r, q, sigma = 100.0, 110.0, 0.25, 0.01, 0.0, 0.35
    price = bs_price(S, K, T, r, q, sigma, "C")
    iv = implied_vol_bisect(price, S, K, T, r, q, "C")
    assert abs(iv - sigma) < 1e-4