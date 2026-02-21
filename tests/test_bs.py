from volsurface.bs import bs_price

def test_bs_call_put_parity_basic():
    S, K, T, r, q, sigma = 100.0, 100.0, 0.5, 0.02, 0.0, 0.2
    C = bs_price(S, K, T, r, q, sigma, "C")
    P = bs_price(S, K, T, r, q, sigma, "P")
    # Put-call parity: C - P = S e^{-qT} - K e^{-rT}
    rhs = S - K * (2.718281828459045 ** (-r * T))
    assert abs((C - P) - rhs) < 1e-2