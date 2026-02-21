from .bs import bs_price

def implied_vol_bisect(
    price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    q: float,
    opt_type: str,
    lo: float = 1e-6,
    hi: float = 5.0,
    tol: float = 1e-7,
    max_iter: int = 200,
) -> float:
    """
    Implied volatility via bisection inversion of Black–Scholes price.
    Returns NaN if a root cannot be bracketed.
    """
    if not (price > 0 and S > 0 and K > 0 and T >= 0):
        return float("nan")

    f_lo = bs_price(S, K, T, r, q, lo, opt_type) - price
    f_hi = bs_price(S, K, T, r, q, hi, opt_type) - price

    expand = 0
    while f_lo * f_hi > 0 and expand < 25:
        hi *= 2.0
        f_hi = bs_price(S, K, T, r, q, hi, opt_type) - price
        expand += 1

    if f_lo * f_hi > 0:
        return float("nan")

    a, b = lo, hi
    fa, fb = f_lo, f_hi

    for _ in range(max_iter):
        m = 0.5 * (a + b)
        fm = bs_price(S, K, T, r, q, m, opt_type) - price

        if abs(fm) < tol or (b - a) < tol:
            return m

        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm

    return 0.5 * (a + b)