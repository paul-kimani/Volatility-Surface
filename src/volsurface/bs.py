import math

def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bs_price(S: float, K: float, T: float, r: float, q: float, sigma: float, opt_type: str) -> float:
    """
    Black–Scholes European option price with continuous dividend yield q.
    opt_type: 'C' (call) or 'P' (put)
    """
    opt = opt_type.upper()
    if T <= 0:
        if opt == "C":
            return max(0.0, S - K)
        if opt == "P":
            return max(0.0, K - S)
        raise ValueError("opt_type must be 'C' or 'P'")

    if sigma <= 0:
        # Degenerate fallback: discounted forward intrinsic
        F = S * math.exp((r - q) * T)
        if opt == "C":
            return math.exp(-r * T) * max(0.0, F - K)
        if opt == "P":
            return math.exp(-r * T) * max(0.0, K - F)
        raise ValueError("opt_type must be 'C' or 'P'")

    sqrtT = math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT

    if opt == "C":
        return S * math.exp(-q * T) * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
    if opt == "P":
        return K * math.exp(-r * T) * _norm_cdf(-d2) - S * math.exp(-q * T) * _norm_cdf(-d1)

    raise ValueError("opt_type must be 'C' or 'P'")